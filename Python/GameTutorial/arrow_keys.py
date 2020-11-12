bif = "cindy.jpeg"
mif = "cursor.png"

import pygame, sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((203, 248), 0, 32)

background = pygame.image.load(bif).convert()
cursor = pygame.image.load(mif).convert_alpha()

x,y = 0,0
movex, movey = 0,0

while True:

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_LEFT:
				movex = -1
			elif event.key == K_RIGHT:
				movex = +1
			elif event.key == K_UP:
				movey = -1
			elif event.key == K_DOWN:
				movey = +1
		if event.type == KEYUP:
			if event.key == K_LEFT:
				movex = 0
			elif event.key == K_RIGHT:
				movex = 0
			elif event.key == K_UP:
				movey = 0
			elif event.key == K_DOWN:
				movey = 0

	x += movex
	y += movey

	if x < 0:
		x = 0
	if x > 203*20:
		x = (203*20)-2
	if y < 0:
		y = 0
	if y > 248*20:
		y = (248*20)-2


	screen.blit(background, (0,0))
	screen.blit(cursor, (x/20,y/20))

	pygame.display.update()




