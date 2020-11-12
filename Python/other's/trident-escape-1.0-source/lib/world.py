from __future__ import division

import collections
import pprint

import script
import entity

from common import *
from constants import *

solid = {'w': True, 'n': False, 'g': False, 'p': False, 'x': True, 'q': True}

class EntityPrettyPrinter(pprint.PrettyPrinter):
    def format(self, obj, context, maxlevels, level):
        if isinstance(obj, type) and issubclass(obj, entity.Entity):
            return (obj.__name__, True, False)
        else:
            # for some reason PrettyPrinter is not a new-style class
            return pprint.PrettyPrinter.format(self, obj, context, maxlevels, level)

class Cell(object):
    def __init__(self, drawn=None, collides=False, pit=False):
        self.collides = collides
        self.drawn = drawn
        self.pit = pit

class Map(collections.defaultdict):
    # If this was Objective-C, this would be a category.
    def __init__(self, game=None):
        empty = Cell('n', True)
        super(Map, self).__init__(lambda: empty)
        self.game = game
        if game:
            game.map = self
            self.startup_script = None
            self.load(game.new_area)
            self.name = game.new_area
        else:
            # we're probably creating a new map in the editor
            self.zones = {}
            self.entities = []
            self.name = ''

    def walls_for_rect(self, x, y, width, height, include_pits=False):
        cx_min = int(x//1)
        cx_max = int((x + width)//1)
        cy_min = int(y//1)
        cy_max = int((y + height)//1)
        res = set()
        for cx in xrange(cx_min, cx_max + 1):
            for cy in xrange(cy_min, cy_max + 1):
                if self[cx, cy].collides or (include_pits and self[cx, cy].pit):
                    res.add((cx, cy, 1, 1, self[cx, cy]))
        return res
        
    def zones_for_rect(self, x, y, width, height):
        cx_min = int(x//1)
        cx_max = int((x + width)//1)
        cy_min = int(y//1)
        cy_max = int((y + height)//1)
        res = set()
        for n, z in self.zones.items():
            p, d = z
            zx, zy = p
            zw, zh = d
            if zx <= cx_max and (zx+zw-1) >= cx_min:
                if zy <= cy_max and (zy+zh-1) >= cy_min:
                    res.add(n)
        return res

    def connected_cells(self, p):
        x, y = p
        res = set()
        for nxy in [(x,y+1), (x,y-1), (x+1,y), (x-1,y)]:
            if nxy in self and not self[nxy].collides and not self[nxy].pit:
                res.add(nxy)
        return res

    def save(self, name):
        f = open("data/maps/%s.map" % name, "w")
        pp = EntityPrettyPrinter(stream=f)
        tilesets = {}
        for k, v in self.items():
            d = v.drawn
            if d not in tilesets:
                tilesets[d] = set()
            tilesets[d].add(k)
        tiles = {}
        for d in tilesets:
            tiles[d] = []
            celllist = list(tilesets[d])
            celllist.sort()
            current = celllist.pop()
            currentnum = 1
            while celllist:
                next = celllist.pop()
                if next == (current[0], current[1]-1):
                    current = next
                    currentnum += 1
                else:
                    tiles[d].append((current, currentnum))
                    current = next
                    currentnum = 1
            tiles[d].append((current, currentnum))
        f.write("tiles = ")
        pp.pprint(tiles)
        f.write("zones = ")
        pp.pprint(self.zones)
        f.write("entities = ")
        pp.pprint(self.entities)
        f.close()
        
    def load(self, name):
        self.clear()
        scope = {}
        exec "from entity import *" in scope
        exec "from scenery import *" in scope
        exec "from monster import *" in scope
        
        f = open("data/maps/%s.map" % name)
        exec f in scope
        assert "tiles" in scope
        for t, tl in scope["tiles"].items():
            tile = Cell()
            tile.drawn = t
            tile.collides = solid[t]
            tile.pit = (t == 'p')
            for b in tl:
                coords, l = b
                x, y = coords
                for yy in xrange(y, y+l):
                    self[x, yy] = tile
        f.close()
        
        assert "zones" in scope
        self.zones = scope["zones"]
        assert "entities" in scope
        self.entities = scope["entities"]
        self.entities = [x if len(x) == 3 else (x[0], x[1], x[0].direction) for x in self.entities]
        if self.game is None: return

        self.zone_triggers = {}
        self.forbid_monster_zones = []

        script.set_current(self.game, self)
        scope = {'flags': self.game.flags}
        exec "from scriptfuncs import *" in scope
        exec "from constants import *" in scope
        
        try:
            f = open("data/maps/%s.py" % name)
            exec f in scope
        except IOError:
            pass
