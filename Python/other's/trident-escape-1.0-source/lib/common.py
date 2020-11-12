"""Common code shared between modules.

This module is intended to be imported with 'from ... import *' semantics and
provides an __all__ specification for this purpose.

"""

from constants import *

__all__ = ["opposite_dir", "rotate_vector", "unrotate_vector", "vector_in_direction", "rotate_cw", "rotate_ccw", "dirname"]

def opposite_dir(d):
    return {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}[d]

def rotate_cw(d):
    return {NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH}[d]
    
def rotate_ccw(d):
    return {NORTH: WEST, EAST: NORTH, SOUTH: EAST, WEST: SOUTH}[d]
    
def rotate_vector(x, y, direction):
    if direction == NORTH:
        return (x, y)
    if direction == SOUTH:
        return (-x, -y)
    if direction == EAST:
        return (y, -x)
    if direction == WEST:
        return (-y, x)
        
def unrotate_vector(x, y, direction):
    return rotate_vector(x, y, {NORTH: NORTH, SOUTH: SOUTH, EAST: WEST, WEST: EAST}[direction])
    
def vector_in_direction(direction, length=1):
    if direction == NORTH:
        return (0, length)
    if direction == SOUTH:
        return (0, -length)
    if direction == EAST:
        return (length, 0)
    if direction == WEST:
        return (-length, 0)
    
def dirname(direction):
    return {NORTH: "N", SOUTH: "S", EAST: "E", WEST: "W"}[direction]