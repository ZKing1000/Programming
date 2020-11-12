music(AREA3_MUSIC)

@zone_trigger("exit_s")
def exit_s():
    yield new_area("area3/rm4", "entry_n", SOUTH)
    
@zone_trigger("exit_n")
def exit_n():
    yield new_area("area4/rm1", "start", NORTH)
    
@zone_trigger("exit_e")
def exit_e():
    yield new_area("area3/rm6", "start", EAST)