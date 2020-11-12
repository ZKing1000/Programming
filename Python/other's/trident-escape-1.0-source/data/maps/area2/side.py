music(AREA2_MUSIC)
@zone_trigger("exit_s")
def exit_s():
    yield new_area("area2/rm8", "entry_n", SOUTH)
    
@zone_trigger("exit_sw")
def exit_sw():
    yield new_area("area2/rm1", "entry_n", SOUTH)
    
@zone_npc("oldman", EAST)
def talk():
    yield dialogue("People who look at the source code of games to find out what they're missing are only cheating themselves.")