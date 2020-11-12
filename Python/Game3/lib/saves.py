import pygame,resource
from PIL import Image
screen = pygame.display.set_mode((0,0))
def convert(location):
	fl = open("../saved/"+location,"r").read()
	lines = fl.split('\n')[:-1]
	pH = [] #lines to be deleted
	for x in range(len(lines)):
		lines[x].replace(' ','')
		if lines[x] == '':
			pH.append(x)
		elif lines[x][0] == '#':
			pH.append(x)
			continue

	for x in pH: del lines[x]
	lookUp = {}
	lines[0] = lines[0].replace('{','')
	lines[0] = lines[0].replace('}','')
	for x in lines[0].split(','):
		x = x.split('=')
		lookUp[x[0]] = pygame.image.load("../resources/"+x[1]).convert_alpha()
	
	lines = lines[1:]
	pH = []
	for x in lines:
		pH.append(x.split(','))
	lines = pH[:]
	pH = [[],[]]
	for line in lines:
		for letter in line:
			pH[1].append(lookUp[letter])
	pH2 = [0,0]
	for y in lines:
		for x in y:
			pH[0].append((pH2[0]*32,pH2[1]*32))
			pH2[0] += 1
		pH2[0] = 0
		pH2[1] += 1
	return pH

#scan whole for material
#run grouping algorythm
#creates 
def convertScale(cnvrt):
	cache = [[],[]]
	for x in range(len(cnvrt[0])):
		ox = cnvrt[0][x]
		cache[0].append((ox[0]/32,ox[1]/32))
		cache[1].append(resource.img(cnvrt[1][x]))
	del cnvrt
	size = resource.imageMultValue
	size = [32*size[0],32*size[1]]
	for x in range(len(cache[0])):
		ox = cache[0][x]
		cache[0][x] = (ox[0]*size[0],ox[1]*size[1])
	return cache
