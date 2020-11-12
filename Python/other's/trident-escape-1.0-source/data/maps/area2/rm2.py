music(AREA2_MUSIC)
@zone_trigger("exit_n")
def exit_n():
    yield new_area("area2/rm1", "entry_s", NORTH)
    
@zone_trigger("exit_e")
def exit_e():
    yield new_area("area2/rm3", "start", EAST)
    
