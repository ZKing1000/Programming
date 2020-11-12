music(AREA3_MUSIC)

@zone_trigger("exit_w")
def exit_w():
    yield new_area("area3/rm2", "entry_e", WEST)
    
@zone_trigger("exit_n")
def exit_n():
    yield new_area("area3/rm4", "start", NORTH)