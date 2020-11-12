import pygame
import sys
import random
pygame.init()
screen = pygame.display.set_mode((1366,768),pygame.FULLSCREEN)
clock = pygame.time.Clock()
while 1:
	clock.tick(1)
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			pygame.quit()
			sys.exit()
	
	screen.fill((0,0,0))
	for x in range(random.randint(10,30)):
		pygame.draw.rect(screen,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),((random.randint(0,1346),random.randint(0,748)),(20,20)))
	pygame.display.update()
