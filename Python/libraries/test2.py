import pygame, collisionDetection as CD
pygame.init()
screen = pygame.display.set_mode((640,460),0,32)

crap = True

blab = pygame.image.load('./rect.png').convert()

clock = pygame.time.Clock()
while crap == True:
	clock.tick(30)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.image.save(screen, "screenshot.png")
			pygame.quit()
			sys.exit()	
	screen.blit(blab, (200, 100))
	print(CD.rectangular((200,100),(300,150)))
	pygame.display.update()
	
