import pygame, sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((203, 248), 0, 32)

color = (200,155,64)
points = []
mouseDown = False

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == MOUSEBUTTONDOWN:
			mouseDown = True
		if event.type == MOUSEBUTTONUP:
			mouseDown = False
		if event.type == MOUSEMOTION and mouseDown == True:
			points.append(event.pos)
			print(points[len(points) - 1])

	if len(points)>1:
		pygame.draw.lines(screen, color, False, points, 5)


	pygame.display.update()
