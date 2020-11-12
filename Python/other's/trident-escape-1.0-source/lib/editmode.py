"""Mode handler for normal play of the game."""

from __future__ import division

import pyglet
from pyglet.event import *
from pyglet.gl import *
from pyglet.window.key import _0, _1, _2, _3
from pyglet.window.key import *

import mode

from world import Cell, Map, solid

import entity
import monster
import scenery

from common import *
from constants import *

colourmap = {'w': (127,127,127),
            'n': (0,0,0),
            'g': (0,255,0),
            'p': (17,0,127),
            'q': (127, 0, 0) }

ent_modules = [monster, scenery]

ent_classes = []
for module in ent_modules:
    for item in module.__dict__.values():
        try:
            if issubclass(item, entity.Entity) and item.__dict__.has_key('anim_name'):
                ent_classes.append(item)
        except TypeError:
            pass
ent_classes.sort(key=lambda cls: cls.__name__)

class EditMode(mode.Mode):
    name = "edit"
    
    mx = 0
    my = 0
    
    def __init__(self):
        super(EditMode, self).__init__()
        self.map = Map()
        self.filename = 'editor'
        self.vx, self.vy = 0, 0
        
        self.tiles = [None] + [Cell(x, solid[x]) for x in 'qgp']
        self.currenttile = self.tiles[1]
        
        self.prompt = pyglet.text.Label(x=50, y=150, color=(255,200,200,255))
        self.entry = pyglet.text.Label(x=50, y=75, color=(255,200,200,255))
        self.entity_display = pyglet.text.Label(x=50, y=420, color=(255, 255, 150, 255))
        self.zone_labels = {}
        self.entity_labels = {}
        self.entrymode = None
        self.ui_mode = None
        self.entity_n = 0
        self.set_entity_display()
    
    def set_entity_display(self):
        self.entity_display.text = "Placing " + ent_classes[self.entity_n].__name__
        
    def screen_to_world(self, x, y):
        return int((x + self.vx) // 50), int((y + self.vy) // 50)
    def on_mouse_motion(self, x, y, dx, dy):
        self.mx = x
        self.my = y
        
    def on_mouse_press(self, x, y, btns, mods):
        cx, cy = self.screen_to_world(x, y)
        if self.ui_mode == 'zone':
            self.zone_coords = cx, cy
        elif self.ui_mode == 'deletezone':
            for name, zone in self.map.zones.items():
                pos, size = zone
                px, py = pos
                sx, sy = size
                if px <= cx < px + sx and py <= cy < py + sy:
                    del self.map.zones[name]
                    del self.zone_labels[name]
            self.ui_mode = None
        elif self.ui_mode == 'placeentity':
            self.add_entity(cx, cy, ent_classes[self.entity_n])
        elif self.ui_mode == 'rotateentity':
            e = self.get_entity(cx, cy)
            self.delete_entity(e)
            e, p, d = e
            self.add_entity(p[0], p[1], e, (d + 1) % 4)
        elif self.ui_mode == 'deleteentity':
            e = self.get_entity(cx, cy)
            self.delete_entity(e)
        else:
            if self.currenttile is None:
                if (cx, cy) in self.map:
                    del self.map[cx, cy]
            else:
                self.map[cx, cy] = self.currenttile
    
    def delete_entity(self, e):
        self.map.entities.remove(e)
        del self.entity_labels[e[0], e[1]]
        
    def get_entity(self, x, y):
        for e, p, d in self.map.entities:
            if p == (x, y): return (e, p, d)
            
    def add_entity(self, x, y, cls, dir=None):
        for e, p, d in self.map.entities:
            if p == (x, y): return
        self.map.entities.append((cls, (x,y), cls.direction if dir is None else dir))
        self.entity_labels[cls, (x,y)] = pyglet.text.Label(cls.__name__, x=x*50 + 10, y=y*50 + 20, color=(255, 100, 0, 255))
        
    def on_mouse_release(self, x, y, btns, mods):
        cx, cy = self.screen_to_world(x, y)
        if self.ui_mode == 'zone':
            ox, oy = self.zone_coords
            self.zone_coords = min(ox, cx), min(oy, cy)
            self.zone_size = abs(ox - cx) + 1, abs(oy - cy) + 1
            self.prompt.text = 'Enter zone name'
            self.entry.text = ''
            self.entrymode = 'zone'
        
    def on_mouse_drag(self, x, y, dx, dy, btns, mods):
        if self.ui_mode == 'zone':
            return
        self.on_mouse_press(x, y, btns, mods)

    def on_text(self, text):
        if self.entrymode is not None:
            self.entry.text += text
            return EVENT_HANDLED
            
    def on_text_motion(self, motion):
        if self.entrymode is not None and motion == MOTION_BACKSPACE:
            self.entry.text = self.entry.text[:-1]
            return EVENT_HANDLED

    def new_map(self):
        self.map = Map()
        self.filename = 'editor'
        self.zone_labels = {}
        self.entity_labels = {}

    def load_map(self, name):
        self.map.load(name)
        self.filename = name
        self.zone_labels = {}
        for name, zone in self.map.zones.items():
            pos, size = zone
            px, py = pos
            self.zone_labels[name] = pyglet.text.Label(name, x=px*50 + 10, y=py*50 + 20, color=(200, 200, 255, 255))
        self.entity_labels = {}
        for cls, pos, dir in self.map.entities:
            px, py = pos
            self.entity_labels[cls, pos] = pyglet.text.Label(cls.__name__, x=px*50 + 10, y=py*50 + 20, color=(255, 100, 0, 255))
        vpt = min(self.map.keys())
        self.vx = vpt[0] * 50
        self.vy = vpt[1] * 50
    
    def add_zone(self, name):
        self.map.zones[name] = self.zone_coords, self.zone_size
        px, py = self.zone_coords
        self.zone_labels[name] = pyglet.text.Label(name, x=px*50 + 10, y=py*50 + 20, color=(200, 200, 255, 255))
        
    def on_key_release(self, sym, mods):
        if self.entrymode is not None:
            if sym == ENTER:
                if self.entrymode == "save":
                    self.map.save(self.entry.text.strip())
                    self.filename = self.entry.text.strip()
                    print "saved"
                elif self.entrymode == "load":
                    self.load_map(self.entry.text.strip())
                elif self.entrymode == 'zone':
                    self.add_zone(self.entry.text.strip())
                self.entrymode = None
                return EVENT_HANDLED
        else:
            if sym == S:
                self.prompt.text = "Enter file name to save:"
                self.entry.text = self.filename
                self.entrymode = "save"
                return EVENT_HANDLED
            if sym == L:
                self.prompt.text  ="Enter file name to load:"
                self.entry.text = ""
                self.entrymode = "load"
                return EVENT_HANDLED
            if sym == N:
                self.new_map()
                return EVENT_HANDLED
            if sym == _0:
                self.currenttile = self.tiles[0]
                return EVENT_HANDLED
            if sym == _1:
                self.currenttile = self.tiles[1]
                return EVENT_HANDLED
            if sym == _2:
                self.currenttile = self.tiles[2]
                return EVENT_HANDLED
            if sym == _3:
                self.currenttile = self.tiles[3]
                return EVENT_HANDLED
            if sym == Z:
                self.ui_mode = 'zone'
            if sym == D:
                self.ui_mode = 'deletezone'
            if sym == E:
                if self.ui_mode == 'placeentity':
                    self.ui_mode = None
                else:
                    self.ui_mode = 'placeentity'
            if sym == BRACKETLEFT:
                self.entity_n += len(ent_classes) - 1
                self.entity_n %= len(ent_classes)
                self.set_entity_display()
            if sym == BRACKETRIGHT:
                self.entity_n += 1
                self.entity_n %= len(ent_classes)
                self.set_entity_display()
            if sym == X:
                self.ui_mode = 'deleteentity'
            if sym == R:
                self.ui_mode = 'rotateentity'
            if sym == SPACE:
                self.ui_mode = None   
    def tick(self):
        if self.entrymode is None:
            if self.keys[LEFT]: self.vx -= EDITOR_SCROLL_SPEED
            if self.keys[RIGHT]: self.vx += EDITOR_SCROLL_SPEED
            if self.keys[UP]: self.vy += EDITOR_SCROLL_SPEED
            if self.keys[DOWN]: self.vy -= EDITOR_SCROLL_SPEED
            
    def on_draw(self):
        self.window.clear()
        glPushMatrix()
        glTranslatef(-self.vx, -self.vy, 0)
        glPushMatrix()
        glScalef(50, 50, 1)
        glColor3f(255,255,255)
        bx, by = self.screen_to_world(self.mx, self.my)

        glBegin(GL_LINE_LOOP)
        glVertex2f(bx, by)
        glVertex2f(bx, by + 1)
        glVertex2f(bx + 1, by + 1)
        glVertex2f(bx + 1, by)
        glEnd()
        glBegin(GL_QUADS)
        for k, v in self.map.items():
            if v.drawn:
                glColor3f(*colourmap[v.drawn])
                x, y = k
                glVertex2f(x + .05, y + .05)
                glVertex2f(x + .05, y + .95)
                glVertex2f(x + .95, y + .95)
                glVertex2f(x + .95, y + .05)
        glColor4f(.5, .5, .5, .8)
        for k, v in self.map.zones.items():
            pos, size = v
            px, py = pos
            sx, sy = size
            glVertex2f(px + 0.1, py + 0.1)
            glVertex2f(px + 0.1, py + sy - 0.1)
            glVertex2f(px + sx - 0.1, py + sy - 0.1)
            glVertex2f(px + sx - 0.1, py + 0.1)
        
        glColor3f(.5, 0, 1)
        for cls, pos, dir in self.map.entities:
            px, py = pos
            px += .5
            py += .5
            glVertex2f(px + (.5 if dir == EAST else .3), py)
            glVertex2f(px, py + (.5 if dir == NORTH else .3))
            glVertex2f(px - (.5 if dir == WEST else .3), py)
            glVertex2f(px, py - (.5 if dir == SOUTH else .3))
        glEnd()
        glPopMatrix()
        
        for label in self.zone_labels.values():
            label.draw()
        for label in self.entity_labels.values():
            label.draw()
        glPopMatrix()        
        if self.entrymode is not None:
            glBegin(GL_QUADS)
            glColor4f(.25, .25, .25, .75)
            glVertex2f(25, 50)
            glVertex2f(275, 50)
            glVertex2f(275, 175)
            glVertex2f(25, 175)
            glEnd()
            self.prompt.draw()
            self.entry.draw()
        if self.ui_mode == 'placeentity':
            glBegin(GL_QUADS)
            glColor4f(.25, .25, .25, .75)
            glVertex2f(25, 400)
            glVertex2f(275, 400)
            glVertex2f(275, 440)
            glVertex2f(25, 440)
            glEnd()
            
            self.entity_display.draw()
                        