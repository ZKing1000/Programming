#!/usr/bin/env python
try:
    import pygame._view
except:
    pass
import levels, classes, overlay
import event, scroll, battle
import items, init, sound
import pygame
from pygame.locals import *
from constants import *

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

class Game(object):
    def __init__(self):
        self.window = pygame.display.get_surface()
        self.bg_manager = scroll.Background_Manager()
        self.font = pygame.font.Font(os.path.join('fonts','arial.ttf'), 16)
        self.sound = sound.sound()
        self.game_over = False
        self.new_game = 1
        self.clock=pygame.time.Clock()
        self.area = 1
        self.sub_area = 1
        self.pressed_list = [None, None, 0]

        #self.sound.play_music('opus.mp3')

    '''
    def change_resolution(self, resolution):
        pygame.display.set_mode(resolution)
        self.window = pygame.display.get_surface()
        self.bg_manager.set_screen(self.window)
        self.menu.set_screen(self.bg_manager.srcRect)
    '''

    def change_level(self):
        self.area = self.ev_handler.area
        self.sub_area = self.ev_handler.sub_area
        self.player, self.map_display, self.object_group, self.npc_group = \
            levels.load_level(self.window, self.area, self.sub_area, self.ev_handler, self.bg_manager)
        self.menu.set_screen(self.bg_manager.srcRect)
        self.map_display.add(self.menu)

    def new_game_start(self):
        inventory = classes.inventory()
        empty_char = classes.character(0, inventory, 'Empty', 'Empty', 'Empty', 'Empty', 'Empty', 'Empty')
        alex_char = classes.character(1, inventory, 'Alex Tramaugh', 'Male', 19, 'Human', 'Italy', 'Who knows?')
        rose_char = classes.character(2, inventory, 'Rose Langley', 'Female', 18, 'Human', 'Italy', 'Who knows?')
        #zach_char = classes.character(3, inventory, 'Zach Forlan', 'Male', 22, 'Human', 'Fenris Isle', 'Who knows?')
        hana_char = classes.character(4, inventory, 'Hana Tsukiyomi', 'Female', 20, 'Daedris', 'Mercanli Forest', 'Who knows?')
        init.inventory_Init(inventory)
        money = 20000
        self.party = classes.party([alex_char, rose_char, None, hana_char], inventory, money)
        init.magic_Init(self.party.members)
        for each in self.party.members:
            if each:
                each.gain_EXP(100000000)
        self.party.members[0].stats['curr']['hp'] = 5
        self.party.members[1].stats['curr']['mp'] = 80

        self.ev_handler = event.Event_Handler(self.party)
        self.menu = overlay.Overlay_Sprite(self.font, self.party, self.ev_handler)
        self.ev_handler.set_menu(self.menu)
        self.change_level()
        self.new_game = 0

    def input(self):
        if self.ev_handler.overlay and self.ev_handler.overlay == 'in_battle':
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.ev_handler.quit = True
                elif e.type == pygame.KEYDOWN:
                    self.battle_sprite.interface.control(e.key)
        elif self.ev_handler.overlay:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.ev_handler.quit = True
                elif e.type == pygame.KEYDOWN:
                    if e.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                        self.menu.move_select(e.key)
                    elif e.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                        self.menu.set_select(e.key)

        elif not self.ev_handler.curr_event_id:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.ev_handler.quit = True
                elif e.type == pygame.KEYDOWN:
                    self.pressed_list[0] = e.key
                    if e.key == pygame.K_END:
                        self.ev_handler.overlay = 'menu'
                    #elif e.key == pygame.K_HOME:
                    #    self.change_resolution([1024,768])
                    elif e.key == pygame.K_RETURN:
                        x, y = self.player.pos
                        d = self.player.direction
                        if self.object_group:
                            sprite = self.object_group.get_sprite((x+DX[d],y+DY[d]))
                            if sprite and not sprite.animation:
                                self.ev_handler.get_event(sprite)

        else:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.ev_handler.quit = True
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        self.ev_handler.curr_event_cont += 1

    def display(self):
        if self.player in self.map_display:
            self.map_display.bgMangr.NotifyPlayerSpritePos(self.player.rect)
        self.map_display.update()
        updates = self.map_display.draw(self.window)
        pygame.display.update(updates)
        self.clock.tick(40)

    def main(self):
        if self.new_game:
            self.new_game_start()
            self.new_game = 0

        while self.ev_handler.quit == False:
            pygame.display.set_caption('Tsuki no Sakura - FPS: %d' % self.clock.get_fps())

            if self.ev_handler.overlay == 'start_battle':
                self.battle_sprite = battle.in_Battle(self.font, self.ev_handler, self.party)
                self.map_display_temp = self.map_display
                self.map_display.empty()
                self.map_display.add(self.battle_sprite)
                self.ev_handler.overlay = 'in_battle'
            elif self.ev_handler.overlay == 'end_battle':
                self.map_display = self.map_display_temp
                self.map_display_temp = None
                self.ev_handler.overlay = None
            elif self.ev_handler.overlay != 'in_battle':
                if self.ev_handler.area != self.area or self.ev_handler.sub_area != self.sub_area:
                    self.change_level()
                elif self.ev_handler.overlay in ['menu','text_box','shop']:
                    if not self.menu.visible:
                        self.menu.set_visible(1)
                elif self.ev_handler.curr_event_id != 0:
                    self.ev_handler.get_event()
                else:
                    self.ev_handler.get_event()
                    if self.player.animation is None:
                        self.pressed_list = self.player.control(self.pressed_list, self.npc_group)
                    if self.npc_group:
                        for each in self.npc_group:
                            if each.animation is None and each.moveable and each.type == "npc":
                                each.auto_control()

            self.display()
            self.input()
        pygame.quit()

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_mode(DEF_SCREEN_SIZE)
    Game().main()