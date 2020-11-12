import os
import pygame

class mkFile():
	def __init__(self):
		pass

	def mkdir(self,name):
		os.system('mkdir -p ../' + name)

	def savePng(self,inputName,outputName):
		pygame.image.save(inputName,os.path.join('data',outputName))
