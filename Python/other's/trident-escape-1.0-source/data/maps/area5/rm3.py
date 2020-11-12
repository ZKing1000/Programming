music(AREA5_MUSIC)
@zone_trigger("exit_s")
def exit_s():
    yield new_area("area5/rm2", "entry_n", SOUTH)
    
@zone_trigger("exit_e")
def exit_e():
    yield new_area("area5/rm4", "start", EAST)