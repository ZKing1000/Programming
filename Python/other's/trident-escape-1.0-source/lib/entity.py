from __future__ import division

from common import *
from constants import *


class Entity(object):
    anim = None
    rot_anim = False
    x = 0
    y = 0
    width = 0.51
    height = 0.51
    direction = SOUTH
    frame = 0
    moved = False
    bumped = False
    thrown = False
    flying = False
    shadow = True
    fall_counter = 0
    block_path = False
    must_kill = False
    respect_monster_zones = False
    low_level = False
    tall = True
    def __init__(self, game):
        super(Entity, self).__init__()
        self.move_target = None
        self.game = game
        self.zones = frozenset()

    def place_in_cell(self, x, y):
        self.x = x + 0.5 - (self.width / 2)
        self.y = y + 0.5 - (self.height / 2)

    def place_in_zone(self, zone):
        zp, zs = self.game.map.zones[zone]
        zx, zy = zp
        zw, zh = zs
        self.place_in_cell(zx + (zw-1) / 2, zy + (zh-1) / 2)

    def get_centre_cell(self):
        x = int((self.x + (self.width / 2)) // 1)
        y = int((self.y + (self.height/ 2)) // 1)
        return x, y

    def get_noncolliders(self):
        return set([self])
        
    def move(self, dx, dy, direction, avoid_pits=False):
        if direction is not None:
            self.direction = direction
        orig_x = self.x
        orig_y = self.y
        orig_dx = dx
        orig_dy = dy
        hit = None
        obs = self.game.obstacles_in_rect(self.x + dx, self.y, self.width, self.height, ignore=self.get_noncolliders(),
                                          is_monster=self.respect_monster_zones, avoid_pits=avoid_pits)
        if obs:
            if dx > 0:
                mxd, mxo = min([(o[0] - self.width - self.x, o[4]) for o in obs])
                dx = max(0, mxd - COLLISION_BUFFER)
                hit = mxo
            if dx < 0:
                mxd, mxo = max([(o[0] + o[2] - self.x, o[4]) for o in obs])
                dx = min(0, mxd + COLLISION_BUFFER)
                hit = mxo
        self.x += dx
        obs = self.game.obstacles_in_rect(self.x, self.y + dy, self.width, self.height, ignore=self.get_noncolliders(),
                                         is_monster=self.respect_monster_zones, avoid_pits=avoid_pits)
        if obs:
            if dy > 0:
                myd, myo = min([(o[1] - self.height - self.y, o[4]) for o in obs])
                dy = max(0, myd - COLLISION_BUFFER)
                hit = myo
            if dy < 0:
                myd, myo = max([(o[1] + o[3] - self.y, o[4]) for o in obs])
                dy = min(0, myd + COLLISION_BUFFER)
                hit = myo
        self.y += dy
        self.moved = not(self.x == orig_x and self.y == orig_y)
        self.bumped = not(self.x == orig_x + orig_dx and self.y == orig_y + orig_dy)
        if isinstance(hit, Entity):
            self.hit_entity(hit)
            hit.hit_entity(self)

        if self.moved:
            z = self.game.map.zones_for_rect(self.x, self.y, self.width, self.height)
            new_zones = z - self.zones
            for nz in new_zones:
                self.game.entity_enter_zone(self, nz)
            self.zones = frozenset(z)
            
        if orig_dx or orig_dy:
            self.frame = self.frame + 1
    
    def cutscene_tick(self):
        if self.move_target:

            tx, ty = self.move_target
            if tx <= self.x <= tx + 1 - self.width and ty <= self.y <= ty + 1 - self.height:
                self.move_target = None
                self.frame = 0
                return
            else:
                direction = self.direction
                cx, cy = self.get_centre_cell()
                if cx != tx or cy != ty:
                    sgmp = self.move_map
                    p = sgmp[cx, cy]
                    if sgmp.get((cx-1, cy), 1000) < p: direction = WEST
                    if sgmp.get((cx+1, cy), 1000) < p: direction = EAST
                    if sgmp.get((cx, cy-1), 1000) < p: direction = SOUTH
                    if sgmp.get((cx, cy+1), 1000) < p: direction = NORTH
                if direction in (NORTH, SOUTH):
                    if self.x <= cx: direction = EAST
                    if self.x + self.width >= cx + 1: direction = WEST
                else:
                    if self.y <= cy: direction = NORTH
                    if self.y + self.height >= cy + 1: direction = SOUTH
                vec = vector_in_direction(direction, self.speed)
                self.move(vec[0], vec[1], direction, avoid_pits=True)
                return True
                
    def tick(self):
        if self.fall_counter == 0:
            if not self.flying and self.game.player.caught_monster is not self and not self.thrown:
                ctrx = (self.x + (self.width / 2)) // 1
                ctry = (self.y + (self.height/ 2)) // 1
                if self.game.map[ctrx, ctry].pit:
                    self.fall_counter = 1
        else:
            self.fall_counter += 1
            if self.fall_counter >= FALL_TIME:
                self.game.destroy_entity(self)
        if not self.moved:
            self.frame = 0
        
    def hit_entity(self, ent):
        pass
        
    def hurt(self, major=False):
        pass
        
    def start_room(self):
        z = self.game.map.zones_for_rect(self.x, self.y, self.width, self.height)
        for nz in z:
            self.game.entity_enter_zone(self, nz)
        self.zones = frozenset(z)
    def set_move_target(self, cell):
        self.move_target = cell
        self.move_map = self.game.get_path_map(cell)

    def fall_vector(self):
        dx = 0
        dy = 0
        for x in [-.25, .25]:
            for y in [-.25, .25]:
                cx, cy = int((self.x + self.width/2 + x) // 1), int((self.y + self.height/2 + y) // 1)
                if self.game.map[cx, cy].pit:
                    dx += x
                    dy += y
        return dx, dy
class Player(Entity):
    attacking = False
    attack_counter = 0
    weapon = None
    initial_attack = False
    caught_monster = None
    caught_monster_offset = None
    wdx = 0
    wdy = 0
    is_dead = False
    std_anim_name = "fishgirl"
    att_anim_name = "attack"
    dead_anim_name = "deadfishgirl"
    anim_name = "fishgirl"
    speed = PLAYER_SPEED
    
    def get_noncolliders(self):
        if (self.caught_monster is None or self.caught_monster.anchored):
            return set([self, self.weapon])
        return set([self, self.weapon, self.caught_monster])
    
    def can_move(self):
        return (self.weapon is None or (self.attack_counter == 0 and not self.initial_attack)) and not (self.is_dead)
        
    def attack(self):
        if self.attack_counter == 0 and not self.attacking:
            dx, dy = vector_in_direction(self.direction, 0.5)
            self.weapon = self.game.create_entity(TridentHead, self.x + self.width / 2 - TridentHead.width / 2 + dx,
                                                 self.y + self.height / 2 - TridentHead.height / 2 + dy)
            self.initial_attack = True
            self.wdx, self.wdy = {NORTH: (0,WEAPON_SPEED),
                                  SOUTH: (0,-WEAPON_SPEED),
                                  EAST: (WEAPON_SPEED,0),
                                  WEST: (-WEAPON_SPEED,0)}[self.direction]
        if self.initial_attack:
            self.attack_counter += 1
            self.weapon.move(self.wdx, self.wdy, self.direction)
            if self.weapon.bumped:
                self.initial_attack = False
        self.attacking = True
        
    def tick(self):
        if self.can_move():
            self.move(self.dx, self.dy, self.move_direction)
        if self.is_dead:
            super(Player, self).tick()
            return
        # if carrying a monster, line it up with the player so it's less likely to clip a wall when thrown
        if self.caught_monster is not None and self.caught_monster_offset is not None:
            xo, yo = self.caught_monster_offset
            xo = max(0, xo - 0.05)
            xo = min(0, xo + 0.05)
            yo = max(CARRY_DIST, yo - 0.05)
            yo = min(CARRY_DIST, yo + 0.05)
            self.caught_monster_offset = (xo, yo)
            offs = rotate_vector(self.caught_monster_offset[0], self.caught_monster_offset[1], self.direction)
            self.caught_monster.x = offs[0] + self.x
            self.caught_monster.y = offs[1] + self.y
        # if attack key not held and a monster is carried, throw it
        if not self.attacking:
            if self.caught_monster is not None and self.attack_counter == 0:
                self.throw_monster()
            self.caught_monster = None
            self.initial_attack = False
        # if the trident is out, retract it
        if self.attack_counter > 0:
            if not self.initial_attack and self.attack_counter > 0:
                if self.caught_monster:
                    if self.caught_monster.anchored:
                        # if we hit a rock, pull towards it
                        self.move(self.wdx, self.wdy, None)
                        self.attack_counter -= 1
                        if self.bumped:
                            self.caught_monster = None
                    else:
                        self.caught_monster.move(-self.wdx, -self.wdy, None)
                        if self.caught_monster and self.caught_monster.bumped:
                            # monster hit something on the way back
                            moffs = (self.caught_monster.x - self.weapon.x, self.caught_monster.y - self.weapon.y)
                            rmoffx, rmoffy = unrotate_vector(moffs[0], moffs[1], self.direction)
                            if rmoffx == 0:
                                self.caught_monster = None
                            else:
                                rmoffdx = max(min(-rmoffx, 0.05), -0.05)
                                mx, my = rotate_vector(rmoffdx, 0, self.direction)
                                self.caught_monster.move(mx, my, None)
                                if self.caught_monster.bumped:
                                    self.caught_monster = None
                        else:
                            # reeling in the monster happily
                            self.attack_counter -= 1
                            self.weapon.move(-self.wdx, -self.wdy, self.direction)                            
                else:
                    # if no monster, always retract trident
                    self.attack_counter -= 1
                    self.weapon.move(-self.wdx, -self.wdy, self.direction)
        # if the trident has just come back, get rid of it and start carrying the monster
        if self.attack_counter <= 0 and self.weapon is not None:
            self.game.destroy_entity(self.weapon)
            self.weapon = None
            if self.caught_monster:
                if self.caught_monster.anchored:
                    self.caught_monster = None
                else:
                    self.caught_monster_offset = unrotate_vector(self.caught_monster.x - self.x,
                                                                 self.caught_monster.y - self.y, self.direction)
        
        super(Player, self).tick()
        if self.fall_counter > 0 and not self.is_dead:
            self.hurt()
        
    def throw_monster(self):
        m = self.caught_monster
        m.thrown = True
        m.direction = self.direction
        if len(self.game.obstacles_in_rect(m.x, m.y, m.width, m.height, ignore=m.get_noncolliders())) > 0:
            m.thrown_impact()
            
    def hurt(self, major=False):
        if not self.is_dead:
            self.is_dead = True
            if self.caught_monster is not None and self.attack_counter == 0:
                self.throw_monster()
            self.caught_monster = None
            self.initial_attack = False
            if self.weapon is not None:
                self.game.destroy_entity(self.weapon)
    
    def reincarnate(self):
        self.is_dead = False
        self.fall_counter = 0
        
    @property
    def flying(self):
        return self.caught_monster and self.caught_monster.anchored

class TridentHead(Entity):
    width = 0.4
    height = 0.4
    anim_name = "trident"
    rot_anim = True
    flying = True
    def get_noncolliders(self):
        return set([self, self.game.player])
        
    def hit_entity(self, ent):
        if isinstance(ent, Monster) and ent.catchable:
            if self.game.player.initial_attack:
                self.game.player.initial_attack = False
                self.game.player.caught_monster = ent
                self.game.player.caught_monster_offset = None

class Monster(Entity):
    anchored = False
    catchable = True
    must_kill = True
    respect_monster_zones = True
    def __init__(self, game):
        super(Monster, self).__init__(game)
        self.parents = set()

    def get_noncolliders(self):
        if self.thrown or self.game.player.caught_monster is self:
            return set([self, self.game.player, self.game.player.weapon]) | self.parents
        else:
            return set([self]) | self.parents

    def tick(self):
        if self.thrown:
            v = vector_in_direction(self.direction, THROW_SPEED)
            self.move(v[0], v[1], None)
            if self.bumped:
                self.thrown_impact()
        elif self.game.player.caught_monster == self:
            pass
        elif self.fall_counter > 0:
            pass
        else:
            self.monster_move()
        
        super(Monster, self).tick()
        
        if self.parents:
            overlapping = self.game.obstacles_in_rect(self.x, self.y, self.width, self.height, ignore=set())
            self.parents &= set([t[4] for t in overlapping])

    def hit_entity(self, ent):
        if self.thrown and ent is not self.game.player:
            self.thrown_impact_entity(ent)
            if not self.bumped:
                self.thrown_impact()
        if ent is self.game.player and not self.thrown and not self.game.player.is_dead:
            ent.hurt()
            self.hurt()

class NPC(Entity):
    anim_name = "oldman"
    talk_func = None
    speed = 0.05
    def get_noncolliders(self):
        return set([self, self.game.player.weapon])
    def hit_entity(self, ent):
        if ent is self.game.player:
            if self.talk_script:
                assert not self.game.script
                self.game.script = self.talk_script()
                self.game.advance_script()
class Scenery(Entity):
    block_path = True
    destructible = False
    width = 0.55
    height = 0.55
    def hurt(self, major=False):
        if self.destructible:
            self.game.destroy_entity(self, explode=True)
