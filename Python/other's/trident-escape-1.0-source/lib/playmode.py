"""Mode handler for normal play of the game."""

from __future__ import division

import pyglet
from pyglet.gl import *
from pyglet.window.key import *
from pyglet.event import EVENT_HANDLED, EVENT_UNHANDLED

import random
import math

import mode
import sprite
import animlist
import entity

import music

from world import Map
from game import Game

from common import *
from constants import *

class AlphaTestGroup(pyglet.graphics.Group):
    def set_state(self):
        glEnable(GL_ALPHA_TEST)
        glEnable(GL_DEPTH_TEST)
        glAlphaFunc(GL_GREATER, 0.5)
    
    def unset_state(self):
        glDisable(GL_ALPHA_TEST) 
        glDisable(GL_DEPTH_TEST)

class Explosion(object):
    def __init__(self, x, y, old_sprite=None):
        self.x = x
        self.y = y
        self._frame = 0
        self.frame = 0
        self.anim = animlist.explosion
        self.sprite = None
        self.old_sprite = old_sprite
        self.finished = False
        self.speed = .5 + random.random()
    def update(self):
        self._frame += self.speed
        self.frame = int(self._frame)
        if self.old_sprite and self.frame > self.anim.cycle / 2:
            self.old_sprite.delete()
            self.old_sprite = None
        if self.frame > 20:
            self.finished = True
              
class PlayMode(mode.Mode):
    name = "play"
    
    def __init__(self, game=None):
        super(PlayMode, self).__init__()
        if game is None:
            self.game = Game()
        else:
            self.game = game
        self.game.push_handlers(self)
        self.missing_tile = pyglet.image.load("data/images/tiles/pppp.png")
        self.shadow_img = pyglet.image.load("data/images/shadow.png")
        self.shadow_img.anchor_x = self.shadow_img.width // 2
        self.shadow_img.anchor_y = self.shadow_img.height // 4
        
        self.tile_cache = {}
        self.tile_bin = pyglet.image.atlas.TextureBin()
        self.batch = pyglet.graphics.Batch()
        self.tile_group = pyglet.graphics.OrderedGroup(0)
        self.trident_vlist = None
        self.shadow_group = pyglet.graphics.OrderedGroup(1)
        self.entity_group = AlphaTestGroup(pyglet.graphics.OrderedGroup(2))
        self.trident_group = pyglet.graphics.TextureGroup(pyglet.image.load("data/images/trident_body.png").texture, self.entity_group)
        self.dia_batch = pyglet.graphics.Batch()
        self.frame_group = pyglet.graphics.TextureGroup(pyglet.image.load("data/images/frame.png").texture, pyglet.graphics.OrderedGroup(0))
        self.frame_vlist = None
        self.tiles = []
        self.debug_hitbox = False
        self.entity_sprs = {}
        self.shadows = {}
        self.explosions = []
        self.dialogue = pyglet.text.Label("", font_name="Komika Display", font_size=18, x=100, y=100, color=(0, 0, 0, 255), multiline=True, width=600, anchor_y='bottom', group=pyglet.graphics.OrderedGroup(1), batch=self.dia_batch)
        self.death_count = DEATH_TICKS

    def connect(self, control):
        super(PlayMode, self).connect(control)
        self.music = music.Player()
        self.game.begin()
    
    def on_switch_music(self, track):
        self.music.switch(track)
           
    def on_enter_area(self):
        for t in self.tiles:
            t.delete()
        self.tiles = []
        for s in self.entity_sprs:
            self.entity_sprs[s].delete()
        for s in self.shadows:
            try:
                self.shadows[s].delete()
            except AttributeError:
                pass
        self.entity_sprs = {}
        for e in self.game.entities:
            self.make_entity_sprite(e)
        
        map_tiles = self.game.map.keys()
        draw_tiles = [(x,y) for x, y in map_tiles] + [(x-1,y) for x, y in map_tiles] + [(x,y-1) for x, y in map_tiles] + [(x-1,y-1) for x, y in map_tiles]
        draw_tiles = list(set(draw_tiles))
        m = self.game.map
        for x, y in draw_tiles:
            tile_name = m[x,y].drawn + m[x+1,y].drawn + m[x,y+1].drawn + m[x+1,y+1].drawn + '.png'
            try:
                tile_img = self.tile_cache[tile_name]
            except KeyError:
                try:
                    tile_img = self.tile_bin.add(pyglet.image.load('data/images/tiles/' + tile_name))
                except IOError:
                    tile_img = self.missing_tile
                self.tile_cache[tile_name] = tile_img
            self.tiles.append(sprite.Sprite(tile_img, x=(x+.5)*TILE_SIZE_IMG, y=(y+.5)*TILE_SIZE_IMG, group=self.tile_group, batch=self.batch))

    def on_create_entity(self, ent):
        self.make_entity_sprite(ent)

    def on_destroy_entity(self, ent, explode):
        if ent in self.entity_sprs:
            if explode:
                ex = Explosion(ent.x + (ent.width / 2), ent.y - EXPLOSION_OFFSET, self.entity_sprs[ent])
                ex.sprite = sprite.Sprite(ex.anim.get_image(ex), batch=self.batch, group=self.entity_group)
                self.explosions.append(ex)
                del self.entity_sprs[ent]
            else:
                self.entity_sprs[ent].delete()
                del self.entity_sprs[ent]
            
            if isinstance(ent, entity.TridentHead):
                self.trident_vlist.delete()
                self.trident_vlist = None
            else:
                if ent in self.shadows:
                    self.shadows[ent].delete()
                    del self.shadows[ent]
                
    def on_detonate(self, x, y):
        for vx in (-0.5,0,0.5):
            for vy in (-0.5,0,0.5):
                ex = Explosion(x+vx*DETONATION_RANGE, y+vy*DETONATION_RANGE, None)
                ex.sprite = sprite.Sprite(ex.anim.get_image(ex), batch=self.batch, group=self.entity_group)
                self.explosions.append(ex)
                
    def on_dialogue(self, dia):
        self.dialogue.text = dia
        if dia:
            vxs = []
            txs = []
            w, h = self.dialogue.content_width, self.dialogue.content_height
            cx, cy = self.window.width // 2, self.window.height // 4
            xs = [cx - w/2 - 32, cx - w/2, cx + w/2, cx + w/2 + 32]
            ys = [cy - h/2 - 32, cy - h/2, cy + h/2, cy + h/2 + 32]
            us = [0, .25, .75, 1]
            for i in xrange(3):
                for j in xrange(3):
                    vxs.extend([xs[i], ys[j], xs[i+1], ys[j], xs[i+1], ys[j+1], xs[i], ys[j+1]])
                    txs.extend([us[i], us[j], us[i+1], us[j], us[i+1], us[j+1], us[i], us[j+1]])
            self.frame_vlist = self.dia_batch.add(36, GL_QUADS, self.frame_group, ('v2f', vxs), ('t2f', txs))
            self.dialogue.x = cx - w/2
            self.dialogue.y = cy - h/2
        else:
            self.frame_vlist.delete()
            self.frame_vlist = None
                
    def tick(self):
        if self.game.player.is_dead:
            self.death_count -= 1
        
        if self.death_count == 0:
            self.death_count = DEATH_TICKS
            self.game.restart_area()
            
        
        if self.dialogue.text:
            return
        
        if not self.game.script:
            if self.keys[SPACE] and not self.game.player.is_dead:
                self.game.player_attack()
            else:
                self.game.player_release()
        dx = 0
        dy = 0
        direction = None
        if self.keys[UP]:
            dy += PLAYER_SPEED
            direction = NORTH
        if self.keys[DOWN]:
            dy -= PLAYER_SPEED
            direction = SOUTH
        if self.keys[LEFT]:
            dx -= PLAYER_SPEED
            direction = WEST
        if self.keys[RIGHT]:
            dx += PLAYER_SPEED
            direction = EAST
        if dx: dy = 0
        self.game.player.dx = dx
        self.game.player.dy = dy
        self.game.player.move_direction = direction
        self.game.tick()
        
        for e in self.explosions:
            e.update()
        self.explosions = [e for e in self.explosions if not e.finished]

    def make_entity_sprite(self, e):
        if not e.anim:
            e.anim = animlist.__dict__[e.anim_name]
        self.entity_sprs[e] = sprite.Sprite(e.anim.get_image(e), batch=self.batch, group=self.entity_group)
        if isinstance(e, entity.TridentHead):
            p = self.game.player
            
            self.trident_vlist = self.batch.add(4, GL_QUADS, self.trident_group, ('v3f', (0,) * 12), ('t2f', [0, 0, 0, 1, 1, 1, 1, 0]), ('c4B', (255,) * 16))
        elif e.shadow:
            self.shadows[e] = sprite.Sprite(self.shadow_img, batch=self.batch, group=self.shadow_group)
        
    def on_draw(self):
        self.window.clear()
        glDisable(GL_DEPTH_TEST)
        sf = TILE_SIZE_SCREEN / TILE_SIZE_IMG

        glPushMatrix()
        glTranslatef(self.window.width / 2-int(self.game.player.x * TILE_SIZE_SCREEN), self.window.height / 2 - int(self.game.player.y * TILE_SIZE_SCREEN), 0)

        glScalef(sf, sf, 1)
        p = self.game.player
        if p.is_dead and p.fall_counter == 0:
            p.anim = animlist.__dict__[p.dead_anim_name]
        elif p.attack_counter > 0:
            p.anim = animlist.__dict__[p.att_anim_name]
        else:
            p.anim = animlist.__dict__[p.std_anim_name]
            
        for e in self.game.entities:
            spr = self.entity_sprs[e]
            spr.x = (e.x + (e.width / 2)) * TILE_SIZE_IMG
            
            
            if isinstance(e, entity.TridentHead):
                spr.y = (e.y + (e.height / 2)) * TILE_SIZE_IMG
                spr.z = -(e.y + 1) * 0.001
            else:
                spr.y = e.y * TILE_SIZE_IMG
                spr.z = -e.y * 0.001 - (0.5 if e.low_level else 0)
            spr.image = e.anim.get_image(e)
            if e.thrown:
                spr.rotation += 30
                theta = math.radians(spr.rotation)
                ct = math.cos(theta)
                st = math.sin(theta)
                spr.x += - st * TILE_SIZE_IMG * (0.5 if e.tall else 0.25)
                spr.y += (1 - ct) * TILE_SIZE_IMG * (0.5 if e.tall else 0.25)
            else:
                spr.rotation = 0
            if e.rot_anim:
                spr.rotation = {EAST: 0, NORTH: 270, WEST:180, SOUTH: 90}[e.direction]

            if isinstance(e, entity.TridentHead):
                px, py = p.x + p.width / 2, p.y + p.height / 2
                ex, ey = e.x + e.width / 2, e.y + e.height / 2
                z = -.001 * (py + 1)
                if e.direction in (NORTH, SOUTH):
                    y = py + (.75 if e.direction == NORTH else -.25)
                    coords = [px - .5, y, z, px + .5, y, z, ex + .5, ey, z, ex - .5, ey, z]
                else:
                    x = px + (.5 if e.direction == EAST else -.5)
                    coords = [x, py - .5, z, x, py + .5, z, ex, ey + .5, z, ex, ey - .5, z]
                coords = [(TILE_SIZE_IMG * x) // 1 if n % 3 in (0,1) else x for n, x in enumerate(coords)]
                self.trident_vlist.vertices[:] = coords
            elif e.shadow:
                self.shadows[e].x = (e.x + e.width / 2) * TILE_SIZE_IMG
                self.shadows[e].y = (e.y) * TILE_SIZE_IMG
            if e.fall_counter > 0:
                dx, dy = e.fall_vector()
                theta = math.radians(e.fall_counter * 20)
                ct = math.cos(theta)
                st = math.sin(theta)
                spr.x += e.fall_counter * dx * 4 - st * TILE_SIZE_IMG * (0.5 if e.tall else 0.25)
                spr.y += e.fall_counter * dy * 4 + (1 - ct) * TILE_SIZE_IMG * (0.5 if e.tall else 0.25)
                spr.rotation = e.fall_counter * 20
                spr.opacity = 255 * (1 - (e.fall_counter / FALL_TIME))
        for ex in self.explosions:
            ex.sprite.x = ex.x * TILE_SIZE_IMG
            ex.sprite.y = ex.y * TILE_SIZE_IMG
            ex.sprite.z = -ex.y * 0.001
            ex.sprite.image = ex.anim.get_image(ex)
            ex.sprite.opacity = 255 - ex.frame * 5
            ex.sprite.scale = 1.01 ** ex.frame
        self.batch.draw()

        if self.debug_hitbox:
            glPushMatrix()
            glScalef(TILE_SIZE_IMG, TILE_SIZE_IMG, 1)
            glColor3f(255,255,255)
            for e in self.game.entities:
                glBegin(GL_LINE_LOOP)
                glVertex2f(e.x, e.y)
                glVertex2f(e.x, e.y + e.height)
                glVertex2f(e.x + e.width, e.y + e.height)
                glVertex2f(e.x + e.width, e.y)
                glEnd()
            for n, z in self.game.map.zones.items():
                p, s = z
                xp, yp = p
                xs, ys = s
                if n in self.game.map.forbid_monster_zones:
                    glColor4f(1,0,0,0.5)
                else:
                    glColor4f(0,1,0,0.5)
                glBegin(GL_POLYGON)
                glVertex2f(xp, yp)
                glVertex2f(xp, yp + ys)
                glVertex2f(xp + xs, yp + ys)
                glVertex2f(xp + xs, yp)
                glEnd()
            for x, y in self.game.paths:
                i = self.game.paths[x, y]
                glColor4f(1,1,0,max(0.5-i/20,0))
                glBegin(GL_POLYGON)
                glVertex2f(x, y)
                glVertex2f(x, y + 1)
                glVertex2f(x + 1, y + 1)
                glVertex2f(x + 1, y)
                glEnd()

            glPopMatrix()
            
        glPopMatrix()
        if self.dialogue.text:
            glColor4f(1,1,1,1)
            self.draw_dialogue()
        if self.death_count < 30:
            a = (30 - self.death_count) / 30
            w, h = self.window.width, self.window.height
            glColor4f(0,0,0,a)
            glBegin(GL_QUADS)
            glVertex2f(0,0)
            glVertex2f(w,0)
            glVertex2f(w,h)
            glVertex2f(0,h)
            glEnd()
            
    def on_key_press(self, sym, mods):
        if sym == H and DEBUG:
            self.debug_hitbox = not self.debug_hitbox
            return EVENT_HANDLED
        if sym == K and DEBUG:
            self.game.flags['key.red'] = True
            self.game.flags['key.yellow'] = True
            self.game.flags['key.green'] = True
        if sym == P and DEBUG:
            while True: pass
        if self.dialogue.text:
            self.on_dialogue('')
            self.game.advance_script()
            return EVENT_HANDLED
        
            
    def draw_dialogue(self):
       
        self.dia_batch.draw()
        