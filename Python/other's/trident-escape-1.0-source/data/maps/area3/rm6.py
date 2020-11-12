music(AREA3_MUSIC)
@zone_trigger("exit_w")
def exit_w():
    yield new_area("area3/rm5", "entry_e", WEST)