import pygame, sys
import textBox
pygame.init()

setting = True
textValues = []

screen = pygame.display.set_mode((1280,720),0,32)
clock = pygame.time.Clock()
                    #screen,clock,position,Length,fontType,maxRenderLength,maxStrLength,backgroundColor,textColor,boarderOffColor,boarderOnColor
#myTextBox = textBox.textBoxInput(screen,clock,(500,500),(700,525),"../minecraftia/Chelsea II.ttf",200,(255,255,255),(0,0,0),(0,0,0),(0,0,255),"Die")
#myTextBox2 = textBox.textBoxInput(screen,clock,(500,100),(700,125),"DroidNaskh-Bold",15,None,(0,0,0),(0,0,0),(0,0,255),"love")
#myDisplayBox = textBox.textBoxDisplay(screen,(100,100),(700,250),"arial",(255,0,0),(0,255,0),(0,0,255),True,"")
#myDisplayBox2 = textBox.textBoxDisplay(screen,(400,550),(800,600),"./SourceCodePro-Medium.otf",(163,82,52),(0,0,0),(255,255,255),True,"Options")
#myDisplayBox2.center()
points = [(100,100),(198,100),(198,498),(100,498),(100,100)]
points2 = [(300,300),(400,300),(400,400),(300,400),(300,300)]
score = 998
output = None
output2 = None
print(pygame.font.get_fonts())
displayBox = textBox.textBoxDisplay(screen,(100,100),(200,500),"arial",(255,0,0),(0,255,0),(0,0,255),True,"minecraft is good and you")
displayBox2 = textBox.textBoxDisplay(screen,(200,100),(300,500),"arial",(255,0,0),(0,255,0),(0,0,255),True,"minecraft is good and you")
displayBox3 = textBox.textBoxDisplay(screen,(300,100),(400,500),"arial",(255,0,0),(0,255,0),(0,0,255),True,"minecraft is good and you")
displayBox4 = textBox.textBoxDisplay(screen,(400,100),(500,500),"arial",(255,0,0),(0,255,0),(0,0,255),True,"minecraft is good and you")
displayBox5 = textBox.textBoxDisplay(screen,(500,100),(600,500),"arial",(255,0,0),(0,255,0),(0,0,255),True,"minecraft is good and you")
displayBox6 = textBox.textBoxDisplay(screen,(600,100),(700,500),"arial",(255,0,0),(0,255,0),(0,0,255),True,"minecraft is good and you")
displayBox7 = textBox.textBoxDisplay(screen,(700,100),(800,500),"arial",(255,0,0),(0,255,0),(0,0,255),True,"minecraft is good and you")
displayBox8 = textBox.textBoxDisplay(screen,(800,100),(900,500),"arial",(255,0,0),(0,255,0),(0,0,255),True,"minecraft is good and you")
displayBox9 = textBox.textBoxDisplay(screen,(900,100),(1000,500),"arial",(255,0,0),(0,255,0),(0,0,255),True,"minecraft is good and you")
displayBox10 = textBox.textBoxDisplay(screen,(1000,100),(1100,500),"arial",(255,0,0),(0,255,0),(0,0,255),True,"minecraft is good and you")
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

		#myTextBox.handler(event)
		#myTextBox2.handler(event)
	screen.fill((100,100,100))
	#myTextBox.textBoxInput()
	#myTextBox2.textBoxInput()
	#myDisplayBox.textBoxDisplay()
	#myDisplayBox2.textBoxDisplay()
	displayBox.textBoxDisplay()
	displayBox2.textBoxDisplay()
	displayBox3.textBoxDisplay()
	displayBox4.textBoxDisplay()
	displayBox5.textBoxDisplay()
	displayBox6.textBoxDisplay()
	displayBox7.textBoxDisplay()
	displayBox8.textBoxDisplay()
	displayBox9.textBoxDisplay()
	displayBox10.textBoxDisplay()

	#if myTextBox.textBoxInput() != None or myTextBox2.textBoxInput() != None:
		#output = myTextBox.textBoxInput()
		#output2 = myTextBox2.textBoxInput()
	#if output != None and output2 != None:
		#setting = False
	#pygame.draw.lines(screen,(0,0,255),False,points,2)
	#pygame.draw.lines(screen,(0,0,255),False,points2,2)
	pygame.display.update()

textValues.append(myTextBox.textBoxInput())
textValues.append(myTextBox2.textBoxInput())
print(textValues[0])
print(textValues[1])
