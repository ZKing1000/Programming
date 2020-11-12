#!/usr/bin/env python
import pygame, os

class Tile_Cache:
    def __init__(self,  width=32, height=32):
        self.width = int(width)
        self.height = int(height)
        self.cache = {}

    def __getitem__(self, filename):
        key = (filename, self.width, self.height)
        try:
            return self.cache[key]
        except KeyError:
            tile_table = self._load_tile_table(filename, self.width,
                                               self.height)
            self.cache[key] = tile_table
            return tile_table

    def _load_tile_table(self, filename, width, height):
        image = pygame.image.load(os.path.join('images',filename)).convert()
        image_width, image_height = image.get_size()
        tile_table = []
        for tile_x in range(0, int(int(image_width)/int(width))):
            line = []
            tile_table.append(line)
            for tile_y in range(0, int(int(image_height)/int(height))):
                rect = (int(tile_x*width), int(tile_y*height), int(width), int(height))
                line.append(image.subsurface(rect))
        return tile_table

TALL_SPRITE_CACHE = Tile_Cache(32, 64)
SHORT_SPRITE_CACHE = Tile_Cache(32, 32)
LARGE_MAP_CACHE = Tile_Cache(64, 64)
MAP_CACHE = Tile_Cache(32, 32)
TINY_MAP_CACHE = Tile_Cache(16, 16)
SHORT_EFFECT_CACHE = Tile_Cache(32, 32)
TALL_EFFECT_CACHE = Tile_Cache(32, 64)
LARGE_EFFECT_CACHE = Tile_Cache(64, 64)

DEF_SCREEN_SIZE=(800,600)

black = [0, 0, 0]
off_black = [25,25,25]
white = [255, 255, 255]
gray = [150,150,150]
ltgray = [200,200,200]
dkgray = [90, 90, 90]
blue = [0,0,180]
ltblue = [0,0,255]
dkblue = [0,0,100]
green = [0,180,0]
ltgreen = [0,255,0]
dkgreen = [0,100,0]
red = [180,0,0]
ltred = [255,0,0]
dkred = [100,0,0]
purple = [0xBF,0x0F,0xB5]
brown = [0x55,0x33,0x00]
ltyellow = [255,255,0]
yellow = [200,200,0]
dkyellow = [90, 90, 0]
excol = [248, 104, 0]

DX = [0, -1, 1, 0]
DY = [1, 0, 0, -1]
#index_direction and DX/DY are directly correlative
index_direction = dict({'up':3, 'down':0, 'left':1, 'right':2})

index_equip = ['main','offh','head','body','legs',
               'hand','feet','acc1','acc2','acc3']
index_equip_text = ['Main Hand:','Off Hand:','Head:','Body:','Legs:',
                    'Hands:','Feet:','Accessory:','Accessory:','Accessory:']
index_equip_stat = ['str','dex','agi','spd','int',
                    'wsd','lck','pow','mpow','def','mdef']
index_shop_cat = ['ALL','CONS','WEAP','ARM','ACC']

def pos_Neg(num):
    if num < 0:
        return -1
    elif num > 0:
        return 1
    else:
        return 0

def is_Odd(num):
    return bool(num & 1)