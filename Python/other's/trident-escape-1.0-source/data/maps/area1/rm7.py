music(AREA1_MUSIC)

@zone_trigger("exit_s")
def exit_s():
    yield new_area("area1/rm6", "entry_n", SOUTH)

@zone_trigger("exit_n")
def exit_n():
    yield new_area("area1/rm8", "entry_s", NORTH)
