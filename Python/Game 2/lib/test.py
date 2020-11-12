import saves,pygame
pygame.init()
screen = pygame.display.set_mode((960,540))
clock = pygame.time.Clock()
tmp = [0,0]
crap = saves.terrain("../saved/terrain/structure/first.txt")
while 1:
	clock.tick(30)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
	for x in range(len(crap[1])):
		screen.blit(crap[0][x],crap[1][x])
	pygame.display.update()
