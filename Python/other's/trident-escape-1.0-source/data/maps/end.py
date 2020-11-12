@startup
def start():
    yield dialogue("Well done. You've completed the game.")
    yield dialogue("This has been a Super Effective production.")
    yield dialogue("FIN")
    yield new_area("menuroom", "start", SOUTH)