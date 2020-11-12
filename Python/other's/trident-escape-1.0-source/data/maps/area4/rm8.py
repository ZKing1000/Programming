@zone_trigger("exit_n")
def exit_n():
    yield new_area("area4/rm7", "entry_s", NORTH)
    
@zone_trigger("exit_e")
def exit_e():
    yield new_area("area3/rm4", "entry_w", EAST)
    
@zone_npc("oldman", SOUTH)
def talk():
    yield dialogue("The dungeon can be a bit confusing ... are you sure you know where you're going?")