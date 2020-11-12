import pygame,sys,saves

def rectOutline(pos,pos2,width = 2): #width makes lines fit perfectly in imaginary box
	subtraction = width - int(((width/2.0)-1) + .5) #doesn't always paste line perfectly in the center
	return (pos,((pos[0] + (pos2[0] - pos[0])) - subtraction,pos[1]),(pos2[0] - subtraction, pos2[1] - subtraction),(pos[0],pos2[1] - subtraction),pos)
