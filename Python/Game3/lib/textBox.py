import pygame,sys
pygame.init()

def rectPos(poss):
	return (poss[0],(poss[1][0]-poss[0][0],poss[1][1]-poss[0][1])) #returns 2 tuples inside a tuple that can be plugged into pygame.draw.rect()[

def rectOutline(poss,lineSize): #lineSize makes lines fit perfectly in imaginary box
	subtraction = lineSize - int(((lineSize/2.0)-1) + .5) #doesn't always paste line perfectly in the center of line

	return (poss[0],((poss[0][0]+(poss[1][0]-poss[0][0]))-subtraction,poss[0][1]),(poss[1][0]-subtraction,poss[1][1]-subtraction),(poss[0][0],poss[1][1]-subtraction),poss[0]) #returns 4 tuples inside 1 tuple that can be plugged in to pygame.draw.lines()
	
class Display:
	def __init__(self,coords=((100,100),(500,200)),text="Hello World!",backgroundColor=None,outlineColor=None,cutMidLine=False,fontType=None,textColor=(0,0,0),outlineSize=2):
		self.coords = coords
		self.fontType = fontType
		self.fontColor = textColor
		self.backgroundColor = backgroundColor
		self.outlineColor = outlineColor
		self.outlineSize = outlineSize
		self.cutMidLine = cutMidLine
		######GENERATED######
		self.textPlacementVar = outlineSize+1 #ensures that outline and text dont touch
		self.backgroundSize = (((coords[1][0]-coords[0][0])-(2*self.outlineSize))-self.textPlacementVar,(coords[1][1]-coords[0][1])-(2*self.outlineSize)) #extra stuff accounts for outline
		self.backgroundDraw = rectPos(coords)
		self.outlineDraw = rectOutline(coords,self.outlineSize)
		if fontType == None:
			self.fontString = "pygame.font.Font(None,fontSize)"
		elif '/' in fontType:
			self.fontString = "pygame.font.Font(self.fontType,fontSize)"
		else:
			self.fontString = "pygame.font.SysFont(self.fontType,fontSize)"
		self.text = self.textGenerate(text)

	def textGenerate(self,text): #returns images that can be blitted directly to the screen and the coords that they should be blitted at, all in a list
		fontSize = -1
		while 1:
			fontSize += 1
			font = eval(self.fontString)
			lines = []
			line = ""
			pH = 0 #placeHolder
			textLen = len(text)-1
			for x in text:
				line += x
				if pH == textLen: #doesn't let index get out of range on line 52 
					continue
				if x == "\n": #check for new line
					lines.append(line[:-1])
					line = ""
				if font.size(line+text[pH+1])[0] > self.backgroundSize[0]:
					if self.cutMidLine == False:
						tmp = ""
						pH2 = 0
						for x in line[::-1]: #reverses line
							pH2 += 1
							if x == " ":
								lines.append(line[:-pH2])
								line = tmp[::-1]
								break
							tmp += x
					else:
						lines.append(line)
						line = ""
				pH += 1

			if line != "": #for the last line of text that wouldn't be counted otherwise
				lines.append(line)

			for x in lines: #checks if text is big enough in x coord because the fontSize variable doesn't stop increasing after new line is decided
				if font.size(x)[0] > self.backgroundSize[0]:
					line = [] #sets off if statement on line 77

			pH = 0
			for x in lines:
				pH += font.size(x)[1]

			if pH > self.backgroundSize[1] or line == []: #checks if text is big enough in y coord or if its big enough in x coord.
				fontSize-=1
				font = eval(self.fontString)
				pasteCoords = []
				coords = list(self.coords[0])
				coords[0] += self.textPlacementVar
				for x in previousLines:
					pasteCoords.append(coords[:])
					coords[1] += font.size(x)[1]

				pH = 0
				for x in previousLines:
					previousLines[pH] = font.render(x,True,self.fontColor)
					pH += 1

				return zip(previousLines,pasteCoords) #previousLines and pasteCoords are going to be itterated over at the same time

			previousLines = lines[:]
	
	def center(self):
		unzip = zip(*self.text) #unzips self.text
		previousLines = list(unzip[0])
		pasteCoords = list(unzip[1])
		coords = list(self.coords[0])
		coords[0] += self.textPlacementVar
		pH = 0
		for x in previousLines: #centers in y coord
			pH += x.get_height()
		pH = int((self.backgroundSize[1]-pH)/2.0)
		pH2 = -1
		for x in pasteCoords:
			pH2 += 1
			pasteCoords[pH2][1] = x[1]+pH

		pH = -1
		for x in previousLines: #centers in x coord
			pH += 1
			pasteCoords[pH][0] = int(((self.backgroundSize[0]-x.get_width())/2.0))+pasteCoords[pH][0]

		self.text = zip(previousLines,pasteCoords)

	def run(self,screen):
		if self.backgroundColor != None:
			pygame.draw.rect(screen,self.backgroundColor,self.backgroundDraw)
		for x,y in self.text:
			screen.blit(x,y)
		if self.outlineColor != None:
			pygame.draw.lines(screen, self.outlineColor, False, self.outlineDraw, self.outlineSize)

class Input:
	def __init__(self,coords=((100,100),(200,125)),font="arial",fontColor=(0,0,0),backgroundColor=(255,255,255),outlineOffColor=(0,0,0),outlineOnColor=(0,255,255),outlineSize=2):
		self.coords = coords
		self.space = ((coords[1][0]-coords[0][0])-(outlineSize*2),(coords[1][1]-coords[0][1])-(outlineSize*2)) #space to fit text in
		if '/' in font:
			self.fontString = "pygame.font.Font('"+font+"',"
		else:
			self.fontString = "pygame.font.SysFont('"+font+"',"
		self.fontColor = fontColor
		self.backgroundColor = backgroundColor
		self.outlineColor = outlineOffColor
		self.outlineOffColor = outlineOffColor
		self.outlineOnColor = outlineOnColor
		self.outlineSize = outlineSize
		###########
		self.text = ""
		self.activeText = "" #text being displayed on the screen
		self.rapid = [0,1,False] #cache for self.rapidMethod()
		self.maxStrSize = 200
		#Generated#
		self.on = True
		self.active = False
		self.publicUnicode = ""
		self.blitTextCoords = (coords[0][0]+outlineSize,coords[0][1]+outlineSize)
		self.biggestLetters = self.biggestLetters()
		self.backgroundDraw = rectPos(coords)
		self.outlineDraw = rectOutline(coords,outlineSize)
		self.font = eval(self.fontString+str(self.fontSizeCalc())+')')
		self.textSurface = None #holds the surface to be blitted on screen
		self.textUpdate() #stores surface in self.textSurface
		self.cursor = ((-1,-1),(1,1))

	def biggestLetters(self):
		font = eval(self.fontString+"100)")
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

	def fontSizeCalc(self):
		fontSize = 0
		while 1:
			font = eval(self.fontString+"fontSize)")
			if font.size(self.biggestLetters[1])[1] > self.space[1]:
				return fontSize-1
			fontSize += 1
	
	def textUpdate(self): #adds or removes letters from self.text, and changes self.activeText and self.activeText
		if self.maxStrSize > len(self.text): #doesn't let to text get to long
			if self.publicUnicode == "\x08": #ASCII for backspace
				try: #doesn't let crash happen when backspace is pressed and no text remains
					self.text = self.text[:-1]
					self.activeText = self.activeText[:-1]
					len1 = len(self.text)
					len2 = len(self.activeText)
					newSeg = self.text[(len1-len2)-1]+self.activeText
					if len1 > len2 and self.font.size(newSeg)[0] <= self.space[0]:
						self.activeText = newSeg[:]
				except: pass
			else:
				self.text += self.publicUnicode
				self.activeText += self.publicUnicode
				if self.font.size(self.activeText)[0] <= self.space[0]:
					pass
				else:
					while 1:
						self.activeText = self.activeText[1:]
						if self.font.size(self.activeText)[0] <= self.space[0]:
							break

			self.textSurface = self.font.render(self.activeText,True,self.fontColor)

	def handler(self,event,mouse): #gets I/O
		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.coords[0][0] <= mouse[0] and self.coords[1][0] >= mouse[0] and self.coords[0][1] <= mouse[1] and self.coords[1][1] >= mouse[1]:
				#clicked inside of box
				self.active = True
				self.outlineColor = self.outlineOnColor
				#self.cursorCalc(mouse)
			else:
				self.active = False
				self.outlineColor = self.outlineOffColor
		elif self.active == True:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					self.on = False
				elif event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
					self.on = False
				elif event.key != pygame.K_ESCAPE and event.key != pygame.K_TAB and event.key != pygame.K_KP_ENTER:
					self.publicUnicode = event.unicode
					self.rapid[2] = True
					self.textUpdate()
			elif event.type == pygame.KEYUP:
				self.rapid[0] = 0
				self.rapid[2] = False
	
	def rapidMethod(self): #rapidly deletes and adds letters
		if self.rapid[2] == True:
			if self.rapid[0] == 10:
				self.textUpdate()
			else:
				self.rapid[0] += 1
	
	def draw(self,screen):
		self.rapidMethod()
		pygame.draw.rect(screen,self.backgroundColor,self.backgroundDraw)
		pygame.draw.lines(screen, self.outlineColor, False, self.outlineDraw, self.outlineSize)
		screen.blit(self.textSurface,self.blitTextCoords)
		#pygame.draw.rect(screen,(0,0,0),self.cursor)


'''	def cursorCalc(self,mouse): #calculates cursor dimensions based on where user clicked + coords for blitting (not in that order)
		pos = mouse[0]-(self.coords[0][0]+self.outlineSize)
		height = self.textSurface.get_height()-1
		pH = [0,0] #right, left
		pH2 = False
		print(self.textSurface.get_width(),self.textSurface.get_height(),"hey")
		pygame.image.save(self.textSurface,"boopz.png")
		while 1:
			pH2 = False
			for y in range(height):
				if self.textSurface.get_at((pos+pH[0],y))[3] > 0:
					pH2 = True
			if pH2 == False:
				break
			pH[0] += 1
		pH2 = False
		while 1:
			pH2 = False
			for y in range(height):
				if self.textSurface.get_at((pos-pH[1],y))[3] > 0:
					pH2 = True
			if pH2 == False:
				break
			pH[1] += 1
		pH2 = 0
		if pH[0] > pH[1]:
			pos -= pH[1]
			crap = True
			while crap == True:
				for y in range(height):
					if self.textSurface.get_at((pos-pH2,y))[3] != 0: #if pixel is not completely transparent
						crap = False
						break
				pH2 += 1
			pos -= pH2

		else:
			pos += pH[0]
			crap = True
			while crap == True:
				for y in range(height):
					print("HEY")
					if self.textSurface.get_at((pos+pH2,y))[3] != 0:
						print("POOP")
						crap = False
				pH2 += 1
			pos += pH2
		self.cursor = ((pos+self.coords[0][0],self.coords[0][1]+self.outlineSize),(pH2,height+1))
'''

class scrollBar:
	def __init__(self,coords=((100,100),(500,200)),text="Hello World!",fontSize=24,fontType=None,scrollBarWidth=5,textColor=(0,0,0),backgroundColor=(255,255,255),outlineColor=(0,0,0),outlineSize=2):
		self.coords = coords
		self.fontType = fontType
		self.fontColor = textColor
		self.backgroundColor = backgroundColor
		self.outlineColor = outlineColor
		self.outlineSize = outlineSize
		######GENERATED######
		self.textPlacementVar = outlineSize+1 #ensures that outline and text dont touch
		self.backgroundSize = [((coords[1][0]-coords[0][0])-(2*self.outlineSize))-self.textPlacementVar,(coords[1][1]-coords[0][1])-(2*self.outlineSize)] #extra stuff accounts for outline
		self.scrollBarBlit = [[coords[0][0]+self.backgroundSize[0],coords[0][1]+self.outlineSize],[scrollBarWidth,0]] #zero will be filled in!
		self.backgroundDraw = rectPos(coords)
		self.outlineDraw = rectOutline(coords,self.outlineSize)
		if fontType == None:
			self.fontString = "pygame.font.Font(None,fontSize)"
		elif '/' in fontType:
			self.fontString = "pygame.font.Font(self.fontType,fontSize)"
		else:
			self.fontString = "pygame.font.SysFont(self.fontType,fontSize)"
		self.allSurfaceText = []
		self.visibleSurfaceText = []
		self.pasteCoords = []
		self.visiblePasteCoords = []
		self.fullTextYLength = 0
		self.visibleTextYLength = 0
		self.textGenerate(text,fontSize)
		self.textLoopThrough = zip(self.visibleSurfaceText,self.pasteCoords)
		self.scrollBarBlit[1][1] = int(((self.visibleTextYLength/float(self.fullTextYLength))*self.backgroundSize[1])+.5)
		self.down = [False,0]
		print(self.scrollBarBlit)
		print(self.backgroundSize[1])

	def textGenerate(self,text,fontSize): #returns images that can be blitted directly to the screen and the coords that they should be blitted at, all in a list
		font = eval(self.fontString)
		lines = []
		line = ""
		pH = 0 #placeHolder
		textLen = len(text)-1
		for x in text:
			line += x
			if pH == textLen: #doesn't let index get out of range on line 52 
				continue
			if x == "\n": #check for new line
				lines.append(line[:-1])
				line = ""
			if font.size(line+text[pH+1])[0] > self.backgroundSize[0]: #checks if line is about to get to long, if so it creates a new one
				tmp = "" #the following stops words from cutting in the middle on a new line
				pH2 = 0
				for x in line[::-1]: #reverses line
					pH2 += 1
					if x == " ":
						lines.append(line[:-pH2])
						line = tmp[::-1]
						break
					tmp += x
			pH += 1

		if line != "": #for the last line of text that wouldn't be counted otherwise
			lines.append(line)

		pasteCoords = []
		coords = list(self.coords[0])
		coords[0] += self.textPlacementVar
		for x in lines:
			pasteCoords.append(coords[:])
			pH2 = font.size(x)[1]
			self.fullTextYLength += pH2
			coords[1] += pH2

		pH = 0
		for x in lines:
			lines[pH] = font.render(x,True,self.fontColor)
			pH += 1

		pH = 0
		pH2 = 0
		for x in lines:
			pH += x.get_height()
			if pH>self.backgroundSize[1]:
				break
			else:
				self.visibleSurfaceText.append(x)
				self.visibleTextYLength += x.get_height()

		self.allSurfaceText = lines[:]
		self.pasteCoords = pasteCoords[:]
		self.visiblePasteCoords = pasteCoords[:-(len(self.allSurfaceText)-len(self.visibleSurfaceText))]
	
	def handler(self,event,mouse):
		if event.type == MOUSEBUTTONDOWN and mouse[0] >= self.scrollBarBlit[0][0] and mouse[0] <= self.scrollBarBlit[0][0]+self.scrollBarBlit[1][0] and mouse[1] >= self.scrollBarBlit[0][1] and mouse[1] <= self.scrollBarBlit[0][1]+self.scrollBarBlit[1][1]:
			self.down[0] = True
		elif event.type == MOUSEBUTTONUP:
			self.down[0] = False
	
	def scrollBarChange(mouse):
		if self.down[0] == True:
			rel = pygame.mouse.get_rel()[1]
			if rel != 0:
				pass

	def center(self):
		unzip = zip(*self.text) #unzips self.text
		previousLines = list(unzip[0])
		pasteCoords = list(unzip[1])
		coords = list(self.coords[0])
		coords[0] += self.textPlacementVar
		pH = 0
		for x in previousLines: #centers in y coord
			pH += x.get_height()
		pH = int((self.backgroundSize[1]-pH)/2.0)
		pH2 = -1
		for x in pasteCoords:
			pH2 += 1
			pasteCoords[pH2][1] = x[1]+pH

		pH = -1
		for x in previousLines: #centers in x coord
			pH += 1
			pasteCoords[pH][0] = int(((self.backgroundSize[0]-x.get_width())/2.0))+pasteCoords[pH][0]

		self.text = zip(previousLines,pasteCoords)

	def run(self,screen):
		if self.backgroundColor != None:
			pygame.draw.rect(screen,self.backgroundColor,self.backgroundDraw)
		for x,y in self.textLoopThrough:
			screen.blit(x,y)
		if self.outlineColor != None:
			pygame.draw.lines(screen, self.outlineColor, False, self.outlineDraw, self.outlineSize)
		pygame.draw.rect(screen,(0,255,0),self.scrollBarBlit)
