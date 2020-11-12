import pygame, sys
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((203, 248), 0, 32)

color = (0,255,255)
rectangle = (20,40,75,45)

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	screen.lock()
	pygame.draw.ellipse(screen, color, rectangle)
	screen.unlock()

	pygame.display.update()
