music(AREA1_MUSIC)

@zone_trigger("exit")
def exit():
    yield new_area("area1/rm5", "entry_xtra", SOUTH)
    
@zone_npc("oldman", WEST)
def advice():
    if len(remaining_monsters()) == 0:
        yield dialogue("I hope you're not expecting me to give you a prize or something.")
    else:
        yield dialogue("If you want my opinion, this room looks like a waste of your time.")