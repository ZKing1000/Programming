# TODO
music(LOBBY_MUSIC)

@zone_trigger("exit_s")
def exit_s():
    yield new_area("area1/rm8", "entry_n", SOUTH)
    
@zone_trigger("exit_n")
def exit_n():
    yield new_area("lobby2", "start", NORTH)
    
@zone_trigger("exit_e")
def exit_e():
    yield new_area("area2/rm1", "start", EAST)
    
@zone_npc("oldman", EAST)
def lobby():
    yield dialogue("This is the lobby!")
    yield dialogue("You were expecting something more grand?")
    yield dialogue("We're not all fancy people like you.")
    yield dialogue("The nerve of some people!")