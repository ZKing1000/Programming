@zone_trigger("exit")
def go_east():
    yield new_area("test/test", "west_entry", EAST)
    
@zone_npc("oldman", SOUTH)
def hello():
    if first_time('gone'):
        yield dialogue("Hello! I am an old man!")
        move_to('oldman', 'oldmantarget')
        yield move_to('oldman2', 'oldman2target')
        yield dialogue("Go away!")
    else:
        yield dialogue("I told you to go away!")

    yield new_area("test/test", "west_entry", EAST)
    
@zone_npc("oldman2", WEST)
def hello():
    yield dialogue("Hello! I am a very old man!")
    yield dialogue("I like bees!")