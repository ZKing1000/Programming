import pygame,sys
pygame.init()

def rectPos(poss):
	return (poss[0],(poss[1][0]-poss[0][0],poss[1][1]-poss[0][1])) #returns 2 tuples inside a tuple that can be plugged into pygame.draw.rect()[

def rectOutline(poss,lineSize): #lineSize makes lines fit perfectly in imaginary box
	subtraction = lineSize - int(((lineSize/2.0)-1)+.5) #doesn't always paste line perfectly in the center of line

	return (poss[0],((poss[0][0]+(poss[1][0]-poss[0][0]))-subtraction,poss[0][1]),(poss[1][0]-subtraction,poss[1][1]-subtraction),(poss[0][0],poss[1][1]-subtraction),poss[0]) #returns 4 tuples inside 1 tuple that can be plugged in to pygame.draw.lines()
	
class Display:
	def __init__(self,coords=((100,100),(500,200)),text="Hello World!",cutMidLine=True,fontType=None,textColor=(0,0,0),backgroundColor=(255,255,255),outlineColor=(0,0,0),outlineSize=2):
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

			for x in lines: #checks if text is big enough in x coord
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
				self.cursorCalc(mouse)
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

	def cursorCalc(self,mouse): #calculates cursor dimensions based on where user clicked + coords for blitting (not in that order)
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

	def draw(self,screen):
		self.rapidMethod()
		pygame.draw.rect(screen,self.backgroundColor,self.backgroundDraw)
		pygame.draw.lines(screen, self.outlineColor, False, self.outlineDraw, self.outlineSize)
		screen.blit(self.textSurface,self.blitTextCoords)
		pygame.draw.rect(screen,(0,0,0),self.cursor)







screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
#coords=((100,100),(500,200)),text="Hello World!",cutMidLine=True,fontType=None,textColor=(0,0,0),backgroundColor=(255,255,255),outlineColor=(0,0,0)
textBox = Display(((100,100),(200,500)),"Hey person how are you doing?")
textBox2 = Display(((200,100),(300,500)),"Hey person how are you doing?",False,None,(255,255,255),(0,0,0),(100,100,100))
textBox3 = Display(((300,100),(400,500)),"Hey person how are you doing?",False,None,(255,0,0),(0,255,0),(0,0,255))
textBox3.center()
textBox4 = Display(((400,100),(1100,150)),"The quick brown fox jumps over the lazy dog.",True,"../minecraftia/Minecraftia.ttf")
textBox5 = Display(((400,150),(1100,200)),"The quick brown fox jumps over the lazy dog.",False,"../minecraftia/Minecraftia.ttf",(255,255,255),(0,0,0),(100,100,100))
textBox5.center()
textBox6 = Display(((400,200),(1100,250)),"The quick brown fox jumps over the lazy dog.",False,"../minecraftia/Minecraftia.ttf",(0,0,255),None,None)
textBox6.center()
textBox7 = Display(((400,250),(1100,500)),"d")
#textBox8 = Display(((800,100),(900,500)),"minecraft is good and you")
#textBox9 = Display(((900,100),(1000,500)),"minecraft is good and you")
#textBox10 = Display(((1000,100),(1100,500)),"minecraft is good and you")
textBox11 = Display(((200,500),(400,600)),"Hello World!",False,"arial",(0,0,0))
textBox11.center()
inputBox = Input(((100,600),(800,700)))
inputBox.text = "default"
inputBox.activeText = "default"
inputBox.textUpdate()
font = pygame.font.Font("../minecraftia/SourceCodePro-Medium.ttf",20)
crap = font.render('f',True,(0,0,0))
crap2 = rectOutline(((10,10),(crap.get_width()+10,crap.get_height()+10)),2)
print(crap.get_width(),crap.get_height())
print(crap.get_at((1,10)))
#77
#1
poop = ""
deleting = False
bloob = 0
boomz = 0
while 1:
	clock.tick(30)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.image.save(screen,"screenshot.png")
			sys.exit()
			pygame.quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_BACKSPACE:
				poop = poop[:-1]
				textBox7 = Display(((400,250),(1100,500)),poop,False)
				deleting = True
			else:
				poop += event.unicode
				textBox7 = Display(((400,250),(1100,500)),poop,False)
		elif event.type == pygame.KEYUP:
			deleting = False
			bloob = 0
		inputBox.handler(event,pygame.mouse.get_pos())
	
	if deleting == True and bloob == 10:
		poop = poop[:-1]
		textBox7 = Display(((400,250),(1100,500)),poop,False)
		bloob = 0
	elif deleting == True:
		bloob += 1
	
	if boomz == 10:
		poop += 'm'
		textBox7 = Display(((400,250),(1100,500)),poop,True)
		boomz = 0
	else:
		boomz += 1

	screen.fill((255,0,0))
	textBox.run(screen)
	textBox2.run(screen)
	textBox3.run(screen)
	textBox4.run(screen)
	textBox5.run(screen)
	textBox6.run(screen)
	textBox7.run(screen)
	#textBox8.run(screen)
	#textBox9.run(screen)
	#textBox10.run(screen)
	textBox11.run(screen)
	inputBox.draw(screen)
	pygame.draw.lines(screen,(255,255,255),False,crap2,1)
	screen.blit(crap,(10,10))
	pygame.display.update()
