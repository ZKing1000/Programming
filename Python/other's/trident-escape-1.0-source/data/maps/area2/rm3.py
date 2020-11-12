music(AREA2_MUSIC)
@zone_trigger("exit_w")
def exit_w():
    yield new_area("area2/rm2", "entry_e", WEST)
    
@zone_trigger("exit_e")
def exit_w():
    yield new_area("area2/rm4", "start", EAST)
    
    