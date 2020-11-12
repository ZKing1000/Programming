music(AREA2_MUSIC)
@zone_trigger("exit_w")
def exit_w():
    yield new_area("area2/rm4", "entry_e", WEST)
    
@zone_trigger("exit_s")
def exit_s():
    yield new_area("area2/rm6", "start", SOUTH)