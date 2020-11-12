music(AREA5_MUSIC)
@zone_trigger("exit_w")
def exit_w():
    yield new_area("area5/rm6", "entry_e", WEST)
    
@zone_trigger("final_exit")
def the_end():
    yield new_area("end", "start", SOUTH)
    
@zone_npc("oldman", SOUTH)
def talk():
    yield dialogue("So, you've made it to the end.")
    yield move_to("oldman", "badass")
    yield dialogue("There's only one thing left to do...")
    yield move_to("oldman", "badass2")
    yield dialogue("Defeat me!")
    destroy_npc("oldman")
    create_entity(scenery.Tree, "moaihere")
    create_entity(monster.BadassOldMan, "badass2")
    # turn into BadassOldMan