import pygame,sys,textBox,resource,random,saves,gravity
from pygame.locals import *
class Main():
	def __init__(self):
		self.on = True
		self.mode = "self.mainMenu()"
		self.fps = 60
		self.fullscreen = True
		self.r = resource.base_rezolution #base rezolution
		print(self.r)
		self.rez = resource.screenSize
		self.currentRez = self.rez[:]
		self.screen = pygame.display.set_mode(self.rez,FULLSCREEN)
		self.clock = pygame.time.Clock()
		self.buttonStyle = ((133,133,133),(100,100,100))

	def screenReload(self):
		if self.fullscreen:
			self.screen = pygame.display.set_mode(self.r)
			reload(resource)
			print(resource.screenSize)
			self.fullscreen = False
			self.currentRez = self.r
		else:
			pygame.display.quit()
			reload(resource)
			self.screen = pygame.display.set_mode(self.rez,FULLSCREEN)
			self.fullscreen = True
			self.currentRez = self.rez
	
	def mainMenu(self):
		on = True
		cornerTextDraw = textBox.Display(((0,0),resource.pos((self.r[0]/3.0,self.r[1]/16.0))),"Press esc to toggle fullscreen. 'b' to go back one step in the menu.")
		button1 = resource.antiRect((resource.pos(((self.r[0]-self.r[0]/3.0)/2.0,self.r[1]/3.0)),resource.pos((self.r[0]/3.0,self.r[1]/16.0))))
		button1Draw = textBox.Display(button1,"Play",self.buttonStyle[0],self.buttonStyle[1])
		button1Draw.center()
		button1Hover = False
		while on:
			self.clock.tick(self.fps)
			for event in pygame.event.get():
				if event.type == QUIT:
					on = False
					self.on = False
				elif event.type == MOUSEBUTTONDOWN:
					if button1Hover == True:
						on = False
						self.mode = "self.play()"
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						self.screenReload()
						cornerTextDraw = textBox.Display(((0,0),resource.pos((self.r[0]/3.0,self.r[1]/16.0))),"Press esc to toggle fullscreen. 'b' to go back one step in the menu.")
						button1 = resource.antiRect((resource.pos(((self.r[0]-self.r[0]/3.0)/2.0,self.r[1]/3.0)),resource.pos((self.r[0]/3.0,self.r[1]/16.0))))
						button1Draw = textBox.Display(button1,"Play",self.buttonStyle[0],self.buttonStyle[1])
						button1Draw.center()

			mouse = pygame.mouse.get_pos()
			button1Hover = False
			if button1Hover == False and mouse[0]>=button1[0][0] and mouse[0]<=button1[1][0] and mouse[1]>=button1[0][1] and mouse[1]<=button1[1][1]:
				button1Draw.backgroundColor = self.buttonStyle[1]
				button1Draw.outlineColor = self.buttonStyle[0]
				button1Hover = True
			else:
				button1Draw.backgroundColor = self.buttonStyle[0]
				button1Draw.outlineColor = self.buttonStyle[1]

			self.screen.fill((255,0,0))
			cornerTextDraw.run(self.screen)
			button1Draw.run(self.screen)
			pygame.display.update()

	def play(self):
		on = True
		move = [0,0,0,0]
		playerSpeed = 1
		player = resource.img("player.png")
		playerPos = list(resource.pos((0,480)))
		playerGravity = gravity.new(50)
		enemy = resource.pos((32,32))
		enemyPos = list(resource.pos(self.r))
		enemySpeed = 1
		enemyColor = (0,0,0)
		goesUp = 0
		projectiles = []
		crap = saves.convertScale(saves.convert("crap"))
		length = len(crap[0])
		surface = pygame.Surface((32,32))
		surface.fill((0,0,0))
		surface2 = pygame.Surface((32,32))
		surface2.fill((0,255,255))
		surface.blit(surface2,(16,16))
		while on:
			self.clock.tick(self.fps)
			pygame.display.set_caption(str(self.clock.get_fps()))
			for event in pygame.event.get():
				if event.type == QUIT:
					on = False
					self.on = False
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						self.screenReload()
						player = resource.img("player.png")
						crap = saves.convertScale(saves.convert("crap"))
						enemy = resource.pos((32,32))
						playerPos = list(resource.pos((0,480)))
						print(playerPos)
						print(crap[0])
					elif event.key == K_LEFT:
						move[0] = -playerSpeed
					elif event.key == K_RIGHT:
						move[1] = playerSpeed
					elif event.key == K_UP:
						playerGravity.jump(50)
						move[2] = -playerSpeed
					elif event.key == K_DOWN:
						move[3] = playerSpeed
				elif event.type == KEYUP:
					if event.key == K_LEFT:
						move[0] = 0
					elif event.key == K_RIGHT:
						move[1] = 0
					elif event.key == K_UP:
						move[2] = 0
					elif event.key == K_DOWN:
						move[3] = 0

			if enemyPos[0] >= playerPos[0]:
				enemyPos[0] -= enemySpeed
			elif enemyPos[0] <= playerPos[0]:
				enemyPos[0] += enemySpeed
			if enemyPos[1] >= playerPos[1]:
				enemyPos[1] -= enemySpeed
			elif enemyPos[1] <= playerPos[1]:
				enemyPos[1] += enemySpeed

			playerPos[0] += move[0]
			playerPos[0] += move[1]
			brab = playerGravity.gravity()
			playerPos[1] += brab
			print(playerPos[1],"BRAB")
			playerPos[1] += move[3]
			goesUp += 1
			if goesUp%4==0:
				enemyColor = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
			if goesUp == self.fps:
				tmp = [abs(enemyPos[0]-playerPos[0]),abs(enemyPos[1]-playerPos[1])]
				tmp.append(float(tmp[0]+tmp[1]))				
				if enemyPos[0] > playerPos[0]:
					tmp[0] = -tmp[0]
				else:
					tmp[0] = tmp[0]
				if enemyPos[1] > playerPos[1]:
					tmp[1] = -tmp[1]
				else:
					tmp[1] = tmp[1]
				tmp = ((tmp[0]/tmp[2])*float(playerSpeed),(tmp[1]/tmp[2])*float(playerSpeed))
				projectiles.append([enemyPos[:],tmp[:]])
				del tmp
				goesUp = 0
			self.screen.fill((255,0,0))
			for x in range(length):
				self.screen.blit(crap[1][x],crap[0][x])
			pygame.draw.rect(self.screen,(0,0,0),(playerPos,enemy))			
			pygame.draw.rect(self.screen,enemyColor,(enemyPos,enemy))
			tmp = []
			for x in range(len(projectiles)):
				if x%4==0:
					tmp2 = [abs(projectiles[x][0][0]-playerPos[0]),abs(projectiles[x][0][1]-playerPos[1])]
					tmp2.append(float(tmp2[0]+tmp2[1]))
					if projectiles[x][0][0] > playerPos[0]:
						tmp2[0] = -tmp2[0]
					else:
						tmp2[0] = tmp2[0]
					if projectiles[x][0][1] > playerPos[1]:
						tmp2[1] = -tmp2[1]
					else:
						tmp2[1] = tmp2[1]
					tmp2 = [(tmp2[0]/tmp2[2])*float(playerSpeed),(tmp2[1]/tmp2[2])*float(playerSpeed)]
					projectiles[x][1] = tmp2[:]
				pygame.draw.circle(self.screen,enemyColor,(int(projectiles[x][0][0]+.5),int(projectiles[x][0][1])),10)
				projectiles[x][0][0] += projectiles[x][1][0]
				projectiles[x][0][1] += projectiles[x][1][1]
				if projectiles[x][0][0] < 0 or projectiles[x][0][1] < 0 or projectiles[x][0][0] > self.currentRez[0] or projectiles[x][0][1] > self.currentRez[1]:
					tmp.append(x)
			tmp2 = 0
			for x in tmp:
				del projectiles[x-tmp2]
				tmp2 += 1
			self.screen.blit(surface,(200,200))

			pygame.display.update()

	def run(self):
		while self.on:
			eval(self.mode)

		print("QUITTING")

main = Main()
main.run()

a
#1366,768
#500,500
#866,268 : 866+268 / 0.76366843,0.23633157 *playerSpeed = 1.52733686,0.47266314
#433,134
