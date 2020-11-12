import fileinput,os,pygame,shutil
from PIL import Image
#I think you can do this with pickle, but this method is more fun.
def read(fl,keyWord):
	fileIn = fileinput.FileInput(fl)
	for x in fileIn:
		vals = x.split(":")
		print(vals, "HIHIHIHI")
		if vals[0] == keyWord:
			return vals[1][:-1]
	fileIn.close()

def write(fl,string):
	separate = string.split(":")
	returnString = ""
	isUsed = False
	fileIn = fileinput.FileInput(fl)
	for x in fileIn:
		vals = x.split(":")
		if vals[0] == separate[0]:
			isUsed = True
			returnString += separate[0] + ":" + separate[1] + "\n"
		else:
			returnString += x
	fileIn.close()
	if isUsed == False:
		returnString += string + "\n"
	newFl = open(fl + ".tmp","w")
	newFl.write(returnString)
	newFl.close()
	os.remove(fl)
	oldFile = open(fl,"w")
	oldFile.write(returnString)
	oldFile.close()
	os.remove(fl + ".tmp")

def crashRecovery(fl):
	if os.path.isfile(fl + ".tmp") == True:
		oldFile = open(fl + ".tmp","r")
		tmp = oldFile.read()
		oldFile.close()
		newFile = open(fl,"w")
		newFile.write(tmp)
		newFile.close()
		os.remove(fl + ".tmp")

def refresh(fl,ls): #incase someone tampers with a saved file manually. Meaning this does not actually edit any thing unless its completely missing or not supposed to be there.
	dictionary = {}
	fileIn = fileinput.FileInput(fl)
	for x in ls:
		dictionary[x] = False
		for y in fileIn:
			if x.split(":")[0] == y.split(":")[0]:
				dictionary[x] = True
			elif dictionary[x] != True:
				dictionary[x] = False
	fileIn.close()
	
	returnString = ""
	for x in dictionary:
		if dictionary[x] == False:
			returnString += x + "\n"


	newFile = open(fl,"a+")
	newFile.write(returnString)
	newFile.close()

def terrain(fl): #for loading terrain
	returnLs = [[],[],[]]
	images = [[],[]]
	goesUp = 0
	goesUp2 = 0
	stopCount = 0
	tmp = ""
	for x in fileinput.FileInput(fl):
		use = x
		if x[0] == "{":
			goesUp = use[1:].split(",")
			for bla in goesUp:
				goesUp = bla.split("=")
				if goesUp[1][len(goesUp[1])-1] == "\n":
					images[1].append(goesUp[1][:-1])
				else:
					images[1].append(goesUp[1])
				images[0].append(goesUp[0])
				
		else:
			goesUp2 = use.split("(")
			for x in goesUp2:
				tmp += x
	goesUp2 = tmp.split(")")
	stopCount = 0
	for x in goesUp2[:-1]:
		goesUp = 0
		for y in images[0]:
			if y == x[0]:
				returnLs[0].append(images[1][goesUp])
				returnLs[1].append(x[1:])
			elif y == x[1] and x[0] == "\n":
				returnLs[0][stopCount-1] += "\n"
				returnLs[0].append(images[1][goesUp])
				returnLs[1].append(x[2:])
			goesUp += 1
		stopCount += 1

	goesUp = [[],[]]
	goesUp2 = ""
	tmp = []
	goesUp = [[],[[0,0]]]
	goesUp2 = returnLs[0][:]
	crap = None
	for x in range(len(returnLs[1])):
		if returnLs[0][x][len(returnLs[0][x])-1] == "\n" and os.path.exists("../resources/pngs/terrian/cache/"+returnLs[0][x][:-5]+"("+returnLs[1][x]+").png") == False:
			crap = "../resources/pngs/terrain/cache/"+returnLs[0][x][:-5]+"("+returnLs[1][x]+").png\n"
			returnLs[0][x] = crap
			if "," in returnLs[1][x]:
				blab = returnLs[1][x].split(",")
				img = Image.new("RGBA", (int(blab[0])*32,int(blab[1])*32))
				img2 = Image.open("../resources/pngs/terrain/"+goesUp2[x][:-1])
				for y in range(int(blab[1])):
					for x2 in range(int(blab[0])):
						img.paste(img2, (x2*32,y*32))
			else:
				img = Image.new("RGBA", (int(returnLs[1][x])*32,32))
				img2 = Image.open("../resources/pngs/terrain/"+goesUp2[x][:-1])
				for x in range(int(returnLs[1][x])):
					img.paste(img2, (x*32,0))


			img.save(crap[:-1])
		elif os.path.exists("../resources/pngs/terrian/cache/"+returnLs[0][x][:-4]+"("+returnLs[1][x]+").png") == False:
			crap = "../resources/pngs/terrain/cache/"+returnLs[0][x][:-4]+"("+returnLs[1][x]+").png"
			returnLs[0][x] = crap
			if "," in returnLs[1][x]:
				blab = returnLs[1][x].split(",")
				img = Image.new("RGBA", (int(blab[0])*32,int(blab[1])*32))
				img2 = Image.open("../resources/pngs/terrain/"+goesUp2[x])
				for y in range(int(blab[1])):
					for x2 in range(int(blab[0])):
						img.paste(img2, (x2*32,y*32))
			else:
				img = Image.new("RGBA", (int(returnLs[1][x])*32,32))
				img2 = Image.open("../resources/pngs/terrain/"+goesUp2[x])
				for x in range(int(returnLs[1][x])):
					img.paste(img2, (x*32,0))

			img.save(crap)

	goesUp = [[],[]]
	goesUp2 = ""
	tmp = []
	for x in range(len(returnLs[1])):
		goesUp2 += returnLs[1][x]
		if returnLs[0][x][len(returnLs[0][x])-1] == "\n":
			goesUp[0].append(goesUp2)
			goesUp[1].append(x)
			goesUp2 = ""

	for x in range(len(goesUp[0])):
		if "," not in goesUp[0][x]:
			returnLs[1][goesUp[1][x]] += ",1"

	for x in returnLs[1]:
		if "," in x:
			crap = x.split(",")
			tmp.append([int(crap[0])*32,int(crap[1])*32])
		else:
			tmp.append(int(x)*32)


	goesUp = [[],[[0,0]]]
	goesUp2 = [0,0]
	for x in range(len(returnLs[1])):
		if str(type(tmp[x])) == "<type 'list'>":
			goesUp2[0] += tmp[x][0]
			goesUp2[1] += tmp[x][1]
		else:
			goesUp2[0] += tmp[x]
			goesUp
		if returnLs[0][x][len(returnLs[0][x])-1] == "\n":
			goesUp2[0] = 0
			goesUp[0].append(returnLs[0][x][:-1])
		else:
			goesUp[0].append(returnLs[0][x])
		goesUp[1].append(goesUp2[:])

	goesUp[0].append(returnLs[0][len(returnLs[0])-1])
	goesUp.append(goesUp[0][:])

	for x in range(len(goesUp[0])):
		goesUp[0][x] = pygame.image.load(goesUp[0][x]).convert_alpha()

	return(goesUp)



def getWorlds(): #Gets a list of saved worlds for main.Main().play()
	return os.listdir("../saved/worlds")

def rmdir(fl):
	shutil.rmtree(fl)

def exists(fl):
	return os.path.exists(fl)

def mkdir(fl):
	if not exists(fl):
    		os.makedirs(fl)

def mkfile(fl):
	open(fl,"a").close()
