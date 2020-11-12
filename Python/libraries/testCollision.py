import pygame,sys,collisionDetection
pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
instance = collisionDetection.complxObj()
x,y = 0,0
movex, movey = 0,0
shoot1 = instance.setup("shoot1.png")
shoot2 = instance.setup("blab.png")
shoot1png = pygame.image.load("shoot1.png").convert_alpha()
shoot2png = pygame.image.load("blab.png").convert_alpha()
previousXY = []
while 1:
	clock.tick(30)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				movex = -4
			elif event.key == pygame.K_RIGHT:
				movex = +4
			elif event.key == pygame.K_UP:
				movey = -4
			elif event.key == pygame.K_DOWN:
				movey = +4
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				movex = 0
			elif event.key == pygame.K_RIGHT:
				movex = 0
			elif event.key == pygame.K_UP:
				movey = 0
			elif event.key == pygame.K_DOWN:
				movey = 0

	x += movex
	y += movey
	screen.fill((100,100,100))
	screen.blit(shoot1png,(x,y))
	screen.blit(shoot2png,(500,500))
	if instance.complxObj(shoot1,shoot2,(x,y),(500,500)) == True:
		x = previousXY[0]
		y = previousXY[1]
	previousXY = [x,y]
	pygame.display.update()
