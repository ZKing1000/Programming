import pygame
from PIL import Image #Check complxObj function

def rectangular(pos,endPos): #Collisions detection for rectangular objects
	mouse = pygame.mouse.get_pos()
	if pos[0] <= mouse[0] and endPos[0] >= mouse[0] and pos[1] <= mouse[1] and endPos[1] >= mouse[1]:
		return True
	else:
		return False

class complxObj(): #Collision detection for things like characters that aren't necessarily rectangular or circullar.
	def __init__(self): #lol
		pass
	def setup(self,initImg): #Use PIL to map out transparent and colored pixeled by y coord! If image is 75 pixels tall there will be 75 lists in the returned list.
		img = Image.open(initImg)
		pix = img.load()
		returnLs = []
		storage = []
		for y in range(img.size[1]):
			storage = [0,0] #[0] how many transparent pixels before colored pixel from left to right [1] how many colored pixels
			for x in range(img.size[0]):
				rgba = pix[x,y] #RGBA value with PIL
				if len(rgba) < 4 or rgba[3] > 0: #is pixel colored?
					storage[1] += 1
				elif len(rgba) == 4 and storage[1] == 0: #is pixel transparent? Does not count after colored is filled in.
					storage[0] += 1
			returnLs.append(storage)
			storage = []

		return returnLs

	def complxObj(self,first,second,pastePos,pastePos2): #First and second are output from self.setup.
		firstModified = [] #Collects parts of first that are in correlation with parts of second based on y coordinate.
		secondModified = [] #For example: two images pasted, both 100 pixels tall, at 100 and 150 (In y coord); the last fifty lists of first would be saved and the first 50 lists of second would be saved.
		for x in range(len(first)-1):
			for y in range(len(second)-1):
				if x + pastePos[1] == y + pastePos2[1]:
					firstModified.append(first[x])
					secondModified.append(second[y])
		orientation1,orientation2,orientation3,orientation4 = firstModified,secondModified,pastePos[0],pastePos2[0] #For when one image is in back of another inx coord.
		if pastePos[0] > pastePos2[0]:
			orientation1,orientation2,orientation3,orientation4 = secondModified,firstModified,pastePos2[0],pastePos[0]
		for x in range(len(orientation1)-1):
			if orientation1[x][0] + orientation1[x][1] + orientation3 >= orientation2[x][0] + orientation4 and orientation1[x][0] + orientation1[x][1] + orientation3 <= orientation2[x][0] + orientation2[x][1] + orientation4:
				return True
