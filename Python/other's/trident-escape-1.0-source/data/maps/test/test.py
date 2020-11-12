forbid_monster_zones(["exit1", "exit2", "new_exit", "west_exit"])

@zone_trigger("start")
def start():
    if first_time('started'):
        yield dialogue("Welcome to Testtown")
        yield move_player('moveto')
    
@zone_trigger("exit1")
def east_exit():
    yield new_area("test/test2", "west_entry", EAST)
    
@zone_trigger("exit2")
def other_east_exit():
    trace("I like melons")
    trace("(This exit goes nowhere)")
    
@zone_trigger("new_exit")
def north_exit():
    yield new_area("test/secret", "entry", NORTH)
    
@zone_trigger("west_exit")
def go_west():
    yield dialogue("Now entering Oldsville: a place with an extremely long introductory text, like a paragraph or so, which just goes on and on and on and on.")
    yield new_area("test/western", "entry", WEST)
    
@zone_trigger("mena_exit")
def go_away():
    yield new_area("test/menagerie", "entry", NORTH)