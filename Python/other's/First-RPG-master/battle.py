#!/usr/bin/env python
import classes, enemy, items
import pygame, math
from pygame.locals import *
from constants import *
from random import randint

class action():
    """A selected action to be performed by a character/enemy"""
    def __init__(self, name, action_type, object, owner):
        self.name = name
        self.action_type = action_type
        self.object = object
        self.owner = owner
        if self.object:
            self.target_type = self.object['target_type']
            self.target_limit = self.object['target_limit']
            self.target_default = self.object['target_default']

    def manual_target_type(self, target_type, target_limit, target_default):
        self.target_type = target_type
        self.target_limit = target_limit
        self.target_default = target_default

    def set_targets(self, target_group_1, target_group_2=None):
        self.targets = target_group_1
        if target_group_2:
            for each in target_group_2:
                self.targets.append(each)

    def execute(self):
        def add_to_list(text, type, target):
            text_dict = dict()
            text_dict['text'] = text
            text_dict['type'] = type
            text_dict['target'] = target
            text_list.append(text_dict)
        text_list = list()

        if self.targets:
            if self.action_type == 'attack':
                for target in self.targets:
                    if target:
                        damage = int(self.owner.char.stats['curr']['pow'] - (target.char.stats['curr']['def'] / 5))
                        if damage < 0:
                            damage = int(0)
                        elif damage > target.char.stats['curr']['hp']:
                            damage = int(target.char.stats['curr']['hp'])
                        target.char.stats['curr']['hp'] -= damage
                        add_to_list(damage, 'damage', target)
            elif self.action_type == 'item':
                for target in self.targets:
                    if target:
                        for each in self.object['effect']:
                            if 'heal hp' in each:
                                healing = int(each['heal hp'])
                                if healing > (target.char.stats['curr']['maxhp'] - target.char.stats['curr']['hp']):
                                    healing = int(target.char.stats['curr']['maxhp'] - target.char.stats['curr']['hp'])
                                target.char.stats['curr']['hp'] += healing
                                add_to_list(healing, 'healing', target)
                            if 'heal mp' in each:
                                healing = int(each['heal mp'])
                                if healing > (target.char.stats['curr']['maxmp'] - target.char.stats['curr']['mp']):
                                    healing = int(target.char.stats['curr']['maxmp'] - target.char.stats['curr']['mp'])
                                target.char.stats['curr']['mp'] += healing
                                add_to_list(healing, 'healing', target)
            elif self.action_type == 'magic':
                removed_cost = False
                for target in self.targets:
                    if target:
                        if not removed_cost and self.owner.char.stats['curr']['mp'] >= self.object['cost']:
                            self.owner.char.stats['curr']['mp'] -= self.object['cost']
                            removed_cost = True
                        if removed_cost:
                            amount = 0
                            modifier = (self.owner.char.stats['curr']['mpow'] / 10) - (target.char.stats['curr']['mdef'] / 100)

                            if self.object['type'] == 'damage':
                                for each_effect in self.object['effect']:
                                    for each_element in ['fire','ice','wind','lightning']:
                                        if each_element in each_effect:
                                            amount += (each_effect[each_element] * (1 + (self.owner.char.stats['curr']['m_'+str(each_element)] / 100))) * (1 - (target.char.stats['curr']['d_'+str(each_element)] / 100))
                                    if 'non-elemental' in each_effect:
                                        amount += each_effect['non-elemental']
                                damage = int(amount * modifier)
                                if damage >= 0:
                                    if damage > target.char.stats['curr']['hp']:
                                        damage = int(target.char.stats['curr']['hp'])
                                    add_to_list(damage, 'damage', target)
                                elif damage < 0:
                                    if damage < -1 * (target.char.stats['curr']['maxhp'] - target.char.stats['curr']['hp']):
                                        damage = int(-1 * (target.char.stats['curr']['maxhp'] - target.char.stats['curr']['hp']))
                                    add_to_list(damage, 'healing', target)
                                target.char.stats['curr']['hp'] -= damage

                            elif self.object['type'] == 'healing': #remember to add a case for undead later
                                for each_effect in self.object['effect']:
                                    if 'revive' in each_effect and target.status == 'dead':
                                        healing = int(target.char.stats['curr']['maxhp'] * (each_effect['revive'] / 100))
                                        target.char.stats['curr']['hp'] = healing
                                        target.status = 'active'
                                        add_to_list(healing, 'healing', target)
                                    elif 'heal' in each_effect:
                                        healing = int(each_effect['heal'] * (self.owner.char.stats['curr']['mpow'] / 10))
                                        if healing > target.char.stats['curr']['maxhp'] - target.char.stats['curr']['hp']:
                                            healing = int(target.char.stats['curr']['maxhp'] - target.char.stats['curr']['hp'])
                                        target.char.stats['curr']['hp'] += healing
                                        add_to_list(healing, 'healing', target)
        return text_list

class interface():
    """Controls the player/battle interface"""
    def __init__(self, font, battle_direction, ally_party, enemy_party, inventory):
        self.window = pygame.display.get_surface()
        self.font = font
        self.rect = self.window.get_rect()
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32).convert_alpha()
        self.x_inc, self.y_inc = self.rect.width/20, self.rect.height/20

        self.battle_direction = battle_direction
        self.ally_party = ally_party
        self.enemy_party = enemy_party
        self.inventory = inventory

        self._char_queue = list() #the active character queue
        self._selection_memory_bool = 1 #config stand-in to 'remember' selections

        self.selection_tier = 0 #selection objects used with control()
        self.selection_cap = None
        self.selection_type = None
        self.selection_memory = dict()
        for each in self.ally_party:
            self.selection_memory[each] = {
                'tier_0': 0,
                'tier_1': 0,
                'tier_1_scroll': 0,
                'tier_2': 0,
                'ally_targets': list(),
                'enemy_targets': list(),
                'target_group': None,
                'target_limit': None
            }

        self.action = None
        self.update_bool = True

    @property
    def char(self):
        """Get the character at the top of the queue"""
        return self._char_queue[0] if self._char_queue else None

    @char.setter
    def char(self, char):
        """Add a char to the char queue"""
        if char not in self._char_queue:
            self._char_queue.append(char)
            self.update_bool = True

    def check_queue_for_dead(self):
        temp_char = self.char
        del_list = list()
        for each in self._char_queue:
            if each.status in ['dead','frozen']:
                del_list.append(each)
        if del_list:
            for each in del_list:
                self._char_queue.remove(each)
            self.update_bool = True

    @char.deleter
    def char(self):
        """Remove the current char from the queue"""
        if self._char_queue:
            del self._char_queue[0]
            self.update_bool = True

    @property
    def is_skill_cat(self):
        return True if self.char.char.skills.useable else False

    @property
    def is_magic_cat(self):
        return True if self.char.char.magic.perm_spells or self.char.char.magic.temp_spells else False

    @property
    def is_item_cat(self):
        return True if self.item_list else False

    @property
    def skill_list(self):
        temp_list = list()
        for key, value in self.char.char.skills.useable.items():
            temp_list.append(key)
        temp_list.sort()
        return temp_list

    @property
    def skill_cap(self):
        return len(self.char.char.skills.useable)

    @property
    def magic_list(self):
        temp_char = self.char
        temp_list = list()
        for key, value in temp_char.char.magic.perm_spells.items():
            temp_list.append(key)
        for key, value in temp_char.char.magic.temp_spells.items():
            temp_list.append(key)
        temp_list.sort()
        return temp_list

    @property
    def magic_cap(self):
        return len(self.char.char.magic.temp_spells) + len(self.char.char.magic.perm_spells)

    @property
    def item_list(self):
        temp_list = list()
        for key, value in self.inventory.items.items():
            if items.get_Type(key) == "Consumable":
                temp_list.append(key)
        temp_list.sort()
        return temp_list

    @property
    def item_cap(self):
        return len(self.item_list)

    @property
    def battle_option_list(self):
        temp_list = list()
        temp_list = self.char.char.basic_battle_options
        temp_list.extend(self.char.char.advanced_battle_options)
        return temp_list

    @property
    def battle_option_cap(self):
        return len(self.char.char.advanced_battle_options) + 4

    @property
    def enemy_cap(self):
        return len(self.enemy_party)

    @property
    def time(self):
        return pygame.time.get_ticks()

    @property
    def time_str(self):
        """Get the current time in 00:00:00 string format"""
        time_temp = self.time
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
        return cur_time

    @property
    def living_allies(self):
        count = 0
        for each in self.ally_party:
            if each and each.status not in ['dead','frozen']:
                count += 1
        return count

    @property
    def living_enemies(self):
        count = 0
        for each in self.enemy_party:
            if each and each.status not in ['dead','frozen']:
                count += 1
        return count

    def check_targets(self, x=1):
        if self.action:
            temp_char = self.char
            if self.selection_memory[temp_char]['target_limit'] in ['single','mult']:
                if self.selection_memory[temp_char]['target_group'] in ['ally','enemy']:
                    if self.selection_memory[temp_char]['target_group'] == 'enemy':
                        if self.living_enemies > 0:
                            target_party = self.enemy_party
                            target_group = 'enemy_targets'
                            self.selection_cap = self.enemy_cap
                        elif self.action.target_limit == 'any':
                            self.selection_memory[temp_char]['target_group'] = 'ally'
                            self.selection_cap = 4
                        else:
                            self.set_selection(1)
                            return
                    if self.selection_memory[temp_char]['target_group'] == 'ally':
                        target_party = self.ally_party
                        target_group = 'ally_targets'
                        self.selection_cap = 4
                    if self.selection_memory[temp_char]['tier_2'] >= self.selection_cap:
                        self.selection_memory[temp_char]['tier_2'] -= self.selection_cap
                    elif self.selection_memory[temp_char]['tier_2'] < 0:
                        self.selection_memory[temp_char]['tier_2'] += self.selection_cap
                    res_object = False
                    if self.action.object:
                        for each_effect in self.action.object['effect']:
                            if 'revive' in each_effect:
                                res_object = True
                    if res_object:
                        while not target_party[self.selection_memory[temp_char]['tier_2']]:
                            self.selection_memory[temp_char]['tier_2'] += x
                            if self.selection_memory[temp_char]['tier_2'] >= self.selection_cap:
                                self.selection_memory[temp_char]['tier_2'] -= self.selection_cap
                            elif self.selection_memory[temp_char]['tier_2'] < 0:
                                self.selection_memory[temp_char]['tier_2'] += self.selection_cap
                    else:
                        while not target_party[self.selection_memory[temp_char]['tier_2']] or target_party[self.selection_memory[temp_char]['tier_2']].status == 'dead':
                            self.selection_memory[temp_char]['tier_2'] += x
                            if self.selection_memory[temp_char]['tier_2'] >= self.selection_cap:
                                self.selection_memory[temp_char]['tier_2'] -= self.selection_cap
                            elif self.selection_memory[temp_char]['tier_2'] < 0:
                                self.selection_memory[temp_char]['tier_2'] += self.selection_cap
                    self.selection_memory[temp_char][target_group] = list()
                    self.selection_memory[temp_char][target_group].append(target_party[self.selection_memory[temp_char]['tier_2']])

    def set_selection(self, tier=0):
        if tier < 0: tier = 0
        elif tier > 3: tier = 3
        if not self.char:
            self.selection_tier = 0
        else:
            temp_char = self.char
            previous_tier = self.selection_tier
            self.selection_tier = tier

            if tier == 0: #select action category (default)
                self.selection_cap = self.battle_option_cap
                self.selection_type = 'command_select'
    
            elif tier == 1: #select specific action
                action_type = self.battle_option_list[self.selection_memory[temp_char]['tier_0']]
                if action_type in ['attack', 'protect', 'steal']:
                    #essentially skip tier 1 for these commands, go straight to target
                    if previous_tier < tier:
                        self.set_selection(2)
                    else:
                        self.set_selection(0)
                elif action_type == 'magic':
                    self.selection_type = '4-way'
                    self.selection_cap = self.magic_cap
                elif action_type == 'skills':
                    self.selection_type = '4-way'
                    self.selection_cap = self.skill_cap
                elif action_type == 'items':
                    self.selection_type = '4-way'
                    self.selection_cap = self.item_cap
    
            elif tier == 2: #target
                action_type = self.battle_option_list[self.selection_memory[temp_char]['tier_0']]
                if action_type == 'attack':
                    self.action = action('attack','attack',None,temp_char)
                    self.action.manual_target_type('single','any','enemy')
                elif action_type == 'protect':
                    self.action = action('protect','protect',None,temp_char)
                    self.action.manual_target_type('all','ally','ally')
                elif action_type == 'steal':
                    self.action = action('steal','steal',None,temp_char)
                    self.action.manual_target_type('single','enemy','enemy')
                elif action_type == 'magic':
                    temp_spell = temp_char.char.magic.available[self.magic_list[self.selection_memory[temp_char]['tier_1']]]
                    self.action = action(temp_spell['name'],'magic',temp_spell,temp_char)
                elif action_type == 'skills':
                    temp_skill = temp_char.char.skills.useable[self.skill_list[self.selection_memory[temp_char]['tier_1']]]
                    self.action = action(temp_skill['name'],'skill',temp_skill,temp_char)
                elif action_type == 'items':
                    temp_item = items.get_Item(self.item_list[self.selection_memory[temp_char]['tier_1']])
                    self.action = action(temp_item['name'],'item',temp_item,temp_char)
                self.selection_memory[temp_char]['target_group'] = self.action.target_default
                if self.action.target_type in ['single','mult']:
                    self.selection_memory[temp_char]['target_limit'] = 'single'
                else:
                    self.selection_memory[temp_char]['target_limit'] = 'all'
                self.selection_type = 'target'
                self.check_targets(1)
    
            elif tier == 3: #execute
                if self.selection_memory[temp_char]['target_group'] == 'ally':
                    self.action.set_targets(self.selection_memory[temp_char]['ally_targets'])
                elif self.selection_memory[temp_char]['target_group'] == 'enemy':
                    self.action.set_targets(self.selection_memory[temp_char]['enemy_targets'])
                elif self.selection_memory[temp_char]['target_group'] == 'all':
                    self.action.set_targets(self.selection_memory[temp_char]['ally_targets'], self.selection_memory[temp_char]['enemy_targets'])
                self.char.action = self.action
                self.action = None
                del self.char
                self.set_selection()

    def control(self, input):
        def reset_selection(tier=0):
            '''Resets all memory beyond the current tier'''
            if tier == 0:
                self.selection_memory[self.char]['tier_1'] = 0
                self.selection_memory[self.char]['tier_1_scroll'] = 0
                self.selection_memory[self.char]['tier_2'] = 0
                self.selection_memory[self.char]['ally_target'] = 0
                self.selection_memory[self.char]['enemy_target'] = 0
            elif tier == 1:
                self.selection_memory[self.char]['tier_2'] = 0
                self.selection_memory[self.char]['ally_target'] = 0
                self.selection_memory[self.char]['enemy_target'] = 0

        def last_char():
            if len(self._char_queue) >= 2:
                last_char = self._char_queue.pop()
                self._char_queue.insert(0,last_char)
                self.set_selection()
                self.update_bool = True

        def next_char():
            if len(self._char_queue) >= 2:
                curr_char = self._char_queue.pop(0)
                self._char_queue.append(curr_char)
                self.set_selection()
                self.update_bool = True

        def switch_group(temp_char):
            if self.action.target_limit == 'any':
                if self.selection_memory[temp_char]['target_group'] == 'ally' and self.living_enemies > 0:
                    self.selection_memory[temp_char]['target_group'] = 'enemy'
                elif self.selection_memory[temp_char]['target_group'] == 'enemy':
                    self.selection_memory[temp_char]['target_group'] = 'ally'
                self.check_targets(1)

        if self.char:
            temp_char = self.char
            self.update_bool = True
            if not self.selection_type:
                self.set_selection()

            if input == 113: #'last char'- Q key
                if self.selection_tier in [0,1]:
                    last_char()
                    self.selection_tier = 0
                elif self.selection_tier == 2:
                    switch_group(temp_char)
            elif input == 101: #'next char'- E key
                if self.selection_tier in [0,1]:
                    next_char()
                    self.selection_tier = 0
                elif self.selection_tier == 2:
                    switch_group(temp_char)
            elif input in range(273, 277): #arrow keys-> up, down, right, left
                x = 0
                temp_cap = self.selection_cap

                if temp_cap > 1:
                    if self.selection_type == 'command_select':
                        if input == 273: x = -1
                        elif input == 274: x = 1
                        elif input == 275 and temp_cap > 4: x = 4
                        elif input == 276 and temp_cap > 4: x = -4
                        if x != 0:
                            reset_selection(0)
                            self.selection_memory[temp_char]['tier_0'] += x
                            if self.selection_memory[temp_char]['tier_0'] >= temp_cap:
                                self.selection_memory[temp_char]['tier_0'] -= temp_cap
                            elif self.selection_memory[temp_char]['tier_0'] < 0:
                                self.selection_memory[temp_char]['tier_0'] += temp_cap
                            if self.selection_memory[temp_char]['tier_0'] < 4: #the complicated stuff is just in the first column
                                while (temp_char.char.basic_battle_options[self.selection_memory[temp_char]['tier_0']] == 'magic' and not self.is_magic_cat) or \
                                      (temp_char.char.basic_battle_options[self.selection_memory[temp_char]['tier_0']] == 'skills' and not self.is_skill_cat) or \
                                      (temp_char.char.basic_battle_options[self.selection_memory[temp_char]['tier_0']] == 'items' and not self.is_item_cat):
                                    self.selection_memory[temp_char]['tier_0'] += pos_Neg(x)
                                    if self.selection_memory[temp_char]['tier_0'] > temp_cap:
                                        self.selection_memory[temp_char]['tier_0'] -= temp_cap
                                    elif self.selection_memory[temp_char]['tier_0'] < 0:
                                        self.selection_memory[temp_char]['tier_0'] += temp_cap

                    elif self.selection_type == '4-way':
                        if input == 273: x = -2
                        elif input == 274: x = 2
                        elif input == 275: x = 1
                        elif input == 276: x = -1
                        reset_selection(1)
                        self.selection_memory[temp_char]['tier_'+str(self.selection_tier)] += x
                        if self.selection_memory[temp_char]['tier_'+str(self.selection_tier)] >= temp_cap:
                            self.selection_memory[temp_char]['tier_'+str(self.selection_tier)] -= temp_cap
                        elif self.selection_memory[temp_char]['tier_'+str(self.selection_tier)] < 0:
                            self.selection_memory[temp_char]['tier_'+str(self.selection_tier)] += temp_cap

                    elif self.selection_type == 'target':
                        if self.selection_memory[temp_char]['target_limit'] == 'single':
                            if input == 273:
                                self.selection_memory[temp_char]['tier_2'] -= 1
                                if self.selection_memory[temp_char]['tier_2'] < 0:
                                    self.selection_memory[temp_char]['tier_2'] += self.selection_cap
                                self.check_targets(-1)
                            elif input == 274:
                                self.selection_memory[temp_char]['tier_2'] += 1
                                if self.selection_memory[temp_char]['tier_2'] > self.selection_cap:
                                    self.selection_memory[temp_char]['tier_2'] -= self.selection_cap
                                self.check_targets(1)

            elif input == 13: #return key
                selection_bool = False
                action_type = self.battle_option_list[self.selection_memory[temp_char]['tier_0']]
                if self.selection_tier == 0:
                    if action_type in ['attack','steal','protect']:
                        selection_bool = True
                    elif action_type == 'items' and self.item_cap > 0:
                        selection_bool = True
                    elif action_type == 'magic' and self.magic_cap > 0:
                        selection_bool = True
                    elif action_type == 'skills' and self.skill_cap > 0:
                        selection_bool = True
                elif self.selection_tier == 1:
                    if action_type in ['attack','steal','protect','items']:
                        selection_bool = True
                    elif action_type == 'magic':
                        spell = temp_char.char.magic.available[self.magic_list[self.selection_memory[temp_char]['tier_1']]]
                        if spell['cost'] <= temp_char.char.stats['curr']['mp']:
                            selection_bool = True
                    elif action_type == 'skills':
                        skill = temp_char.char.skills.useable[self.skill_list[self.selection_memory[temp_char]['tier_1']]]
                        if skill['cost'] <= temp_char.char.stats['curr']['energy']:
                            selection_bool = True
                elif self.selection_tier == 2:
                    if self.selection_memory[temp_char]['target_group'] == 'ally' and self.selection_memory[temp_char]['target_limit'] == 'single':
                        if self.selection_memory[temp_char]['ally_targets'] and self.selection_memory[temp_char]['ally_targets'][0] in self.ally_party:
                            selection_bool = True
                    elif self.selection_memory[temp_char]['target_group'] == 'enemy' and self.selection_memory[temp_char]['target_limit'] == 'single':
                        if self.selection_memory[temp_char]['enemy_targets'] and self.selection_memory[temp_char]['enemy_targets'][0] in self.enemy_party:
                            selection_bool = True
                if selection_bool:
                    self.set_selection(self.selection_tier+1)
            elif input == 27: #escape key
                self.set_selection(self.selection_tier-1)

    def update(self):
        def base_display():
            def vert_label(position, value, rect, count):
                text = self.font.render(value, True, white)
                text_rect = text.get_rect()
                width_inc = rect.width / (count*2)
                text_rect.centerx = rect.left + width_inc + (width_inc * 2 * position)
                text_rect.bottom = rect.top - (self.y_inc / 5)
                self.image.blit(text, text_rect)

            def hor_label(position, value, rect, count):
                text = self.font.render(value, True, white)
                text_rect = text.get_rect()
                height_inc = rect.height / (count*2)
                text_rect.right = rect.left - (self.x_inc / 5)
                text_rect.centery = rect.top + height_inc + (height_inc * 2 * position)
                self.image.blit(text, text_rect)

            def stat_bars(position, char, rect):
                width_inc = rect.width / 6
                height_inc = rect.height / 8
                for index in range(3):
                    if index == 0:
                        curr_stat = char.stats['curr']['hp']
                        max_stat = char.stats['curr']['maxhp']
                        stat_colour = dkgreen
                    elif index == 1:
                        curr_stat = char.stats['curr']['mp']
                        max_stat = char.stats['curr']['maxmp']
                        stat_colour = dkblue
                    elif index == 2:
                        curr_stat = char.stats['curr']['energy']
                        max_stat = 100
                        stat_colour = yellow
                    stat_percentage = curr_stat / max_stat
                    stat_rect = Rect(0, 0, rect.width / 4, rect.height / 8)
                    stat_rect.centerx = rect.left + width_inc + (width_inc * 2 * index)
                    stat_rect.centery = rect.top + height_inc + (height_inc * 2 * position)
                    curr_stat_rect = stat_rect.copy()
                    curr_stat_rect.width = curr_stat_rect.width * stat_percentage
                    if 0 < stat_percentage < 0.01:
                        curr_stat_rect.width = 1
                    self.image.fill(stat_colour, curr_stat_rect)

            self.image.fill(blue, Rect(0, self.y_inc*14.3, self.x_inc*20, self.y_inc*5.7))
            pygame.draw.line(self.image, dkblue, (0, self.y_inc*14.3), (self.x_inc*20, self.y_inc*14.3), 3)

            stat_box_rect = Rect(self.x_inc*12, self.y_inc*15.5, self.x_inc*7.5, self.y_inc*4)
            pygame.draw.rect(self.image, ltblue, stat_box_rect, 0)
            pygame.draw.rect(self.image, dkblue, stat_box_rect, 3)
            for i, each in enumerate(['HP', 'MP', 'EN']):
                vert_label(i, each, stat_box_rect, 3)
            for i, each in enumerate(self.ally_party):
                if each: #in case there isn't a char in that slot
                    hor_label(i, str.upper(each.char.first_Name()), stat_box_rect, 4)
                    stat_bars(i, each.char, stat_box_rect)

        def char_label():
            temp_char = self.char
            rect = Rect(self.x_inc*.5, self.y_inc*15.5, self.x_inc*6, self.y_inc*4)
            label_text = temp_char.char.first_Name()
            if self.selection_tier > 0:
                if self.battle_option_list[self.selection_memory[temp_char]['tier_0']] in ['magic', 'skills', 'items']:
                    label_text += " => " + str.upper(self.battle_option_list[self.selection_memory[temp_char]['tier_0']])
            if self.selection_tier > 1:
                label_text += " => " + str.upper(self.action.name)
            label = self.font.render(label_text, True, white)
            label_rect = label.get_rect()
            label_rect.left = rect.left + ((rect.centerx - rect.left) / 3)
            label_rect.bottom = rect.top - (self.y_inc / 5)
            self.image.blit(label, label_rect)

        def tier_zero_display():
            def display_actions(rect):
                #basic battle commands
                action_type = self.char.char.basic_battle_options
                for i, each in enumerate(action_type):
                    if i == 0 or (action_type[i] == 'magic' and self.is_magic_cat) or (action_type[i] == 'skills' and self.is_skill_cat) or (action_type[i] == 'items' and self.is_item_cat):
                        if i == self.selection_memory[self.char]['tier_0']:
                            action_colour = dkyellow
                        else:
                            action_colour = white
                        action = self.font.render(str.upper(each), True, action_colour)
                        action_rect = action.get_rect()
                        height_inc = rect.height / 8
                        action_rect.left = rect.left + (self.x_inc / 3)
                        action_rect.centery = rect.top + height_inc + (height_inc * 2 * i)
                        self.image.blit(action, action_rect)

                #advanced battle commands (if any)
                for i, each in enumerate(self.char.char.advanced_battle_options):
                    position = i+4
                    if position == self.selection_memory[self.char]['tier_0']:
                        action_colour = yellow
                    else:
                        action_colour = white
                    action = self.font.render(str.upper(each), True, action_colour)
                    action_rect = action.get_rect()
                    height_inc = rect.height / 8
                    action_rect.left = rect.centerx + (self.x_inc / 3)
                    action_rect.centery = rect.top + height_inc + (height_inc * 2 * i)
                    self.image.blit(action, action_rect)

            #the battle command rect (lower left corner)
            command_box_rect = Rect(self.x_inc*.5, self.y_inc*15.5, self.x_inc*6, self.y_inc*4)
            pygame.draw.rect(self.image, ltblue, command_box_rect, 0)
            pygame.draw.rect(self.image, dkblue, command_box_rect, 3)

            display_actions(command_box_rect)

        def tier_one_display():
            def display_options(rect):
                temp_char = self.char
                scroll_cap = 8
                curr_selection = self.selection_memory[temp_char]['tier_1']
                while curr_selection < self.selection_memory[temp_char]['tier_1_scroll']:
                    self.selection_memory[temp_char]['tier_1_scroll'] -= 2
                while curr_selection >= (self.selection_memory[temp_char]['tier_1_scroll'] + scroll_cap):
                    self.selection_memory[temp_char]['tier_1_scroll'] += 2
                curr_scroll = self.selection_memory[temp_char]['tier_1_scroll']
                option_cat = self.battle_option_list[self.selection_memory[temp_char]['tier_0']]

                if option_cat in ['magic','skills']:
                    if option_cat == 'magic':
                        option_list = self.magic_list[curr_scroll:curr_scroll + scroll_cap]
                        option_info = temp_char.char.magic.available
                        option_pool = temp_char.char.stats['curr']['mp']
                        option_cap = self.magic_cap
                    elif option_cat == 'skills':
                        option_list = self.skill_list[curr_scroll:curr_scroll + scroll_cap]
                        option_info = temp_char.char.skills.useable
                        option_pool = temp_char.char.stats['curr']['energy']
                        option_cap = self.skill_cap

                    for i, each in enumerate(option_list):
                        if option_pool >= option_info[each]['cost']:
                            if curr_selection == curr_scroll + i:
                                temp_colour = yellow
                            else:
                                temp_colour = white
                        else:
                            if curr_selection == curr_scroll + i:
                                temp_colour = dkyellow
                            else:
                                temp_colour = dkgray
                        option_row = round((i+1) / 2 + .01)
                        option_text = self.font.render(str(option_info[each]['name']), True, temp_colour)
                        option_rect = option_text.get_rect()
                        height_inc = rect.height / 5
                        option_rect.centery = rect.top + height_inc * option_row
                        if not is_Odd(i):
                            option_rect.left = rect.left + self.x_inc/2
                        else:
                            option_rect.left = rect.centerx + self.x_inc/2
                        self.image.blit(option_text, option_rect)
                        
                        cost_text = self.font.render(str(option_info[each]['cost']), True, temp_colour)
                        cost_rect = cost_text.get_rect()
                        cost_rect.centery = rect.top + height_inc * option_row
                        if not is_Odd(i):
                            cost_rect.right = rect.centerx - self.x_inc/2
                        else:
                            cost_rect.right = rect.right - self.x_inc/2
                        self.image.blit(cost_text, cost_rect)

                elif option_cat == 'items':
                    option_list = self.item_list
                    option_info = self.inventory.items
                    option_cap = self.item_cap

                    for i, each in enumerate(option_list):
                        if curr_selection == curr_scroll + i:
                            temp_colour = yellow
                        else:
                            temp_colour = white
                        option_row = round((i+1) / 2 + .01)
                        option_text = self.font.render(str(each), True, temp_colour)
                        option_rect = option_text.get_rect()
                        height_inc = rect.height / 5
                        option_rect.centery = rect.top + height_inc * option_row
                        if not is_Odd(i):
                            option_rect.left = rect.left + self.x_inc/2
                        else:
                            option_rect.left = rect.centerx + self.x_inc/2
                        self.image.blit(option_text, option_rect)
                        
                        cost_text = self.font.render(str(option_info[each]), True, temp_colour)
                        cost_rect = cost_text.get_rect()
                        cost_rect.centery = rect.top + height_inc * option_row
                        if not is_Odd(i):
                            cost_rect.right = rect.centerx - self.x_inc/2
                        else:
                            cost_rect.right = rect.right - self.x_inc/2
                        self.image.blit(cost_text, cost_rect)

            #the battle command rect (lower left corner)
            option_box_rect = Rect(self.x_inc*.5, self.y_inc*15.5, self.x_inc*9, self.y_inc*4)
            pygame.draw.rect(self.image, ltblue, option_box_rect, 0)
            pygame.draw.rect(self.image, dkblue, option_box_rect, 3)

            display_options(option_box_rect)

        def tier_two_display():
            temp_char = self.char
            if self.selection_memory[temp_char]['target_group'] in ['ally','all']:
                for each in self.ally_party:
                    if each in self.selection_memory[temp_char]['ally_targets']:
                        pygame.draw.rect(self.image,yellow,each.rect,1)
            if self.selection_memory[temp_char]['target_group'] in ['enemy','all']:
                for each in self.enemy_party:
                    if each in self.selection_memory[temp_char]['enemy_targets']:
                        pygame.draw.rect(self.image,yellow,each.rect,1)

        if self.update_bool == True:
            self.update_bool = False
            self.check_queue_for_dead()
            self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32).convert_alpha()
            base_display()

            if self.char:
                char_label()
                if self.selection_tier == 0: #select action type (attack, skill, etc)
                    tier_zero_display()
                elif self.selection_tier == 1: #select specific action
                    tier_one_display()
                elif self.selection_tier == 2: #select target
                    tier_two_display()

class ally():
    """Each member of the ally group"""
    def __init__(self, index, char, battle_direction, window_rect):
        #basic assignments, initializations
        self.char = char
        self.index = index
        self.direction = 0
        self.status = None
        self.action = None #action object
        self.action_points = randint(500,1000)

        #tilesets
        self.move_tileset = TALL_SPRITE_CACHE['player_'+str(self.char.index)+'_sprite_sheet.png']
        self.stand_tileset = list((list((self.move_tileset[0][1], self.move_tileset[0][2])), list((self.move_tileset[0][1], self.move_tileset[0][2]))))
        self.attack_tileset = TALL_SPRITE_CACHE['player_'+str(self.char.index)+'_attack_sprite_sheet.png']
        self.cast_tileset = list((self.attack_tileset[1][1], self.attack_tileset[1][2]))
        self.knockback_tileset = list()
        self.dead_tileset = TALL_SPRITE_CACHE['tombstone.bmp']

        #image/rect and origin/cast points
        self.image = self.stand_tileset[0][self.direction]
        self.image.set_colorkey(white)
        self.rect = Rect(0,0,32,64)
        self.hitbox = Rect(0,0,32,32)
        x_inc, y_inc = window_rect.width / 20, window_rect.height / 20
        self.rect.center = (x_inc*16+(index*x_inc*.5), y_inc*8+(index * y_inc))
        self.hitbox.center = self.rect.center
        self.origin = self.rect.copy()
        if battle_direction == 0:
            self.cast_point = self.rect.move(-x_inc,0)
        else:
            self.cast_point = self.rect.move(x_inc,0)
        self._animation_queue = list()

        #animation info
        self.x, self.y = float(self.rect.centerx), float(self.rect.bottom)
        self.animation_direction = self.direction #direction of animation
        self.animation_frame = 0 #current frame of animation
        self.animation_start = None #start time for animation, for timing executions
        self.animation_timer = None #last animation update

        #if alive, stand in start point, or if dead, be a corpse
        if self.char.stats['curr']['hp'] < 1:
            self.animation_queue = self.dead_animation
        else:
            self.animation_queue = self.stand_animation

    @property
    def animation_queue(self):
        """Get the current animation"""
        if self._animation_queue:
            return self._animation_queue[0]
        else:
            return None

    @animation_queue.setter
    def animation_queue(self, animation):
        """Add to the top of the animation queue"""
        self._animation_queue.insert(0, animation)

    @animation_queue.deleter
    def animation_queue(self):
        """Remove the current animation from the queue"""
        if self._animation_queue:
            self.reset_animation()
            del self._animation_queue[0]

    def reset_animation(self):
        self.animation_start = None
        self.animation_timer = None
        self.animation_frame = 0
        self.animation_direction = self.direction

    def move_to_cast_animation(self):
        if self.rect.centerx < self.cast_point.centerx:
            self.animation_direction = 2
        else:
            self.animation_direction = 1

        if not self.animation_timer:
            self.animation_timer = pygame.time.get_ticks()
            self.image = self.move_tileset[0][self.animation_direction]
            self.status = 'moving'
        elif pygame.time.get_ticks() >= self.animation_timer + 200: #.2 seconds
            if len(self.move_tileset) <= self.animation_frame+1:
                self.animation_frame = 0
            else:
                self.animation_frame += 1
            self.image = self.move_tileset[self.animation_frame][self.animation_direction]

        x1, y1 = self.x, self.y
        x2, y2 = self.cast_point.midbottom
        angle = math.atan2(y2-y1,x2-x1)
        self.x += 2*math.cos(angle)
        self.y += 2*math.sin(angle)
        self.rect.midbottom = (int(self.x), int(self.y))
        if (self.rect.bottom - self.cast_point.bottom) in range(-2,2) and (self.rect.centerx - self.cast_point.centerx) in range(-2,2):
            self.rect.midbottom = self.cast_point.midbottom
            self.x, self.y = float(self.rect.centerx), float(self.rect.bottom)
            del self.animation_queue

    def move_to_target_animation(self):
        if self.rect.centerx < self.action.targets[0].hitbox.centerx:
            self.animation_direction = 2
        else:
            self.animation_direction = 1

        if not self.animation_timer:
            self.animation_timer = pygame.time.get_ticks()
            self.image = self.move_tileset[0][self.animation_direction]
            self.status = 'moving'
        elif pygame.time.get_ticks() >= self.animation_timer + 200: #.2 seconds
            if len(self.move_tileset) <= self.animation_frame+1:
                self.animation_frame = 0
            else:
                self.animation_frame += 1
            self.image = self.move_tileset[self.animation_frame][self.animation_direction]

        if self.action.targets[0] == self:
            del self.animation_queue
        elif self.rect.colliderect(self.action.targets[0].hitbox):
            del self.animation_queue
        else:
            x1, y1 = self.x, self.y
            x2, y2 = self.action.targets[0].hitbox.center
            angle = math.atan2(y2-y1,x2-x1)
            self.x += 2*math.cos(angle)
            self.y += 2*math.sin(angle)
            self.rect.midbottom = (int(self.x), int(self.y))
            if self.rect.colliderect(self.action.targets[0].hitbox):
                del self.animation_queue

    def move_to_origin_animation(self):
        if self.rect.centerx < self.origin.centerx:
            self.animation_direction = 2
        else:
            self.animation_direction = 1

        if not self.animation_timer:
            self.animation_timer = pygame.time.get_ticks()
            self.image = self.move_tileset[0][self.animation_direction]
            self.status = 'moving'
        elif pygame.time.get_ticks() >= self.animation_timer + 200: #.2 seconds
            if len(self.move_tileset) <= self.animation_frame+1:
                self.animation_frame = 0
            else:
                self.animation_frame += 1
            self.image = self.move_tileset[self.animation_frame][self.animation_direction]

        x1, y1 = self.x, self.y
        x2, y2 = self.origin.midbottom
        angle = math.atan2(y2-y1,x2-x1)
        self.x += 2*math.cos(angle)
        self.y += 2*math.sin(angle)
        self.rect.midbottom = (int(self.x), int(self.y))
        if (self.rect.bottom - self.origin.bottom) in range(-2,2) and (self.rect.centerx - self.origin.centerx) in range(-2,2):
            self.rect.midbottom = self.origin.midbottom
            self.x, self.y = float(self.rect.centerx), float(self.rect.bottom)
            del self.animation_queue

    def stand_animation(self):
        if self.status not in ['standing','waiting']:
            self.status = 'standing'
        self.image = self.stand_tileset[0][self.direction]

    def attack_animation(self):
        if self.rect.centerx < self.action.targets[0].rect.centerx:
            self.animation_direction = 2
        else:
            self.animation_direction = 1

        if not self.animation_start:
            self.animation_start = pygame.time.get_ticks()
            self.animation_timer = self.animation_start
            self.image = self.attack_tileset[self.animation_frame][self.animation_direction]
            self.status = 'start attack'
        else:
            if pygame.time.get_ticks() >= self.animation_timer + 250:
                if len(self.attack_tileset) <= self.animation_frame+1:
                    self.animation_frame = 0
                else:
                    self.animation_frame += 1
                self.image = self.attack_tileset[self.animation_frame][self.animation_direction]
                self.animation_timer = pygame.time.get_ticks()
        if pygame.time.get_ticks() >= self.animation_start + 700:
            del self.animation_queue

    def cast_animation(self):
        if not self.animation_start:
            self.animation_start = pygame.time.get_ticks()
            self.animation_timer = self.animation_start
            self.image = self.cast_tileset[self.direction]
            self.status = 'start cast'
        else:
            if self.animation_timer + 200 <= pygame.time.get_ticks():
                if len(self.cast_tileset) <= self.animation_frame+1:
                    self.animation_frame = 0
                else:
                    self.animation_frame += 1
                self.image = self.cast_tileset[self.direction]
                self.animation_timer = pygame.time.get_ticks()
        if pygame.time.get_ticks() >= self.animation_start + 1000: #1 second
            del self.animation_queue

    def execute_animation(self):
        '''
        if not self.animation_start:
            self.animation_start = pygame.time.get_ticks()
            self.animation_timer = self.animation_start
            self.status = 'start execute'
        else:
            if self.animation_timer + 200 <= pygame.time.get_ticks():
                if len(self.cast_tileset) <= self.animation_frame+1:
                    self.animation_frame = 0
                else:
                    self.animation_frame += 1
                self.image = self.cast_tileset[self.direction]
                self.animation_timer = pygame.time.get_ticks()
        '''
        self.status = 'execute'

    def knockback_animation(self):
        self.status = 'knockback'

    def frozen_animation(self):
        self.status = 'frozen'

    def dead_animation(self):
        self.status = 'dead'
        self.image = self.dead_tileset[0][0]
        self.image.set_colorkey(white)

    def update(self, time): #work in progress
        if self.char.stats['curr']['hp'] < 1:
            self.animation_queue = self.dead_animation()
        else:
            if self.action and self.status == 'waiting':
                if self.action.action_type in ['attack','steal'] or (self.action.action_type == 'skill' and self.action.object['type'] in ['damage','debuff']):
                    self.status = 'acting'
                    self.animation_queue = self.stand_animation
                    self.animation_queue = self.move_to_origin_animation
                    self.animation_queue = self.execute_animation
                    self.animation_queue = self.attack_animation
                    self.animation_queue = self.move_to_target_animation
                elif self.action.action_type in ['magic','item'] or (self.action.action_type == 'skill' and self.action.object['type'] in ['heal','buff']):
                    self.status = 'acting'
                    self.animation_queue = self.stand_animation
                    self.animation_queue = self.move_to_origin_animation
                    self.animation_queue = self.execute_animation
                    self.animation_queue = self.cast_animation
                    self.animation_queue = self.move_to_cast_animation
            if self.animation_queue:
                self.animation_queue()
            elif self.rect != self.origin:
                self.animation_queue = self.stand_animation
                self.animation_queue = self.move_to_origin_animation
            else:
                self.animation_queue = self.stand_animation
            self.image.set_colorkey(white)

class animation():
    """Each special effect animation displayed"""
    def __init__(self, sheet, target):
        self.active = True
        self.start_time = pygame.time.get_ticks()
        self.last_frame = self.start_time
        self.current_frame = 0
        caches = [SHORT_EFFECT_CACHE, TALL_EFFECT_CACHE, LARGE_EFFECT_CACHE]
        #self.sheet = caches[size][str(sheet)+"_animation.bmp"]
        if sheet == 'cast':
            self.sheet = caches[0]['cast_animation.bmp']
            self.frame_length = 6
        elif sheet == 'action':
            self.sheet = caches[2]['explode_animation.bmp']
            self.frame_length = 7
        self.image = self.sheet[0][0]
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.target = target
        self.rect.midbottom = self.target.rect.midbottom
        self.time_inc = 1000 / self.frame_length #1 second spells

    def advance_animation(self):
        self.current_frame += 1
        self.last_frame = pygame.time.get_ticks()
        if self.current_frame >= self.frame_length:
            self.active = False

    def update(self):
        if self.active:
            self.rect.center = self.target.rect.center
            self.image = self.sheet[self.current_frame][0]
            self.image.set_colorkey(white)
            if self.last_frame + self.time_inc <= pygame.time.get_ticks():
                self.advance_animation()

class text_animation():
    """Each text-display animation displayed"""
    def __init__(self, object, font):
        self.active = True
        self.start_time = pygame.time.get_ticks()
        self.last_frame = self.start_time
        self.current_frame = 0
        self.frame_length = 8
        if object['type'] == 'damage':
            temp_colour = red
        elif object['type'] == 'healing':
            temp_colour = green
        else:
            temp_colour = white
        self.image = font.render(str(object['text']), True, temp_colour)
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.target = object['target']
        self.rect.midbottom = self.target.rect.midbottom
        self.time_inc = 1000 / self.frame_length #1 second duration

    def advance_animation(self):
        self.current_frame += 1
        self.rect.move_ip(0,-10)
        self.last_frame = pygame.time.get_ticks()
        if self.current_frame >= self.frame_length:
            self.active = False

    def update(self):
        if self.active:
            if self.last_frame + self.time_inc <= pygame.time.get_ticks():
                self.advance_animation()

class in_Battle(pygame.sprite.DirtySprite):
    """The sprite that controls the overall battle system"""
    def __init__(self, font, ev_handler, party):
        pygame.sprite.DirtySprite.__init__(self)
        self.window = pygame.display.get_surface()
        self.font = font
        self.ev_handler = ev_handler
        self._layer = 0
        self.elevation = 0
        self.depth = 0
        self.dirty = 2

        self.rect = self.window.get_rect()
        self.image = pygame.Surface(self.rect.size)

        self.party = party
        self.inventory = party.inventory
        self._set_battle_vars()
        self._set_party()
        self._set_enemy()

        self.interface = interface(self.font, self.battle_direction, self.ally_party, self.enemy_party, self.inventory)
        self.animations = list()

    #for things such as direction of combat
    def _set_battle_vars(self):
        #if randint(0,100) > 90: self.battle_direction = 1
        #else: self.battle_direction = 0
        self.battle_direction = 0
        if self.ev_handler.area == 1 and self.ev_handler.sub_area == 1:
            image_name = 'dunes.png'
        else:
            image_name = 'dunes.png'
        try:
            self.battle_bg = pygame.transform.smoothscale(pygame.image.load(os.path.join('images',image_name)).convert(),
                                                          (self.rect.width, int(self.rect.height*.75)))
        except:
            print('Cannot load background image')
            pygame.quit()

    def _set_party(self):
        self.ally_party = list()
        for index, each in enumerate(self.party.members):
            if each:
                each.set_battle_options()
                self.ally_party.append(ally(index, each, self.battle_direction, self.rect))
            else:
                self.ally_party.append(None)

    def _set_enemy(self):
        self.enemy_party = list()

    def execute(self, char):
        if char.status == 'standing':
            char.action_points -= char.char.stats['curr']['spd'] / 8
            if char.action_points <= 0:
                char.action_points = 0
                self.interface.char = char
                self.interface.update_bool = True
                char.status = 'waiting'
        elif char.status == 'start cast':
            self.animations.append(animation('cast',char))
            char.status = 'casting'
        elif char.status == 'execute':
            if char.action.action_type == 'magic' and char.action.object['type'] == 'damage':
                for target in char.action.targets:
                    self.animations.append(animation('action', target))
            text_list = char.action.execute()
            for each in text_list:
                self.animations.append(text_animation(each, self.font))
            if char.action.action_type == 'item':
                self.inventory.rem_Item(char.action.object['name'],1)
            char.action = None
            del char.animation_queue
            self.interface.update_bool = True

    def effect_tick(self):
        pass

    def update(self):
        self.image.blit(self.battle_bg, self.rect)
        for each in self.ally_party:
            if each:
                each.update(self.interface.time)
                self.execute(each)
                self.image.blit(each.image, each.rect)

        for each in self.enemy_party:
            pass

        del_list = list()
        for each in self.animations:
            if each.active:
                each.update()
                self.image.blit(each.image, each.rect)
            else:
                del_list.append(each)
        for each in del_list:
            self.animations.remove(each)

        self.interface.update()
        self.image.blit(self.interface.image, self.rect)