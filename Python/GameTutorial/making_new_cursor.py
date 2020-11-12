bif = "cindy.jpeg"
mif = "cursor.png"

import pygame, sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((203, 248), 0, 32)

background = pygame.image.load(bif).convert()
cursor = pygame.image.load(mif).convert_alpha()

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	screen.blit(background, (0, 0))

	x,y = pygame.mouse.get_pos()
	x -= cursor.get_width()/2
	y -= cursor.get_height()/2

	screen.blit(cursor, (x,y))

	pygame.display.update()



		
