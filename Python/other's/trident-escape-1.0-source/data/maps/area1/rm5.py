music(AREA1_MUSIC)

@zone_trigger("exit_s")
def exit_s():
    yield new_area("area1/rm4", "entry_n", SOUTH)

@zone_trigger("exit_n")
def exit_s():
    yield new_area("area1/rm5b", "entry_s", NORTH)

@zone_trigger("exit_xtra")
def exit_xtra():
    yield new_area("area1/rm5a", "entry", NORTH)