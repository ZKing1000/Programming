music(AREA3_MUSIC)

@zone_trigger("exit_s")
def exit_s():
    yield new_area("area3/rm3", "entry_n", SOUTH)
    
@zone_trigger("exit_n")
def exit_n():
    yield new_area("area3/rm5", "start", NORTH)
    
@zone_trigger("exit_w")
def exit_w():
    yield new_area("area4/rm8", "entry_e", WEST)
    
@zone_trigger("exit_e")
def exit_e():
    yield new_area("area5/rm1", "start", EAST)