from __future__ import division

import random

from common import *
from constants import *

from entity import Entity, Monster, Scenery
import monster

class Barrel(Scenery):
    destructible = True
    anim_name = "barrel"

class Campfire(Scenery):
    anim_name = "campfire"

class VictoryDoor(Scenery):
    anim_name = "moai"
    def tick(self):
        if len([e for e in self.game.entities if e.must_kill]) == 0:
            self.game.flags["%s.roomclear" % self.game.map.name] = True
            self.game.destroy_entity(self, explode=True)
    def hit_entity(self, ent):
        if ent is self.game.player:
            self.game.show_dialogue("You cannot pass until the enemies in this room are defeated.")
    def start_room(self):
        if ("%s.roomclear" % self.game.map.name) in self.game.flags:
            self.game.destroy_entity(self)
    
class FuzzleHole(Scenery):
    baby = None
    shadow = False
    low_level = True
    def tick(self):
        ctrx = self.x + self.width / 2
        ctry = self.y + self.height / 2
        if len(self.game.obstacles_in_rect(self.x - COLLISION_BUFFER, self.y - COLLISION_BUFFER,
                                           self.width + 2*COLLISION_BUFFER, self.height + 2*COLLISION_BUFFER, set([self]))) == 0:
            if self.baby is None or self.baby not in self.game.entities:
                m = self.game.create_entity(self.fuzzle_cls, self.x, self.y)
                m.direction = self.direction
                m.parents.add(self)
                m.must_kill = False
                self.baby = m

class FuzzleHoleLeft(FuzzleHole):
    anim_name = "fuzzlehole"
    fuzzle_cls = monster.FuzzleLeft
    
class FuzzleHoleRight(FuzzleHole):
    anim_name = "fuzzlehole"
    fuzzle_cls = monster.FuzzleRight
    
class Tree(Scenery):
    @property
    def anim_name(self):
        s = self.x * 2 + self.y
        return "tree%d" % (int(s) % 6 + 1)

class DeadTree(Scenery):
    @property
    def anim_name(self):
        s = self.x * 2 + self.y
        return "deadtree%d" % (int(s) % 3 + 1)

class BigTree(Scenery):
    anim_name = "bigtree"
    width = 1.0
    height = 0.55
    
class Door(Scenery):
    block_path = True
    width = 1.2
    height = 1.0
    shadow = False
    def hit_entity(self, ent):
        if ent is self.game.player:
            if "key.%s" % self.colourname in self.game.flags:
                self.game.destroy_entity(self, explode=True)
            else:
                self.game.show_dialogue("You will need a %s key to open this door." % self.colourname)

class RedDoor(Door):
    anim_name = "red_door"
    colourname = "red"
    
class YellowDoor(Door):
    anim_name = "yellow_door"
    colourname = "yellow"
    
class GreenDoor(Door):
    anim_name = "green_door"
    colourname = "green"
    
class Key(Scenery):
    block_path = True
    def start_room(self):
        if "key.%s" % self.colourname in self.game.flags:
            self.game.destroy_entity(self)
    def hit_entity(self, ent):
        if ent is self.game.player:
            self.game.show_dialogue("You picked up a %s key!" % self.colourname)
            self.game.flags["key.%s" % self.colourname] = True
            self.game.destroy_entity(self)
            
class RedKey(Key):
    anim_name = "red_key"
    colourname = "red"
    
class YellowKey(Key):
    anim_name = "yellow_key"
    colourname = "yellow"
    
class GreenKey(Key):
    anim_name = "green_key"
    colourname = "green"