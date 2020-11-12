import pygame, sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((203, 248), 0, 32)

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			print(event.unicode)
