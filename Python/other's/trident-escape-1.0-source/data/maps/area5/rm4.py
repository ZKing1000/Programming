music(AREA5_MUSIC)
@zone_trigger("exit_w")
def exit_w():
    yield new_area("area5/rm3", "entry_e", WEST)
    
@zone_trigger("exit_e")
def exit_e():
    yield new_area("area5/rm5", "start", EAST)