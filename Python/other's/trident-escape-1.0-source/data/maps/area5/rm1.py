music(AREA5_MUSIC)
@zone_trigger("exit_w")
def exit_w():
    yield new_area("area3/rm4", "entry_e", WEST)
    
@zone_trigger("exit_e")
def exit_e():
    yield new_area("area5/rm2", "start", EAST)
    
@zone_npc("oldman", SOUTH)
def talk():
    yield dialogue("You're nearly there ... but there are still a few more challenges in store!")