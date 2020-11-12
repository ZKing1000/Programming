import pygame, sys
from pygame.locals import *

def biggestLetterInFontSize(fontType):
	font = pygame.font.SysFont(fontType,100)
	cache = [0,0,"",""] #Sizes in pixels and biggest letters. cache[2] is longest, cache[3] is tallest, cache[0] and [1] are sizes in pixels to be compared
	for x in range(32,127):
		fontSize = font.size(chr(x))
		if cache[0] < fontSize[0]:
			cache[0] = fontSize[0]
			cache[2] = chr(x)
		if cache[1] < fontSize[1]:
			cache[1] = fontSize[1]
			cache[3] = chr(x)
	return (cache[2],cache[3])

class textBoxInput():
	def __init__(self,screen,clock,pos,endPos,fontType,maxStrSize,backgroundColor,textColor,boarderOffColor,boarderOnColor,textEnter=""):
		self.pos = pos #handler, fontPastePos, drawBox
		self.length = (endPos[0] - pos[0] -4,endPos[1] - pos[1] -4)
		self.maxStrSize = maxStrSize #textBoxInput
		self.fontType = fontType #textSizeCalc, fontPastePos, drawBox
		self.backgroundColor = backgroundColor #drawBox
		self.textColor = textColor #drawBox
		self.boarderOffColor = boarderOffColor #drawBox
		self.boarderOnColor = boarderOnColor #drawBox
		self.screen = screen #drawBox
		self.clock = clock #rapidEnterFunc
		if textEnter != None:
			self.textEnter = textEnter #handler, rapidEnterFunc, drawBox, textBoxInput
			self.currentText = textEnter
		else:
			self.textEnter = ""
			self.currentText = ""
		self.rapidEnter = False #handler, rapidEnterFunc
		self.time = 0 #handler, rapidEnterFunc
		self.delayToRapidEnter = 0 #handler, rapidEnterFunc
		self.publicUnicode = None #handler, rapidEnterFunc
		self.on = False #handler, drawBox
		self.shiftButton = False #handler
		self.mousepos = (0,0) #handler
		self.textSizeCalc = self.textSizeCalc() #drawBox, fontPastePos
		self.isDone = False #handler, textBoxInput
		xposition = (pos[0] - 4,pos[1] - 4) #__init__
		self.points = [pos,(endPos[0] -2,pos[1]),(endPos[0] -2,endPos[1] -2),(pos[0],endPos[1] -2),pos]
 #drawBox

	def textSizeCalc(self):
		fontSize = 1
		while True:
			if "/" in self.fontType:
				font = pygame.font.Font(self.fontType,fontSize)
			else:
				font = pygame.font.SysFont(self.fontType,fontSize)
			if font.size(biggestLetterInFontSize(self.fontType)[1])[1] >= self.length[1]:
				return fontSize - 1
			fontSize += 1

	def handler(self,event):
		if event.type == MOUSEBUTTONDOWN:
			self.mousepos = pygame.mouse.get_pos()

			if self.pos[0] <= self.mousepos[0] and self.pos[1] <= self.mousepos[1] and (self.pos[0] + self.length[0]) >= self.mousepos[0] and (self.pos[1] + self.length[1]) >= self.mousepos[1]:
				
				self.on = True #Click on textbox

			elif self.pos[0] + self.length[0] <= self.mousepos[0] or self.pos[0] >= self.mousepos[0] or self.pos[1] + self.length[1] <= self.mousepos[1] or self.pos[1] >= self.mousepos[1]:
				
				self.on = False #Click outside of box
				
		if self.on == True:
			if event.type == KEYDOWN:
				if event.key == K_RETURN:
					self.isDone = True
				elif event.key == K_BACKSPACE:
					self.textEnter = self.textEnter[:-1]
					self.currentText = self.currentTextDelete()
					self.publicUnicode = event.unicode
					self.rapidEnter = True
				elif event.key == K_RSHIFT or event.key == K_LSHIFT:
					self.shiftButton = True
				elif self.shiftButton == True and event.key != K_DELETE and event.key != K_ESCAPE and event.key != K_TAB and event.key != K_KP_ENTER:
					currentKey = event.unicode
					self.textEnter += currentKey.upper()
					if len(self.textEnter) <= self.maxStrSize:
						self.currentText += currentKey.upper()
				elif event.key != K_DELETE and event.key != K_ESCAPE and event.key != K_TAB and event.key != K_KP_ENTER:
					self.textEnter += event.unicode
					if len(self.textEnter) <= self.maxStrSize:
						self.currentText += event.unicode
					self.publicUnicode = event.unicode
					self.rapidEnter = True
			elif event.type == KEYUP:
				self.rapidEnter = False
				self.shiftButton = False
				self.delayToRapidEnter = 0
				self.time = 0
				self.publicUnicode = None

	def fontPastePos(self):
		if "/" in self.fontType:
			font = pygame.font.Font(self.fontType,self.textSizeCalc)
		else:
			font = pygame.font.SysFont(self.fontType,self.textSizeCalc)
		return (self.pos[0] + 2,((self.pos[1] + 2) + (self.length[1] - font.size("a")[1]) / 2))

	def currentTextDelete(self):
		if "/" in self.fontType:
			font = pygame.font.Font(self.fontType,self.textSizeCalc)
		else:
			font = pygame.font.SysFont(self.fontType,self.textSizeCalc)
		cache = ""
		for x in self.textEnter[::-1]:
			cache += x
			if (font.size(cache)[0] + font.size(biggestLetterInFontSize(self.fontType)[0])[0]) >= self.length[0]:
				return cache[::-1]
		return self.textEnter


	def rapidEnterFunc(self): #The name is necessary and the function is only called once; check line 17.
		if self.rapidEnter == True and self.time >= 1 and self.delayToRapidEnter >= 16:
			if self.publicUnicode == "\b":
				self.textEnter = self.textEnter[:-1]
				self.currentText = self.currentTextDelete()
			else:
				self.textEnter += self.publicUnicode
				if len(self.textEnter) <= self.maxStrSize:
					self.currentText += self.publicUnicode
			self.time = 0
			self.delayToRapidEnter = 16
		elif self.rapidEnter == True:
			self.time += (1 * (30 /(int(self.clock.get_fps()) + 0.0)))
			self.delayToRapidEnter += (1 * (30 /(int(self.clock.get_fps()) + 0.0)))

	def drawBox(self):
		if "/" in self.fontType:
			font = pygame.font.Font(self.fontType,self.textSizeCalc)
		else:
			font = pygame.font.SysFont(self.fontType,self.textSizeCalc)
		if font.size(self.currentText)[0] >= self.length[0]:
			self.currentText = self.currentText[1:]
		if self.backgroundColor != None:
			pygame.draw.rect(self.screen,self.backgroundColor,Rect((self.pos[0] +2,self.pos[1] +2),(self.length[0],self.length[1])))
		if self.on == False:
			pygame.draw.lines(self.screen, self.boarderOffColor, False, self.points, 2)
		else:
			pygame.draw.lines(self.screen, self.boarderOnColor, False, self.points, 2)
		self.screen.blit(font.render(self.currentText,True,self.textColor),self.fontPastePos())

	def textBoxInput(self):
		self.rapidEnterFunc()
		self.drawBox()
		if self.isDone == True:
			return self.textEnter
		elif len(self.textEnter) > self.maxStrSize:
			self.textEnter = self.textEnter[:-1]





class textBoxDisplay():
	def __init__(self,screen,pos,endPos,fontType,backgroundColor,textColor,boarderColor,cutInMidWord,text):
		self.screen = screen
		self.pos = pos
		self.endPos = endPos
		self.length = (endPos[0] - pos[0] -4,endPos[1] - pos[1] -4)
		self.fontType = fontType
		self.backgroundColor = backgroundColor
		self.textColor = textColor
		self.boarderColor = boarderColor
		self.cutWord = cutInMidWord
		self.text = text
		self.biggestLetter = biggestLetterInFontSize(fontType)
		self.fontStuffs = self.fontSizeCalc()
		self.outlinePoints = [pos,(endPos[0] -2,pos[1]),(endPos[0] -2,endPos[1] -2),(pos[0],endPos[1] -2),pos]
		self.rect = Rect(self.pos,((endPos[0] - pos[0]),(endPos[1] - pos[1])))
		if "/" in fontType:
			self.font = pygame.font.Font(self.fontType,self.fontStuffs[0])
		else:
			self.font = pygame.font.SysFont(self.fontType,self.fontStuffs[0])
		#Following is for blitting text more efficiently
		self.SURFACEFONT = []
		self.pastePos2 = []
		for y in range(self.fontStuffs[2]):
			self.SURFACEFONT.append(self.font.render(self.fontStuffs[1][y],True,self.textColor))
			self.pastePos2.append(self.pos[1] + (y * self.font.size(self.biggestLetter[1])[1]))
		self.pastePos = self.pos[0]+2

	def didCutInMid(self,inStr):
		lnNumber = 0
		lnCount = 0
		string = ""
		cut = ""
		for x in self.text:
			if x == "\n":
				lnNumber += 1
		for x in self.text:
			if x == "\n":
				lnCount += 1
			elif lnCount == lnNumber:
				cut += x
			else:
				string += x
		if inStr == cut: return False
		else: return True

	def fontSizeCalc(self):
		fontSize = 1
		forStr = ""
		fullStr = []
		goesUp = 0
		while True:
			if "/" in self.fontType:
				font = pygame.font.Font(self.fontType,fontSize)
			else:
				font = pygame.font.SysFont(self.fontType,fontSize)
			for x in self.text:
				goesUp += 1
				if x != "\n":
					forStr += x
				if font.size(forStr)[0] + font.size(self.biggestLetter[0])[0] > self.length[0] and x != "\n":
					subStr = ""
					if self.cutWord == False and goesUp < len(self.text) and self.text[goesUp] != " ":
						for x in forStr[::-1]:
							if x == " ":
								subStr = subStr[::-1]
								break
							else:
								subStr += x
					if len(subStr) > 0:
						fullStr.append(forStr[:-len(subStr)])
					else:
						fullStr.append(forStr)
					forStr = ""
					forStr = subStr
				if x == "\n" and forStr != "":
					fullStr.append(forStr)
					forStr = ""
				if len(fullStr) * font.size(self.biggestLetter[1])[1] + (font.size(self.biggestLetter[1])[1] * 2) >= self.length[1] and goesUp == len(self.text) and forStr != "" and self.didCutInMid(forStr) == True:
					fullStr.append(forStr)
					return (fontSize,fullStr,len(fullStr))
				elif ((len(fullStr) * font.size(self.biggestLetter[1])[1]) + font.size(self.biggestLetter[1])[1]) >= self.length[1] and goesUp == len(self.text):
					fullStr.append(forStr)
					return (fontSize,fullStr,len(fullStr))
			goesUp = 0
			forStr = ""
			fullStr = []
			fontSize += 1

	def center(self):
		if len(self.fontStuffs[1]) == 1 or self.fontStuffs[1][1] == '':
			self.SURFACEFONT = []
			self.pastePos2 = []
			self.pos = (self.pos[0] + (self.length[0] - self.font.size(self.fontStuffs[1][0])[0])/2,self.pos[1] + (self.length[1] - self.font.size(self.fontStuffs[1][0])[1])/2)
			for y in range(self.fontStuffs[2]):
				self.SURFACEFONT.append(self.font.render(self.fontStuffs[1][y],True,self.textColor))
				self.pastePos2.append(self.pos[1] + (y * self.font.size(self.biggestLetter[1])[1]))
			self.pastePos = self.pos[0]+2
		else:
			print("from textBoxDisplay.center: More than one line detected; this should be used for things like buttons in menus.")

	def textBoxDisplay(self):
		if self.backgroundColor != None:
			pygame.draw.rect(self.screen, self.backgroundColor,self.rect)
		if self.boarderColor != None:
			pygame.draw.lines(self.screen,self.boarderColor,False,self.outlinePoints,2)
		for y in range(self.fontStuffs[2]):
			self.screen.blit(self.SURFACEFONT[y],(self.pastePos,self.pastePos2[y]))
			
