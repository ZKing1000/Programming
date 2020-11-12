from __future__ import division

from anim import Animation, ConstantAnimation, DirectionAnimationSet, MovingAnimationSet, StunAnimationSet, TurretAnimationSet

from common import *
from constants import *

# The heroine herself

fishgirl = DirectionAnimationSet({ NORTH: Animation(map(lambda n: "fishgirl_n_%d" % n, [1, 2, 1, 3]), frame_duration=5),
                                   SOUTH: Animation(map(lambda n: "fishgirl_s_%d" % n, [1, 2, 1, 3]), frame_duration=5),
                                   EAST: Animation(map(lambda n: "fishgirl_e_%d" % n, [1, 2, 1, 3]), frame_duration=5),
                                   WEST: Animation(map(lambda n: "fishgirl_w_%d" % n, [1, 2, 1, 3]), frame_duration=5)})

attack = DirectionAnimationSet({ NORTH: Animation(['fishgirl_attack_n']),
                                 SOUTH: Animation(['fishgirl_attack_s']),
                                 EAST: Animation(['fishgirl_attack_e']),
                                 WEST: Animation(['fishgirl_attack_w'])})
                                                                 
trident = Animation(['trident_head'])
i = trident.images[0]
i.anchor_y = i.height // 2

deadfishgirl = Animation(['fishgirl_dead'])
deadfishgirl.images[0].anchor_y = 10

# The cast of NPCs

oldman = DirectionAnimationSet({ NORTH: Animation(map(lambda n: "oldman_n_%d" % n, [1, 2, 1, 3]), frame_duration=5),
                                 SOUTH: Animation(map(lambda n: "oldman_s_%d" % n, [1, 2, 1, 3]), frame_duration=5),
                                 EAST: Animation(map(lambda n: "oldman_e_%d" % n, [1, 2, 1, 3]), frame_duration=5),
                                 WEST: Animation(map(lambda n: "oldman_w_%d" % n, [1, 2, 1, 3]), frame_duration=5)})

# Monsters

squid = Animation(map(lambda n: "squid_%d" % n, [1, 2, 3, 4]))

spider = DirectionAnimationSet({ NORTH: Animation(map(lambda n: "spider_n_%d" % n, [1, 2, 3, 4]), frame_duration=5),
                                 SOUTH: Animation(map(lambda n: "spider_s_%d" % n, [1, 2, 3, 4]), frame_duration=5),
                                 EAST: Animation(map(lambda n: "spider_e_%d" % n, [1, 2, 3, 4]), frame_duration=5),
                                 WEST: Animation(map(lambda n: "spider_w_%d" % n, [1, 2, 3, 4]), frame_duration=5)})

eye_blue = DirectionAnimationSet({ NORTH: Animation(map(lambda n: "eye_n_%d" % n, [1, 2, 1, 3]), frame_duration=5),
                                   SOUTH: Animation(map(lambda n: "eye_s_%d" % n, [1, 2, 1, 3]), frame_duration=5),
                                   EAST: Animation(map(lambda n: "eye_e_%d" % n, [1, 2, 1, 3]), frame_duration=5),
                                   WEST: Animation(map(lambda n: "eye_w_%d" % n, [1, 2, 1, 3]), frame_duration=5)})

eye_red = DirectionAnimationSet({ NORTH: Animation(map(lambda n: "reye_n_%d" % n, [1, 2, 1, 3]), frame_duration=5),
                                  SOUTH: Animation(map(lambda n: "reye_s_%d" % n, [1, 2, 1, 3]), frame_duration=5),
                                  EAST: Animation(map(lambda n: "reye_e_%d" % n, [1, 2, 1, 3]), frame_duration=5),
                                  WEST: Animation(map(lambda n: "reye_w_%d" % n, [1, 2, 1, 3]), frame_duration=5)})

catknight = DirectionAnimationSet({ NORTH: Animation(map(lambda n: "catwarrior_n_%d" % n, [1, 2, 1, 3]), frame_duration=8),
                                    SOUTH: Animation(map(lambda n: "catwarrior_s_%d" % n, [1, 2, 1, 3]), frame_duration=8),
                                    EAST: Animation(map(lambda n: "catwarrior_e_%d" % n, [1, 2, 1, 3]), frame_duration=8),
                                    WEST: Animation(map(lambda n: "catwarrior_w_%d" % n, [1, 2, 1, 3]), frame_duration=8)})

catknight_s = DirectionAnimationSet({ NORTH: Animation(map(lambda n: "catknight_n_%d" % n, [1, 2, 1, 3]), frame_duration=8),
                                      SOUTH: Animation(map(lambda n: "catknight_s_%d" % n, [1, 2, 1, 3]), frame_duration=8),
                                      EAST: Animation(map(lambda n: "catknight_e_%d" % n, [1, 2, 1, 3]), frame_duration=8),
                                      WEST: Animation(map(lambda n: "catknight_w_%d" % n, [1, 2, 1, 3]), frame_duration=8)})

fuzzle_r = DirectionAnimationSet({ NORTH: Animation(map(lambda n: "rfish_n_%d" % n, [1, 2, 1, 3]), frame_duration=5),
                                   SOUTH: Animation(map(lambda n: "rfish_s_%d" % n, [1, 2, 1, 3]), frame_duration=5),
                                   EAST: Animation(map(lambda n: "rfish_e_%d" % n, [1, 2, 1, 3]), frame_duration=5),
                                   WEST: Animation(map(lambda n: "rfish_w_%d" % n, [1, 2, 1, 3]), frame_duration=5)})

fuzzle_b = DirectionAnimationSet({ NORTH: Animation(map(lambda n: "bfish_n_%d" % n, [1, 2, 1, 3]), frame_duration=5),
                                   SOUTH: Animation(map(lambda n: "bfish_s_%d" % n, [1, 2, 1, 3]), frame_duration=5),
                                   EAST: Animation(map(lambda n: "bfish_e_%d" % n, [1, 2, 1, 3]), frame_duration=5),
                                   WEST: Animation(map(lambda n: "bfish_w_%d" % n, [1, 2, 1, 3]), frame_duration=5)})

edile = Animation(map(lambda n: "dile_%d" % n, [1, 2, 3, 4]))
wdile = Animation(map(lambda n: "wdile_%d" % n, [1, 2, 3, 4]))
spookydile = DirectionAnimationSet({ NORTH: edile, SOUTH: wdile, EAST: edile, WEST: wdile})

sparky = Animation(map(lambda n: "sparky%d" % n, [1, 2, 3, 4]))

barrelbeast = MovingAnimationSet(Animation(["barrelhide"]), Animation(map(lambda n: "barrelguy_s_%d" % n, [1, 2, 1, 3])))

mine = Animation(["mine"])

bullet = Animation(["bullet"])

easybomb = StunAnimationSet(Animation(map(lambda n: "scuttlebomb%d" % n, [1,2,1,3])),
                            ConstantAnimation(map(lambda n: "scuttlestun%d" % n, [1,2,3])))

hardbomb = StunAnimationSet(Animation(map(lambda n: "doombomb%d" % n, [1,2,1,3])),
                            ConstantAnimation(map(lambda n: "stunbomb%d" % n, [1,2,3])))

eviloldman = StunAnimationSet(oldman,
                            ConstantAnimation(map(lambda n: "oldmanstun_%d" % n, [1,2,3,4])))

rock = ConstantAnimation(["eyerock"] * 5 + ["eyerock_blink"])
for r in rock.images:
    r.anchor_y = 10
    
turret = DirectionAnimationSet({NORTH: TurretAnimationSet(map(lambda n: "turret_n_%d" % n, [1,2,3])),
                                SOUTH: TurretAnimationSet(map(lambda n: "turret_s_%d" % n, [1,2,3])),
                                EAST: TurretAnimationSet(map(lambda n: "turret_e_%d" % n, [1,2,3])),
                                WEST: TurretAnimationSet(map(lambda n: "turret_w_%d" % n, [1,2,3]))})

# Scenery

barrel = Animation(["barrelhide"])

fuzzlehole = Animation(["fuzzlehole"])

moai = DirectionAnimationSet({ NORTH: Animation(["moai_n"]), SOUTH: Animation(["moai_s"]),
                                EAST: Animation(["moai_e"]), WEST: Animation(["moai_w"])})

campfire = ConstantAnimation(["fire1", "fire2", "fire3"])

tree1 = Animation(["tree1"])
tree2 = Animation(["tree2"])
tree3 = Animation(["tree3"])
tree4 = Animation(["tree4"])
tree5 = Animation(["tree5"])
tree6 = Animation(["tree6"])

deadtree1 = Animation(["tree7"])
deadtree2 = Animation(["tree8"])
deadtree3 = Animation(["tree9"])

bigtree = Animation(["megatree"])
bigtree.images[0].anchor_y = 40

red_door = Animation(["reddoor"])
green_door = Animation(["greendoor"])
yellow_door = Animation(["yellowdoor"])

red_key = Animation(["redkey"])
yellow_key = Animation(["yellowkey"])
green_key = Animation(["greenkey"])

# Effects

explosion = Animation(map(lambda n: "explode_%d" % n, [1, 2, 3, 3, 4, 4, 5, 5, 6, 6]), frame_duration=1, loop=False)