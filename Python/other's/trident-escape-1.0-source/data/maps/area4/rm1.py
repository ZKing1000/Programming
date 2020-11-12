@zone_trigger("exit_s")
def exit_s():
    yield new_area("area3/rm5", "entry_n", SOUTH)
    
@zone_trigger("exit_w")
def exit_w():
    yield new_area("area4/rm2", "start", WEST)
    
@zone_npc("oldman", SOUTH)
def talk():
    yield dialogue("There's a surprise waiting for you in the next room. Enjoy!")