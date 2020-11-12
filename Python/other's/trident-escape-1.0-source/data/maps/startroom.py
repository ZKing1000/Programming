# TODO
music(AREA1_MUSIC)

@zone_trigger("exit")
def exit():
    yield new_area("area1/rm1", "entry_s", NORTH)
    
@zone_npc("oldman", WEST)
def talk():
    yield dialogue("Welcome to the Dungeon of Destiny, young lady!")
    yield dialogue("Here the finest warriors in all the land come to prove their mettle.")
    yield dialogue("What are you doing here?")
    yield dialogue("Anyway, press and hold the space bar to extend your trident.")