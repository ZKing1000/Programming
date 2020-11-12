music(LOBBY_MUSIC)

@zone_trigger("exit_s")
def exit_s():
    yield new_area("lobby1", "entry_n", SOUTH)
    
@zone_trigger("exit_n")
def exit_n():
    yield new_area("area3/rm1", "start", NORTH)