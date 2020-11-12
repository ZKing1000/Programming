@zone_trigger("west_exit")
def go_west():
    yield new_area("test/test", "ne_entry", WEST)
    
@zone_trigger("south_exit")
def go_south():
    yield new_area("test/subtest/subroom", "n_entry", SOUTH)
    
@zone_trigger("new_exit")
def go_east():
    yield new_area("test/test3", "entry", EAST)