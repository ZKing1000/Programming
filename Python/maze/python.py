import pygame,sys,random
resolution = (1366,768)
screen = pygame.display.set_mode(resolution,pygame.FULLSCREEN)
playerPos = 0
difficulty = 15
positions = [[0,resolution[1]/2.0]]
positionConnections = []
positionJoints = []
positions2 = []
for x in range(difficulty-1):
	positions.append([random.randint(0,resolution[0]),random.randint(0,resolution[1])])

def leastToGreatest():
	global positions
	global positions2
	cache = [0,resolution[0]]
	goesUp = 0
	for x in positions:
		x0 = x[0]
		if x0 < cache[1]:
			cache[1] = x0
			cache[0] = goesUp
		goesUp += 1
	positions2.append(positions[cache[0]])
	del positions[cache[0]]

for x in range(difficulty):
	leastToGreatest()

positions = positions2[:]
del positions2

for x in range(difficulty):
	positionConnections.append([])
	_set = [p for p in range(difficulty)]
	del _set[x]
	for y in range(random.randint(1,difficulty-1)): #how much its connected to
		current = random.choice(_set)
		del _set[_set.index(current)]
		positionConnections[x].append(current)
	
	positionJoints.append([])
	for w in range(len(positionConnections[x])):
		positionJoints[x].append(random.randint(0,difficulty))

linePoints = []
goesUp = 0
goesUp2 = 0
goesUp3 = 0
print(positions)
print(positionConnections)
print(positionJoints)
print("##############################################")
for x in positionJoints:
	for y in x:
		linePoints.append([positions[goesUp3]])
		for z in range(y):
			linePoints[goesUp2].append([random.randint(0,resolution[0]),random.randint(0,resolution[1])])
		linePoints[goesUp2].append(positions[positionConnections[goesUp3][goesUp]])
		goesUp += 1
		goesUp2 += 1

	goesUp = 0
	goesUp3 += 1

clock = pygame.time.Clock()
while 1:
	clock.tick(1)
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			pygame.quit()
			sys.exit()
	
	positions = [[0,resolution[1]/2.0]]
	positionConnections = []
	positionJoints = []
	positions2 = []
	for x in range(difficulty-1):
		positions.append([random.randint(0,resolution[0]),random.randint(0,resolution[1])])

	for x in range(difficulty):
		leastToGreatest()

	positions = positions2[:]
	del positions2

	for x in range(difficulty):
		positionConnections.append([])
		_set = [p for p in range(difficulty)]
		del _set[x]
		for y in range(random.randint(1,difficulty-1)): #how much its connected to
			current = random.choice(_set)
			del _set[_set.index(current)]
			positionConnections[x].append(current)
		
		positionJoints.append([])
		for w in range(len(positionConnections[x])):
			positionJoints[x].append(random.randint(0,difficulty))

	del current
	linePoints = []
	goesUp = 0
	goesUp2 = 0
	goesUp3 = 0
	print(positions)
	print(positionConnections)
	print(positionJoints)
	print("##############################################")
	for x in positionJoints:
		for y in x:
			linePoints.append([positions[goesUp3]])
			for z in range(y):
				linePoints[goesUp2].append([random.randint(0,resolution[0]),random.randint(0,resolution[1])])
			linePoints[goesUp2].append(positions[positionConnections[goesUp3][goesUp]])
			goesUp += 1
			goesUp2 += 1

		goesUp = 0
		goesUp3 += 1

	screen.fill((0,0,0))
	for x in linePoints:
		pygame.draw.lines(screen, (random.randint(0,255),random.randint(0,255),random.randint(0,255)), False, x, 1)
	for x in positions:
		pygame.draw.rect(screen,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),(x,(10,10)))
	pygame.display.update()
