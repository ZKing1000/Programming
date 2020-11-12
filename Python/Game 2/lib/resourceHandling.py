import pygame,sys,saves

pygame.init()
if saves.read("../saved/options.txt","resolution") == "fullscreen":
	print("HI")
	screenSize = pygame.display.Info().current_w,pygame.display.Info().current_h #Monitor size
else:
	print("DIE")
	tmp = saves.read("../saved/options.txt","resolution")
	screenSize = (int(tmp.split("x")[0]),int(tmp.split("x")[1]))

imageMultValue = (screenSize[0]/960.0,screenSize[1]/540.0)
def background(img):
	return pygame.transform.scale(pygame.image.load(img).convert_alpha(),screenSize)

def pastePos(in1,in2):
	return (int((imageMultValue[0] * in1) + 0.5),int((imageMultValue[1] * in2) + 0.5))

def imgConvert(imgLocation):
	initialImg = pygame.image.load(imgLocation).convert_alpha()
	return pygame.transform.scale(initialImg,(int((initialImg.get_width() * imageMultValue[0]) + 0.5),int((initialImg.get_height() * imageMultValue[1]) + 0.5)))

def rectPos(pos,pos2):
	return (pos,(pos2[0] - pos[0],pos2[1] - pos[1]))

def rectOutline(pos,pos2,width = 2): #width makes lines fit perfectly in imaginary box
	subtraction = width - int(((width/2.0)-1) + .5) #doesn't always paste line perfectly in the center
	return (pos,((pos[0] + (pos2[0] - pos[0])) - subtraction,pos[1]),(pos2[0] - subtraction, pos2[1] - subtraction),(pos[0],pos2[1] - subtraction),pos)
