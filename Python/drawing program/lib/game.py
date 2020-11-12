import pygame, sys
from pygame.locals import *
import os

class gameLoop():
	def __init__(self):
		self.screenInfo = pygame.display.Info()
		self.screenSize = (self.screenInfo.current_w,self.screenInfo.current_h)
		self.scaleVariable = (self.screenSize[0] / 1280.0, screenSize[1] / 720.0)
		self.overlySimplifiedPencilVariable = (scaleVariable[0] + scaleVariable[1]) / 2
		self.pencilSize = 10
		self.previousPencilSize = 0
		self.background = None
		self.screen = pygame.display.set_mode(self.screenSize,FULLSCREEN)
		self.colors = {
				'background' : (255,255,255),
				'mainPencil' : (200,155,64)
				}
		self.points = []
		self.mouseDown = False

		pygame.display.set_caption('ImageProgrammer')

		self.clock = pygame.time.Clock()

		self.goesUp = 0

	def gameLoop(self):
		while True:		
			self.clock.tick(30)
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						self.screen = pygame.display.set_mode(screenSize)
				if event.type == MOUSEBUTTONDOWN:
					self.mouseDown = True
				if event.type == MOUSEBUTTONUP:
					self.mouseDown = False
					pygame.image.save(screen,os.path.join('data','background.png'))
					if self.goesUp == 0:
						self.goesUp = 1
				if event.type == MOUSEMOTION and self.mouseDown == True:
					self.points.append(event.pos)
					print(self.points[len(self.points) - 1])

			if self.previousPencilSize != self.pencilSize:
				self.pencilSize = int(self.pencilSize * self.overlySimplifiedPencilVariable)
			self.previousPencilSize = self.pencilSize

			if self.goesUp == 1:
				self.screen.blit(background,(0,0))
			else:
				self.screen.fill(self.colors['background'])

			if len(self.points)>1:
				pygame.draw.lines(self.screen, self.color, False, self.points, self.pencilSize)
			
			pygame.display.update()

