@zone_trigger("exit_w")
def exit_w():
    yield new_area("area4/rm5", "entry_e", WEST)
    
@zone_trigger("exit_s")
def exit_s():
    yield new_area("area4/rm7", "start", SOUTH)