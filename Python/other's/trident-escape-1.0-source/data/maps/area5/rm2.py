music(AREA5_MUSIC)
@zone_trigger("exit_w")
def exit_w():
    yield new_area("area5/rm1", "entry_e", WEST)
    
@zone_trigger("exit_n")
def exit_n():
    yield new_area("area5/rm3", "start", NORTH)
    
@zone_npc("oldman", WEST)
def talk():
    yield dialogue("You really didn't have to kill every monster in this room. You're only making your life difficult.")