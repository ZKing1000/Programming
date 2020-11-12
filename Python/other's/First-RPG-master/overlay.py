#!/usr/bin/env python
import os, sys, pygame
import time, items, equip
from pygame.locals import *
from operator import itemgetter, attrgetter
from constants import *

def load_Image(name, alpha=False, colorkey=None):
    try:
        image = pygame.image.load(os.path.join('images',name)).convert()
    except:
        print('Cannot load image:'+str(name))
        pygame.quit()
    if alpha:
        image = image.convert_alpha()
    else:
        image=image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class Overlay_Sprite(pygame.sprite.DirtySprite):
    def __init__(self, font, party, ev_handler):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2
        self.visible = 0
        self._layer = 99
        self.depth = 9999
        self.elevation = 99

        self.ev_handler = ev_handler
        self.party = party
        self.inventory = party.inventory
        self.image = None

        self.font = font
    
        self.menus = {
            'menu': 0, #entirely different menu screens, main (0), status (1), items (2), etc
            'menu_select': 0, #character selection binary flag, 0 or 1
            'item_select': 0, #item selection flag, 0, 1, 2, 3
            'item_selected': "Empty", #tracks a selected item's name
            'item_scroll_cap': 28, #number of items per 'page' in items
            'equip_select': 0, #equip selection flag, 0, 1, or 2
            'equip_selected': "Empty", #tracks a selected equipment piece's name
            'magic_select': 0, #magic selection flag, 0, 1, 2, 3
            'magic_selected': "Empty", #tracks a selected magic's name
            'mag_scroll_cap': 28, #number of items per 'page' in magic
            'skill_select': 0, #skill selection flag, 0, 1, 2
            'skill_scroll_cap': 14, #number of items per 'page' in skills
            'main_menu': 0, #tracks hovering selections on main menu items
            'sub_menu0': 0, #tracks hovering selections on selectable categories
            'sub_menu1': 0, #tracks hovering selections on selectable items within categories
            'sub_menu2': 0, #tracks selected operations to be performed on selected items
            'char_select': 0, #tracks which character is being displayed
            'char_select2': 0, #tracks the performer when selecting an action recipient
            'switch_select': 0, #tracks a selected char in Switch mode
            'variable_menu': 0, #tracks changing sub_menu maximums for keypresses
            'scroll_var': 0, #tracks scrolling through overwhelmed menus
            'control_type': 'Keyboard', #keyboard, mouse, or controller
            'mouse_coords': (0,0), #X,Y coords of cursor location
            'mouse_hover': 0, #mouse selection target as int
            'shop_select': 0, #shop selection flag
            'shop_selected': None,
            'shop_selected_dict': {},
            'shop_scroll_cap':10, #number of items per menu in the shops
        }
        self.current_menu_key = 'main_menu'
        self.current_menu_type = 'vert_menu'
        self.current_menu_max = 7

    def set_screen(self, screen):
        self.rect = screen
        x, y = self.rect.topleft
        self.x_inc = int(self.rect.width / 10)
        self.y_inc = int(self.rect.height / 10)
        self.width = self.rect.width
        self.height = self.rect.height
        self.init_image = pygame.Surface((int(self.rect.width), int(self.rect.height)), pygame.SRCALPHA, 32).convert_alpha()
        self.image = self.init_image.copy()

        self.textbox_rect = Rect(self.x_inc*.25, self.y_inc*7.5, self.x_inc*9.5, self.y_inc*2.25)
        textbox_width = self.textbox_rect.width
        textbox_height = self.textbox_rect.height

        textbox_image, textbox_image_rect = load_Image('text_box.png')
        textbox_image_width, textbox_image_height = textbox_image.get_size()

        textbox_tile_width = 32
        textbox_tile_height = 32

        textbox_tile_table = []
        for tile_x in range(0, int(int(textbox_image_width)/int(textbox_tile_width))):
            line = []
            textbox_tile_table.append(line)
            for tile_y in range(0, int(int(textbox_image_height)/int(textbox_tile_height))):
                rect = (int(tile_x*textbox_tile_width), int(tile_y*textbox_tile_height), int(textbox_tile_width), int(textbox_tile_height))
                line.append(textbox_image.subsurface(rect))

        textbox_hor_tiles = int(textbox_width / textbox_tile_width)
        if textbox_hor_tiles < 3: textbox_hor_tiles = 3
        textbox_vert_tiles = int(textbox_height / textbox_tile_height)
        if textbox_vert_tiles < 3: textbox_vert_tiles = 3

        self.textbox_image_bg = pygame.Surface((textbox_hor_tiles*textbox_tile_width,
                                    textbox_vert_tiles*textbox_tile_height), pygame.SRCALPHA, 32).convert_alpha()

        for row in range(textbox_vert_tiles):
            for column in range(textbox_hor_tiles):
                if column == 0 and row == 0:
                    image_tile = textbox_tile_table[0][0]
                elif column == textbox_hor_tiles-1 and row == textbox_vert_tiles-1:
                    image_tile = textbox_tile_table[2][2]
                elif column == textbox_hor_tiles-1 and row == 0:
                    image_tile = textbox_tile_table[2][0]
                elif column == 0 and row == textbox_vert_tiles-1:
                    image_tile = textbox_tile_table[0][2]
                elif column == 0:
                    image_tile = textbox_tile_table[0][1]
                elif column == textbox_hor_tiles-1:
                    image_tile = textbox_tile_table[2][1]
                elif row == 0:
                    image_tile = textbox_tile_table[1][0]
                elif row == textbox_vert_tiles-1:
                    image_tile = textbox_tile_table[1][2]
                else:
                    image_tile = textbox_tile_table[1][1]
                image_tile.set_colorkey(white)
                self.textbox_image_bg.blit(image_tile,(column*textbox_tile_width,
                                row*textbox_tile_height))

        self.textbox_rect = Rect(self.textbox_rect.left + (self.textbox_rect.right - self.textbox_rect.left - (textbox_hor_tiles * textbox_tile_width))/2,
                                 self.textbox_rect.top + (self.textbox_rect.bottom - self.textbox_rect.top - (textbox_vert_tiles * textbox_tile_height))/2,
                                 textbox_hor_tiles * textbox_tile_width,
                                 textbox_vert_tiles * textbox_tile_height
                                 )

    def set_shop(self, shop_number):
        shop_all, shop_cons, shop_weap, shop_arm, shop_acc = [],[],[],[],[]
        
        if shop_number == 1:
            shop_cons.append(items.get_Item('Potion'))
            shop_cons.append(items.get_Item('Ether'))
            shop_weap.append(items.get_Item('Dagger'))
            shop_weap.append(items.get_Item('Copper Longsword'))
            shop_weap.append(items.get_Item('Light Staff'))
            shop_weap.append(items.get_Item('Copper Buckler'))
            shop_arm.append(items.get_Item('Nettled Hat'))
            shop_arm.append(items.get_Item('Nettled Doublet'))
            shop_arm.append(items.get_Item('Nettled Trousers'))
            shop_arm.append(items.get_Item('Nettled Halfgloves'))
            shop_arm.append(items.get_Item('Nettled Shoes'))
            shop_arm.append(items.get_Item('Leather Helm'))
            shop_arm.append(items.get_Item('Leather Vest'))
            shop_arm.append(items.get_Item('Leather Leggings'))
            shop_arm.append(items.get_Item('Leather Gloves'))
            shop_arm.append(items.get_Item('Leather Boots'))

        for each in shop_cons:
            shop_all.append(each)
        for each in shop_weap:
            shop_all.append(each)
        for each in shop_arm:
            shop_all.append(each)
        for each in shop_acc:
            shop_all.append(each)

        self.shop_items = [shop_all, shop_cons, shop_weap, shop_arm, shop_acc]
        self.menus['main_menu'] = 0
        self.current_menu_key = 'main_menu'
        self.current_menu_type = 'vert_menu'
        self.current_menu_max = 2
        self.temp_money = self.party.money

    def set_textbox_text(self, text, target = None, justification = 0):
        self.image = self.init_image.copy()

        final_lines = []
        requested_lines = text.splitlines()

        temp_rect = self.textbox_rect.copy()
        temp_rect = temp_rect.inflate(-self.x_inc*.5,-self.y_inc*.5)

        for requested_line in requested_lines:
            if self.font.size(requested_line)[0] > temp_rect.width:
                words = requested_line.split(' ')

                for word in words:
                    if self.font.size(word)[0] >= temp_rect.width:
                        print("The word " + str(word) + " is too long to fit in the rect passed.")
                        pygame.quit()
                accumulated_line = ""

                for word in words:
                    test_line = accumulated_line + word + " "

                    if self.font.size(test_line)[0] < temp_rect.width:
                        accumulated_line = test_line
                    else:
                        final_lines.append(accumulated_line)
                        accumulated_line = word + " "
                final_lines.append(accumulated_line)
            else:
                final_lines.append(requested_line)

        image_text = pygame.Surface(temp_rect.size, pygame.SRCALPHA, 32).convert_alpha()
        accumulated_height = 0
        for line in final_lines:
            if accumulated_height + self.font.size(line)[1] >= temp_rect.height:
                print("Once word-wrapped, the text string was too tall to fit in the rect.")
                pygame.quit()

            if line != "":
                tempsurface = self.font.render(line, True, white)
                if justification == 0:
                    image_text.blit(tempsurface, (0, accumulated_height))
                elif justification == 1:
                    image_text.blit(tempsurface, ((temp_rect.width - tempsurface.get_width()) / 2, accumulated_height))
                elif justification == 2:
                    image_text.blit(tempsurface, (temp_rect.width - tempsurface.get_width(), accumulated_height))
                else:
                    print("Invalid justification argument: " + str(justification))
                    pygame.quit()
            else:
                print("Line is empty.")

            accumulated_height += self.font.size(line)[1]

        self.image.blit(self.textbox_image_bg, self.textbox_rect)
        temp_x, temp_y = temp_rect.topleft
        temp_width, temp_height = temp_rect.size
        
        if target:
            image_target_text = self.font.render(target, True, white)
            self.image.blit(image_target_text, (temp_x, temp_y-(self.y_inc*.6), temp_width, temp_height))
            self.image.blit(image_text, temp_rect)
        else:
            self.image.blit(image_text, temp_rect)

    def set_visible(self, visible=0):
        self.visible = visible

    def move_select(self, direction):
        if self.current_menu_type == 'char_select':    # char select menu (special)
            if direction == 273: x = -1 #up
            elif direction == 274: x = 1 #down
            elif direction == 275: x = 2 #right
            elif direction == 276: x = -2 #left
            self.menus[self.current_menu_key] += x
            while True:
                self._select_min_max()
                if not self.party.members[self.menus[self.current_menu_key]]:
                    self.menus[self.current_menu_key] += pos_Neg(x)
                else:
                    break

        elif self.current_menu_type == 'char_select2':    # switch select menu (special)
            if direction == 273: x = -1
            elif direction == 274: x = 1
            elif direction == 275: x = 2
            elif direction == 276: x = -2
            self.menus[self.current_menu_key] += x
            self._select_min_max()

        elif self.current_menu_type == 'vert_menu':    # vertical (Y) increment menus
            if direction == 273: x = -1
            elif direction == 274: x = 1
            else: x = 0
            self.menus[self.current_menu_key] += x
            self._select_min_max()

        elif self.current_menu_type == 'hor_menu':    # horizonal (X) increment menus
            if direction == 275: x = 1
            elif direction == 276: x = -1
            else: x = 0
            self.menus[self.current_menu_key] += x
            self._select_min_max()

        elif self.current_menu_type == 'number_menu':     # left/right and up/down separate increment menus
            x,y = 0,0
            item_value = items.get_Item(self.menus['shop_selected'])['value']

            if direction == 273: x = -1
            elif direction == 274: x = 1
            elif direction == 275:
                if self.menus['menu'] == 1: #buy more
                    if self.temp_money >= item_value and self._get_num_of_shop_item(self.menus['shop_selected']) < 99 - int(self.inventory.get_Num_of_Item(self.menus['shop_selected'])):
                        try:
                            self.menus['shop_selected_dict'][self.menus['shop_selected']] += 1
                        except:
                            self.menus['shop_selected_dict'][self.menus['shop_selected']] = 1
                        self.temp_money -= item_value
                elif self.menus['menu'] == 2: #sell more
                    if self.inventory.get_Num_of_Item_Avail(self.menus['shop_selected']) > self._get_num_of_shop_item(self.menus['shop_selected']):
                        try:
                            self.menus['shop_selected_dict'][self.menus['shop_selected']] += 1
                        except:
                            self.menus['shop_selected_dict'][self.menus['shop_selected']] = 1
                        self.temp_money += int(item_value/2)
            elif direction == 276:
                if self._get_num_of_shop_item(self.menus['shop_selected']) > 0:
                    if self.menus['menu'] == 1: #buy less
                        self.menus['shop_selected_dict'][self.menus['shop_selected']] -= 1
                        self.temp_money += item_value
                        if self.menus['shop_selected_dict'][self.menus['shop_selected']] == 0:
                            del self.menus['shop_selected_dict'][self.menus['shop_selected']]
                    elif self.menus['menu'] == 2: #sell less
                        self.menus['shop_selected_dict'][self.menus['shop_selected']] -= 1
                        self.temp_money -= int(item_value/2)
                        if self.menus['shop_selected_dict'][self.menus['shop_selected']] == 0:
                            del self.menus['shop_selected_dict'][self.menus['shop_selected']]
            self.menus[self.current_menu_key] += x
            self._select_min_max()

        elif self.current_menu_type == 'xy_menu':     # X/Y increment menus
            if direction == 273: x = -2
            elif direction == 274: x = 2
            elif direction == 275: x = 1
            elif direction == 276: x = -1
            self.menus[self.current_menu_key] += x
            self._select_min_max()

    def _select_min_max(self):
        if self.menus[self.current_menu_key] >= self.current_menu_max:
            self.menus[self.current_menu_key] -= self.current_menu_max
        elif self.menus[self.current_menu_key] < 0:
            self.menus[self.current_menu_key] += self.current_menu_max

    def _char_select_min(self):
        while not self.party.members[self.menus[self.current_menu_key]]:
            self.menus[self.current_menu_key] += 1

    def _set_to_init(self):
        self.menus['menu'] = 0
        self.menus['char_select'] = 0
        self.menus['char_select2'] = 0
        self.menus['sub_menu0'] = 0
        self.menus['sub_menu1'] = 0
        self.menus['sub_menu2'] = 0
        self.current_menu_key = 'main_menu'
        self.current_menu_type = 'vert_menu'
        self.current_menu_max = 7

    def set_select(self, direction=None):
        #for controlling the textbox system
        if self.ev_handler.overlay == 'text_box':
            if direction in [13,27]:
                self.ev_handler.curr_event_cont += 1
                self.ev_handler.overlay = None
        #for controlling the shop system
        elif self.ev_handler.overlay == 'shop':
            if direction == 13: #return key
                if self.menus['shop_select'] == 0: #Buy/Sell
                    self.menus['menu'] = self.menus['main_menu']+1
                    self.menus['shop_select'] +=1
                    self.current_menu_key = 'sub_menu0'
                    self.current_menu_type = 'hor_menu'
                    self.current_menu_max = 5
                elif self.menus['shop_select'] == 1: #Cat Selection - max set during update
                    if self.menus['variable_menu'] > 0:
                        self.menus['shop_select'] += 1
                        self.current_menu_key = 'sub_menu1'
                        self.current_menu_type = 'number_menu'
                elif self.menus['shop_select'] == 2: #Item Selection
                    self.menus['shop_select'] += 1
                    self.current_menu_key = 'sub_menu2'
                    self.current_menu_type = 'vert_menu'
                    if self.menus['menu'] == 1:
                        self.current_menu_max = 3
                    elif self.menus['menu'] == 2:
                        self.current_menu_max = 2
                elif self.menus['shop_select'] == 3: #Oper Selection - update resets back to Item Selection
                    self.menus['shop_select'] += 1
            elif direction == 27: #escape key
                if self.menus['shop_select'] == 0: #Buy/Sell
                    self.ev_handler.overlay = None
                    self.ev_handler.curr_event_cont += 1
                    self.set_visible()
                    self._set_to_init()
                elif self.menus['shop_select'] == 1: #Cat Selection
                    self.menus['shop_select'] = 0
                    self.menus['menu'] = 0
                    self.menus['sub_menu0'] = 0
                    self.menus['shop_selected_dict'] = {}
                    self.current_menu_key = 'main_menu'
                    self.current_menu_type = 'vert_menu'
                    self.current_menu_max = 2
                elif self.menus['shop_select'] == 2: #Item Selection
                    self.menus['shop_select'] = 1
                    self.menus['sub_menu1'] = 0
                    self.current_menu_key = 'sub_menu0'
                    self.current_menu_type = 'hor_menu'
                    self.current_menu_max = 5
                elif self.menus['shop_select'] == 3: #Oper Selection - max set during update
                    self.menus['shop_select'] = 2
                    self.menus['sub_menu2'] = 0
                    self.current_menu_key = 'sub_menu1'
                    self.current_menu_type = 'number_menu'
        #for controlling the menu system
        elif self.ev_handler.overlay == 'menu':
            if direction == 13: #forward! (RETURN KEY)
                if self.menus['menu'] == 0:
                    if self.menus['main_menu'] != 6: #if not config, since config isn't made yet
                        self.menus['menu'] = self.menus['main_menu']+1
                        if self.menus['menu'] in [1,3,4,5]:
                            self.current_menu_key = 'char_select'
                            self.current_menu_type = 'char_select'
                            self.current_menu_max = 4
                            self._char_select_min()
                        elif self.menus['menu'] == 2:
                            self.current_menu_key = 'sub_menu0'
                            self.current_menu_type = 'hor_menu'
                            self.current_menu_max = 6
                        elif self.menus['menu'] == 6:
                            self.current_menu_key = 'char_select'
                            self.current_menu_type = 'char_select2'
                            self.current_menu_max = 4
                            self._char_select_min()
                elif self.menus['menu'] == 1: #status
                    self.menus['menu_select'] = 1
                    #also char_select menu key
                    #also char_select menu type
                    #also max = 4
                elif self.menus['menu'] == 2: #items
                    if self.menus['item_select'] == 0:
                        if self.menus['variable_menu']:
                            self.current_menu_key = 'sub_menu1'
                            self.current_menu_type = 'xy_menu'
                            self.current_menu_max = self.menus['variable_menu']
                            self.menus['item_select'] = 1
                    elif self.menus['item_select'] == 1:
                        if items.get_Type(self.menus['item_selected']) == "Consumable":
                            self.current_menu_key = 'char_select'
                            self.current_menu_type = 'char_select'
                            self.current_menu_max = 4
                            self._char_select_min()
                            self.menus['item_select'] = 2
                    elif self.menus['item_select'] == 2:
                        self.menus['item_select'] = 3
                elif self.menus['menu'] == 3: #equip
                    if self.menus['equip_select'] == 0:
                        self.current_menu_key = 'sub_menu0'
                        self.current_menu_type = 'vert_menu'
                        self.current_menu_max = 10
                        self.menus['equip_select'] = 1
                    elif self.menus['equip_select'] == 1:
                        self.current_menu_key = 'sub_menu1'
                        #also vert_menu type
                        #maximum set in update phase
                        self.menus['equip_select'] = 2
                    elif self.menus['equip_select'] == 2:
                        self.current_menu_key = 'sub_menu0'
                        #also vert_menu type
                        #maximum set in update phase
                        self.menus['equip_select'] = 3
                elif self.menus['menu'] == 4: #magic
                    if self.menus['magic_select'] == 0:
                        self.current_menu_key = 'sub_menu0'
                        self.current_menu_type = 'hor_menu'
                        self.current_menu_max = 4
                        self.menus['magic_select'] = 1
                    elif self.menus['magic_select'] == 1:
                        if self.menus['variable_menu']:
                            self.current_menu_key = 'sub_menu1'
                            self.current_menu_type = 'xy_menu'
                            #maximum set in update phase
                            self.menus['magic_select'] = 2
                    elif self.menus['magic_select'] == 2:
                        temp_char = self.party.members[self.menus['char_select']]
                        if temp_char.magic.get_Spell(self.menus['magic_selected'])['type'] == 'healing' and \
                            temp_char.stats['curr']['mp'] >= temp_char.magic.get_Spell(self.menus['magic_selected'])['cost']:
                            self.current_menu_key = 'char_select2'
                            self.current_menu_type = 'char_select'
                            self.current_menu_max = 4
                            self._char_select_min()
                            self.menus['magic_select'] = 3
                    elif self.menus['magic_select'] == 3:
                        self.menus['magic_select'] = 4
                elif self.menus['menu'] == 5: #skills
                    if self.menus['skill_select'] == 0:
                        self.current_menu_key = 'sub_menu0'
                        self.current_menu_type = 'hor_menu'
                        self.current_menu_max = 2
                        self.menus['skill_select'] = 1
                    elif self.menus['skill_select'] == 1:
                        if self.menus['variable_menu']:
                            self.current_menu_key = 'sub_menu1'
                            self.current_menu_type = 'vert_menu'
                            #maximum set in update phase
                            self.menus['skill_select'] = 2
                elif self.menus['menu'] == 6: #switch
                    if self.menus['switch_select'] == 0:
                        self.current_menu_key = 'char_select2'
                        self.current_menu_type = 'char_select2'
                        self.current_menu_max = 4
                        self.menus['switch_select'] = 1
                    elif self.menus['switch_select'] == 1:
                        self.party.members[self.menus['char_select']], self.party.members[self.menus['char_select2']] = self.party.members[self.menus['char_select2']], self.party.members[self.menus['char_select']]
                        self.current_menu_key = 'char_select'
                        self.current_menu_type = 'char_select'
                        self._char_select_min()
                        self.menus['switch_select'] = 0
                        self.menus['char_select2'] = 0
    
            elif direction == 27: #back! (ESCAPE KEY)
                if self.menus['menu'] == 0:
                    self.ev_handler.overlay = None
                    self.set_visible()
                elif self.menus['menu'] == 1:
                    if self.menus['menu_select'] == 0:
                        self._set_to_init()
                    elif self.menus['menu_select'] == 1:
                        self.menus['menu_select'] = 0
                elif self.menus['menu'] == 2:
                    if self.menus['item_select'] == 0:
                        self._set_to_init()
                    elif self.menus['item_select'] == 1:
                        self.menus['item_select'] = 0
                        self.current_menu_key = 'sub_menu0'
                        self.current_menu_type = 'hor_menu'
                        self.current_menu_max = 6
                        self.menus['sub_menu1'] = 0
                    elif self.menus['item_select'] == 2:
                        self.menus['item_select'] = 1
                        self.current_menu_key = 'sub_menu1'
                        self.current_menu_type = 'xy_menu'
                        self.current_menu_max = self.menus['variable_menu']
                        self.menus['char_select'] = 0
                elif self.menus['menu'] == 3:
                    if self.menus['equip_select'] == 0:
                        self._set_to_init()
                    elif self.menus['equip_select'] == 1:
                        self.current_menu_key = 'char_select'
                        self.current_menu_type = 'char_select'
                        self.current_menu_max = 4
                        self.menus['sub_menu0'] = 0
                        self.menus['equip_select'] = 0
                    elif self.menus['equip_select'] == 2:
                        self.current_menu_key = 'sub_menu0'
                        self.current_menu_type = 'vert_menu'
                        self.current_menu_max = 10
                        self.menus['sub_menu1'] = 0
                        self.menus['equip_select'] = 1
                elif self.menus['menu'] == 4:
                    if self.menus['magic_select'] == 0:
                        self._set_to_init()
                    elif self.menus['magic_select'] == 1:
                        self.current_menu_key = 'char_select'
                        self.current_menu_type = 'char_select'
                        self.current_menu_max = 4
                        self.menus['sub_menu0'] = 0
                        self.menus['magic_select'] = 0
                    elif self.menus['magic_select'] == 2:
                        self.current_menu_key = 'sub_menu0'
                        self.current_menu_type = 'hor_menu'
                        self.current_menu_max = 4
                        self.menus['sub_menu1'] = 0
                        self.menus['scroll_var'] = 0
                        self.menus['magic_select'] = 1
                    elif self.menus['magic_select'] == 3:
                        self.current_menu_key = 'sub_menu1'
                        self.current_menu_type = 'xy_menu'
                        self.current_menu_max = self.menus['variable_menu']
                        self.menus['char_select2'] = 0
                        self.menus['magic_select'] = 2
                elif self.menus['menu'] == 5:
                    if self.menus['skill_select'] == 0:
                        self._set_to_init()
                    elif self.menus['skill_select'] == 1:
                        self.current_menu_key = 'char_select'
                        self.current_menu_type = 'char_select'
                        self.current_menu_max = 4
                        self.menus['sub_menu0'] = 0
                        self.menus['skill_select'] = 0
                    elif self.menus['skill_select'] == 2:
                        self.current_menu_key = 'sub_menu0'
                        self.current_menu_type = 'hor_menu'
                        self.current_menu_max = 2
                        self.menus['sub_menu1'] = 0
                        self.menus['scroll_var'] = 0
                        self.menus['skill_select'] = 1
                elif self.menus['menu'] == 6:
                    if self.menus['switch_select'] == 0:
                        self._set_to_init()
                    elif self.menus['switch_select'] == 1:
                        self.current_menu_key = 'char_select'
                        self.current_menu_type = 'char_select2'
                        self.menus['switch_select'] = 0
                        self.menus['char_select2'] = 0

    def _get_time(self):
        time_temp = pygame.time.get_ticks()
        sec_temp = int(time_temp / (1000))
        while sec_temp > 59:
            sec_temp -= 60
        min_temp = int(time_temp  / (1000 * 60))
        while min_temp > 59:
            min_temp -= 60
        hour_temp = int(time_temp / (1000 * 3600))
        min_temp = "%02d" % min_temp
        sec_temp = "%02d" % sec_temp
        cur_time = str(hour_temp) + ":" + str(min_temp) + ":" + str(sec_temp)
        time_played = self.font.render(cur_time,True,white)
        time_played_pos = time_played.get_rect()
        time_played_pos.centerx = self.x_inc * 9
        time_played_pos.centery = self.y_inc * 9.5
        self.image.blit(time_played, time_played_pos)

    def _get_num_of_shop_item(self, item):
        if item in self.menus['shop_selected_dict']:
            return int(self.menus['shop_selected_dict'][item])
        else:
            return 0

    def update(self):
        if self.ev_handler.overlay in ['menu','shop']:
            self.image = self.init_image.copy()

        if self.ev_handler.overlay == 'menu':
            def menu_Text_Display(text, pos):
                if pos == self.menus['menu']-1:
                    menu_text = self.font.render(text,True,red)
                elif self.menus['main_menu'] == pos:
                    menu_text = self.font.render(text,True,yellow)
                else:
                    menu_text = self.font.render(text,True,white)
            
                text_pos = menu_text.get_rect()
                text_pos.centerx = self.x_inc*9
                text_pos.centery = self.y_inc*.75*(pos+1)
                self.image.blit(menu_text, text_pos)
                
                if text_pos.collidepoint(self.menus['mouse_coords']):
                    self.menus['mouse_hover'] = pos
        
            def char_Portrait_Display(pos):
                char_rect = Rect(self.x_inc*.5 if pos < 2 else self.x_inc*4.5, self.y_inc*.5 if not is_Odd(pos) else self.y_inc*5.5, self.x_inc*3, self.y_inc*4)
            
                self.image.fill(blue, char_rect)
                if (self.menus['menu'] == 6 and self.menus['switch_select'] == 1 and self.menus['char_select'] == pos) or \
                    (self.menus['menu'] == 4 and self.menus['magic_select'] == 3 and self.menus['char_select2'] == pos):
                    pygame.draw.rect(self.image,red,char_rect,4)
                elif (self.menus['menu'] in [1,3,4,5,6] and self.menus['char_select'] == pos) or \
                    (self.menus['menu'] == 2 and self.menus['item_select'] == 2 and self.menus['char_select'] == pos) or \
                    (self.menus['menu'] ==6 and self.menus['switch_select'] == 1 and self.menus['char_select2'] == pos):
                    pygame.draw.rect(self.image,yellow,char_rect,4)
                else:
                    pygame.draw.rect(self.image,dkblue,char_rect,4)
                    
                if char_rect.collidepoint(self.menus['mouse_coords']):
                    self.menus['mouse_hover'] = pos
            
            def char_Text_Display(char, pos):
                x_offset = self.x_inc*.7 if pos < 2 else self.x_inc*4.7
                y_offset = self.y_inc*.7 if not is_Odd(pos) else self.y_inc*5.7
            
                charname = self.font.render(char.first_Name(),True,white)
                charlevel = self.font.render("Level: "+str(char.stats['curr']['lvl']),True,white)
                charhptext = self.font.render("HP:",True,white)
                charmptext = self.font.render("MP:",True,white)
                charstatustext = self.font.render("Status:",True,white)
                charnextlevel = self.font.render("Next Level: "+str(char.stats['curr']['exp'])+" / "+str(char.stats['curr']['exn']),True,white)
                divider = self.font.render("/",True,white)
                charminhp = self.font.render(str(char.stats['curr']['hp']),True,white)
                charmaxhp = self.font.render(str(char.stats['curr']['maxhp']),True,white)
                charminmp = self.font.render(str(char.stats['curr']['mp']),True,white)
                charmaxmp = self.font.render(str(char.stats['curr']['maxmp']),True,white)
                self.image.blit(charname, (x_offset+0,y_offset+0))
                self.image.blit(charlevel, (x_offset+0,y_offset+20))
                self.image.blit(charhptext, (x_offset+0,y_offset+61))
                self.image.blit(charminhp, (x_offset+41,y_offset+61))
                self.image.blit(divider, (x_offset+76,y_offset+61))
                self.image.blit(charmaxhp, (x_offset+91,y_offset+61))
                self.image.blit(charmptext, (x_offset+0,y_offset+81))
                self.image.blit(charminmp, (x_offset+41,y_offset+81))
                self.image.blit(divider, (x_offset+76,y_offset+81))
                self.image.blit(charmaxmp, (x_offset+91,y_offset+81))
                self.image.blit(charstatustext, (x_offset+0,y_offset+141))
                self.image.blit(charnextlevel, (x_offset+0,y_offset+166))
        
            def in_Status():
                char = self.party.members[self.menus['char_select']]
                
                statusrect = Rect(self.x_inc*.5,self.y_inc*.5,self.x_inc*7,self.y_inc*9)
                self.image.fill(blue, statusrect)
                pygame.draw.rect(self.image,dkblue,statusrect,4)
                
                status_Top_Display("Name:", char.name, 0)
                status_Top_Display("Class:", "Not Implemented Yet", 1)
                status_Top_Display("Age:", char.age, 2)
                status_Top_Display("Sex:", char.sex, 3)
                status_Top_Display("Race:", char.race, 4)
                status_Top_Display("Birthplace:", char.birthplace, 5)
                status_Top_Display("Biography:", char.biography, 7)
            
                pygame.draw.line(self.image, dkblue, [self.x_inc*.5,self.y_inc*5.8],[self.x_inc*7.5,self.y_inc*5.8],5)
            
                a,b=0,0
                for each in ['lvl','str','dex','agi','spd','exp','int','wsd','lck','ext','pow','mpow','def','mdef']:
                    status_Bottom_Display(str.upper(each)+":", str(char.stats['curr'][each]), char, a, b)
                    a += 1
                    if a == 4 and b == 1:
                        a = 5
                    if a > 4:
                        a = 0
                        b += 1
        
            def status_Top_Display(text, result, pos):
                statusleftrect = Rect(self.x_inc,self.y_inc*.8,self.x_inc*.7,self.y_inc*.5)
                statusrightrect = Rect(self.x_inc*2,self.y_inc*.8,self.x_inc*.7,self.y_inc*.5)
            
                statustext = self.font.render(str(text),True,white)
                statustext_pos = statustext.get_rect()
                statustext_pos.right = statusleftrect.right
                statustext_pos.centery = statusleftrect.centery + (pos * self.y_inc*.4)
                self.image.blit(statustext, statustext_pos)
                
                nameresult = self.font.render(str(result),True,white)
                nameresult_pos = nameresult.get_rect()
                nameresult_pos.left = statusrightrect.left
                nameresult_pos.centery = statusrightrect.centery + (pos * self.y_inc*.4)
                self.image.blit(nameresult, nameresult_pos)
            
            def status_Bottom_Display(text, result, char, pos1, pos2):
                if text == "EXT:":
                    text = ""
                    result = ""
                if text == "EXP:":
                    result = str(char.stats['curr']['exp'])+" / "+str(char.stats['curr']['exn'])
                if pos1 > 0:
                    pos1 += 1
                statusbleftrect = Rect(self.x_inc*.3,self.y_inc*5.8,self.x_inc,self.y_inc)
                statusbrightrect = Rect(self.x_inc*1.5,self.y_inc*5.8,self.x_inc,self.y_inc)
                
                stattext = self.font.render(text,True,white)
                stattext_pos = stattext.get_rect()
                stattext_pos.right = statusbleftrect.right
                stattext_pos.centery = statusbleftrect.centery + (pos1 * self.y_inc*.5)
                stattext_pos = stattext_pos.move((pos2 * self.x_inc*2.5),0)
                self.image.blit(stattext, stattext_pos)
                
                statresult = self.font.render(result,True,white)
                statresult_pos = statresult.get_rect()
                statresult_pos.left = statusbrightrect.left
                statresult_pos.centery = statusbrightrect.centery + (pos1 * self.y_inc*.5)
                statresult_pos = statresult_pos.move((pos2 * self.x_inc*2.5),0)
                self.image.blit(statresult, statresult_pos)
        
            def in_Items():
                itemrect = Rect(self.x_inc*.5,self.y_inc*.5,self.x_inc*7,self.y_inc*9)
                self.image.fill(blue, itemrect)
                pygame.draw.rect(self.image,dkblue,itemrect,4)
                pygame.draw.line(self.image,dkblue,[self.x_inc*.5,self.y_inc*1.3],[self.x_inc*7.5,self.y_inc*1.3],2)
                for i, v in enumerate(['All','CONS', 'WEP', 'ARM','ACC','KEY']):
                    item_Cat_Display(v, i)
            
                temp_inventory = sorted(self.inventory.items)
                temp_items = []
                for each in temp_inventory:
                    temp = items.get_Type(each)
                    try:
                        if self.menus['sub_menu0'] == 0 or temp in (['Consumable'],
                                                              ['Dagger','1H Sword','2H Sword','Staff','Bow','Spear'],
                                                              ['Light Head Armor','Light Body Armor','Light Leg Armor','Light Hand Armor','Light Feet Armor',
                                                               'Medium Head Armor','Medium Body Armor','Medium Leg Armor','Medium Hand Armor','Medium Feet Armor',
                                                               'Heavy Head Armor','Heavy Body Armor','Heavy Leg Armor','Heavy Hand Armor','Heavy Feet Armor',
                                                               'Light Shield', 'Heavy Shield'],
                                                              ['Accessories1','Accessories2','Accessories3','Acessories4','Accessories5','Accessories6','Accessories7'],
                                                              ['Key Items'])[self.menus['sub_menu0']-1]:
                            temp_items.append(each)
                    except: continue
            
                self.menus['variable_menu'] = len(temp_items)
                if self.menus['item_select'] == 1:
                    self.current_menu_max = self.menus['variable_menu']
                temp_items.sort()
                mindisplay = self.menus['scroll_var']
                maxdisplay = self.menus['item_scroll_cap'] + self.menus['scroll_var']
            
                for each in temp_items:
                    item_Text_Display(each, temp_items.index(each))
        
            def item_Cat_Display(text, pos):
                itemrect = Rect(self.x_inc, self.y_inc*.7, self.x_inc*.5, self.y_inc*.5)
                itemtext = self.font.render(text,True,white)
                itemtext_pos = itemtext.get_rect()
                itemtext_pos.centerx = itemrect.centerx
                itemtext_pos.centery = itemrect.centery
                itemtext_pos = itemtext_pos.move((pos * self.x_inc*1.1),0)
                self.image.blit(itemtext, itemtext_pos)
                if self.menus['item_select'] == 1:
                    colortemp = red
                else:
                    colortemp = yellow
                if pos == self.menus['sub_menu0']:
                    itemtext_pos = itemtext_pos.inflate(4,4)
                    pygame.draw.rect(self.image,colortemp,itemtext_pos,2)
        
            def item_Text_Display(text, pos):
                if items.get_Type(text) == "Consumable":
                    tempcolor = white
                else:
                    tempcolor = gray
            
                itemrect = Rect(self.x_inc*.8, self.y_inc*1.2, self.x_inc, self.y_inc)
                itemtext = self.font.render(text,True,tempcolor)
                itemtext_pos = itemtext.get_rect()
                itemtext_pos.centerx = itemrect.centerx
                itemtext_pos.centery = itemrect.centery
                itemtext_pos.left = itemrect.left
                if is_Odd(pos+1):
                    itemtext_pos = itemtext_pos.move(0,(pos * self.y_inc*.24))
                else:
                    itemtext_pos = itemtext_pos.move(self.x_inc*3.5,((pos-1) * self.y_inc*.24))
                self.image.blit(itemtext, itemtext_pos)
                if pos == self.menus['sub_menu1'] and self.menus['item_select'] == 1:
                    pygame.draw.rect(self.image,yellow,itemtext_pos,2)
                    self.menus['item_selected'] = text
                
                itemamt = self.font.render(str(self.inventory.items[text]),True,tempcolor)
                itemamt_pos = itemtext_pos.move(self.x_inc*2.8,0)
                self.image.blit(itemamt, itemamt_pos)
                
                pygame.draw.line(self.image,dkblue,[self.x_inc*4,self.y_inc*1.3],[self.x_inc*4,self.y_inc*8.4],2)
                pygame.draw.line(self.image,dkblue,[self.x_inc*.5,self.y_inc*8.4],[self.x_inc*7.5,self.y_inc*8.4],2)
                
                if pos == self.menus['sub_menu1'] and self.menus['item_select'] == 1:
                    descrect = Rect(self.x_inc*.7,self.y_inc*8.75,self.x_inc*7.3,self.y_inc)
                    desctext = self.font.render("Description: "+str(items.get_Item(text)['desc']),True,white)
                    self.image.blit(desctext,descrect)
        
            def use_Items():
                char = self.party.members[self.menus['char_select']]
                itemtemp = items.get_Item(self.menus['item_selected'])
                if itemtemp['effect'] == "heal hp":
                    if char.stats['curr']['hp'] < char.stats['curr']['maxhp']:
                        char.stats['curr']['hp'] += itemtemp['amount']
                        self.inventory.rem_Item(itemtemp['name'],1)
                        if char.stats['curr']['hp'] > char.stats['curr']['maxhp']:
                            char.stats['curr']['hp'] = char.stats['curr']['maxhp']
                    else:
                        pass
                elif itemtemp['effect'] == "heal mp":
                    if char.stats['curr']['mp'] < char.stats['curr']['maxmp']:
                        char.stats['curr']['mp'] += itemtemp['amount']
                        self.inventory.rem_Item(itemtemp['name'],1)
                        if char.stats['curr']['mp'] > char.stats['curr']['maxmp']:
                            char.stats['curr']['mp'] = char.stats['curr']['maxmp']
                    else:
                        pass
                if self.inventory.has_Item(itemtemp['name']):
                    self.menus['item_select'] = 2
                else:
                    if self.current_menu_max == 1:
                        self.menus['item_select'] = 0
                        self.current_menu_key = 'sub_menu0'
                        self.current_menu_type = 'hor_menu'
                        self.current_menu_max = 6
                        self.menus['sub_menu1'] = 0
                        self.menus['char_select'] = 0
                    else:
                        self.menus['item_select'] = 1
                        self.current_menu_key = 'sub_menu1'
                        self.current_menu_type = 'xy_menu'
                        self.current_menu_max == self.menus['variable_menu']
                        if self.menus['sub_menu1'] == self.current_menu_max:
                            self.menus['sub_menu1'] -= 1
                        self.menus['char_select'] = 0
        
            def in_Equip():
                char = self.party.members[self.menus['char_select']]
                
                window_rect = (self.x_inc*.5,self.y_inc*.5,self.x_inc*7,self.y_inc*9)
                self.image.fill(blue,window_rect)
                pygame.draw.rect(self.image, dkblue,window_rect,4)
                
                charname = self.font.render(char.name,True,white)
                self.image.blit(charname, (self.x_inc*.75,self.y_inc*.75,self.x_inc*.5,self.y_inc*.5))
            
                for value in index_equip:
                    equip_Top_Display(index_equip_text[index_equip.index(value)],char.equip[value],index_equip.index(value))
                
                pygame.draw.line(self.image, dkblue, (self.x_inc*.5,self.y_inc*5),(self.x_inc*7.5,self.y_inc*5),3)
                
                for value in index_equip_stat:
                    equip_Bottom_Display(str.upper(value)+":", value, char.stats['curr'][value], index_equip_stat.index(value))
                    
                pygame.draw.line(self.image,dkblue,[self.x_inc*.5,self.y_inc*8.5],[self.x_inc*7.5,self.y_inc*8.5],3)
                
                if self.menus['equip_select'] == 2 and self.menus['equip_selected'] != "Empty":
                    desc_text_temp = "Description: " + str(items.get_Item(self.menus['equip_selected'])['desc'])
                elif self.menus['equip_select'] == 1:
                    desc_text_temp = "Description: " + str(char.equip[index_equip[self.menus['sub_menu0']]]['desc'])
                else:
                    desc_text_temp = "Description: None"
                desc_rect = Rect(self.x_inc*.75,self.y_inc*8.8,self.x_inc*7,self.y_inc)
                desc_text = self.font.render(desc_text_temp,True,white)
                self.image.blit(desc_text,desc_rect)
            
            def equip_Top_Display(text, slot, pos):
                if pos < 2:
                    offset = self.y_inc*.35 * pos
                elif pos < 7:
                    offset = (self.y_inc*.35 * pos) + self.y_inc*.25
                else:
                    offset = (self.y_inc*.35 * pos) + self.y_inc*.5
                equiprect = Rect(self.x_inc*5, self.y_inc*.65, self.x_inc*.5, self.y_inc*.5)
                equiptext = self.font.render(text,True,white)
                equiptext_pos = equiptext.get_rect()
                equiptext_pos.right = equiprect.right
                equiptext_pos.centery = equiprect.centery + offset
                self.image.blit(equiptext, equiptext_pos)
            
                equipgearrect = Rect(self.x_inc*5.7, self.y_inc*.65, self.x_inc*.5, self.y_inc*.5)
                equipgear = self.font.render(slot['name'],True,white)
                equipgear_pos = equipgear.get_rect()
                equipgear_pos.left = equipgearrect.left
                equipgear_pos.centery = equipgearrect.centery + offset
                self.image.blit(equipgear, equipgear_pos)
                if self.menus['equip_select'] == 2:
                    colortemp = red
                else:
                    colortemp = yellow
                if pos == self.menus['sub_menu0']:
                    equipgear_pos = equipgear_pos.inflate(4,4)
                    pygame.draw.rect(self.image,colortemp,equipgear_pos,2)
            
            def equip_Bottom_Display(text, slot, stat, pos1):
                char = self.party.members[self.menus['char_select']]
                if pos1 < 4:
                    pos2 = 0
                elif pos1 < 7:
                    pos1 -= 4
                    pos2 = 1
                else:
                    pos1 -= 7
                    pos2 = 2
                equip_left_rect = Rect(self.x_inc*.75,self.y_inc*5.25,self.x_inc*.5,self.y_inc*.5)
                equip_right_rect = Rect(self.x_inc*1.5,self.y_inc*5.25,self.x_inc*.5,self.y_inc*.5)
            
                equip_text = self.font.render(text,True,white)
                equip_text_pos = equip_text.get_rect()
                equip_text_pos.right = equip_left_rect.right
                equip_text_pos.centery = equip_left_rect.centery + (pos1 * self.y_inc*.5)
                equip_text_pos = equip_text_pos.move((pos2 * self.x_inc*2.5),0)
                self.image.blit(equip_text, equip_text_pos)
                
                color_temp = white
                stat_temp = stat
            
                if slot != "Empty" and self.menus['equip_select'] == 2:
                    temp_name = items.get_Item(self.menus['equip_selected'])
                    temp_equip = temp_name[slot]
                    if temp_equip != 0:
                        stat_temp += temp_equip
                    if self.menus['sub_menu0'] == 0:
                        stat_temp -= char.equip['main'][slot]
                        if temp_name['name'] != "Empty" and temp_name['type'] in ['Staff', '2H Sword', 'Spear', 'Bow']:
                            stat_temp -= char.equip['offh'][slot]
                    elif self.menus['sub_menu0'] == 1:
                        stat_temp -= char.equip['offh'][slot]
                        if temp_name['name'] != "Empty" and char.equip['main']['type'] in ['Staff', '2H Sword', 'Spear', 'Bow']:
                            stat_temp -= char.equip['main'][slot]
                    elif self.menus['sub_menu0'] == 2:
                        stat_temp -= char.equip['head'][slot]
                    elif self.menus['sub_menu0'] == 3:
                        stat_temp -= char.equip['body'][slot]
                    elif self.menus['sub_menu0'] == 4:
                        stat_temp -= char.equip['legs'][slot]
                    elif self.menus['sub_menu0'] == 5:
                        stat_temp -= char.equip['hand'][slot]
                    elif self.menus['sub_menu0'] == 6:
                        stat_temp -= char.equip['feet'][slot]
                    elif self.menus['sub_menu0'] == 7:
                        stat_temp -= char.equip['acc1'][slot]
                    elif self.menus['sub_menu0'] == 8:
                        stat_temp -= char.equip['acc2'][slot]
                    elif self.menus['sub_menu0'] == 9:
                        stat_temp -= char.equip['acc3'][slot]
                    if stat_temp > int(stat):
                        color_temp = yellow
                        stat_temp = str(stat_temp)+" (+"+str(int(stat_temp)-int(stat))+")"
                    elif stat_temp < int(stat):
                        color_temp = red
                        stat_temp = str(stat_temp)+" (-"+str(int(stat)-int(stat_temp))+")"
                    stat = stat_temp
                
                equip_stat = self.font.render(str(stat),True,color_temp)
                equip_stat_pos = equip_stat.get_rect()
                equip_stat_pos.left = equip_right_rect.left
                equip_stat_pos.centery = equip_right_rect.centery + (pos1 * self.y_inc*.5)
                equip_stat_pos = equip_stat_pos.move((pos2 * self.x_inc*2.6),0)
                self.image.blit(equip_stat, equip_stat_pos)
        
            def change_Equip():
                char = self.party.members[self.menus['char_select']]
            
                temp_inventory = sorted(self.inventory.avail)
                equipChange = []
                equipChange.append('Empty')
                
                for each in temp_inventory:
                    temp = items.get_Type(each)
                    try:
                        if temp in (char.equip_avail['main'],
                                    char.equip_avail['offh'],
                                    char.equip_avail['head'],
                                    char.equip_avail['body'],
                                    char.equip_avail['legs'],
                                    char.equip_avail['hand'],
                                    char.equip_avail['feet'],
                                    char.equip_avail['acc'],
                                    char.equip_avail['acc'],
                                    char.equip_avail['acc'])[self.menus['sub_menu0']]:
                            equipChange.append(each)
                    except:continue
        
                self.menus['variable_menu'] = len(equipChange)
                self.current_menu_max = self.menus['variable_menu']
                
                self.image.fill(blue,(self.x_inc*7,self.y_inc*.5,self.x_inc*2,self.y_inc*.3+(self.menus['variable_menu'] * self.y_inc*.5)))
                pygame.draw.rect(self.image, dkblue,(self.x_inc*7,self.y_inc*.5,self.x_inc*2,self.y_inc*.3+(self.menus['variable_menu'] * self.y_inc*.5)),4)
            
                for each in equipChange:
                    change_Equip_Display(each,equipChange.index(each))
            
                if self.menus['equip_select'] == 3:
                    equip.equip_Item(char, self.inventory, index_equip[self.menus['sub_menu0']], equipChange[self.menus['sub_menu1']])
                    self.menus['equip_select'] = 1
                    self.menus['sub_menu1'] = 0
                    self.menus['equip_selected'] = 'Empty'
                    self.current_menu_max = 10
                    in_Equip()
        
            def change_Equip_Display(text, pos):
                texttemp = text
                if texttemp == "Empty":
                    texttemp = "Unequip"
                equiprect = Rect(self.x_inc*7.2,self.y_inc*.7,self.x_inc*.5,self.y_inc*.5)
                equiptext = self.font.render(texttemp,True,white)
                equiptext_pos = equiptext.get_rect()
                equiptext_pos.left = equiprect.left
                equiptext_pos.top = equiprect.top
                equiptext_pos.centery = equiptext_pos.centery + (pos * self.y_inc*.5)
                self.image.blit(equiptext, equiptext_pos)
                if pos == self.menus['sub_menu1']:
                    equiptext_pos = equiptext_pos.inflate(4,4)
                    pygame.draw.rect(self.image,yellow,equiptext_pos,2)
                    self.menus['equip_selected'] = text
        
            def in_Magic():
                char = self.party.members[self.menus['char_select']]
            
                magicrect = Rect(self.x_inc*.5,self.y_inc*.5,self.x_inc*7,self.y_inc*9)
                self.image.fill(blue, magicrect)
                pygame.draw.rect(self.image,dkblue,magicrect,4)
                pygame.draw.line(self.image,dkblue,[self.x_inc*.5,self.y_inc*1.25],[self.x_inc*7.5,self.y_inc*1.25],2)
        
                for i, each in enumerate(['ALL','HEAL','ATT','UTIL']):
                    magic_Cat_Display(each, i)
            
                temp_magics = char.magic.perm_spells
                temp_magics_temp = char.magic.temp_spells
                temp_magics.update(temp_magics_temp)
            
                temp_magic = []
                for each in temp_magics:
                    temp = char.magic.get_Spell(each)['type']
                    try:
                        if self.menus['sub_menu0'] == 0 or temp in (['healing'],
                                                              ['damage'],
                                                              ['utility'])[self.menus['sub_menu0']-1]:
                            temp_magic.append(each)
                    except: continue
        
                self.menus['variable_menu'] = len(temp_magic)
        
                if self.menus['magic_select'] == 2:
                    self.current_menu_max = self.menus['variable_menu']
                    while self.menus['sub_menu1'] < self.menus['scroll_var']:
                        self.menus['scroll_var'] -= 2
                    while self.menus['sub_menu1'] > self.menus['scroll_var']+(self.menus['mag_scroll_cap']-1):
                        self.menus['scroll_var'] += 2
                temp_magic.sort()
                mindisplay = self.menus['scroll_var']
                maxdisplay = self.menus['scroll_var'] + (self.menus['mag_scroll_cap'])
                temp_magic = temp_magic[mindisplay:maxdisplay]
            
                for each in temp_magic:
                    magic_Text_Display(char, each, temp_magic.index(each))
                    
                pygame.draw.line(self.image,dkblue,[self.x_inc*4,self.y_inc*1.25],[self.x_inc*4,self.y_inc*8.5],2)
                pygame.draw.line(self.image,dkblue,[self.x_inc*.5,self.y_inc*8.5],[self.x_inc*7.5,self.y_inc*8.5],2)
                
                arrow_down = pygame.image.load('images/arrow_down.gif')
                arrow_down.set_colorkey([255,255,255])
                arrow_up = pygame.transform.flip(arrow_down,True,True)
                if self.menus['scroll_var'] > 0:
                    self.image.blit(arrow_up,[self.x_inc*3.9,self.y_inc*1.15])
                if self.menus['variable_menu'] > self.menus['scroll_var'] + self.menus['mag_scroll_cap']:
                    self.image.blit(arrow_down,[self.x_inc*3.9,self.y_inc*8.3])
            
            def magic_Cat_Display(text, pos):
                magic_rect = Rect(self.x_inc*.75, self.y_inc*.62, self.x_inc*.5, self.y_inc*.5)
                magic_text = self.font.render(text,True,white)
                magic_text_pos = magic_text.get_rect()
                magic_text_pos.centerx = magic_rect.centerx
                magic_text_pos.centery = magic_rect.centery
                magic_text_pos = magic_text_pos.move((pos * self.x_inc),0)
                self.image.blit(magic_text, magic_text_pos)
                if self.menus['magic_select'] == 2:
                    color_temp = red
                else:
                    color_temp = yellow
                if pos == self.menus['sub_menu0']:
                    magic_text_pos = magic_text_pos.inflate(4,4)
                    pygame.draw.rect(self.image,color_temp,magic_text_pos,2)
            
            def magic_Text_Display(char, text, pos):
                if char.magic.get_Spell(text)['type'] == "healing" and \
                    char.stats['curr']['mp'] >= char.magic.get_Spell(text)['cost']:
                    temp_color = white
                else:
                    temp_color = gray
            
                magic_rect = Rect(self.x_inc*.75, self.y_inc*1.4, self.x_inc*.5, self.y_inc*.5)
                magic_text = self.font.render(text,True,temp_color)
                magic_text_pos = magic_text.get_rect()
                magic_text_pos.centerx = magic_rect.centerx
                magic_text_pos.centery = magic_rect.centery
                magic_text_pos.left = magic_rect.left
                if is_Odd(pos+1):
                    magic_text_pos = magic_text_pos.move(0,(pos * self.y_inc*.25))
                else:
                    magic_text_pos = magic_text_pos.move(self.x_inc*3.5,((pos-1) * self.y_inc*.25))
                self.image.blit(magic_text, magic_text_pos)
                if pos == self.menus['sub_menu1']-self.menus['scroll_var'] and self.menus['magic_select'] == 2:
                    magic_text_pos = magic_text_pos.inflate(4,4)
                    pygame.draw.rect(self.image,yellow,magic_text_pos,2)
                    self.menus['magic_selected'] = text
                
                magic_amt = self.font.render(str(char.magic.get_Spell(text)['cost']),True,temp_color)
                magic_amt_pos = magic_text_pos.move(self.x_inc*2,0)
                self.image.blit(magic_amt, magic_amt_pos)
                
                if pos == self.menus['sub_menu1']-self.menus['scroll_var'] and self.menus['magic_select'] == 2:
                    desc_rect = Rect(self.x_inc*.75,self.y_inc*8.8,self.x_inc*7,self.y_inc)
                    desc_text = self.font.render("Description: "+str(char.magic.get_Spell(text)['desc']),True,white)
                    self.image.blit(desc_text,desc_rect)
        
            def use_Magic():
                char1 = self.party.members[self.menus['char_select2']]
                char2 = self.party.members[self.menus['char_select']]
                magic_temp = char2.magic.get_Spell(self.menus['magic_selected'])
            
                if magic_temp['type'] == 'healing':
                    for each in magic_temp['effect']:
                        if 'heal' in each:
                            if char2.stats['curr']['mp'] >= magic_temp['cost']:
                                if char1.stats['curr']['hp'] < char1.stats['curr']['maxhp']:
                                    char1.stats['curr']['hp'] += each['heal']
                                    char2.stats['curr']['mp'] -= magic_temp['cost']
                                    if char1.stats['curr']['hp'] > char1.stats['curr']['maxhp']:
                                        char1.stats['curr']['hp'] = char1.stats['curr']['maxhp']
                        elif 'revive' in each:
                            if char2.stats['curr']['mp'] >= magic_temp['cost']:
                                if char1.stats['curr']['hp'] == 0:
                                    char1.stats['curr']['hp'] = int(char1.stats['curr']['maxhp'] * (.01 * each['revive']))
                                    char2.stats['curr']['mp'] -= magic_temp['cost']
                if char2.stats['curr']['mp'] >= magic_temp['cost']:
                    self.menus['magic_select'] = 3
                else:
                    self.menus['magic_select'] = 2
                    self.current_menu_key = 'sub_menu1'
                    self.current_menu_type = 'xy_menu'
                    self.current_menu_max = self.menus['variable_menu']
        
            def in_Skills():
                char = self.party.members[self.menus['char_select']]
            
                skillrect = Rect(self.x_inc*.5,self.y_inc*.5,self.x_inc*7,self.y_inc*9)
                self.image.fill(blue, skillrect)
                pygame.draw.rect(self.image,dkblue,skillrect,4)
                pygame.draw.line(self.image,dkblue,[self.x_inc*.5,self.y_inc*1.25],[self.x_inc*7.5,self.y_inc*1.25],2)
                for i, v in enumerate(['Available Skills','All Known Skills']):
                    skill_Cat_Display(v, i)
            
                temp_skills = char.skills.useable
                temp_skills_temp = char.skills.learned
                temp_skills_temp.update(temp_skills)
            
                if self.menus['sub_menu0'] == 0:
                    temp_skill = temp_skills
                else:
                    temp_skill = temp_skills_temp
            
                self.menus['variable_menu'] = len(temp_skill)
                if self.menus['skill_select'] == 2:
                    self.current_menu_max = self.menus['variable_menu']
                    while self.menus['sub_menu1'] < self.menus['scroll_var']:
                        self.menus['scroll_var'] -= 2
                    while self.menus['sub_menu1'] > self.menus['scroll_var']+(self.menus['skill_scroll_cap']-1):
                        self.menus['scroll_var'] += 2
        
                sorted(temp_skill,key=temp_skill.get)
                mindisplay = self.menus['scroll_var']
                maxdisplay = self.menus['scroll_var'] + self.menus['skill_scroll_cap']
            
                index = 0
                view_index = 0
                for i, each in temp_skill.items():
                    if index >= mindisplay and index < maxdisplay:
                        skill_Text_Display(char, each, view_index)
                        view_index += 1
                    index += 1
                    
                pygame.draw.line(self.image,dkblue,[self.x_inc*4,self.y_inc*1.25],[self.x_inc*4,self.y_inc*8.5],2)
                pygame.draw.line(self.image,dkblue,[self.x_inc*.5,self.y_inc*8.5],[self.x_inc*7.5,self.y_inc*8.5],2)
                    
                arrow_down = pygame.image.load('images/arrow_down.gif')
                arrow_down.set_colorkey([255,255,255])
                arrow_up = pygame.transform.flip(arrow_down,True,True)
                if self.menus['scroll_var'] > 0:
                    self.image.blit(arrow_up,[self.x_inc*3.9,self.y_inc*1.15])
                if self.menus['variable_menu'] > self.menus['scroll_var'] + self.menus['skill_scroll_cap']:
                    self.image.blit(arrow_down,[self.x_inc*3.9,self.y_inc*8.3])
            
            def skill_Cat_Display(text, pos):
                if self.menus['skill_select'] == 1:
                    temp_color = yellow
                elif self.menus['skill_select'] == 2:
                    temp_color = red
                skill_rect = Rect(self.x_inc*1.2, self.y_inc*.62, self.x_inc*.5, self.y_inc*.5)
                skill_text = self.font.render(text,True,white)
                skill_text_pos = skill_text.get_rect()
                skill_text_pos.centerx = skill_rect.centerx
                skill_text_pos.centery = skill_rect.centery
                skill_text_pos = skill_text_pos.move((pos * self.x_inc*2),0)
                self.image.blit(skill_text, skill_text_pos)
                if pos == self.menus['sub_menu0']:
                    skill_text_pos = skill_text_pos.inflate(4,4)
                    pygame.draw.rect(self.image,temp_color,skill_text_pos,2)
            
            def skill_Text_Display(char, skill, pos):
                skill_rect = Rect(self.x_inc*.75, self.y_inc*1.4, self.x_inc*.5, self.y_inc*.5)
                skill_text = self.font.render(skill['name'],True,white)
                skill_text_pos = skill_text.get_rect()
                skill_text_pos.centerx = skill_rect.centerx
                skill_text_pos.centery = skill_rect.centery
                skill_text_pos.left = skill_rect.left
                if is_Odd(pos+1):
                    skill_text_pos = skill_text_pos.move(0,(pos * self.y_inc*.25))
                else:
                    skill_text_pos = skill_text_pos.move(self.x_inc*3.5,((pos-1) * self.y_inc*.25))
                self.image.blit(skill_text, skill_text_pos)
                if pos == self.menus['sub_menu1']-self.menus['scroll_var'] and self.menus['skill_select'] == 2:
                    skill_text_pos = skill_text_pos.inflate(4,4)
                    pygame.draw.rect(self.image,yellow,skill_text_pos,2)
            
                skill_type = self.font.render(skill['weapon'],True,white)
                skill_type_pos = skill_text_pos.move(self.x_inc*2.4,0)
                self.image.blit(skill_type, skill_type_pos)
                
                if pos == self.menus['sub_menu1']-self.menus['scroll_var'] and self.menus['skill_select'] == 2:
                    desc_rect = Rect(self.x_inc*.75,self.y_inc*8.8,self.x_inc*7,self.y_inc)
                    desc_text = self.font.render("Description: "+str(skill['desc']),True,white)
                    self.image.blit(desc_text,desc_rect)

            self.image.fill(blue, [self.x_inc*8, 0, self.x_inc*3, self.y_inc*10])
            pygame.draw.line(self.image,dkblue,[self.x_inc*8,0],[self.x_inc*8,self.y_inc*10],5)
            self._get_time()
    
            for i, v in enumerate(['Status','Items','Equip','Magic','Skills','Switch','Config']):
                menu_Text_Display(v, i)
    
            for each in range(0,4):
                char_Portrait_Display(each)
                if self.party.members[each]:
                    char_Text_Display(self.party.members[each], each)
    
            if self.menus['menu'] == 1 and self.menus['menu_select'] == 1:
                in_Status()
            if self.menus['menu'] == 2 and self.menus['item_select'] < 2:
                in_Items()
            if self.menus['menu'] == 2 and self.menus['item_select'] == 3:
                use_Items()
            if self.menus['menu'] == 3 and (0 < self.menus['equip_select'] < 3):
                in_Equip()
            if self.menus['menu'] == 3 and self.menus['equip_select'] > 1:
                change_Equip()
            if self.menus['menu'] == 4 and self.menus['magic_select'] == 4:
                use_Magic()
            if self.menus['menu'] == 4 and (0 < self.menus['magic_select'] < 3):
                in_Magic()
            if self.menus['menu'] == 5 and self.menus['skill_select'] > 0:
                in_Skills()

        elif self.ev_handler.overlay == 'shop':
            if self.menus['shop_select'] == 0:
                main_menu_rect = Rect(self.x_inc*4.5, self.y_inc*4.5, self.x_inc, self.current_menu_max*(self.y_inc*.5))
                self.image.fill(blue, main_menu_rect)
                pygame.draw.rect(self.image, dkblue, main_menu_rect, 4)
                for i, each in enumerate(['Buy', 'Sell']):
                    if self.menus['main_menu'] == i:
                        temp_color = yellow
                    else:
                        temp_color = white
                    var = self.font.render(each, True, temp_color)
                    var_rect = var.get_rect()
                    self.image.blit(var, (main_menu_rect.centerx-(var_rect.centerx-var_rect.left),
                                         ((main_menu_rect.top+self.y_inc*.1)+(i*(self.y_inc*.45)))))

            elif self.menus['shop_select'] == 4:
                def cancel_all():
                    self.menus['shop_selected_dict'] = {}
                    self.current_menu_key = 'sub_menu1'
                    self.current_menu_type = 'number_menu'
                    self.menus['sub_menu2'] = 0
                    self.menus['shop_select'] = 2

                if self.menus['menu'] == 1: #buy
                    if self.menus['sub_menu2'] == 0: #buy all!
                        for key, value in self.menus['shop_selected_dict'].items():
                            self.inventory.add_Item(key, value)
                        self.party.money = self.temp_money
                        cancel_all()
                    elif self.menus['sub_menu2'] == 2: #cancel all!
                        self.temp_money = self.party.money
                        cancel_all()
                    elif self.menus['sub_menu2'] == 1: #try out
                        self.menus['shop_select'] = 3 #to be added later

                elif self.menus['menu'] == 2: #sell
                    if self.menus['sub_menu2'] == 0: #sell all!
                        i = 0
                        for key, value in self.menus['shop_selected_dict'].items():
                            self.inventory.rem_Item(key, value)
                            if not self.inventory.has_Item(key):
                                i+=1
                        self.party.money = self.temp_money
                        if i > (self.menus['variable_menu']-(self.menus['sub_menu1']+1)):
                            self.menus['sub_menu1'] = self.menus['variable_menu']-(i+1)
                            self.menus['scroll_var'] -= i
                            if self.menus['scroll_var'] < 0: self.menus['scroll_var'] = 0
                        cancel_all()
                        if i == self.menus['variable_menu']:
                            self.menus['shop_selected_dict'] = {}
                            self.current_menu_key = 'sub_menu0'
                            self.current_menu_type = 'hor_menu'
                            self.current_menu_max = 5
                            self.menus['sub_menu1'] = 0
                            self.menus['sub_menu2'] = 0
                            self.menus['shop_select'] = 1
                            self.menus['variable_menu'] = 0
                            self.menus['scroll_var'] = 0
                        self.menus['variable_menu'] -= i
                    elif self.menus['sub_menu2'] == 1: #cancel all!
                        self.temp_money = self.party.money
                        cancel_all()

            if self.menus['shop_select'] > 0:
                buy_main_rect = Rect(self.x_inc*2, self.y_inc, self.x_inc*6, self.y_inc*8)
                self.image.fill(blue, buy_main_rect)
                pygame.draw.rect(self.image, dkblue, buy_main_rect, 4)
                pygame.draw.line(self.image, dkblue,
                                 (buy_main_rect.left, buy_main_rect.top+self.y_inc*3/4),
                                 (buy_main_rect.right, buy_main_rect.top+self.y_inc*.75), 2)
                for i, each in enumerate(['ALL','CONS','WEP','ARM','ACC']):
                    if self.menus['sub_menu0'] == i and self.menus['shop_select'] > 1:
                        temp_color = red
                    elif self.menus['sub_menu0'] == i:
                        temp_color = yellow
                    else:
                        temp_color = white
                    var = self.font.render(each, True, temp_color)
                    var_rect = var.get_rect()
                    self.image.blit(var, (buy_main_rect.left+((buy_main_rect.width/6)*(i+1))-(var_rect.centerx-var_rect.left),
                                          buy_main_rect.top+self.y_inc*3/8-(var_rect.centery-var_rect.top)))

                if self.menus['menu'] == 1: #buy
                    display_list = sorted(self.shop_items[self.menus['sub_menu0']],key=itemgetter('name'))
                elif self.menus['menu'] == 2: #sell
                    display_list = []
                    for key, value in self.inventory.items.items():
                        if self.menus['sub_menu0'] == 0 or items.get_Cat(key) == index_shop_cat[self.menus['sub_menu0']]:
                            display_list.append(dict({'name': key, 'value': items.get_Item(key)['value']}))
                    display_list = sorted(display_list,key=itemgetter('name'))
                self.menus['variable_menu'] = len(display_list)

                if self.menus['shop_select'] == 2:
                    self.current_menu_max = self.menus['variable_menu']

                if self.menus['sub_menu1'] < self.menus['scroll_var']:
                    self.menus['scroll_var'] = self.menus['sub_menu1']
                elif self.menus['sub_menu1'] > self.menus['scroll_var']+(self.menus['shop_scroll_cap']-1):
                    self.menus['scroll_var'] = self.menus['sub_menu1']-(self.menus['shop_scroll_cap']-1)

                min_display = self.menus['scroll_var']
                max_display = self.menus['scroll_var'] + (self.menus['shop_scroll_cap'])
                display_list = display_list[min_display:max_display]

                for i, each in enumerate(display_list):
                    if self.menus['menu'] == 1: #buy
                        if self.menus['shop_select'] > 1:
                            if self.menus['sub_menu1'] == i+min_display and self.temp_money >= int(each['value']):
                                temp_color = yellow
                            elif self.temp_money >= int(each['value']):
                                temp_color = white
                            else:
                                temp_color = dkgray
                        else:
                            if self.temp_money >= int(each['value']):
                                temp_color = white
                            else:
                                temp_color = dkgray
                    elif self.menus['menu'] == 2: #sell
                        if self.menus['shop_select'] > 1:
                            if self.menus['sub_menu1'] == i+min_display and self.inventory.get_Num_of_Item_Avail(each['name']) > self._get_num_of_shop_item(each['name']):
                                temp_color = yellow
                            elif self.inventory.get_Num_of_Item_Avail(str(each['name'])) > self._get_num_of_shop_item(str(each['name'])):
                                temp_color = white
                            else:
                                temp_color = dkgray
                        else:
                            if self.inventory.get_Num_of_Item_Avail(each['name']) > self._get_num_of_shop_item(each['name']):
                                temp_color = white
                            else:
                                temp_color = dkgray
                    if self.menus['sub_menu1'] == i+min_display:
                        self.menus['shop_selected'] = each['name']
                    var = self.font.render(str(each['name']), True, temp_color)
                    var_rect = var.get_rect()
                    inflated_var_rect = var_rect.inflate(buy_main_rect.width/50,buy_main_rect.height/50)
                    self.image.blit(var, (buy_main_rect.left+(buy_main_rect.width/24),
                                          buy_main_rect.top+self.y_inc+(buy_main_rect.height/13*(i))))
                    if self.menus['shop_select'] > 1 and self.menus['sub_menu1'] == i+min_display:
                        pygame.draw.rect(self.image, yellow, (buy_main_rect.left+(buy_main_rect.width/24)-((inflated_var_rect.width-var_rect.width)/2),
                                                              buy_main_rect.top+self.y_inc+(buy_main_rect.height/13*(i))-((inflated_var_rect.height-var_rect.height)/2),
                                                              inflated_var_rect.width,
                                                              inflated_var_rect.height),2)
                    var = self.font.render("x"+str(self._get_num_of_shop_item(each['name'])), True, temp_color)
                    var_rect = var.get_rect()
                    self.image.blit(var, (buy_main_rect.left+(buy_main_rect.width/12*5)-(var_rect.centerx-var_rect.left),
                                          buy_main_rect.top+self.y_inc+(buy_main_rect.height/13*(i))))
                    if self.menus['menu'] == 1: #buy
                        var_var = str(self.inventory.get_Num_of_Item(each['name']))
                    elif self.menus['menu'] == 2: #sell
                        var_var = str(self.inventory.get_Num_of_Item_Avail(each['name']))
                    var = self.font.render(var_var, True, temp_color)
                    var_rect = var.get_rect()
                    self.image.blit(var, (buy_main_rect.left+(buy_main_rect.width/12*8)-(var_rect.centerx-var_rect.left),
                                          buy_main_rect.top+self.y_inc+(buy_main_rect.height/13*(i))))
                    if self.menus['menu'] == 1: #buy
                        var_var = str(each['value'])
                    elif self.menus['menu'] == 2: #sell
                        var_var = str(int(each['value']/2))
                    var = self.font.render(var_var, True, temp_color)
                    var_rect = var.get_rect()
                    self.image.blit(var, (buy_main_rect.left+(buy_main_rect.width/12*11.5)-(var_rect.right-var_rect.left),
                                          buy_main_rect.top+self.y_inc+(buy_main_rect.height/13*(i))))

                pygame.draw.rect(self.image, dkblue,(buy_main_rect.left,
                                                     buy_main_rect.top+self.y_inc+(buy_main_rect.height/13*10),
                                                     buy_main_rect.width,
                                                     buy_main_rect.bottom-(buy_main_rect.top+self.y_inc+(buy_main_rect.height/13*10))),0)
                var = self.font.render("Gold: "+str(self.party.money), True, white)
                var_rect = var.get_rect()
                inflated_var_rect = var_rect.inflate(8,8)
                pygame.draw.rect(self.image, blue, (buy_main_rect.left+(buy_main_rect.width/24)-(var_rect.left-inflated_var_rect.left),
                                                    buy_main_rect.top+self.y_inc+(buy_main_rect.height/13*10.5)-(var_rect.top-inflated_var_rect.top),
                                                    inflated_var_rect.width,
                                                    inflated_var_rect.height))
                self.image.blit(var, (buy_main_rect.left+(buy_main_rect.width/24),
                                      buy_main_rect.top+self.y_inc+(buy_main_rect.height/13*10.5)))
                var = self.font.render("Remaining Gold: "+str(self.temp_money), True, white)
                var_rect = var.get_rect()
                inflated_var_rect = var_rect.inflate(8,8)
                pygame.draw.rect(self.image, blue, (buy_main_rect.right-(buy_main_rect.width/24)-(var_rect.right-var_rect.left)-(var_rect.left-inflated_var_rect.left),
                                                    buy_main_rect.top+self.y_inc+(buy_main_rect.height/13*10.5)-(var_rect.top-inflated_var_rect.top),
                                                    inflated_var_rect.width,
                                                    inflated_var_rect.height))
                self.image.blit(var, (buy_main_rect.right-(buy_main_rect.width/24)-(var_rect.right-var_rect.left),
                                      buy_main_rect.top+self.y_inc+(buy_main_rect.height/13*10.5)))

                if self.menus['shop_select'] == 3:
                    if self.menus['menu'] == 1: #buy
                        temp_menu_num = 3
                        temp_list = ['Buy All', 'Try On', 'Cancel All']
                    elif self.menus['menu'] == 2: #sell
                        temp_menu_num = 2
                        temp_list = ['Sell All', 'Cancel All']
                    oper_menu_rect = Rect(self.x_inc*8,
                                          self.y_inc*2,
                                          self.x_inc*1.5,
                                          self.y_inc*(temp_menu_num*.5))
                    self.image.fill(blue, oper_menu_rect)
                    pygame.draw.rect(self.image, dkblue, oper_menu_rect, 4)
                    for i, each in enumerate(temp_list):
                        if self.menus['sub_menu2'] == i:
                            temp_color = yellow
                        else:
                            temp_color = white
                        var = self.font.render(each, True, temp_color)
                        var_rect = var.get_rect()
                        self.image.blit(var, (oper_menu_rect.centerx-(var_rect.centerx-var_rect.left),
                                             ((oper_menu_rect.top+self.y_inc*.1)+(i*(self.y_inc*.45)))))