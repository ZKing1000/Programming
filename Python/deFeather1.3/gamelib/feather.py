import pygame
from pygame.locals import *

import gamelib
import data
import renderer
from myconstants import *

class Feather(pygame.sprite.Sprite):
    gravity = 2
    maxVel = 30
    lenToVelScaling = 10
    def __init__(self):
        self.x = 100
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.state = MOTION_FREEFALL 
        self.background = pygame.surface.Surface(gamelib.feather_img[0].get_size(), 0, gamelib.feather_img[0]) #data.loadImage("feather0.png") 
        self.curframe = 0
        self.images = gamelib.feather_img
        self.color = (255, 255, 255)

    def setState(self, state, len):
        self.state = state
        vel = len/Feather.lenToVelScaling
        if vel > Feather.maxVel:
            vel = Feather.maxVel
        #set velocity based on the state
        if state == MOTION_UP:
            self.vy = -vel 
        elif state == MOTION_DOWN:
            self.vy = vel
        elif state == MOTION_RIGHT:
            self.vx = vel
        elif state == MOTION_LEFT:
            self.vx = -vel
    def getRect(self):
        size = self.background.get_size()
        return pygame.rect.Rect(self.x, self.y, size[0], size[1])

    def update(self):
        #if not(self.vx == 0) or not(self.vy == 0):
        if self.vx < 0: 
            self.vx += Feather.gravity
            if self.vx > 0:
                self.vx = 0
        elif self.vx > 0:
            self.vx -= Feather.gravity
            if self.vx < 0:
                self.vx = 0
        if self.vy < 0: 
            self.vy += Feather.gravity
            if self.vy > 0:
                self.vy = 0
#        elif self.vy > 0:
#           self.vy -= Feather.gravity
#           if self.vy < 0:
#               self.vy = 0

        self.x += self.vx
        self.y += self.vy

        self.y = self.y + Feather.gravity

        #animation code, continue animating if feather_img above ground or v != 0
        if abs(self.vy) == 0 and self.y + self.images[0].get_size()[1] < renderer.getHeight()-gamelib.grnd_img.get_size()[1] :
            self.curframe += 1
            if self.curframe > len(self.images)-1:
                self.curframe = 0

        img_size = self.images[0].get_size()
        sw = renderer.getWidth()
        sh = renderer.getHeight()
        #bounding at left
        if self.x < 0:
            self.vx = 0
            self.x = 0
        #bounding at right
        if self.x + img_size[0] > renderer.getWidth():
            self.x = renderer.getWidth() - img_size[0] 
            self.vx = 0
        #bounding the movement if touching the ground
        if self.y + img_size[1] > sh-gamelib.grnd_img.get_size()[1]: 
            self.y = sh - gamelib.grnd_img.get_size()[1] - img_size[1] + 10 #aah the magic number
            self.vy = 0
            self.vx = 0
        #bounding at top
        if self.y < 0:
            self.y = 0
            self.vy = 0

    def addColor(self, color=(0, 0, 0)):
        tmp = []
        sum = 0
        i = 0
        flag = False
        for c in color:
            tmp.append(self.color[i] + c)
            sum += self.color[i]
            if tmp[i] > 255:
                flag = True
            i+= 1

        if sum > 255 or flag:
            self.color = color 
        else:
            self.color = (tmp[0], tmp[1], tmp[2])            
        #print self.color, color, tmp
            
    def isPointOver(self, pos):                
        cur_image = self.images[int(self.curframe)]
        cur_size = cur_image.get_size()
        if self.x < pos[0] and pos[0] < self.x + cur_size[0]:
            if self.y < pos[1] and pos[1] < self.y + cur_size[1]:
                x_img = pos[0] - self.x
                y_img = pos[1] - self.y
                pixel = cur_image.get_at((x_img, y_img))
                if pixel[3] > 0:
                    return True
        return False

    def render(self):
        self.background.fill(self.color)
        self.background.blit(self.images[int(self.curframe)], (0, 0), None, BLEND_RGBA_MULT)
        renderer.drawImage(self.background, (self.x, self.y))

