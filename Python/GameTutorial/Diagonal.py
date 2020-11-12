bif = "cindy.jpeg"
mif = "cursor.png"

import pygame, sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((203, 248), 0, 32)

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	pygame.display.update()
