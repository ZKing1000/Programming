import pygame, sys
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((203, 248), 0, 32)

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	pygame.draw.rect(screen, (255,0,0), Rect((25,25), (50,50)))

	pygame.display.update()









