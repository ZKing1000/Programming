@zone_trigger("exit_n")
def exit_n():
    yield new_area("area4/rm3", "entry_s", NORTH)
    
@zone_trigger("exit_s")
def exit():
    yield new_area("area4/rm5", "start", SOUTH)