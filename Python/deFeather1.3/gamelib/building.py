import pygame
from pygame.locals import *

import data
import gamelib
import renderer
import gestures 
from myconstants import *

class Building:
    baseLine = 0
    def __init__(self, x, index):
        if Building.baseLine == 0:
            Building.baseLine =  renderer.getHeight() - gamelib.grnd_img.get_size()[1] 
        self.x = x 
        self.baseColor = (255, 255, 255)
        self.color = (255, 255, 255)
        self.image = gamelib.amb_imgs[index]
        self.decoration = gamelib.det_imgs[index]
        self.colorplane = pygame.surface.Surface(self.image.get_size(), 0, gamelib.det_imgs[index])
        self.updateColor((255, 255, 255), (self.x, (Building.baseLine-self.image.get_size()[1])))
        self.colorPercent= 1
        self.filltype = F_FROM_MID 

    def render(self):
        if not(self.color == (255, 255, 255)):
            self.colorplane.blit(self.decoration, (0, 0))
        renderer.drawImage(self.colorplane, (self.x, (Building.baseLine-self.image.get_size()[1])))

    def updateColor(self, newcolor, pos):
        if self.color == newcolor:
            return 0
        #decide the fill type based on pos
        size = self.colorplane.get_size()
        self.y = (Building.baseLine-size[1])
        top_rect = pygame.rect.Rect(self.x, self.y, size[0], size[1]/3)  
        mid_rect = pygame.rect.Rect(self.x, self.y + size[1]/3, size[0], size[1]/3)
#        bot_rect = pygame.rect.Rect(self.x, self.y + 2*size[1]/3, size[0], size[1]/3)
        if top_rect.collidepoint(pos):
            self.filltype = F_FROM_TOP
        elif mid_rect.collidepoint(pos):
            self.filltype = F_FROM_MID
        else:
            self.filltype = F_FROM_BOT

        #handle other animation data
        self.baseColor = self.color
        self.color = newcolor
        self.colorPercent = 0
        sum = 0
        for c in newcolor:
            sum += c
        if sum > 255:
            return 200
        else:
            return 100

    def isPointOver(self, pos = (0, 0)):
        imSize = self.image.get_size()
        if self.x < pos[0] and (self.x + imSize[0]) > pos[0]:
            if ( (Building.baseLine-imSize[1]) < pos[1] ):
                if pos[1] < Building.baseLine:
                    return True
        return False

    def update(self):
        if self.colorPercent > 1:
            return 
        self.colorPercent += 0.2
        size = self.colorplane.get_size()
        self.colorplane.fill(self.baseColor)
        #change the parameters to the rectangle to change the fill style
        if self.filltype == F_FROM_MID:
            self.colorplane.fill(self.color, ((1-self.colorPercent)*size[0]/2, (1-self.colorPercent)*size[1]/2, size[0]*self.colorPercent, size[1]*self.colorPercent))
        elif self.filltype == F_FROM_TOP:
            self.colorplane.fill(self.color, (0, 0, size[0], self.colorPercent * size[1]))
        elif self.filltype == F_FROM_BOT:
            self.colorplane.fill(self.color, (0, (1-self.colorPercent)*size[1], size[0], self.colorPercent * size[1]))
        self.colorplane.blit(self.image, (0, 0), None, BLEND_RGBA_MULT)

