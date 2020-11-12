bif = "10240*720.png"

import pygame, sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1280,720),0,32)
Clock = pygame.time.Clock()

background = pygame.image.load(bif).convert()

x = 0
move = 0

while True:
	tick = Clock.tick(30)

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_LEFT:
				move = -1
			if event.key == K_RIGHT:
				move = 1
		if event.type == KEYUP:
			move = 0
	
	if move == -1 and x != 0:
		x += 4
	if move == 1 and x != -8960:
		x -= 4

	screen.blit(background,(x,0))

	print(x)

	pygame.display.update()
