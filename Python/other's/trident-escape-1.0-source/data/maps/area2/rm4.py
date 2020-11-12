music(AREA2_MUSIC)
@zone_trigger("exit_w")
def exit_w():
    yield new_area("area2/rm3", "entry_e", WEST)
    
@zone_trigger("exit_e")
def exit_e():
    yield new_area("area2/rm5", "start", EAST)
    
@zone_npc("oldman", WEST)
def talk():
    yield dialogue("If you went out of your way to kill all the monsters in this room, I think you're overdoing it.")