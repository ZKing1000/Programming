music(AREA2_MUSIC)
@zone_trigger("exit_s")
def exit_s():
    yield new_area("area2/rm7", "entry_n", SOUTH)
    
@zone_trigger("exit_n")
def exit_n():
    yield new_area("area2/side", "start", NORTH)