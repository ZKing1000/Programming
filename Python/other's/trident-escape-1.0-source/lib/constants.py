"""Constant definitions.

This file is loaded during the program initialisation before the main module is
imported. Consequently, this file must not import any other modules, or those
modules will be initialised before the main module, which means that the DEBUG
value may not have been set correctly.

This module is intended to be imported with 'from ... import *' semantics but
it does not provide an __all__ specification.

"""

#: Enable debug features. Should never be changed manually but is set to True
#: automatically when running `test_game.py`.
DEBUG = False

#: Version string. This may be represented somewhere in-game. It is also read
#: by `setup.py` as part of its versioning features.
VERSION = u"1.0"

#: The directory (relative to the top level) wherein all the resources for the
#: game are stored, probably subdivided into types of resources. See `data.py`.
DATA_DIR = "data"

#: The name of the game used in locating the saved settings directory. Its best
#: not to have any spaces in this name.
CONFIG_NAME = "TridentEscape"

#: The caption that appears at the top of the window. Obviously this is only
#: visible in windowed mode.
CAPTION = u"Trident Escape: The Dungeon of Destiny"

#: The "top-level" tick rate; the maximum number of times per second that the
#: controller will call its tick method.
TICK_RATE = 60.0

#: The "top-level" update rate; the maximum number of times per second that the
#: controller will call its update method.
UPDATE_RATE = 60.0



TILE_SIZE_IMG = 64
TILE_SIZE_SCREEN = 64

NORTH, EAST, SOUTH, WEST = range(4)

PLAYER_SPEED = 0.08
WEAPON_SPEED = 0.12
THROW_SPEED = 0.18

# how far a carried monster sits in front of the player
CARRY_DIST = 0.3

# how far in front of the exploding sprite an explosion is drawn
EXPLOSION_OFFSET = 0.05

# damage radius when stuff explodes
DETONATION_RANGE = 1

EDITOR_SCROLL_SPEED = 10

COLLISION_BUFFER = 0.01

FALL_TIME = 30
PATH_TIMER = 20
MAGIC_NUMBER = 0.79

DEATH_TICKS = 60

TURRET_FIRE_TIME = 100

MENU_MUSIC = 'Pinball Spring.mp3'
LOBBY_MUSIC = 'Pinball Spring.mp3'
AREA1_MUSIC = 'Kick Shock.mp3'
AREA2_MUSIC = 'Blipotron.mp3'
AREA3_MUSIC = 'Spazzmatica Polka.mp3'
AREA4_MUSIC = 'Kick Shock.mp3'
AREA5_MUSIC = 'Pinball Spring.mp3'
