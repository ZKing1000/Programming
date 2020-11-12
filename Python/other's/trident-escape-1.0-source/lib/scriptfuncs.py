import entity
import script
import monster
import scenery
import config

def trace(s):
    print s
    
def get_game():
    return script.current[0]
    
def get_map():
    return script.current[1]
    
# functions to call on map load

def forbid_monster_zones(zones):
    get_map().forbid_monster_zones.extend(zones)
       
# decorators for scripts

def startup(f):
    get_map().startup_script = f
            
def zone_trigger(zone_name):
    def deco(f):
        get_map().zone_triggers[zone_name] = f
    return deco

def zone_npc(zone_name, direction):
    def deco(f):
        e = get_game().create_entity_in_zone(entity.NPC, zone_name, direction)
        e.talk_script = f
    return deco    

# functions to call from scripts

def new_area(area, entry_zone, direction):
    get_game().new_area = area
    get_game().new_area_entry = entry_zone
    get_game().new_area_dir = direction
    
def dialogue(dia):
    get_game().show_dialogue(dia)

def first_time(flag):
    flags = get_game().flags
    if flag in flags:
        return False
    else:
        flags[flag] = True
        return True

def move_to(npc, zone):
    g = get_game()
    g.scripted_move = True
    if isinstance(npc, str): npc = g.zone_ents[npc]
    cell = g.map.zones[zone][0]
    npc.set_move_target(cell)
 
def move_player(zone):
    g = get_game()
    g.scripted_move = True
    pc = g.player
    cell = g.map.zones[zone][0]
    pc.set_move_target(cell)
   
def remaining_monsters():
    g = get_game()
    return [e for e in g.entities if e.must_kill]

def load_game():
    get_game().new_area = config.continue_room
    get_game().new_area_entry = config.continue_entrance
    get_game().new_area_dir = config.continue_dir
    
def new_game():
    get_game().new_area = config.new_game_room
    get_game().new_area_entry = 'start'
    get_game().new_area_dir = 2
    get_game().flags = {}
    
def music(track):
    get_game().dispatch_event('on_switch_music', track)

def create_entity(cls, zone):
    return get_game().create_entity_in_zone(cls, zone)

def destroy_npc(zone):
    g = get_game()
    npc = g.zone_ents[zone]
    g.destroy_entity(npc, explode=False)   