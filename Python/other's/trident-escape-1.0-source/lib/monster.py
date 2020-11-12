from __future__ import division

import random

from common import *
from constants import *

from entity import Entity, Monster, TridentHead

class BaseMonster(Monster):
    speed = 0.05
    catchable = True
    
    def thrown_impact(self):
        # when this is called, it's possible that the monster is over a wall or in other illegal location
        self.game.destroy_entity(self, explode=True)

    def thrown_impact_entity(self, ent):
        # this is called before thrown_impact if thrown monster hit another entity
        ent.hurt()

    def hurt(self, major=False):
        # this monster's default response to being injured, e.g. by a thrown monster
        self.game.destroy_entity(self, explode=True)
        
    def monster_move(self):
        # override this for monster-specific movement logic
        pass

class BackForthMonster(BaseMonster):
    def start_room(self):
        super(BackForthMonster, self).start_room()
        self.initial_dir = self.direction
        self.other_dir = opposite_dir(self.direction)
    def monster_move(self):
        if self.direction not in (self.initial_dir, self.other_dir):
            self.direction = random.choice([self.initial_dir, self.other_dir])
        vec = vector_in_direction(self.direction, self.speed)
        self.move(vec[0], vec[1], self.direction)
        if self.bumped:
            self.direction = opposite_dir(self.direction)

class Spookydile(BackForthMonster):
    direction = EAST
    anim_name = 'spookydile'
    catchable = True    
    tall = False
    
class CatKnight(BackForthMonster):
    speed = 0.03
    anim_name = 'catknight'
    catchable = False
    
class CatKnightShield(CatKnight):
    anim_name = 'catknight_s'
    def hurt(self, major=False):
        if major:
            super(CatKnightShield, self).hurt(major=True)
    def hit_entity(self, ent):
        # this is ugly. sorry.
        if ent is self.game.player and not self.game.player.is_dead:
            ent.hurt()
            self.hurt()
        if ent.thrown or isinstance(ent, TurretProjectile):
            offs = unrotate_vector(ent.x - self.x, ent.y - self.y, self.direction)
            if offs[1] < abs(offs[0]):
                self.hurt(major=True)
            else:
                self.bumped = False

    
class BaseFuzzle(BaseMonster):
    catchable = True
    direction = NORTH
    tall = False
    def monster_move(self):
        vec = vector_in_direction(self.direction, self.speed)
        self.move(vec[0], vec[1], self.direction)
        if self.bumped:
            self.rotate()
    
class FuzzleLeft(BaseFuzzle):
    anim_name = "fuzzle_r"
    def rotate(self):
        self.direction = rotate_ccw(self.direction)
    
class FuzzleRight(BaseFuzzle):
    anim_name = "fuzzle_b"
    def rotate(self):
        self.direction = rotate_cw(self.direction)

class FloatingEyeLeft(FuzzleLeft):
    tall = False
    anim_name = "eye_red"
    flying = True

class FloatingEyeRight(FuzzleRight):
    tall = False
    anim_name = "eye_blue"
    flying = True

class Mine(BaseMonster):
    catchable = True
    anim_name = "mine"
    must_kill = False
    tall = False
    @property
    def block_path(self):
        return self is not self.game.player.caught_monster
    def thrown_impact(self):
        self.hurt()
    def hurt(self, major=False):
        super(Mine, self).hurt()
        self.game.detonate(self.x + self.width / 2, self.y + self.height / 2)
    
class WanderingMonster(BaseMonster):
    def monster_move(self):
        dx, dy = vector_in_direction(self.direction, self.speed)
        self.move(dx, dy, self.direction)
        if self.bumped or random.random() < 0.01:
            self.direction = random.choice([NORTH, SOUTH, EAST, WEST])

class Squid(WanderingMonster):
    catchable = True
    anim_name = "squid"

class ChaserMonster(BaseMonster):
    sense_range = None
    last_change = 0
    def monster_move(self):
        self.moved = False
        if self.sense_range is not None:
            direction = None
        else:
            direction = self.direction
            if self.last_change < self.game.ticks - 10:
                direction = random.choice([NORTH, SOUTH, EAST, WEST])
                self.last_change = self.game.ticks
        cx, cy = self.get_centre_cell()
        sgmp = self.game.paths
        if sgmp.has_key((cx, cy)):
            p = sgmp[cx, cy]
            if self.sense_range is None or p <= self.sense_range:
                if sgmp.get((cx-1, cy), 1000) < p: direction = WEST
                if sgmp.get((cx+1, cy), 1000) < p: direction = EAST
                if sgmp.get((cx, cy-1), 1000) < p: direction = SOUTH
                if sgmp.get((cx, cy+1), 1000) < p: direction = NORTH
        if direction in (NORTH, SOUTH):
            if self.x <= cx: direction = EAST
            if self.x + self.width >= cx + 1: direction = WEST
        elif direction in (EAST, WEST):
            if self.y <= cy: direction = NORTH
            if self.y + self.height >= cy + 1: direction = SOUTH
        if direction is not None:
            vec = vector_in_direction(direction, self.speed)
            self.move(vec[0], vec[1], direction, avoid_pits=True)

class Spider(ChaserMonster):
    catchable = True
    anim_name = "spider"

class BarrelBeast(ChaserMonster):
    catchable = True
    sense_range = 5
    anim_name = "barrelbeast"
    
class CrawlingBomb(ChaserMonster):
    tall = False
    stun_timer = 0
    def thrown_impact(self):
        obs = self.game.obstacles_in_rect(self.x, self.y, self.width, self.height,
                                          ignore=self.get_noncolliders(), is_monster=self.respect_monster_zones)
        if len(obs) == 0:
            self.thrown = False
            self.hurt()
        else:
            self.detonate()
    def detonate(self):
        self.game.destroy_entity(self, explode=True)
        self.game.detonate(self.x + self.width / 2, self.y + self.height / 2)
    def hurt(self, major=False):
        if major:
            self.detonate()
        else:
            self.stun_timer = 60
    def monster_move(self):
        if self.stun_timer > 0:
            self.stun_timer -= 1
        else:
            super(CrawlingBomb, self).monster_move()
    def hit_entity(self, ent):
        if ent is self.game.player and not self.thrown:
            self.detonate()
        else:
            super(CrawlingBomb, self).hit_entity(ent)
    
class EasyCrawlingBomb(CrawlingBomb):
    anim_name = "easybomb"
    
class HardCrawlingBomb(CrawlingBomb):
    anim_name = "hardbomb"
    @property
    def catchable(self):
        return self.stun_timer > 0
    def hurt(self, major=False):
        super(HardCrawlingBomb, self).hurt(major=False)

class BadassOldMan(HardCrawlingBomb):
    anim_name = "eviloldman"
        
class Sparky(BackForthMonster):
    anim_name = "sparky"
    catchable = True
    flying  = True
    def hit_entity(self, ent):
        ent.hurt()
        if ent is self.game.player:
            self.hurt()
    def hurt(self, major=False):
        super(Sparky, self).hurt()
        self.game.detonate(self.x + self.width / 2, self.y + self.height / 2)
    def tick(self):
        if self.game.player.caught_monster is self and self.game.player.attack_counter == 0:
            self.hurt()
        else:
            super(Sparky, self).tick()
    
class Turret(BaseMonster):
    catchable = False
    fire_timer = TURRET_FIRE_TIME
    def hurt(self, major=False):
        if major:
            super(Turret, self).hurt()
    anim_name = "turret"
    def tick(self):
        self.fire_timer -= 1
        if self.fire_timer <= 0 and len(self.game.obstacles_in_rect(self.x - COLLISION_BUFFER, self.y - COLLISION_BUFFER,
                                        self.width + 2*COLLISION_BUFFER, self.height + 2*COLLISION_BUFFER, set([self]))) == 0:
            m = self.game.create_entity(TurretProjectile, self.x + self.width/2 - TurretProjectile.width/2, self.y+0.3)
            m.direction = self.direction
            m.parents.add(self)
            self.fire_timer = TURRET_FIRE_TIME

class TurretProjectile(BaseMonster):
    catchable = False
    flying = True
    shadow = False
    speed = 0.12
    height = 0.25
    width = 0.25
    must_kill = False
    anim_name = "bullet"
    def monster_move(self):
        vec = vector_in_direction(self.direction, self.speed)
        self.move(vec[0], vec[1], self.direction)
        if self.bumped:
            self.hurt()
    def hit_entity(self, ent):
        ent.hurt()
        if isinstance(ent, TridentHead):
            self.bumped = False # so we don't explode
        else:
            self.hurt()
    
class PetRock(BaseMonster):
    anim_name = "rock"
    catchable = True
    anchored = True
    block_path = True
    must_kill = False
    def hurt(self, major=False):
        return
    def hit_entity(self, ent):
        pass
