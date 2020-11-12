import pygame, sys
import textBox
pygame.init()

setting = True
textValues = []

screen = pygame.display.set_mode((1280,720),0,32)
clock = pygame.time.Clock()
                    #screen,clock,position,Length,fontType,maxRenderLength,maxStrLength,backgroundColor,textColor,boarderOffColor,boarderOnColor
myTextBox = textBox.textBoxInput(screen,clock,(500,500),(750,600),"./Chelsea II.ttf",200,(255,255,255),(0,0,0),(0,0,0),(0,0,255))
myTextBox2 = textBox.textBoxInput(screen,clock,(500,100),(1200,200),"DroidNaskh-Bold",15,None,(0,0,0),(0,0,0),(0,0,255))
myDisplayBox = textBox.textBoxDisplay(screen,(400,400),(1200,550),"arial",(255,0,0),(0,255,0),(0,0,255),False,"Once apon a time there was a boy named Holden. Holden lived in a very strange land, where animals ruled. The caste system of that world is as follows (1 being the strongest, and 6 being the weekest creature.): 1. orcas, 2. hippcampy, 3. unicorns, 4. pacmen, 5. honeybadgers, because they don't care, and last, but totally least 6. humans. Some people should die for fun, because they are ugly.")
myDisplayBox2 = textBox.textBoxDisplay(screen,(400,550),(800,600),"./SourceCodePro-Medium.otf",None,(0,0,0),None,True,"Type text in textbox, try rapid enter and delete, press enter in box of them, and check console output.")
points = [(100,100),(198,100),(198,498),(100,498),(100,100)]
points2 = [(300,300),(400,300),(400,400),(300,400),(300,300)]
score = 998
while setting == True:
	clock.tick(30)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.image.save(screen, "screenshot.png")
			pygame.quit()
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			score += 1
			myDisplayBox = textBox.textBoxDisplay(screen,(400,400),(700,500),"ubuntu",None,(0,255,0),(0,0,255),False,"Attack: " + str(score) + "\n" + "Defence: " + str(score + 1) + "\n" + "Poop: " + str(score + 2) + "\n" + "Love: " + str(score + 3) + "\n" + "Crap: " + str(score + 4) + "\n" + "braba: " + str(score + 5))

		myTextBox.handler(event)
		myTextBox2.handler(event)
	screen.fill((100,100,100))
	myTextBox.textBoxInput()
	myTextBox2.textBoxInput()
	myDisplayBox.textBoxDisplay()
	myDisplayBox2.textBoxDisplay()

	if myTextBox.textBoxInput() != None and myTextBox2.textBoxInput() != None:
		setting = False
	pygame.draw.lines(screen,(0,0,255),False,points,2)
	pygame.draw.lines(screen,(0,0,255),False,points2,2)
	pygame.display.update()

textValues.append(myTextBox.textBoxInput())
textValues.append(myTextBox2.textBoxInput())
print(textValues[0])
print(textValues[1])
