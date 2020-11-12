alphabet = ""
for x in range(97,123):
	if x != "k" or "z":
		alphabet += chr(x)

poop = True
crap = "aei"
cache = 0
ls = []
while poop == True:
	for x in range(len(crap)):
		cache = x
		ls.append(crap[cache])
	for x in range(len(crap)):
		print(ls[cache])
		ls[cache] += crap[x]
		print(cache)
		cache -= 1
	print(ls)
	poop = False	
