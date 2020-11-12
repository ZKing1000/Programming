from __future__ import division

import pyglet.event

import config

from entity import Player
from world import Map

from common import *
from constants import *

class Game(pyglet.event.EventDispatcher):
    event_types = ["on_enter_area", "on_create_entity", "on_destroy_entity", "on_dialogue", "on_detonate", "on_switch_music"]
    def __init__(self):
        self.entities_to_add = set()
        self.entities_to_remove = set()
        self.tick_n = 0
        
    def begin(self):
        self.ticks = 0
        self.flags = config.continue_flags.copy()
        self.player = Player(self)
        self.new_area = config.start_room
        self.new_area_entry = "start"
        self.new_area_dir = SOUTH
        self.enter_new_area()        
        
    def enter_new_area(self):
        if self.new_area != 'menuroom':
            config.save_option('continue_flags', self.flags.copy())
            config.save_option('continue_room', self.new_area)
            config.save_option('continue_entrance', self.new_area_entry)
            config.save_option('continue_dir', self.new_area_dir)
        
        self.script = None
        self.scripted_move = False
        self.zone_ents = {}
        self.entities = set([self.player])
        Map(self) # map constructor reads game.new_area to find out what to load and sets game.map
        self.player.place_in_zone(self.new_area_entry)
        self.player.direction = self.new_area_dir
        self.update_entities() # in case scripts created some
        self.create_map_entities()
        for e in self.entities:
            e.start_room()
        self.update_entities() # in case start_room functions did anything
        self.update_path_map()
        self.new_area = None
        self.dispatch_event("on_enter_area")
        if self.map.startup_script:
            self.script = self.map.startup_script()
            self.advance_script()

    def restart_area(self):
        self.player.reincarnate()
        self.new_area = self.map.name
        self.flags = config.continue_flags.copy()
        self.enter_new_area()
    def update_entities(self):
        self.entities |= self.entities_to_add 
        self.entities_to_add = set()
        self.entities -= self.entities_to_remove
        self.entities_to_remove = set()

    def create_map_entities(self):
        for ec, pos, dir in self.map.entities:
            new_entity = ec(self)
            new_entity.direction = dir
            new_entity.place_in_cell(*pos)
            self.entities.add(new_entity)

    def create_entity(self, cls, x, y, direction=None):
        new_entity = cls(self)
        new_entity.x = x
        new_entity.y = y
        if direction is not None:
            new_entity.direction = direction
        self.entities_to_add.add(new_entity)
        self.dispatch_event("on_create_entity", new_entity)
        return new_entity

    def create_entity_in_zone(self, cls, zone_name, direction=None):
        new_entity = self.create_entity(cls, 0, 0, direction=direction)
        new_entity.place_in_zone(zone_name)
        self.zone_ents[zone_name] = new_entity
        return new_entity

    def destroy_entity(self, ent, explode=False):
        if ent not in self.entities_to_remove:
            self.entities_to_remove.add(ent)
            self.dispatch_event("on_destroy_entity", ent, explode)

    def entities_in_rect(self, x, y, w, h):
        res = set()
        for e in (self.entities | self.entities_to_add - self.entities_to_remove):
            if e.x < x+w and e.x+e.width > x and e.y < y+h and e.y+e.height > y and e.fall_counter == 0:
                res.add(e)
        return res
        
    def obstacles_in_rect(self, x, y, w, h, ignore=set(), is_monster=False, avoid_pits=False):
        res = set([(e.x, e.y, e.width, e.height, e) for e in (self.entities_in_rect(x, y, w, h) - ignore)])
        res.update(self.map.walls_for_rect(x, y, w, h, include_pits=avoid_pits))
        if is_monster:
            zones = self.map.zones_for_rect(x, y, w, h)
            for z in zones:
                if z in self.map.forbid_monster_zones:
                    zp, zs = self.map.zones[z]
                    res.add((zp[0], zp[1], zs[0], zs[1], z))
        return res
        
    def cell_path_blocked(self, cx, cy):
        for e in self.entities_in_rect(cx, cy, 1, 1):
            if e.block_path:
                return True
        return False

    def detonate(self, x, y):
        for e in self.entities_in_rect(x-DETONATION_RANGE, y-DETONATION_RANGE, DETONATION_RANGE*2, DETONATION_RANGE*2):
            if e not in self.entities_to_remove:
                e.hurt(major=True)
        self.dispatch_event("on_detonate", x, y)

    def entity_enter_zone(self, entity, zone):
        if entity is self.player and zone in self.map.zone_triggers:
            assert not self.script
            self.script = self.map.zone_triggers[zone]()
            self.advance_script()
    def player_move(self, dx, dy, direction):
        if self.player.can_move():
            self.player.move(dx, dy, direction)
        
    def player_attack(self):
        self.player.attack()
        
    def player_release(self):
        self.player.attacking = False
    
    def tick(self):
        self.tick_n += 1
        if self.script:
            if self.scripted_move:
                advance = True
                for e in self.entities:
                    ect = e.cutscene_tick()
                    advance = advance and not ect
                for e in self.entities_to_add:
                    advance = advance and not e.move_target
                if advance: 
                    self.scripted_move = False
                    self.advance_script()
        else:
            for e in self.entities:
                e.tick()
        self.entities |= self.entities_to_add
        self.entities -= self.entities_to_remove
        self.entities_to_add = set()
        self.entities_to_remove = set()
        
        if self.new_area is not None: # because it was set by a script
            self.enter_new_area()
            
        self.ticks += 1
        if self.ticks % PATH_TIMER == 0:
            self.update_path_map()
            
    def show_dialogue(self, dia):
        self.dispatch_event("on_dialogue", dia)

    def get_player_cell(self):
        return self.player.get_centre_cell()
        
    def update_path_map(self):
        self.paths = self.get_path_map(self.player.get_centre_cell())
        
    def get_path_map(self, cell):
        paths = {}
        gen = 0
        old_cells = set()
        new_cells = set([cell])
        while new_cells:
            old_cells |= new_cells
            n = list(new_cells)
            new_cells = set()
            for c in n:
                if not self.cell_path_blocked(c[0], c[1]):
                    paths[c] = gen
                    new_cells.update(self.map.connected_cells(c))
            new_cells -= old_cells
            gen += 1
        return paths
            
    def advance_script(self):
        if self.script:
            try:
                next(self.script)
            except StopIteration, TypeError:
                self.script = None
            
