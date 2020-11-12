import pygame,sys

pygame.init()
base_rezolution = (1024,576)
screenSize = pygame.display.Info().current_w,pygame.display.Info().current_h #Monitor size

imageMultValue = (screenSize[0]/float(base_rezolution[0]),screenSize[1]/float(base_rezolution[1]))
def background(img):
	return pygame.transform.scale(pygame.image.load(img).convert_alpha(),screenSize)

def pos(tp):
	return (int((imageMultValue[0]*tp[0])+0.5),int((imageMultValue[1]*tp[1]) + 0.5))

def img(img):
	if type(img) == type(str()):
		print("POOPY DOOPY")
		img = pygame.image.load("../resources/"+img).convert_alpha()
	return pygame.transform.scale(img,(int((img.get_width()*imageMultValue[0])+0.5),int((img.get_height()*imageMultValue[1])+0.5)))

def rect(tp):
	return (tp[0],(tp[1][0]-tp[0][0],tp[1][1]-tp[0][1]))

def antiRect(tp):
	return (tp[0],(tp[0][0]+tp[1][0],tp[0][1]+tp[1][1]))

def rectOutline(tp,width = 2): #width makes lines fit perfectly in imaginary box
	subtraction = width - int(((width/2.0)-1)+.5) #doesn't always paste line perfectly in the center
	return (tp[0],((tp[0][0]+(tp[1][0]-tp[0][0]))-subtraction,tp[0][1]),(tp[1][0]-subtraction,tp[1][1]-subtraction),(tp[0][0],tp[1][1]-subtraction),tp[0])
