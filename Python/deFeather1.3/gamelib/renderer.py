import pygame
from pygame.locals import *


def init((width, height)):
    global screen
    screen = pygame.display.set_mode((width, height), FULLSCREEN)       
    return screen

def getWidth():
    global screen
    return screen.get_size()[0]

def getHeight():
    global screen
    return screen.get_size()[1]

def drawImage(image, (x, y)):
    global screen
    screen.blit(image, (x, y))

def getScreenSize():
    global screen
    return screen.get_size()

def clearScreen(color = (0, 0, 0)):
    global screen
    screen.fill(color)
