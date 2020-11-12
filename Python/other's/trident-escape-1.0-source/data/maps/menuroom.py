music(MENU_MUSIC)

@startup
def msg():
    yield dialogue("Trident Escape: The Dungeon of Destiny\nA Super Effective Game")
    
@zone_trigger("cont_msg")
def msg():
    yield dialogue("Walk through here to continue your game. The other exit lets you start a new game.")
    
@zone_trigger("new_msg1")
def msg():
    yield dialogue("Walk through here to start a new game. The other exit lets you continue where you left off.")

@zone_trigger("new_msg2")
def msg():
    yield dialogue("If you continue through here, you'll lose all your saved progress.")

@zone_trigger("new_msg3")
def msg():
    yield dialogue("Seriously, think of all that delicious saved progress!")

@zone_trigger("new_msg4")
def msg():
    yield dialogue("Well, I warned you. Enjoy.")
    
@zone_trigger("new_exit")
def msg():
    yield new_game()
    
@zone_trigger("cont_exit")
def msg():
    yield load_game()


