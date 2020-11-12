from __future__ import division

import pyglet

from common import *
from constants import *

def load_image(fn):
    i = pyglet.image.load(fn)
    i.anchor_x = i.width // 2
    return i

class Animation(object):
    def __init__(self, images, frame_duration=5, loop=True):
        self.images = map(lambda fn: load_image("data/images/%s.png" % fn), images)
        self.fd = frame_duration
        self.cycle = len(self.images) * self.fd
        self.loop = loop
        
    def get_image(self, ent):
        if self.loop: 
            return self.images[(ent.frame % self.cycle) // self.fd]
        else:
            return self.images[min(ent.frame // self.fd, len(self.images) - 1)]

class ConstantAnimation(Animation):
    def get_image(self, ent):
        return self.images[(ent.game.ticks % self.cycle) // self.fd]
            
class DirectionAnimationSet(object):
    def __init__(self, anim_index):
        self.anim_index = anim_index
    def get_image(self, e):
        return self.anim_index[e.direction].get_image(e)

class MovingAnimationSet(object):
    def __init__(self, static_anim, moving_anim):
        self.static_anim = static_anim
        self.moving_anim = moving_anim
    def get_image(self, e):
        if e.moved:
            return self.moving_anim.get_image(e)
        else:
            return self.static_anim.get_image(e)
            
class StunAnimationSet(object):
    def __init__(self, normal_anim, stun_anim):
        self.normal_anim = normal_anim
        self.stun_anim = stun_anim
    def get_image(self, e):
        if e.stun_timer > 0:
            return self.stun_anim.get_image(e)
        else:
            return self.normal_anim.get_image(e)
            
class TurretAnimationSet(object):
    def __init__(self, images, frame_duration=5):
        self.images = map(lambda fn: load_image("data/images/%s.png" % fn), images)
        self.fd = frame_duration
    def get_image(self, e):
        if e.fire_timer < self.fd:
            return self.images[1]
        elif e.fire_timer < 2 * self.fd:
            return self.images[2]
        else:
            return self.images[0]