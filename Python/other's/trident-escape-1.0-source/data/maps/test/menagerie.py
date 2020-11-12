@zone_trigger("exit")
def leave():
    yield new_area("test/test", "mena_entry", SOUTH)