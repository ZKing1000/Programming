letters = "abdefghijklmnoprstuvwyz123456789"
vowels = "aeiou123456"
def isVowel(thing):
	for x in vowels:
		if x == thing:
			return True

def isProper(thing):
	if isVowel(thing[0]) == None and isVowel(thing[1]) == None:
		return False

print(isVowel("b"))

one = 0
two = 0
three = 0
crap = []
print("1 = ee")
print("2 = ng")
print("3 = oo")
print("4 = oh")
print("5 = I")
print("6 = or")
print("7 = ch")
print("8 = s in measure")
print("9 = th")
while 1:
	if three == 32:
		three = 0
		two += 1
	if two == 32:
		two = 0
		one += 1
	if one == 32:
		break
	if one != two and two != three and isProper(letters[one] + letters[two]) == None and isProper(letters[two] + letters[three]) == None:
		crap.append(letters[one] + letters[two] + letters[three])
	three += 1
fl = open("crap2.txt","a+")
for x in crap:
	fl.write(x + "\n")
fl.close()

