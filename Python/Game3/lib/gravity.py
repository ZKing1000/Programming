gravity = 1
class new():
	def __init__(self,weight):
		self.weight = weight
		self.moveQuotient = 0
		self.momentum = 0
		self.moved = 0
		self.cache = 0
		self.cache2 = 0
	
	def jump(self,momentum):
		global gravity
		self.momentum = (self.weight/float(gravity))/float(momentum)
		self.moveQuotient = momentum/float(self.weight)**2
		print(self.momentum)
		print(self.moveQuotient)

	def gravity(self):
		if self.momentum > 0:
			self.momentum -= self.moveQuotient
			self.moved += self.momentum
			return -self.momentum
		elif self.moved > 0:
			if self.moved <= self.cache:
				self.moved = 0
				self.cache = 0
				self.cache2 = 0
			else:
				print("CRAOBOO")
				self.cache2 += self.moveQuotient
				self.cache += self.cache2
				return self.cache2
		return 0
		
