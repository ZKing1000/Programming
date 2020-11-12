music(AREA1_MUSIC)

@zone_trigger("exit_s")
def exit_s():
    yield new_area("area1/rm5b", "entry_n", SOUTH)
    
@zone_trigger("exit_n")
def exit_n():
    yield new_area("area1/rm7", "entry_s", NORTH)
        