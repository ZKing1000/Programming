music(AREA2_MUSIC)
@zone_trigger("exit_w")
def exit_w():
    yield new_area("area2/rm6", "entry_e", WEST)
    
@zone_trigger("exit_n")
def exit_n():
    yield new_area("area2/rm8", "start", NORTH)