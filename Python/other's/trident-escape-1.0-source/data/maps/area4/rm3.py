@zone_trigger("exit_n")
def exit_n():
    yield new_area("area4/rm2", "entry_s", NORTH)
    
@zone_trigger("exit_s")
def exit_s():
    yield new_area("area4/rm4", "start", SOUTH)
    
@zone_npc("oldman", EAST)
def talk():
    yield dialogue("Are you enjoying yourself?")
    
@startup
def start():
    if 'area4/rm3.roomclear' not in flags:
        yield move_player('move_player')
        yield dialogue('...')
        bomb = create_entity(monster.EasyCrawlingBomb, 'exit_n')
        yield move_to(bomb, 'start')
        yield dialogue('...!')