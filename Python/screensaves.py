import pygame
import sys
pygame.init()
screen = pygame.display.set_mode((1366,768),pygame.FULLSCREEN)
xy = [0,(768-68)/2.0]
xy2 = [(1366-68)/2.0,0]
place = 3
place2 = 3
clock = pygame.time.Clock()
while 1:
	clock.tick(30)
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			pygame.quit()
			sys.exit()

	screen.fill((255,133,0))
	pygame.draw.rect(screen,(0,255,255),(xy,(68,68)))
	pygame.draw.rect(screen,(0,255,255),(((1366-xy[0])-68,xy[1]),(68,68)))
	pygame.draw.rect(screen,(0,255,255),(xy2,(68,68)))
	pygame.draw.rect(screen,(0,255,255),((xy2[0],(768-xy2[1])-68),(68,68)))
	if place == 3:
		if xy[0]+68+place>1366:
			place = -3
	else:
		if xy[0]+place<0:
			place = 3
	if place2 == 3:
		if xy2[1]+68+place2>768:
			place2 = -3
	else:
		if xy2[1]+place2<0:
			place2 = 3
	xy[0] += place
	xy2[1] += place2
	pygame.display.update()
