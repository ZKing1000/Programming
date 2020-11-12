import pygame
import os
import ConfigParser
import random
from pygame.locals import *

import data
import renderer
import gamelib


def MessageBox(heading = 'Pause Menu', items = ['Esc to Continue', 'Enter to Main Menu'], color = (255, 255, 255)):
    headFont = pygame.font.Font(data.filepath('deftone.ttf'), 100)
    bodyFont = pygame.font.Font(pygame.font.get_default_font(), 20)
    surf = pygame.surface.Surface((700, 500)).convert_alpha()
    surf.set_alpha(40)

    head = headFont.render(heading, True, color)
    x = surf.get_size()[0]/2 - head.get_size()[0]/2
    y = 0
    surf.blit(head,(x, y))

    i = 1
    for item in items:
        surf.blit(bodyFont.render(item, True, color), (x, i * 40 + 110)) 
        i+= 1
    pygame.draw.rect(surf, color, surf.get_rect(), 2)
    renderer.drawImage(surf, (50, 50))

    pygame.display.flip()
    while 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return 'continue'
                elif event.key == K_RETURN:
                    return 'newlvl'
                        
class MenuItem:
    font = pygame.font.Font(data.filepath('deftone.ttf'), 30)
    def __init__(self, pos = (0, 0), text = 'fix this', img = None, enabled=True):
        self.x = pos[0]
        self.y = pos[1]
        self.image = img
        self.text = text
        self.isEnabled = enabled
        txt = self.font.render(self.text.upper(), True, (255, 255, 255))
        rect = self.image.get_rect()
        txtrect = txt.get_rect()
        self.image.blit(txt, (rect[2]/2 - txtrect[2]/2, rect[3]-txtrect[3]))

    def isPosOver(self, pos = (0, 0)):
        if self.x < pos[0] and  self.x+self.image.get_size()[0] > pos[0]:
            if self.y < pos[1] and self.y + self.image.get_size()[1] > pos[1]:
                return True
        return False

    def render(self, highlight = False):
        rect = self.image.get_rect()
        if highlight :
            pygame.draw.rect(self.image, (0, 255, 0), rect, 2) 
        else:
            pygame.draw.rect(self.image, (255, 255, 255), rect, 2) 

        renderer.drawImage(self.image, (self.x, self.y))


class Menu:
    levels = []
    def __init__(self):
        files = os.listdir(data.data_dir)
        files.sort()
        self.isDone = False
        self.items = []
        tmp = []
        i = 0
        data_font = pygame.font.Font(pygame.font.get_default_font(), 15)
        title_font = pygame.font.Font(data.filepath('deftone.ttf'), 100)
        self.title = title_font.render('deFeather', True, random.choice(gamelib.colors))
        for file in files:
            if file.endswith('.txt'):
                #print file
                fp = open(data.filepath(file))
                parser = ConfigParser.ConfigParser()
                parser.readfp(fp)
                fp.close()
                #get the icon data from lvl file
                buildings = []
                #/4 for all the values
                image = pygame.surface.Surface((200, 150))
                baseLine = 120
                #if stored score > 0 then color the previews
                score = parser.getint('score', 'maxscore')  
                time = parser.getint('time', 'best')
                if parser.has_section('b2'):
                    xcoords = parser.get('b2', 'x').split(',')
                    w = 118/4
                    h = 375/4
                    for x in xcoords:
                        if score > 0:
                            pygame.draw.rect(image, random.choice(gamelib.colors), (int(x)/4, baseLine-h, w, h)) 
                        else:
                            pygame.draw.rect(image, (255, 255, 255), (int(x)/4, baseLine-h, w, h)) 


                if parser.has_section('b4'):
                    xcoords = parser.get('b4', 'x').split(',')
                    w = 227/4
                    h = 306/4
                    for x in xcoords:
                        if score > 0:
                            pygame.draw.rect(image, random.choice(gamelib.colors), (int(x)/4, baseLine-h, w, h))
                        else:
                            pygame.draw.rect(image, (255, 255, 255), (int(x)/4, baseLine-h, w, h))

                if parser.has_section('b3'):
                    xcoords = parser.get('b3', 'x').split(',')
                    w = 188/4
                    h = 185/4
                    for x in xcoords:
                        if score > 0:
                            pygame.draw.rect(image, random.choice(gamelib.colors), (int(x)/4, baseLine-h, w, h))
                        else:
                            pygame.draw.rect(image, (255, 255, 255), (int(x)/4, baseLine-h, w, h))

                if parser.has_section('b5'):
                    xcoords = parser.get('b5', 'x').split(',')
                    w = 160/4
                    h = 165/4
                    for x in xcoords:
                        if score > 0:
                            pygame.draw.rect(image, random.choice(gamelib.colors), (int(x)/4, baseLine-h, w, h))
                        else:
                            pygame.draw.rect(image, (255, 255, 255), (int(x)/4, baseLine-h, w, h))

                text = file
                pos = ((i%3)*220 + 80 , i/3 * 160 + 100 )
                enabled = True
                tmp = data_font.render('score: '+score.__str__(), True, (255, 255, 255))
                image.blit(tmp, (2, 2))
                tmp = data_font.render('time: '+time.__str__(), True, (255, 255, 255))
                image.blit(tmp, (2, 17))
                self.items.append(MenuItem(pos, text, image))
                Menu.levels.append(text)
                i += 1
                

    def show(self):
        if gamelib.hasSounds:
            pygame.mixer.music.stop()

        while not(self.isDone):
            renderer.clearScreen()
            txt = None
            isItemEnabled = False
            tsize = self.title.get_size()
            tx = renderer.getWidth()/2 - tsize[0]/2
            ty = 0
            renderer.drawImage(self.title, (tx, ty))
            for item in self.items:
                val = item.isPosOver(pygame.mouse.get_pos())
                item.render(val)
                if val:
                    txt = item.text
                    isItemEnabled = True

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.isDone = True
                        print 'exiting....'
                        return 'exit'
                if event.type == MOUSEBUTTONDOWN and isItemEnabled == True:
                    self.isDone = True
                    return txt

            pygame.display.flip()
