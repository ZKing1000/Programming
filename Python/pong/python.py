import pygame,random,sys
pygame.init()
score = [0,0]
ballPos = [640,360]
ballSpeed = 5
tiltFactor = 2
ballTilt = random.randint(-2,2)
playerPos = 0
compPos = 0
isPressedY = 0
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
while 1:
	clock.tick(30)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.image.save(screen,"boobies.png")
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN:
				isPressedY = 8
			elif event.key == pygame.K_UP:
				isPressedY = -8
		elif event.type == pygame.KEYUP:
			isPressedY = 0
	
	screen.fill((0,0,0))
	ballPos = [ballPos[0] + ballSpeed,ballPos[1] + ballTilt]
	pygame.draw.circle(screen,(255,0,0),ballPos,20)
	playerPos += isPressedY
	pygame.draw.rect(screen,(90,90,90),((1260,playerPos),(20,120)))
	pygame.draw.rect(screen,(90,90,90),((0,compPos),(20,120)))
	if ballPos[1] + 5 <= 0:
		tiltFactor += 1
		ballTilt = random.randint(0,tiltFactor)
	elif ballPos[1] + 40 >= 720:
		tiltFactor += 1
		ballTilt = random.randint(-tiltFactor,0)
	if compPos + 60 <= ballPos[1]:
		compPos += 8
	else:
		compPos -= 8
	if ballPos[1] >= playerPos and playerPos + 120 >= ballPos[1] and ballPos[0] + 20 >= 1260:
		ballSpeed = -ballSpeed - 1
		ballTilt = random.randint(-2,2)
	elif ballPos[1] >= compPos and compPos + 120 >= ballPos[1] and ballPos[0] <= 20:
		ballSpeed = +ballSpeed + 1
		ballTilt = random.randint(-2,2)
	pygame.display.update()
