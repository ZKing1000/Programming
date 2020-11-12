#!/usr/bin/env python
import os, math, sys
import equip, init, items
import pygame
from random import randint
from constants import *
try:
    import configparser
except:
    import ConfigParser

class Special_Map(pygame.sprite.DirtySprite):
    def __init__(self, foldername, filename, layer, keyword, tile_width=32, tile_height=32):
        pygame.sprite.DirtySprite.__init__(self)
        self._layer = layer
        self.dirty = 2
        self.visible = 0
        self.depth = 0
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.map = []
        self.key = {}
        try:
            parser = configparser.ConfigParser()
        except:
            parser = ConfigParser.ConfigParser()
        parser.read(os.path.join('maps/'+str(foldername),str(filename)))
        self.map = parser.get("level", "map").split("\n")
        for section in parser.sections():
            if len(section) == 1:
                desc = dict(parser.items(section))
                self.key[section] = desc
        self.width = len(self.map[0])
        self.height = len(self.map)
        
        self.tileset = []
        temp_surface_1 = pygame.Surface((tile_width,tile_height))
        temp_surface_1.fill(white)
        temp_surface_2 = pygame.Surface((tile_width,tile_height))
        temp_surface_2.fill(black)
        self.tileset.append(temp_surface_1)
        self.tileset.append(temp_surface_2)
        self.render(keyword)

    def get_tile_bool(self, pos):
        map_x, map_y = pos
        try:
            color_temp = self.image.get_at((int(map_x*self.tile_width),
                                            int(map_y*self.tile_height)))
            if color_temp == (0,0,0,255):
                return True
            else:
                return False
        except:
            return True

    def modify_map(self, pos_1=None, pos_2=None):
        if pos_1:
            map_x, map_y = pos_1
            self.image.blit(self.tileset[0],(map_x*self.tile_width,
                                             map_y*self.tile_height))
        if pos_2:
            map_x, map_y = pos_2
            self.image.blit(self.tileset[1],(map_x*self.tile_width,
                                             map_y*self.tile_height))

    def render(self, keyword):
        self.image = pygame.Surface((self.width*self.tile_width,
                                    self.height*self.tile_height))
        for map_y, line in enumerate(self.map):
            if line != "":
                for map_x, c in enumerate(line):
                    if c != "":
                        try:
                            tile = self.key[c][keyword]
                            tile = 1
                        except (ValueError, KeyError):
                            tile = 0
                        tile_image = self.tileset[tile]
                        self.image.blit(tile_image,(map_x*self.tile_width,
                                                    map_y*self.tile_height))
        self.rect = self.image.get_rect()

class Dirty_Map(pygame.sprite.DirtySprite):
    def __init__(self, foldername, filename, layer, MAP_CACHE, elevation, tile_width=32, tile_height=32):
        pygame.sprite.DirtySprite.__init__(self)
        self._layer = layer
        self.dirty = 2
        self.elevation = elevation
        self.tile_width = tile_width
        self.tile_height = tile_height
        
        self.map = []
        self.key = {}
        try:
            parser = configparser.ConfigParser()
        except:
            parser = ConfigParser.ConfigParser()
        parser.read(os.path.join('maps/'+foldername,filename))
        self.tileset = MAP_CACHE[parser.get("level", "tileset")]
        self.map = parser.get("level", "map").split("\n")
        try:
            self.x_offset, self.y_offset = parser.get("level", "offset").split(",")
            self.x_offset = int(self.x_offset)
            self.y_offset = int(self.y_offset)
        except:
            self.x_offset = 0
            self.y_offset = 0
        for section in parser.sections():
            if len(section) == 1:
                desc = dict(parser.items(section))
                self.key[section] = desc
        self.width = len(self.map[0])
        self.height = len(self.map)
        
        self.image = pygame.Surface((self.width*self.tile_width,
                                     self.height*self.tile_height))
        for map_y, line in enumerate(self.map):
            if line != "":
                for map_x, c in enumerate(line):
                    if c != "":
                        try:
                            tile = self.key[c]['tile'].split(",")
                            tile = int(tile[0]), int(tile[1])
                        except (ValueError, KeyError):
                            continue
                        tile_image = self.tileset[tile[0]][tile[1]]
                        try:
                            flip_y, flip_x = self.key[c]['flip'].split(",")
                            tile_image = pygame.transform.flip(tile_image,
                                                               int(flip_x),
                                                               int(flip_y))
                        except (ValueError, KeyError):
                            pass
                        tile_image.set_colorkey(white)
                        self.image.blit(tile_image,(map_x*self.tile_width,
                                                    map_y*self.tile_height))
                        try:
                            tile = self.key[c]['overlay'].split(",")
                            tile = int(tile[0]), int(tile[1])
                            tile_image = self.tileset[tile[0]][tile[1]]
                        except KeyError:
                            continue
                        try:
                            flip_y2, flip_x2 = self.key[c]['overlay_flip'].split(",")
                            tile_image = pygame.transform.flip(tile_image,
                                                               int(flip_x2),
                                                               int(flip_y2))
                        except:
                            pass
                        tile_image.set_colorkey(white)
                        self.image.blit(tile_image,(map_x*self.tile_width,
                                                    map_y*self.tile_height))
                        try:
                            tile = self.key[c]['overlay_2'].split(",")
                            tile = int(tile[0]), int(tile[1])
                            tile_image = self.tileset[tile[0]][tile[1]]
                        except KeyError:
                            continue
                        try:
                            flip_y2, flip_x2 = self.key[c]['overlay_2_flip'].split(",")
                            tile_image = pygame.transform.flip(tile_image,
                                                               int(flip_x2),
                                                               int(flip_y2))
                        except:
                            pass
                        tile_image.set_colorkey(white)
                        self.image.blit(tile_image,(map_x*self.tile_width,
                                                    map_y*self.tile_height))

        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x_offset*self.tile_width,
                             self.y_offset*self.tile_height)
        self.depth = self.rect.midbottom[1]

class Static_Sprite(pygame.sprite.DirtySprite):
    def __init__(self, spritesheet, pos, direction, layer, elevation, type, object_index, collision_cache):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2
        self.direction = direction
        self._layer = layer
        self.elevation = elevation
        self.type = type
        self.index = object_index
        
        if not self.type == "hidden":
            self.frames = spritesheet
            self.image = self.frames[0][self.direction]
            self.image.set_colorkey(white)
        else:
            self.image = pygame.Surface((tile_width,tile_height))
            self.visible = 0
        self.rect = self.image.get_rect()
        self.depth = self.rect.midbottom[1]
        self.animation = None
        self._set_pos(pos)
        self.start_pos = self._get_pos()

        self.collision_cache = collision_cache
        self.collision_map = self.collision_cache[self.elevation]
        if not self.type == "hidden":
            self.collision_map.modify_map(None, self._get_pos())

    def _get_pos(self):
        return (int((self.rect.midbottom[0]-16)/32), int((self.rect.midbottom[1]-16)/32))

    def _set_pos(self, pos):
        self.rect.midbottom = int(pos[0]*32+16), int(pos[1]*32+16)
        self.depth = self.rect.midbottom[1]

    pos = property(_get_pos, _set_pos)

    def change_state(self, state, direction=None, visible=-1):
        if not direction: direction = self.direction
        if not visible == -1: self.visible = visible

        self.image = self.frames[state][direction]
        self.image.set_colorkey([255,255,255])

class Moving_Sprite(Static_Sprite):
    def __init__(self, spritesheet, pos, direction, layer, elevation, type, object_index, collision_cache, level_cache, moveable=1):
        Static_Sprite.__init__(self, spritesheet, pos, direction, layer, elevation, type, object_index, collision_cache)
        self.moveable = moveable
        self.level_cache = level_cache
        self.set_level(elevation)

    def set_level(self, elevation):
        self.elevation = elevation
        self.level = self.level_cache[self.elevation]
        if self.collision_map != self.collision_cache[self.elevation]:
            self.collision_map.modify_map(self._get_pos())
            self.collision_map = self.collision_cache[self.elevation]
            self.collision_map.modify_map(None, self._get_pos())

    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)
        self.depth = self.rect.midbottom[1]

    def slow_walk_animation(self):
        for frame in range(4):
            self.image = self.frames[frame][self.direction]
            yield None
            self.move(2*DX[self.direction], 2*DY[self.direction])
            yield None
            self.move(2*DX[self.direction], 2*DY[self.direction])
            yield None
            self.move(2*DX[self.direction], 2*DY[self.direction])
            yield None
            self.move(2*DX[self.direction], 2*DY[self.direction])

    def walk_animation(self):
        for frame in range(4):
            self.image = self.frames[frame][self.direction]
            yield None
            self.move(4*DX[self.direction], 4*DY[self.direction])
            yield None
            self.move(4*DX[self.direction], 4*DY[self.direction])

    def auto_control(self): #for NPCs
        def walk(d):
            if self.animation == None:
                x, y = self._get_pos()
                start_x, start_y = self.start_pos
                self.direction = d
                if not self.collision_map.get_tile_bool((x+DX[d], y+DY[d])) \
                    and (x+DX[d]) in range(start_x-1, start_x+1) and (y+DY[d]) in range(start_y-1, start_y+1):
                        self.collision_map.modify_map((x,y), (x+DX[d],y+DY[d]))
                        self.animation = self.walk_animation()

        if randint(0,100) == 100:
            i = randint(0,100)
            if 0 <= i <= 25:
                walk(index_direction['up'])
            elif 26 <= i <= 50:
                walk(index_direction['down'])
            elif 51 <= i <= 75:
                walk(index_direction['left'])
            else:
                walk(index_direction['right'])

    def update(self, *args):
        if self.animation is None:
            self.image = self.frames[0][self.direction]
        else:
            try:
                next(self.animation)
                dirty = 1
            except StopIteration:
                self.animation = None
        self.image.set_colorkey(white)

class Player_Sprite(Moving_Sprite):
    def __init__(self, spritesheet, pos, direction, layer, elevation, type, object_index, collision_cache, level_cache, event_map):
        Moving_Sprite.__init__(self, spritesheet, pos, direction, layer, elevation, type, object_index, collision_cache, level_cache)
        self.event_map = event_map
        self.attack_frames = TALL_SPRITE_CACHE['player_1_attack_sprite_sheet.png']
        self.attack_effect = None

    def set_attack_effect(self, attack_effect):
        self.attack_effect = attack_effect

    def attack_animation(self):
        for frame in range(3):
            self.image = self.attack_frames[frame][self.direction]
            yield None
            yield None
            yield None
            yield None

    def push_animation(self):
        for frame in range(4):
            self.image = self.frames[frame][self.direction]
            yield None
            self.move(4*DX[self.direction], 4*DY[self.direction])
            yield None
            self.move(4*DX[self.direction], 4*DY[self.direction])

    def control(self, pressed_list, npc_group): #for the player
        keys = pygame.key.get_pressed()

        def pressed(key):
            return pressed_list[0] == key or keys[key]

        def walk(d):
            x, y = self._get_pos()
            self.direction = d
            if not self.collision_map.get_tile_bool((x+DX[d], y+DY[d])):
                pressed_list[2] = 0
                self.collision_map.modify_map((x,y),(x+DX[d], y+DY[d]))
                self.animation = self.walk_animation()

        def push():
            x, y = self._get_pos()
            d = self.direction
            if npc_group and not self.collision_map.get_tile_bool((x+(DX[d]*2),y+(DY[d]*2))):
                sprite = npc_group.get_sprite((x+DX[d],y+DY[d]))
                if self.event_map.get_tile_bool((x+(DX[d]*2),y+(DY[d]*2))):
                    event_key = self.event_map.map[(y+(DY[d]*2))][(x+(DX[d]*2))]
                    if str.lower(self.event_map.key[event_key]['not_pushable']):
                        return
                if sprite and sprite.moveable and not sprite.animation:
                    self.collision_map.modify_map((x+(DX[d]),y+(DY[d])),(x+(DX[d]*2),y+(DY[d]*2)))
                    self.collision_map.modify_map((x,y),(x+DX[d], y+DY[d]))
                    sprite.direction = d
                    sprite.animation = sprite.walk_animation()
                    self.animation = self.push_animation()
                    pressed_list[2] = 25
                        

        if pressed(pygame.K_UP):
            pressed_list[1] = pygame.K_UP
            walk(index_direction['up'])
        elif pressed(pygame.K_DOWN):
            pressed_list[1] = pygame.K_DOWN
            walk(index_direction['down'])
        elif pressed(pygame.K_LEFT):
            pressed_list[1] = pygame.K_LEFT
            walk(index_direction['left'])
        elif pressed(pygame.K_RIGHT):
            pressed_list[1] = pygame.K_RIGHT
            walk(index_direction['right'])
        elif pressed(pygame.K_e):
            if self.attack_effect:
                self.animation = self.attack_animation()
                self.attack_effect.animation = self.attack_effect.attack_animation()

        if pressed_list[1] and pressed(pressed_list[1]):
            pressed_list[2] += 1
            if pressed_list[2] > 30:
                push()
        else:
            pressed_list[2] = 0

        pressed_list[0] = None
        return pressed_list

class Shadow(pygame.sprite.DirtySprite):
    def __init__(self, owner, sprite_cache):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2
        self._layer = 5
        self.image = sprite_cache["shadow.png"][0][0]
        self.image.set_alpha(64)
        self.rect = self.image.get_rect()
        self.owner = owner
        self.depth = owner.depth-1
        self.elevation = owner.elevation

    def update(self, *args):
        self.rect.midbottom = self.owner.rect.midbottom
        if self.owner.dirty:
            self.dirty = 1

class Attack_Effect(pygame.sprite.DirtySprite):
    def __init__(self, owner, sprite_cache):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 1
        self.visible = 0
        self._layer = 5
        self.frames = sprite_cache['attack_effect_1.png']
        self.image = self.frames[0][0]
        self.image.set_alpha(64)
        self.rect = self.image.get_rect()
        self.depth = self.rect.midbottom[1]
        self.owner = owner
        self.direction = owner.direction
        self.elevation = owner.elevation
        self.animation = None

    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)
        self.depth = self.rect.bottom

    def attack_animation(self):
        for frame in range(3):
            self.image = self.frames[frame][self.direction]
            yield None
            self.move(4*DX[self.direction], 4*DY[self.direction])
            yield None
            self.move(4*DX[self.direction], 4*DY[self.direction])

    def update(self, *args):
        if self.animation is None:
            self.image = self.frames[0][self.direction]
            x, y = self.owner.rect.midbottom
            d = self.owner.direction
            x, y = x+(DX[d]*32), y+(DY[d]*32)
            self.rect.midbottom = (x,y)
            self.direction = d
            self.elevation = self.owner.elevation
            self.depth = self.rect.bottom
        else:
            try:
                next(self.animation)
                self.dirty = 1
                self.visible = 1
            except StopIteration:
                self.animation = None
                self.visible = 0
        self.image.set_colorkey([255,255,255])

'''
EVERYTHING BELOW THIS POINT DEALS WITH DATA, NOT SPRITES/VISUALS
'''
class party:
    def __init__(self, members, inventory, money):
        self.members = members
        self.money = money
        self.inventory = inventory

class character:
    def __init__(self, index, inventory, name, sex, age, race, birthplace, biography):
        self.index = index
        self.name = name
        self.sex = sex
        self.age = age
        self.race = race
        self.birthplace = birthplace
        self.biography = biography
        self.basic_battle_options = list()
        self.advanced_battle_options = list()
        self.status = list()
        if self.name != "Empty":
            self.stats = init.stat_Init(index)
            self.equip = init.equip_Init(index, inventory)
            self.equip_avail = init.equip_Avail_Init(index)
            self.magic = magic()
            self.skills = skills(self.equip_avail)
            self.skills.change_Learning(self)
            self.skills.add_Progress(self,100)
            self.gain_EXP(0)

    def first_Name(self):
        return self.name.split()[0]

    def last_Name(self):
        return self.name.split()[-1]

    def set_battle_options(self):
        self.basic_battle_options = list()
        for each in ['attack','magic','skills','items']:
            self.basic_battle_options.append(each)
        self.advanced_battle_options = list()
        if items.get_Type(self.equip['offh']['name']) in ['Light Shield', 'Heavy Shield']:
            self.advanced_battle_options.append('protect')
        if 'Thief Ring' in [self.equip['acc1']['name'], self.equip['acc2']['name'], self.equip['acc3']['name']]:
            self.advanced_battle_options.append('steal')

    def gain_EXP(self,amount):
        curr = self.stats['curr']
        base = self.stats['base']
        mult = self.stats['mult']
        curr['ext'] += amount
        if curr['lvl'] < 99:
            curr['exp'] += amount
            while curr['exp'] >= curr['exn'] and curr['lvl'] < 99:
                curr['lvl'] += 1
                curr['exp'] = int(curr['exp'] - curr['exn'])
                curr['exn'] = int((curr['exn'] * 1.25)**.99)
                for each in ['str','dex','agi','spd','int','wsd','lck']:
                    base[each] = base[each] + (mult[each] * 1.5)
                    curr[each] = int(round(base[each]))
                base['maxhp'] = base['maxhp'] + (mult['maxhp'] * 18.5)**1.25
                curr['maxhp'] = int(round(base['maxhp']))
                base['maxmp'] = base['maxmp'] + (mult['maxmp'] * 5.2)**1.21
                curr['maxmp'] = int(round(base['maxmp']))
            curr['pow'],curr['mpow'] = curr['str'],curr['int']
            curr['def'],curr['mdef'] = 0,0
            equip.load_Stats(self)
            curr['hp'] = curr['maxhp']
            curr['mp'] = curr['maxmp']
            if curr['lvl'] == 99:
                curr['exp'] = 0
                curr['exn'] = 0
    
class magic(object):
    def __init__(self):
        self.perm_spells = {}
        self.temp_spells = {}
        self.progress = {}
        self.available = init.init_Spells()
        
    def add_Spell(self,name,status='temp'):
        if name not in self.perm_spells:
            if status == 'perm':
                self.perm_spells[name] = self.get_Spell(name)
            elif status == 'temp' and name not in self.temp_spells:
                self.temp_spells[name] = self.get_Spell(name)
            
    def rem_Spell(self,name):
        if name in self.temp_spells:
            del self.temp_spells[name]
            
    def add_Progress(self,amt):
        for key, value in self.progress.items():
            if key in self.temp_spells:
                if value < 100:
                    value += amt
                    if value > 99:
                        value = 100
                    self.progress[key] = value
                    if value == 100:
                        if key not in self.perm_spells:
                            self.add_Spell(key, 'perm')
                            self.rem_Spell(key)

    def get_Spell(self,name):
        if name in self.available:
            temp = self.available[name]
        else:
            temp = {}
            print("Spell " + name + " does not exist.")
        return temp
    
class skills(object):
    def __init__(self,equip_avail):
        self.useable = {}
        self.learned = {}
        self.learning = {}
        self.available = init.init_Skills(equip_avail)

    def change_Learning(self,char):
        del_temp = []
        level_temp = char.stats['curr']['lvl']

        for key, value in self.available.items():
            if value['level'] <= level_temp:
                self.learning[key] = value
                del_temp.append(key)
        for each in del_temp:
            del self.available[each]

    def add_Progress(self, char, amount):
        del_temp = []
        for key, value in self.learning.items():
            if char.equip['main']['type'] == value['weapon'] or char.equip['offh']['type'] == value ['weapon']:
                value['progress'] += amount
                
                if value['progress'] >= value['progress_cap']:
                    self.useable[key] = value
                    del_temp.append(key)
            else:
                if value['progress'] >= value['progress_cap']:
                    self.learned[key] = value
                    del_temp.append(key)
        for each in del_temp:
            del self.learning[each]
        
    def change_Useable(self,char,slot,new = {'name': 'Empty'},old = {'name': 'Empty'}):
        if slot == 'main': other_slot = 'offh'
        elif slot == 'offh': other_slot = 'main'

        if old['name'] != "Empty":
            del_temp = []
            for key, value in self.useable.items():
                if value['weapon'] == old['type'] and char.equip[other_slot]['type'] != value['weapon']:
                    self.learned[key] = value
                    del_temp.append(key)
            for each in del_temp:
                del self.useable[each]
        if new['name'] != "Empty":
            del_temp = []
            for key, value in self.learned.items():
                if value['weapon'] == new['type'] and char.equip[other_slot]['type'] != value['weapon']:
                    self.useable[key] = value
                    del_temp.append(key)
            for each in del_temp:
                del self.learned[each]

class inventory(object):
    def __init__(self):
        self.items = {}
        self.avail = {}
        self.descs = {}

    def add_Avail(self,item,amt):
        if item != "Empty":
            if item in self.avail:
                self.avail[item] += amt
            else:
                self.avail[item] = amt

    def rem_Avail(self,item,amt):
        if item != "Empty":
            if item in self.avail:
                self.avail[item] -= amt
                if self.avail[item] == 0:
                    del self.avail[item]

    def add_Item(self, item, amt):
        if item != "Empty":
            if item in self.items:
                self.items[item] += amt
            else:
                self.items[item] = amt
            self.add_Avail(item, amt)
                

    def rem_Item(self, item, amt):
        if item != "Empty":
            if item in self.items and self.items[item] >= amt:
                self.items[item] -= amt
                self.rem_Avail(item, amt)
                if self.items[item] == 0:
                    del self.items[item]
                return True
            else:
                return False

    def has_Item(self, item):
        if item in self.items:
            return True
        else:
            return False

    def has_Item_Avail(self, item):
        if item in self.avail:
            return True
        else:
            return False

    def has_Num_of_Item(self, item, amt):
         if item in self.items and self.items[item] >= amt:
             return True
         else:
             return False

    def get_Num_of_Item(self, item):
        if item in self.items:
            return int(self.items[item])
        else:
            return 0

    def has_Num_of_Item_Avail(self, item, amt):
        if item in self.avail and self.avail[item] >= amt:
            return True
        else:
            return False

    def get_Num_of_Item_Avail(self, item):
        if item in self.avail:
            return int(self.avail[item])
        else:
            return 0

class enemy:
    def __init__(self, type):
        self.stats = enemy.enemy_Stats(type)
