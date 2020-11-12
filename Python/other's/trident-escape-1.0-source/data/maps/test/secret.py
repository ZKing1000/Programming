@zone_trigger("exit")
def exit():
    yield new_area("test/test", "new_entry", SOUTH)
    
