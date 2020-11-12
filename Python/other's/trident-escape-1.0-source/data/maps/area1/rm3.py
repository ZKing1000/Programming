music(AREA1_MUSIC)

@zone_trigger("exit_s")
def exit_s():
    yield new_area("area1/rm2", "entry_n", SOUTH)

@zone_trigger("exit_e")
def exit_s():
    yield new_area("area1/rm4", "entry_w", EAST)
