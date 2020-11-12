music(AREA2_MUSIC)
@zone_trigger("exit_w")
def w_exit():
    yield new_area("lobby1", "entry_e", WEST)
    
@zone_trigger("exit_n")
def exit_n():
    yield new_area("area2/side", "entry_sw", NORTH)
    
@zone_trigger("exit_s")
def exit_s():
    yield new_area("area2/rm2", "start", SOUTH)
    
@zone_npc("oldman", WEST)
def talk():
    yield dialogue("People who look at the source code of games to find out what they're missing are only cheating themselves.")