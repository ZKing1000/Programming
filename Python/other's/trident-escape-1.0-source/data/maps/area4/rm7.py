@zone_trigger("exit_n")
def exit_n():
    yield new_area("area4/rm6", "entry_s", NORTH)
    
@zone_trigger("exit_s")
def exit_s():
    yield new_area("area4/rm8", "start", SOUTH)