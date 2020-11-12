music(AREA2_MUSIC)
@zone_trigger("exit_n")
def exit_n():
    yield new_area("area2/rm5", "entry_s", NORTH)
    
@zone_trigger("exit_e")
def exit_e():
    yield new_area("area2/rm7", "start", EAST)
    
