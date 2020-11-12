#!/usr/bin/env python
import pygame
import items
from pygame.locals import *
from constants import *

'''
    Event Area List:
        0: World Map
        1: Village 1
'''

class Event_Handler(object):
    def __init__(self, party):
        self.overlay = None
        self.party = party
        self.inventory = party.inventory
        self.start_position = None

        self.quit = False
        self.progress = 0 #int, track total progress through the game, increments at game-changing events
        self.sub_progress = 0 #int, tracks progress through a series of events, resets to zero as self.progress increments
        self.past_events = [] #for events that need to have long-term data storage, such as opening chests

        self.curr_event_target = None
        self.curr_event_target_dir = None
        self.curr_event_id = 0
        self.curr_event_type = None
        self.curr_event_cont = 0
        self.curr_event_success = False

        self._set_area(1,1)

    def set_level(self, event_map, player, objects, npcs): #this should only be called when changing maps
        self.event_map = event_map
        self.player = player
        self.objects = objects
        self.npcs = npcs

    def set_menu(self, menu):
        self.menu = menu

    def _set_area(self, area, sub_area): #used by 'change area' events
        self.area = area
        self.sub_area = sub_area

    def get_event(self, target=None):
        if self.curr_event_id != 0: #continuing an event, takes precedance
            if self.curr_event_type == 'exec': #exectution event
                self.exec_event()
            elif self.curr_event_type == 'seq': #sequence event
                self.seq_event()
        elif target: #an event just triggered through execution
            self.curr_event_type = 'exec'
            self.curr_event_target = target
            self.exec_event(target.index)
        else: #an event caused by standing in a certain spot
            if self.event_map.get_tile_bool(self.player.pos):
                self.area_event()

    def area_event(self):
        y, x = self.player.pos
        x = int(x)
        y = int(y)
        event_key = self.event_map.map[x][y]
        try:
            if self.event_map.key[event_key]['elevation']:
                self.player.set_level(int(self.event_map.key[event_key]['elevation']))
        except:
            pass
        try:
            if self.event_map.key[event_key]['change_map']:
                area, sub_area, start_position = self.event_map.key[event_key]['change_map'].split(',')
                self.area = int(area)
                self.sub_area = int(sub_area)
                self.start_position = int(start_position)
        except:
            pass

    def exec_event(self, event_no=None):
        if event_no: self.curr_event_id = event_no

        if self.area == 1: #first village
            if self.sub_area == 1: #main village area
                if self.curr_event_target.type == 'npc':
                    if self.curr_event_id == 1:
                        if self.curr_event_cont == 0:
                            self.flip_target()
                            self.overlay = 'text_box'
                            self.menu.set_textbox_text("Welcome to Tsuki no Sakura!", "Cowboy 1")
                        elif self.curr_event_cont == 1:
                            self._reset_event('flip')
                    elif self.curr_event_id == 2:
                        if self.curr_event_cont == 0:
                            self.flip_target()
                            self.overlay = 'text_box'
                            self.menu.set_textbox_text("This is a really long text test, just to see what happens to it with the text-wrap function. Text-wrapping is awesome when you can manage it. Actually managing it can be quite difficult though, especially when the inner and outer rects are different.", "Cowboy 2")
                        elif self.curr_event_cont == 1:
                            self._reset_event('flip')
                    elif self.curr_event_id == 3:
                        if self.curr_event_cont == 0:
                            self.flip_target()
                            self.overlay = 'text_box'
                            self.menu.set_textbox_text("I'm here to test multi-text events!", "Cowboy 3")
                        elif self.curr_event_cont == 1:
                            self.overlay = 'text_box'
                            self.menu.set_textbox_text("If you can see this text, then it worked!", "Cowboy 3")
                        elif self.curr_event_cont == 2:
                            self._reset_event('flip')
                elif self.curr_event_target.type == 'object':
                    if self.curr_event_id == 1:
                        if self.curr_event_cont == 0:
                            self.flip_target()
                            self.overlay = 'text_box'
                            self.menu.set_textbox_text("I'm just a ball. Try pushing me around!")
                        elif self.curr_event_cont == 1:
                            self._reset_event('flip')
                elif self.curr_event_target.type == 'chest':
                    if self.curr_event_id == 1:
                        if self._get_record() not in self.past_events:
                            if self.curr_event_cont == 0:
                                self.curr_event_target.change_state(1)
                                self.add_chest_item('Shiny Rock', 1)
                            elif self.curr_event_cont == 1 and self.curr_event_success:
                                self.inventory.add_Item('Shiny Rock', 1)
                                self._set_record()
                                self._reset_event()
                            elif self.curr_event_cont == 1:
                                self._reset_event()
                        else:
                            if self.curr_event_cont == 0:
                                self.overlay = 'text_box'
                                self.menu.set_textbox_text("The chest is empty.")
                            elif self.curr_event_cont == 1:
                                self._reset_event()
                    elif self.curr_event_id == 2:
                        if self._get_record() not in self.past_events:
                            if self.curr_event_cont == 0:
                                self.curr_event_target.change_state(1)
                                self.add_chest_item('Super Ether', 99)
                            elif self.curr_event_cont == 1 and self.curr_event_success:
                                self.inventory.add_Item('Super Ether', 99)
                                self._set_record()
                                self._reset_event()
                            elif self.curr_event_cont == 1:
                                self._reset_event()
                        else:
                            if self.curr_event_cont == 0:
                                self.overlay = 'text_box'
                                self.menu.set_textbox_text("The chest is empty.")
                            elif self.curr_event_cont == 1:
                                self._reset_event()
                    elif self.curr_event_id == 3:
                        if self._get_record() not in self.past_events:
                            if self.curr_event_cont == 0:
                                self.curr_event_target.change_state(1)
                                self.overlay = 'text_box'
                                self.menu.set_textbox_text("There chest was full of monsters!")
                            elif self.curr_event_cont == 1:
                                self.overlay = "start_battle"
                            elif self.curr_event_cont == 2:
                                self._set_record()
                                self._reset_event()
                        else:
                            if self.curr_event_cont == 0:
                                self.overlay = 'text_box'
                                self.menu.set_textbox_text("The chest is empty.")
                            elif self.curr_event_cont == 1:
                                self._reset_event()
            elif self.sub_area == 2:
                if self.curr_event_target.type == 'npc':
                    if self.curr_event_id == 1:
                        if self.curr_event_cont == 0:
                            self.flip_target()
                            self.overlay = 'text_box'
                            self.menu.set_textbox_text("Did you want something?", "Shopkeeper")
                        elif self.curr_event_cont == 1:
                            self.menu.set_shop(1)
                            self.overlay = 'shop'
                        elif self.curr_event_cont == 2:
                            self._reset_event('flip')
                elif self.curr_event_target.type == 'chest':
                    if self.curr_event_id == 1:
                        if self._get_record() not in self.past_events:
                            if self.curr_event_cont == 0:
                                self.curr_event_target.change_state(1)
                                self.add_chest_item('Tanto', 1)
                            elif self.curr_event_cont == 1 and self.curr_event_success:
                                self.inventory.add_Item('Tanto', 1)
                                self._set_record()
                                self._reset_event()
                            elif self.curr_event_cont == 1:
                                self._reset_event()
                        else:
                            if self.curr_event_cont == 0:
                                self.overlay = 'text_box'
                                self.menu.set_textbox_text("The chest is empty.")
                            elif self.curr_event_cont == 1:
                                self._reset_event()

    def _get_record(self):
        return str(str(self.area)+"-"+str(self.sub_area)+"-"+str(self.curr_event_target.type)+"-"+str(self.curr_event_id))

    def _set_record(self):
        self.past_events.append(str(str(self.area)+"-"+str(self.sub_area)+"-"+str(self.curr_event_target.type)+"-"+str(self.curr_event_id)))

    def get_record_bool(self, area, sub_area, type, id):
        if str(str(area)+"-"+str(sub_area)+"-"+str(type)+"-"+str(id)) in self.past_events:
            return True
        else:
            return False

    def add_chest_item(self, name, amount):
        if name in self.inventory.items and self.inventory.items[name] > (99 - amount) and amount > 1:
            self.overlay = 'text_box'
            self.menu.set_textbox_text("Chest contains "+str(name)+" x"+str(amount)+", but you can't hold any more!")
            self.curr_event_success = False
        elif name in self.inventory.items and self.inventory.items[name] > (99 - amount):
            self.overlay = 'text_box'
            self.menu.set_textbox_text("Chest contains "+str(name)+", but you can't hold any more!")
            self.curr_event_success = False
        elif amount > 1:
            self.overlay = 'text_box'
            self.menu.set_textbox_text("You obtain "+str(name)+" x"+str(amount)+"!")
            self.curr_event_success = True
        else:
            self.overlay = 'text_box'
            self.menu.set_textbox_text("You obtain "+str(name)+"!")
            self.curr_event_success = True

    def _reset_event(self, flip=None):
        if flip:
            self.flip_target_back()
        self.curr_event_id = 0
        self.curr_event_type = None
        self.curr_event_cont = 0
        self.curr_event_target = None
        self.curr_event_target_dir = None
        self.menu.set_visible()
    
    def flip_target(self):
        if not self.curr_event_target_dir:
            self.curr_event_target_dir = self.curr_event_target.direction
            if self.player.direction == 0:
                self.curr_event_target.direction = 3
            elif self.player.direction == 1:
                self.curr_event_target.direction = 2
            elif self.player.direction == 2:
                self.curr_event_target.direction = 1
            elif self.player.direction == 3:
                self.curr_event_target.direction = 0

    def flip_target_back(self):
        self.curr_event_target.direction = self.curr_event_target_dir