import pygame,sys,collisionDetection,textBox,saves,math
import resourceHandling as resource
from PIL import Image
pygame.init()
#<CONSTANTS>#
optionsLocation = "../saved/options.txt"
font = "../resources/fonts/SourceCodePro-Medium.otf"
r = [960,540] #base resolution of game (scaling not considered)
#</CONSTANTS>#
class Main():
	def __init__(self):
		self.on = 1
		saves.crashRecovery(optionsLocation)
		saves.refresh(optionsLocation,["resolution:fullscreen"])
		print(saves.read(optionsLocation,"resolution"),"saves.read")
		tmp = saves.read(optionsLocation,"resolution")
		if tmp == "fullscreen": #incase game broke while in fullscreen
			self.defaultResolution = r[:]
			self.screen = pygame.display.set_mode(resource.screenSize,pygame.FULLSCREEN)
		else:
			self.defaultResolution = [int(tmp.split("x")[0]),int(tmp.split("x")[1])]
			self.screen = pygame.display.set_mode(resource.screenSize)

		self.mode = "self.mainMenu()"
		if self.defaultResolution == "fullscreen":
			self.screen = pygame.display.set_mode(resource.screenSize,pygame.FULLSCREEN)
		else:
			self.screen = pygame.display.set_mode(resource.screenSize)

		self.defaultResolutionStr = "resolution:"+str(self.defaultResolution[0])+"x"+str(self.defaultResolution[1])
		self.clock = pygame.time.Clock()
		self.savedFile = None #what world is going to be used changed at self.play()
		self.location = None		

	def savedWorldInterpret():
		location = "../saved/worlds/" + self.savedFile + "/all.txt"
		if saves.exists(location) == False:
			saves.mkfile(location)
			saves.write(location,"money:0")
			saves.write(location,"level:0")
			saves.write(location,"stage:0")
			saves.write(location,"details:None")



	def mainMenu(self):
		on = 1
		button1a1 = resource.pastePos((r[0]/2)-(r[0]/8),(r[1]/2)-(r[1]/32))
		button1a2 = resource.pastePos((r[0]/2)+(r[0]/8),(r[1]/2)+(r[1]/32))
		button1a3 = (button1a2[0]-button1a1[0],button1a2[1]-button1a1[1])
		button2a1 = (button1a1[0],button1a1[1]+int((button1a3[1]*1.5)))
		button2a2 = (button1a2[0],(button2a1[1]+button1a3[1]))
		button2a3 = (button2a2[0]-button2a1[0],button2a2[1]-button2a1[1])
		button1Text = textBox.textBoxDisplay(self.screen,button1a1,button1a2,"../resources/fonts/SourceCodePro-Medium.otf",None,(0,0,0),None,True,"Play")
		button2Text = textBox.textBoxDisplay(self.screen,button2a1,button2a2,"../resources/fonts/SourceCodePro-Medium.otf",None,(0,0,0),None,True,"Options")
		fullscreenInfoText = textBox.textBoxDisplay(self.screen,(0,0),resource.pastePos(r[0]/3,r[1]/8.0),font,None,(0,0,0),None,False,"Press esc to toggle fullscreen. Default resolution can be changed in options. Press 'b' to move one step back in the menu.")
		button1Text.center()
		button2Text.center()
		while on == 1:
			self.clock.tick(30)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.on = 0
					on = 0
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if collisionDetection.rectangular(button1a1,button1a2) == True:
						self.mode = "self.play()"
						on = 0
					elif collisionDetection.rectangular(button2a1,button2a2) == True:
						self.mode = "self.options()"
						on = 0
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						if saves.read("../saved/options.txt","resolution") == "fullscreen":
							saves.write(optionsLocation,self.defaultResolutionStr)
						else:
							saves.write(optionsLocation,"resolution:fullscreen")

						pygame.display.quit() #So that resource gets monitor resolution as apposed to screen size.
						reload(resource) #Reloads resourceHandling.py, because resolution is changed.
						pygame.display.init()
						self.screen = pygame.display.set_mode(resource.screenSize)
						button1a1 = resource.pastePos((r[0]/2)-(r[0]/8),(r[1]/2)-(r[1]/32))
						button1a2 = resource.pastePos((r[0]/2)+(r[0]/8),(r[1]/2)+(r[1]/32))
						button1a3 = (button1a2[0] - button1a1[0],button1a2[1] - button1a1[1])
						button2a1 = (button1a1[0],button1a1[1] + int((button1a3[1] * 1.5)))
						button2a2 = (button1a2[0],(button2a1[1] + button1a3[1]))
						button2a3 = (button2a2[0] - button2a1[0],button2a2[1] - button2a1[1])
						button1Text = textBox.textBoxDisplay(self.screen,button1a1,button1a2,font,None,(0,0,0),None,True,"Play")
						button2Text = textBox.textBoxDisplay(self.screen,button2a1,button2a2,font,None,(0,0,0),None,True,"Options")
						fullscreenInfoText = textBox.textBoxDisplay(self.screen,(0,0),resource.pastePos(r[0]/3,r[1]/8.0),font,None,(0,0,0),None,False,"Press esc to toggle fullscreen. Default resolution can be changed in options. Press 'b' to move one step back in the menu.")

						button1Text.center()
						button2Text.center()
						if saves.read(optionsLocation,"resolution") == "fullscreen":
							self.screen = pygame.display.set_mode(resource.screenSize,pygame.FULLSCREEN)
						
			self.screen.fill((255,0,0))
			color1 = (100,100,100)
			color2 = (100,100,100)
			if collisionDetection.rectangular(button1a1,button1a2) == True:
				color1 = (50,50,50)
			elif collisionDetection.rectangular(button2a1,button2a2) == True:
				color2 = (50,50,50)

			pygame.draw.rect(self.screen,color1,(button1a1,button1a3))
			pygame.draw.rect(self.screen,color2,(button2a1,button2a3))
			button1Text.textBoxDisplay()
			button2Text.textBoxDisplay()
			fullscreenInfoText.textBoxDisplay()
			pygame.display.update()

	def options(self):
		on = 1
		title = textBox.textBoxDisplay(self.screen,(0,0),resource.pastePos(r[0],r[1]/8.0),font,None,(255,255,255),None,True,"Options")
		title.center()
		while on == 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.on = 0
					on = 0
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_b:
						self.mode = "self.mainMenu()"
						on = 0

			self.screen.fill((255,0,0))
			title.textBoxDisplay()
			pygame.display.update()


	def play(self):
		on = 1
		worlds = saves.getWorlds() #returns list of strings
		worldButtons = [[]] #Seperates collumns by lists filled of strings from worlds
		goesUp = 0 #used by following for loop
		for x in worlds:
			worldButtons[goesUp].append(x)
			if resource.pastePos(r[0],((r[1]/8)*7)/len(worldButtons[goesUp]))[1] < 40: #if indivisual world button is shorter than 40 pixels
				worldButtons.append([])
				goesUp += 1 #goesUp seperates collumns

		screenSize = resource.screenSize
		ID = 0 #each worldButton has an ID used when blitting them
		worldButtonCoords = [[],[]] #[0] is is left corner and [1] is right. check MOUSEBUTTONDOWN event for usage
		goesUp2 = 0 #used by following for loop
		for x in worldButtons: #All this figures out how to divide the screen up into world buttons.
			pastePos = ((screenSize[0]/len(worldButtons)) * goesUp2,0) #upper left corner
			goesUp2 += 1
			for y in range(len(x)):
				secondPos = ((screenSize[0]/len(worldButtons)) * goesUp2,(y + 1) * ((screenSize[1] - (screenSize[1]/8.0))/len(x)))
				worldButtonCoords[0].append(pastePos)
				worldButtonCoords[1].append(secondPos)
				exec("worldButton" + str(ID) + " = textBox.textBoxDisplay(self.screen," + str(pastePos) + "," + str(secondPos) + ",font,(163,82,52),(0,0,0),(255,255,255),False,"+"'"+x[y]+"')")
				eval("worldButton" + str(ID) + ".center()")
				pastePos = (pastePos[0],pastePos[1]+((screenSize[1]-(screenSize[1]/8))/len(x))) #I have to do it with a tuple, because weird stuff.
				ID += 1

		button1a1 = resource.pastePos(0,(r[1]/8.0)*7)
		button1a2 = resource.pastePos(r[0]/3.0,r[1])
		button2a1 = resource.pastePos(r[0]/3.0,(r[1]/8.0)*7)
		button2a2 = resource.pastePos((r[0]/3.0)*2,r[1])
		button3a1 = resource.pastePos((r[0]/3.0)*2,(r[1]/8.0)*7)
		button3a2 = resource.pastePos(r[0],r[1])
		worldSelectHighlight = ""
		button1Text = textBox.textBoxDisplay(self.screen,button1a1,button1a2,font,(90,90,90),(0,0,0),(0,0,0),True,"Play")
		button2Text = textBox.textBoxDisplay(self.screen,button2a1,button2a2,font,(90,90,90),(0,0,0),(0,0,0),True,"New World")
		button3Text = textBox.textBoxDisplay(self.screen,button3a1,button3a2,font,(90,90,90),(0,0,0),(0,0,0),True,"Delete")

		button1Text.center()
		button2Text.center()
		button3Text.center()
		delete = False
		while on == 1:
			self.clock.tick(30)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.on = 0
					on = 0
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						if saves.read(optionsLocation,"resolution") == "fullscreen":
							saves.write(optionsLocation,self.defaultResolutionStr)
						else:
							saves.write(optionsLocation,"resolution:fullscreen")

						pygame.display.quit()
						reload(resource)
						reload(collisionDetection)
						pygame.init()
						self.screen = pygame.display.set_mode(resource.screenSize)
						worlds = saves.getWorlds() #returns list of strings
						worldButtons = [[]] #Seperates collumns by lists filled of strings from worlds
						goesUp = 0 #used by following for loop
						for x in worlds:
							worldButtons[goesUp].append(x)
							if resource.pastePos(r[0],((r[1]/8)*7)/len(worldButtons[goesUp]))[1] < 40: #if indivisual world button is shorter than 40 pixels
								worldButtons.append([])
								goesUp += 1 #goesUp seperates collumns

						screenSize = resource.screenSize
						ID = 0 #each worldButton has an ID used when blitting them
						worldButtonCoords = [[],[]] #[0] is is left corner and [1] is right. check MOUSEBUTTONDOWN event for usage
						goesUp2 = 0 #used by following for loop
						for x in worldButtons: #All this figures out how to divide the screen up into world buttons.
							pastePos = ((screenSize[0]/len(worldButtons)) * goesUp2,0) #upper left corner
							goesUp2 += 1
							for y in range(len(x)):
								secondPos = ((screenSize[0]/len(worldButtons)) * goesUp2,(y + 1) * ((screenSize[1] - (screenSize[1]/8.0))/len(x)))
								worldButtonCoords[0].append(pastePos)
								worldButtonCoords[1].append(secondPos)
								exec("worldButton"+str(ID)+" = textBox.textBoxDisplay(self.screen,"+str(pastePos)+","+str(secondPos)+",font,(163,82,52),(0,0,0),(255,255,255),False,"+"'"+x[y]+"')")
								eval("worldButton"+str(ID)+".center()")
								pastePos = (pastePos[0],pastePos[1]+((screenSize[1]-(screenSize[1]/8))/len(x))) #I have to do it with a tuple, because weird stuff.
								ID += 1

						button1a1 = resource.pastePos(0,(r[1]/8.0)*7)
						button1a2 = resource.pastePos(r[0]/3.0,r[1])
						button2a1 = resource.pastePos(r[0]/3.0,(r[1]/8.0)*7)
						button2a2 = resource.pastePos((r[0]/3.0)*2,r[1])
						button3a1 = resource.pastePos((r[0]/3.0)*2,(r[1]/8.0)*7)
						button3a2 = resource.pastePos(r[0],r[1])
						worldSelectHighlight = ""
						button1Text = textBox.textBoxDisplay(self.screen,button1a1,button1a2,font,(90,90,90),(0,0,0),(0,0,0),True,"Play")
						button2Text = textBox.textBoxDisplay(self.screen,button2a1,button2a2,font,(90,90,90),(0,0,0),(0,0,0),True,"New World")
						button3Text = textBox.textBoxDisplay(self.screen,button3a1,button3a2,font,(90,90,90),(0,0,0),(0,0,0),True,"Delete")

						button1Text.center()
						button2Text.center()
						button3Text.center()
						if saves.read(optionsLocation,"resolution") == "fullscreen":
							self.screen = pygame.display.set_mode(screenSize,pygame.FULLSCREEN)
					elif event.key == pygame.K_b:
						self.mode = "self.mainMenu()"
						on = 0

				elif event.type == pygame.MOUSEBUTTONDOWN:
					if collisionDetection.rectangular(button1a1,button1a2) == True and delete != False:
						self.savedFile = delete
						self.location = "../saved/worlds/" + self.savedFile + "/all.txt"
						if saves.exists(self.location) == False:
							saves.mkfile(self.location)
							saves.write(self.location,"money:0")
							saves.write(self.location,"level:0")
							saves.write(self.location,"details:None") #what is pertinent to stage like lives when left off in maze, 2 lines down
							self.mode = "self.drawSprite()"
							saves.write(self.location,"stage:self.drawSprite()")
							
						else:
							self.mode = saves.read(self.location,"stage")


						on = 0
					elif collisionDetection.rectangular(button2a1,button2a2) == True:
						self.mode = "self.createWorld()"
						on = 0
					elif collisionDetection.rectangular(button3a1,button3a2) == True:
							if delete != False:
								saves.rmdir("../saved/worlds/"+delete)
								delete = False
								worlds = saves.getWorlds()
								worldButtons = [[]] #Seperates collumns by lists filled of strings from worlds
								goesUp = 0 #used by following for loop
								for x in worlds:
									worldButtons[goesUp].append(x)
									if resource.pastePos(r[0],((r[1]/8)*7)/len(worldButtons[goesUp]))[1] < 40: #if indivisual world button is shorter than 40 pixels
										worldButtons.append([])
										goesUp += 1 #goesUp seperates collumns

								screenSize = resource.screenSize
								ID = 0 #each worldButton has an ID used when blitting them
								worldButtonCoords = [[],[]] #[0] is is left corner and [1] is right. check MOUSEBUTTONDOWN event for usage
								goesUp2 = 0 #used by following for loop
								for x in worldButtons: #All this figures out how to divide the screen up into world buttons.
									pastePos = ((screenSize[0]/len(worldButtons)) * goesUp2,0) #upper left corner
									goesUp2 += 1
									for y in range(len(x)):
										secondPos = ((screenSize[0]/len(worldButtons)) * goesUp2,(y + 1) * ((screenSize[1] - (screenSize[1]/8.0))/len(x)))
										worldButtonCoords[0].append(pastePos)
										worldButtonCoords[1].append(secondPos)
										exec("worldButton"+str(ID) + " = textBox.textBoxDisplay(self.screen,"+str(pastePos)+","+str(secondPos)+",font,(163,82,52),(0,0,0),(255,255,255),False,"+"'"+x[y]+"')")
										eval("worldButton" + str(ID) + ".center()")
										pastePos = (pastePos[0],pastePos[1]+((screenSize[1]-(screenSize[1]/8))/len(x))) #I have to do it with a tuple, because weird stuff.
										ID += 1

					for x in range(len(worldButtonCoords[0])): #highlights worldButton when pressed
						if collisionDetection.rectangular(worldButtonCoords[0][x],worldButtonCoords[1][x]) == True:
							print(x)
							print(worlds)
							delete = worlds[x]
							worldSelectHighlight = "pygame.draw.rect(self.screen,(233,233,233),pygame.Rect((worldButtonCoords[0]["+str(x)+"],(worldButtonCoords[1]["+str(x)+"][0]-worldButtonCoords[0]["+str(x)+"][0],int((worldButtonCoords[1]["+str(x)+"][1]-worldButtonCoords[0]["+str(x)+"][1])+.5)))))"
							print(worldSelectHighlight)
							break
			
			self.screen.fill((0,0,100))
			button1Text.backgroundColor = (90,90,90)
			button2Text.backgroundColor = (90,90,90)
			button3Text.backgroundColor = (90,90,90)
			if collisionDetection.rectangular(button1a1,button1a2) == True:
				button1Text.backgroundColor = (120,120,120)
			elif collisionDetection.rectangular(button2a1,button2a2) == True:
				button2Text.backgroundColor = (120,120,120)
			elif collisionDetection.rectangular(button3a1,button3a2) == True:
				button3Text.backgroundColor = (120,120,120)

			button1Text.textBoxDisplay()
			button2Text.textBoxDisplay()
			button3Text.textBoxDisplay()
			for x in range(ID): #blits all world buttons
				eval("worldButton"+str(x)+".textBoxDisplay()")

			try:
				exec(worldSelectHighlight) #Highlights selected worlds
			except:
				pass
			pygame.display.update()

	def createWorld(self):
		on = 1
		textBoxInput = textBox.textBoxInput(self.screen,self.clock,resource.pastePos((r[0]/3.0),(r[1]-(r[1]/16.0))/2.0),resource.pastePos((r[0]/3.0)*2,(r[1]/2.0)+((r[1]/16.0)/2.0)),font,200,(255,255,255),(0,0,0),(0,0,0),(255,0,0))
		while on == 1:
			self.clock.tick(30)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.on = 0
					on = 0
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						if saves.read(optionsLocation,"resolution") == "fullscreen":
							saves.write(optionsLocation,self.defaultResolutionStr)
						else:
							saves.write(optionsLocation,"resolution:fullscreen")

						pygame.display.quit()
						reload(resource)
						pygame.init()
						self.screen = pygame.display.set_mode(resource.screenSize)
						textBoxInput = textBox.textBoxInput(self.screen,self.clock,resource.pastePos((r[0]/3.0),(r[1]-(r[1]/16.0))/2.0),resource.pastePos((r[0]/3.0)*2,(r[1]/2.0)+((r[1]/16.0)/2.0)),optionsLocation,200,(255,255,255),(0,0,0),(0,0,0),(0,0,255),"")
						if saves.read("../saved/options.txt","resolution") == "fullscreen":
							self.screen = pygame.display.set_mode(resource.screenSize,pygame.FULLSCREEN)
					elif textBoxInput.on == False and event.key == pygame.K_b: #first parameter allows 'b' to be typed in test box without going back in menu
						self.mode = "self.play()"
						on = 0

				textBoxInput.handler(event)

			if textBoxInput.textBoxInput() != None:
				saves.mkdir("../saved/worlds/" + textBoxInput.textBoxInput())
				self.mode = "self.play()"
				on = 0

			self.screen.fill((0,0,255))
			textBoxInput.textBoxInput()
			pygame.display.update()

	def drawSprite(self):
		on = 1
		didClickOnDone = False
		doneButton1a1 = resource.pastePos((r[1]/8.0)/8.0,(r[1]/8.0)/8.0 + ((r[1]/8.0) * 7))
		doneButton1a2 = resource.pastePos(r[0]/6.0,(((r[1]/8.0)/8.0) * 7) + ((r[1]/8.0) * 7))
		bottomRect1a1 = resource.pastePos(0,(r[1]/8.0) * 7)
		bottomRect1a2 = resource.pastePos(r[0],r[1])
		bottomRect = resource.rectPos(bottomRect1a1,bottomRect1a2)
		bottomOutline = resource.rectOutline(bottomRect1a1,bottomRect1a2)
		upperText = textBox.textBoxDisplay(self.screen,(0,0),resource.pastePos(r[0],r[1]/8.0),font,(255,255,255),(0,0,0),(0,0,0),True,"Draw your character!")
		upperText.center()
		doneButtonText = textBox.textBoxDisplay(self.screen,doneButton1a1,doneButton1a2,font,(40,30,90),(0,0,0),(0,0,0),True,"Done")
		doneButtonText.center()
		#draw grid start
		#                              how much of the screen we have           plus position
		drawGridStart = ((r[0] - (32 * 10.5))/2.0,((((r[1]/4.0) * 3) - (10.5 * 32))/2.0) + r[1]/8.0)
		drawGridStart = resource.pastePos(drawGridStart[0],drawGridStart[1])
		indivisualSize = resource.pastePos(10.5,10.5) #Size of any particular pixel in pixels
		print(indivisualSize)
		drawGridEnd = (drawGridStart[0] + (indivisualSize[0] * 32),drawGridStart[1] + (indivisualSize[1] * 32))
		drawGridOutline = resource.rectOutline((drawGridStart[0] - 2,drawGridStart[1] -2),(drawGridEnd[0] + 2,drawGridEnd[1] + 2))
		previous = [0,0] #used for positions while drawing grid
		selectedColor = [255,150,0]
		coloring = [] #coloring for all pixels
		wasPressed = False #turns into a list with position of the colored pixel when pressed
		#stop
		rgbColorTextBox = textBox.textBoxInput(self.screen,self.clock,resource.pastePos((r[0]/4.0)/8.0,((r[1]/8.0) + ((r[1] - (r[1]/4.0))/2.0)) - 18.75),resource.pastePos(((r[0]/4.0)/8.0)*7,((r[1]/8.0) + ((r[1] - (r[1]/4.0))/2.0)) + 18.75),font,200,(255,255,255),(0,0,0),(0,0,0),(0,0,255),"255,255,255")
		rgbColorTextBox.isDone = True
		eraseInfoTextBox = textBox.textBoxDisplay(self.screen,resource.pastePos((r[0] - (32 * 10.5))/2.0,r[1]/8.0),resource.pastePos(((r[0] - (32 * 10.5))/2.0)+(10.5*32),((((r[1]/4.0) * 3) - (10.5 * 32))/2.0) + r[1]/8.0),font,None,(255,0,0),None,True,"Press 'r' to toggle erase mode.")
		eraseMode = False
		while on == 1:
			self.clock.tick(30)
			mousepos = pygame.mouse.get_pos()			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.on = 0
					on = 0
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						if saves.read(optionsLocation,"resolution") == "fullscreen":
							saves.write(optionsLocation,self.defaultResolutionStr)
						else:
							saves.write(optionsLocation,"resolution:fullscreen")

						pygame.display.quit()
						reload(resource)
						reload(collisionDetection)
						pygame.init()
						self.screen = pygame.display.set_mode(resource.screenSize)
						didClickOnDone = False
						doneButton1a1 = resource.pastePos((r[1]/8.0)/8.0,(r[1]/8.0)/8.0+((r[1]/8.0)*7))
						doneButton1a2 = resource.pastePos(r[0]/6.0,(((r[1]/8.0)/8.0)*7)+((r[1]/8.0)*7))
						bottomRect1a1 = resource.pastePos(0,(r[1]/8.0)*7)
						bottomRect1a2 = resource.pastePos(r[0],r[1])
						bottomRect = resource.rectPos(bottomRect1a1,bottomRect1a2)
						bottomOutline = resource.rectOutline(bottomRect1a1,bottomRect1a2)
						upperText = textBox.textBoxDisplay(self.screen,(0,0),resource.pastePos(r[0],r[1]/8.0),font,(255,255,255),(0,0,0),(0,0,0),True,"Draw your character!")
						upperText.center()
						doneButtonText = textBox.textBoxDisplay(self.screen,doneButton1a1,doneButton1a2,font,(40,30,90),(0,0,0),(0,0,0),True,"Done")
						doneButtonText.center()
						#draw grid start
						#                              how much of the screen we have           plus position
						drawGridStart = ((r[0]-(32*10.5))/2.0,((((r[1]/4.0)*3)-(10.5*32))/2.0)+r[1]/8.0)
						drawGridStart = resource.pastePos(drawGridStart[0],drawGridStart[1])
						indivisualSize = resource.pastePos(10.5,10.5)
						drawGridEnd = (drawGridStart[0]+(indivisualSize[0]*32),drawGridStart[1]+(indivisualSize[1]*32))
						drawGridOutline = resource.rectOutline((drawGridStart[0]-2,drawGridStart[1]-2),(drawGridEnd[0]+2,drawGridEnd[1]+2))
						#stop
						rgbColorTextBox = textBox.textBoxInput(self.screen,self.clock,resource.pastePos((r[0]/4.0)/8.0,((r[1]/8.0)+((r[1]-(r[1]/4.0))/2.0))-18.75),resource.pastePos(((r[0]/4.0)/8.0)*7,((r[1]/8.0)+((r[1]-(r[1]/4.0))/2.0))+18.75),font,200,(255,255,255),(0,0,0),(0,0,0),(0,0,255),"255,255,255")
						rgbColorTextBox.isDone = True
						eraseInfoTextBox = textBox.textBoxDisplay(self.screen,resource.pastePos((r[0]-(32*10.5))/2.0,r[1]/8.0),resource.pastePos(((r[0]-(32*10.5))/2.0)+(10.5*32),((((r[1]/4.0)*3)-(10.5*32))/2.0)+r[1]/8.0),font,None,(255,0,0),None,True,"Press 'r' to toggle erase mode.")
						eraseMode = False
						if saves.read(optionsLocation,"resolution") == "fullscreen":
							self.screen = pygame.display.set_mode(resource.screenSize,pygame.FULLSCREEN)
					elif event.key == pygame.K_r:
						if eraseMode == True:
							eraseMode = False
						else:
							eraseMode = True
					elif event.key == pygame.K_b:
						self.mode = "self.play()"
						on = 0
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if collisionDetection.rectangular(doneButton1a1,doneButton1a2) == True and didClickOnDone == True:
						list_of_pixels = []
						for x in range(1024): #32 * 32
							if len(coloring) > goesUp and coloring[goesUp][0] == x: #first check is to avoid index error at the end
								list_of_pixels.append(tuple(coloring[goesUp][1])) #this whole thing makes list of pixels
								goesUp += 1
							else:
								list_of_pixels.append((0,0,0,0))
						im2 = Image.new("RGBA", (32,32))						
						im2.putdata(list_of_pixels)
						im2.save("../saved/worlds/" + self.savedFile + "/character.png") #saves to world directory
						self.mode = "self.spawn()"
						saves.write(self.location,"stage:self.spawn()")
						on = 0
					elif collisionDetection.rectangular(doneButton1a1,doneButton1a2) == True:
						doneButtonText = textBox.textBoxDisplay(self.screen,doneButton1a1,doneButton1a2,font,(40,30,90),(0,0,0),(0,0,0),False,"Are you sure?")
						doneButtonText.center()
						didClickOnDone = True
					elif collisionDetection.rectangular(drawGridStart,(drawGridStart[0]+(indivisualSize[0]*32),drawGridStart[1]+(indivisualSize[1]*32))) == True: #tells if clicked inside grid
						wasPressed = True
				elif event.type == pygame.MOUSEBUTTONUP:
					wasPressed = False

				rgbColorTextBox.handler(event)

			if collisionDetection.rectangular(doneButton1a1,doneButton1a2) == True:
				doneButtonText.backgroundColor = (90,80,140)
			else:
				doneButtonText.backgroundColor = (40,30,90)

			if rgbColorTextBox.textBoxInput() != None: #this thing keeps rgb value from being messed up
				goesUp = rgbColorTextBox.textEnter.split(",")
				try:
					selectedColor = [int(goesUp[0]),int(goesUp[1]),int(goesUp[2])]
				except:
					pass
				try:
					if int(goesUp[0]) > 255:
						selectedColor[0] = 255
						rgbColorTextBox.currentText = "255"
						rgbColorTextBox.textEnter = "255"
				except:
					pass
				try:
					if int(goesUp[1]) > 255:
						selectedColor[1] = 255
						rgbColorTextBox.currentText = goesUp[0]+",255"
						rgbColorTextBox.textEnter = goesUp[0]+",255"
				except:
					pass
				try:
					if int(goesUp[2]) > 255:
						selectedColor[2] = 255
						rgbColorTextBox.currentText = goesUp[0]+","+goesUp[1]+",255"
						rgbColorTextBox.textEnter = goesUp[0]+","+goesUp[1]+",255"
				except:
					pass

				rgbColorTextBox.backgroundColor = selectedColor #this part turns text color to white when selectedColor is to low
				if selectedColor[0] < 40 and selectedColor[1] < 40 and selectedColor[2] < 40:
					rgbColorTextBox.textColor = [255,255,255]
				elif selectedColor[0] < 150 and selectedColor[1] < 40 and selectedColor[2] < 40:
					rgbColorTextBox.textColor = [255,255,255]
				elif selectedColor[0] < 40 and selectedColor[1] < 150 and selectedColor[2] < 40:
					rgbColorTextBox.textColor = [255,255,255]
				elif selectedColor[0] < 40 and selectedColor[1] < 40 and selectedColor[2] < 150:
					rgbColorTextBox.textColor = [255,255,255]
				else:
					rgbColorTextBox.textColor = [0,0,0]
				goesUp = 0

			self.screen.fill((187,233,230))
			pygame.draw.rect(self.screen,(255,255,255),bottomRect)
			pygame.draw.lines(self.screen,(0,0,0),False,bottomOutline,2)
			pygame.draw.lines(self.screen,(0,0,0),False,drawGridOutline,2)
			upperText.textBoxDisplay()
			doneButtonText.textBoxDisplay()
			eraseInfoTextBox.textBoxDisplay()
			rgbColorTextBox.textBoxInput()
			#draw drawing grid
			for y in range(32):
				previous[0] = 0
				for x in range(32):
					pos = drawGridStart[0]+previous[0]
					pos2 = drawGridStart[1]+previous[1]
					color = (187,233,230)
					for burr in coloring: #checks if pixel has been colored
						if burr[0] == (y*32)+x:
							color = burr[1]
							break
					pygame.draw.rect(self.screen,color,((pos,pos2),indivisualSize)) #draws pixel
					if mousepos[0] > pos and mousepos[1] > pos2 and mousepos[0] < pos + indivisualSize[0] and mousepos[1] < pos2+indivisualSize[1]: #is mouse in pixel?
						goesUp = [0,0,0] #used to store outline of selected pixel color
						if eraseMode == True:
							goesUp = [255,0,0]
						pygame.draw.lines(self.screen,goesUp,False,resource.rectOutline((pos,pos2),(indivisualSize[0]+previous[0]+drawGridStart[0],indivisualSize[1]+previous[1]+drawGridStart[1]),1),1) #draws outline around this pixel
						coloringLength = len(coloring)						
						if wasPressed == True:
							pixelId = (y*32)+x #1024 pixels first being pixel id: 0 last: 1023
							if eraseMode == False: #all of this orders colored pixels in coloring from least to greatest
								if coloringLength > 0 and coloring[coloringLength-1][0] < pixelId:
									coloring.append([pixelId,selectedColor])
								elif coloringLength > 0:
									goesUp = 0
									for q in coloring[::-1]:
										if q[0] == pixelId:
											goesUp = 0
											break
										elif q[0] < pixelId:
											coloring.insert(coloringLength-goesUp,[pixelId,selectedColor])
											goesUp = 0
											break
										goesUp += 1
									if goesUp > 0:
										coloring.insert(0,[pixelId,selectedColor])
										goesUp = 0
								else:
									coloring.append([pixelId,selectedColor])
							else:
								for w in range(coloringLength):
									if coloring[w][0] == pixelId:
										del coloring[w]
										break

					previous[0] += indivisualSize[0]
				previous[1] += indivisualSize[1]
			goesUp = 0
			previous = [0,0]
			pygame.display.update()

	def spawn(self):
		on = 1
		bottomBar1a1 = resource.pastePos(0,512)
		bottomBar1a2 = resource.pastePos(r[0],28)
		print(bottomBar1a1)
		print(bottomBar1a2)
		textBox1a2 = resource.pastePos(r[0]/3.0,r[1])
		textBox2a1 = resource.pastePos(r[0]/3.0,512)
		textBox2a2 = resource.pastePos((r[0]/3.0)*2,r[1])
		moneyTextBox = textBox.textBoxDisplay(self.screen,bottomBar1a1,textBox1a2,font,None,(255,0,0),None,True,"money: "+saves.read(self.location,"money"))
		moneyTextBox.center()
		levelTextBox = textBox.textBoxDisplay(self.screen,textBox2a1,textBox2a2,font,None,(255,0,0),None,True,"level: "+saves.read(self.location,"level"))
		levelTextBox.center()
		crap = saves.terrain("../saved/terrain/playersBase.txt")
		movement = [0,0]
		pos = [0,0]
		player = pygame.image.load("player.png").convert_alpha()
		collisionInstance = collisionDetection.ComplxObj()
		collisionStone = collisionInstance.setup(crap[2][2])
		collisionStonePos = crap[1][2]
		collisionPlayer = collisionInstance.setup("player.png")
		print(crap)
		while on == 1:
			self.clock.tick(60)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.on = 0
					on = 0
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						if saves.read(optionsLocation,"resolution") == "fullscreen":
							saves.write(optionsLocation,self.defaultResolutionStr)
						else:
							saves.write(optionsLocation,"resolution:fullscreen")

						pygame.display.quit()
						reload(resource)
						pygame.init()
						self.screen = pygame.display.set_mode(resource.screenSize)
						bottomBar1a1 = resource.pastePos(0,512)
						bottomBar1a2 = resource.pastePos(r[0],28)
						textBox1a2 = resource.pastePos(r[0]/3.0,r[1])
						textBox2a1 = resource.pastePos(r[0]/3.0,512)
						textBox2a2 = resource.pastePos((r[0]/3.0)*2,r[1])
						moneyTextBox = textBox.textBoxDisplay(self.screen,bottomBar1a1,textBox1a2,font,None,(255,0,0),None,True,"money: "+saves.read(self.location,"money"))
						moneyTextBox.center()
						levelTextBox = textBox.textBoxDisplay(self.screen,textBox2a1,textBox2a2,font,None,(255,0,0),None,True,"level: "+saves.read(self.location,"level"))
						levelTextBox.center()
						if saves.read(optionsLocation,"resolution") == "fullscreen":
							self.screen = pygame.display.set_mode(resource.screenSize,pygame.FULLSCREEN)
					if event.key == pygame.K_UP:
						movement[1] = -2
					elif event.key == pygame.K_DOWN:
						movement[1] = 2
					elif event.key == pygame.K_LEFT:
						movement[0] = -2
					elif event.key == pygame.K_RIGHT:
						movement[0] = 2
					elif event.key == pygame.K_b:
						self.mode = "self.play()"
						on = 0
				elif event.type == pygame.KEYUP:
					if event.key == pygame.K_UP:
						movement[1] = 0
					elif event.key == pygame.K_DOWN:
						movement[1] = 0
					elif event.key == pygame.K_LEFT:
						movement[0] = 0
					elif event.key == pygame.K_RIGHT:
						movement[0] = 0

			self.screen.fill((0,0,0))
			pygame.draw.rect(self.screen,[0,0,0],[bottomBar1a1,bottomBar1a2])
			moneyTextBox.textBoxDisplay()
			levelTextBox.textBoxDisplay()
			for x in range(len(crap[1])-1):
				self.screen.blit(crap[0][x],crap[1][x])
			pos[0] += movement[0]
			pos[1] += movement[1]
			self.screen.blit(player,pos)
			if collisionInstance.complxObj(collisionPlayer,collisionStone,pos,collisionStonePos) == True:
				print(pos)
				pos = previousPos
			
			previousPos = pos[:]
			pygame.display.update()

	def playersBase(self):
		on = 1

	def run(self):
		while self.on == 1:
			print(self.mode)
			eval(self.mode) #Eval interprets a string as real code.

		saves.write(optionsLocation,self.defaultResolutionStr)
		saves.rmdir("../resources/pngs/terrain/cache")
		saves.mkdir("../resources/pngs/terrain/cache")

Main().run()
