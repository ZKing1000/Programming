@zone_trigger("exit_e")
def exit_e():
    yield new_area("area4/rm1", "entry_w", EAST)
    
@zone_trigger("exit_s")
def exit_s():
    yield new_area("area4/rm3", "start", SOUTH)