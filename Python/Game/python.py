#!/usr/bin/python
import os
crap = os.path.realpath(__file__)[:-9]
bif = crap + "background0.png"
mif = crap + "cursor.png"
mif2 = crap + "Duck.png"
mif3 = crap + "Duck2.png"
mif4 = crap + "DuckWing.png"
mif5 = crap + "DuckWing2.png"
bif2 = crap + "background1.png"
bif3 = crap + "background2.png"

import pygame, sys, pygame.mixer
import random
from pygame.locals import *
import fileinput

#Options:
volume = 0.5
#Options
#

pygame.init()
gunshot = pygame.mixer.Sound('gunshot.wav')
gunshot.set_volume(volume)
GameType = 0
screen = pygame.display.set_mode((1280, 720), 0, 32)
die = pygame.event.set_blocked(pygame.MOUSEMOTION)

background1 = pygame.image.load(bif2).convert()
background0 = pygame.image.load(bif).convert()
background = pygame.image.load(bif3).convert()

cursor = pygame.image.load(mif).convert_alpha()
duckImage = pygame.image.load(mif2).convert_alpha()
duckImage2 = pygame.image.load(mif3).convert_alpha()

clock = pygame.time.Clock()
listDown = [1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024]
listUp = [128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128]
listExtra = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
listExtra2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
yAxis = [128, 192, 256, 320, 384, 448, 512, 128, 192, 256, 320, 384, 448, 512, 128, 192, 256, 320, 384, 448, 512]
yAxis2 = [128, 192, 256, 320, 384, 448, 512, 128, 192, 256, 320, 384, 448, 512, 128, 192, 256, 320, 384, 448, 512]
timer = 0
timer2 = 60000
extra = 0
points = 0
lives = 10
textEnter = ""
alphabet = [x for x in "qwertyuiopasdfghjklzxcvbnm"]
goesUp = 0
number = 0

font = pygame.font.SysFont("monospace", 150)
fontSubtitle = pygame.font.SysFont("monospace", 75)

duckList = []

class Duck():
	def __init__(self):
		self.y = random.randint(128,512)
		self.direction = random.randint(0,1)
		if self.direction == 0:
			self.direction = -1
			self.x = 1024
		else:
			self.x = 128
		self.startDelay = 0

	def DuckFly(self, speed):
		global timer
		global extra
		global duckImage
		global duckImage2
		global points
		global listExtra
		global yAxis
		global lives
		global fps

		if speed > 6:
			speed = 6
		self.x += speed * self.direction
		extra += milli/1000.0
		#Determines if the duck will move from left to right or right to left 0 = right to left, 1 = left to right
		if self.direction == -1:
			screen.blit(duckImage, (self.x,self.y))
			if self.x < 128 and self.x > 100:
				lives -= 1
				print("Lives - = " + str(lives))
				self.x = 1024
			#Creates a hit box around the duck
			if event.type == MOUSEBUTTONDOWN and x >= self.x + 15 and x <= self.x + 97 and y >= self.y - 4 and y <= self.y + 44:
				points += 1
				print("Points + 1 = " + str(points))
				self.startDelay = self.x
				self.x = -128
				self.y = random.randint(128,512)
			if self.x <= -128 - self.startDelay:
				self.startDelay = 0
				self.x = 1024

			if extra < 1 and extra > 0.5:
				duckImage = pygame.image.load(mif4).convert_alpha()
			if extra < 0.5:
				duckImage = pygame.image.load(mif2).convert_alpha()
			if extra > 1:
				extra = 0

		else:
			screen.blit(duckImage2, (self.x,self.y))
			if self.x > 1024 and self.x < 1200:
				lives -= 1
				print("lives - 1 = " + str(lives))
				self.x = 128
			if event.type == MOUSEBUTTONDOWN and x >= self.x - 1 and x <= self.x + 81 and y >= self.y + 11 and y <= self.y + 41:
				points += 1
				print("Points + 1 = " + str(points))
				self.startDelay = 1024 - self.x
				self.x = 1280
				self.y = random.randint(128,512)
			if self.x > self.startDelay + 1280:
				self.startDelay = 0
				self.x = 128

			if extra < 1 and extra > 0.5:
				duckImage2 = pygame.image.load(mif5).convert_alpha()
			if extra < 0.5:
				duckImage2 = pygame.image.load(mif3).convert_alpha()
			if extra > 1:
				extra = 0

	
def duckSpawn(speed, numberOfDucks):
	for x in range(numberOfDucks):
		if x >= len(duckList):
			duckList.append(Duck())

		duckList[x].DuckFly(speed)

class scoreInterperate(object):
	def __init__(self):
		pass

	def biggestInt(self, ints):
		if len(ints) == 0:
			return 0
		number = ints[0]

		for x in ints:
			if x > number:
				number = x
		return number			

	def scoreInterperate(self, name):
		ints = []
		for x in fileinput.input("scores.txt"):
			vals = x.split(':')
			if vals[1][:-1] == name:
				ints.append(int(vals[0]))
		return self.biggestInt(ints)

	def fontPosition(self, name):
		return 640 - fontSubtitle.size(name)[0] / 2
		




while True:		
	while GameType == 0:
		clock.tick(30)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if event.type == MOUSEBUTTONDOWN and x > 426 and x < 810 and y > 270 and y < 334:
				GameType = 1
			if event.type == MOUSEBUTTONDOWN and x > 426 and x < 810 and y > 368 and y < 432:
				GameType = 3
			if event.type == MOUSEBUTTONDOWN and x > 426 and x < 810 and y > 464 and y < 528:
				GameType = 4
			if event.type == MOUSEBUTTONDOWN:
				gunshot.play()

		x,y = pygame.mouse.get_pos()
		x -= cursor.get_width()/2
		y -= cursor.get_height()/2

		screen.blit(background0, (0, 0))
		screen.blit(cursor, (x,y))

		milli = clock.tick()
		timer += milli

		pygame.display.update()

	while GameType == 1:
		milli = clock.tick(30)		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				gunshot.play()


		x,y = pygame.mouse.get_pos()
		x -= cursor.get_width()/2
		y -= cursor.get_height()/2

		screen.blit(background1, (0, 0))
		screen.blit(cursor, (x,y))

		minutes = timer2/60000

		speed = minutes
		numDucks = minutes * 2

		duckSpawn(speed, numDucks)

		timer2 += milli
		SURFACEFONT = font.render(str(points),True,(0,0,0))
		SURFACEFONT2 = font.render(str(lives),True,(0,0,0))
		screen.blit(SURFACEFONT, (970, 0))
		screen.blit(SURFACEFONT2, (130, 0))

		if lives < 1:
			GameType = 2

		pygame.display.update()

	while GameType == 2:
		clock.tick(30)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				gunshot.play()
			if event.type == KEYDOWN:
				if event.key == K_BACKSPACE:
					textEnter = textEnter[:-1]
				elif event.key == K_RETURN:
					scores = open("scores.txt", "a+")
					scores.write(str(points) + ":" + textEnter + "\n")
					scores.close()
					textEnter = ""
					GameType = 0
					lives = 10
					points = 0
				else:
					currentKey = event.unicode
					textEnter += str(currentKey)

		x,y = pygame.mouse.get_pos()

		x -= cursor.get_width()/2
		y -= cursor.get_height()/2

		screen.blit(background, (0, 0))
		screen.blit(cursor, (x,y))

		if textEnter != "":
			score = str(scoreInterperate().scoreInterperate(textEnter))
			SURFACEFONT4 = fontSubtitle.render(score,True,(227,208,58))
			screen.blit(SURFACEFONT4, (scoreInterperate().fontPosition(score), 361))

		if len(str(textEnter)) > 5:
			SURFACEFONT3 = font.render(str(textEnter)[len(str(textEnter)) - 5:],True,(0,0,0))
		else:
			SURFACEFONT3 = font.render(str(textEnter),True,(0,0,0))
			
		screen.blit(SURFACEFONT, (146, 146))
		screen.blit(SURFACEFONT3, (646, 146))

		pygame.display.update()
