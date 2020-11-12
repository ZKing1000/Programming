music(AREA1_MUSIC)

@zone_trigger("exit_w")
def exit_w():
    yield new_area("area1/rm3", "entry_e", WEST)
    
@zone_trigger("exit_n")
def exit_n():
    yield new_area("area1/rm5", "entry_s", NORTH)
