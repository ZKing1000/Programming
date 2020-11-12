music(AREA3_MUSIC)

@zone_trigger("exit_s")
def exit_s():
    yield new_area("area3/rm1", "entry_n", SOUTH)
    
@zone_trigger("exit_e")
def exit_e():
    yield new_area("area3/rm3", "start", EAST)