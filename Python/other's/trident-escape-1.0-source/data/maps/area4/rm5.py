@zone_trigger("exit_n")
def exit_n():
    yield new_area("area4/rm4", "entry_s", NORTH)
    
@zone_trigger("exit_e")
def exit_e():
    yield new_area("area4/rm6", "start", EAST)