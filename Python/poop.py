import pygame, sys, os
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((640,360))
img = pygame.image.load("png.png").convert()
while True:
	clock.tick(30)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			pygame.image.save(screen, "screenshot.png")
			pygame.quit()
			sys.exit()
	screen.blit(img,(100,100))
	pygame.display.update()

