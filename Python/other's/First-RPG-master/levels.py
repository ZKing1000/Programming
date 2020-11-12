#!/usr/bin/env python
import pygame, pygame.locals
import classes, scroll
from constants import *

'''
    Get the starting position from the evHandler, then choose the
    specific area/sub_area to load. Load the level maps first,
    then the collision maps, then create the bg_Manager while
    passing in the 'elevation 1' level map. Load the event map,
    then all scenery sprite-objects, then the player (position
    based on the evHandler start_position we created earlier).
    Finally load all NPCs/movable/event objects including text-box
    and create our three sprite groups. Set the level details on
    the evHandler and return the player and groups.
    
    Every elevation that can be walked on should have it's own
    collision map, every scenery sprite should have two maps for
    different layers (in front of movable sprites or behind).
    Since elevation takes rendering priority over layers and depth,
    all scenery objects on a higher elevation will be 'in front of'
    anything at a lower elevation. Objects sharing the same layer
    and on the same elevation will be rendered based on depth
    (Y-coordinate). Anything that has a different state of existence
    based on a past event should be created based on the return of
    a get_record_bool call to the evHandler with area, sub_area,
    object type, and object index as parameters.
'''
def load_level(window, area, sub_area, ev_handler, bg_manager):
    temp_pos = ev_handler.start_position

    if area == 1:
        if sub_area == 1:
            area_name = 'village_1'
            if temp_pos:
                if temp_pos == 1:
                    start_position = (17,18)
                else:
                    start_position = (10,7)
            else:
                start_position = (10,7)
    
            level_E1 = classes.Dirty_Map(area_name,'level_E1.map', 0, MAP_CACHE, 0)
            level_E2 = classes.Dirty_Map(area_name,'level_E2.map', 0, MAP_CACHE, 1)
            level_cache = [level_E1, level_E2]
            collision_E1 = classes.Special_Map(area_name,'collision_E1.map', 10, 'collision')
            collision_E2 = classes.Special_Map(area_name,'collision_E2.map', 10, 'collision')
            collision_cache = [collision_E1, collision_E2]
            event_map = classes.Special_Map(area_name,'event.map', 10, 'event')
            
            bg_manager.set_screen(window, level_E1.image)

            house_1_a = classes.Dirty_Map(area_name,'house1_bottom.map', 3, MAP_CACHE, 0)
            house_1_b = classes.Dirty_Map(area_name,'house1_top.map', 7, MAP_CACHE, 0)
            
            #spritesheet, X/Y tile position, direction facing, layer, elevation, type, index of this type, caches and maybe event map
            player = classes.Player_Sprite(TALL_SPRITE_CACHE['player_1_sprite_sheet.png'], start_position, index_direction['down'], 5, 0, 'player', 1, collision_cache, level_cache, event_map)
            player_shadow = classes.Shadow(player, SHORT_SPRITE_CACHE)
            player_attack_effect = classes.Attack_Effect(player, SHORT_SPRITE_CACHE)
            player.set_attack_effect(player_attack_effect)
    
            npc_1 = classes.Moving_Sprite(TALL_SPRITE_CACHE['npc_1_sprite_sheet.png'], (7,9), index_direction['right'], 5, 0, 'npc', 1, collision_cache, level_cache)
            npc_1_shadow = classes.Shadow(npc_1, SHORT_SPRITE_CACHE)
            npc_2 = classes.Moving_Sprite(TALL_SPRITE_CACHE['npc_2_sprite_sheet.png'], (10,10), index_direction['left'], 5, 0, 'npc', 2, collision_cache, level_cache)
            npc_2_shadow = classes.Shadow(npc_2, SHORT_SPRITE_CACHE)
            npc_3 = classes.Moving_Sprite(TALL_SPRITE_CACHE['npc_1_sprite_sheet.png'], (12,10), index_direction['up'], 5, 0, 'npc', 3, collision_cache, level_cache)
            npc_3_shadow = classes.Shadow(npc_3, SHORT_SPRITE_CACHE)
            ball_1 = classes.Moving_Sprite(SHORT_SPRITE_CACHE['ball_1_sprite_sheet.png'], (5,4), index_direction['right'], 5, 1, 'object', 1, collision_cache, level_cache)
            ball_1_shadow = classes.Shadow(ball_1, SHORT_SPRITE_CACHE)
            chest_1 = classes.Static_Sprite(SHORT_SPRITE_CACHE['wood_chest_sprite_sheet.png'], (5,7), index_direction['down'], 5, 0, 'chest', 1, collision_cache)
            chest_2 = classes.Static_Sprite(SHORT_SPRITE_CACHE['wood_chest_sprite_sheet.png'], (4,5), index_direction['left'], 5, 0, 'chest', 2, collision_cache)
            chest_3 = classes.Static_Sprite(SHORT_SPRITE_CACHE['wood_chest_sprite_sheet.png'], (11,7), index_direction['down'], 5, 0, 'chest', 3, collision_cache)
            for each in (chest_1, chest_2, chest_3):
                if ev_handler.get_record_bool(area, sub_area, each.type, each.index):
                    each.change_state(1)

            map_display = scroll.Scroll_Group(bg_manager)
            map_display.add(level_E2, house_1_a, house_1_b, player, player_shadow,
                            player_attack_effect, npc_1, npc_1_shadow, npc_2, npc_2_shadow,
                            npc_3, npc_3_shadow, ball_1, ball_1_shadow, chest_1, chest_2, chest_3) #is it displayable?
            object_group = scroll.Scroll_Group(bg_manager)
            object_group.add(npc_1, npc_2, npc_3, ball_1, chest_1, chest_2, chest_3) #is it interactable?
            npc_group = scroll.Scroll_Group(bg_manager)
            npc_group.add(npc_1, npc_2, npc_3, ball_1) #is it movable?
    
        elif sub_area == 2:
            area_name = 'village_1'
            filename = '_house_1_'
            start_position = (12,24)
    
            level_E1 = classes.Dirty_Map(area_name,filename+'level_E1.map', 0, MAP_CACHE, 0)
            level_E2 = classes.Dirty_Map(area_name,filename+'level_E2.map', 0, MAP_CACHE, 1)
            level_cache = [level_E1, level_E2]
            collision = classes.Special_Map(area_name,filename+'collision.map', 10, 'collision')
            collision_cache = [collision]
            event_map = classes.Special_Map(area_name,filename+'event.map', 10, 'event')
            
            bg_manager.set_screen(window, level_E1.image)
            
            #spritesheet, X/Y tile position, direction facing, layer, elevation, type, index of this type, caches and maybe event map
            player = classes.Player_Sprite(TALL_SPRITE_CACHE['player_1_sprite_sheet.png'], start_position, index_direction['up'], 5, 0, 'player', 1, collision_cache, level_cache, event_map)
            player_shadow = classes.Shadow(player, SHORT_SPRITE_CACHE)
            npc_1 = classes.Moving_Sprite(TALL_SPRITE_CACHE['npc_1_sprite_sheet.png'], (12,18), index_direction['down'], 5, 0, 'npc', 1, collision_cache, level_cache, 0)
            npc_1_shadow = classes.Shadow(npc_1, SHORT_SPRITE_CACHE)
            chest_1 = classes.Static_Sprite(SHORT_SPRITE_CACHE['wood_chest_sprite_sheet.png'], (6,6), index_direction['right'], 5, 0, 'chest', 1, collision_cache)
            if ev_handler.get_record_bool(area, sub_area, chest_1.type, chest_1.index):
                chest_1.change_state(1)
    
            map_display = scroll.Scroll_Group(bg_manager)
            map_display.add(level_E2, npc_1, player, player_shadow, chest_1)
            object_group = scroll.Scroll_Group(bg_manager)
            object_group.add(npc_1, chest_1)
            npc_group = scroll.Scroll_Group(bg_manager)
            npc_group.add(npc_1)

    ev_handler.set_level(event_map, player, object_group, npc_group)
    return player, map_display, object_group, npc_group