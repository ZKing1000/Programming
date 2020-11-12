import pygame, sys
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((203, 248), 0, 32)
color = (230,170,0)
position = (75,75)
radius = (60)

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	screen.lock()
	pygame.draw.circle(screen, color, position, radius)
	pygame.draw.circle(screen, (100,100,100), position, radius/4)	
	screen.unlock()

	pygame.display.update()
