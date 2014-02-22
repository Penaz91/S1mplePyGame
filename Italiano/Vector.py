import math
class Vector(object):
	def __init__(self,x=0.,y=0.):
		self.x=x
		self.y=y
	@staticmethod
	def FromPoints(a,b):
		return Vector(b[0]-a[0],b[1]-a[1])
	def __add__ (self,vec2):
		return Vector(self.x + vec2.x, self.y+vec2.y)
	def __str__(self):
		return "(%s,%s)"%(self.x,self.y)
	def __sub__(self,vec2):
		return Vector(self.x-vec2.x, self.y-vec2.y)
	def __mul__(self,scal):
		return Vector(self.x*scal, self.y*scal)
	def __div__(self, scal):
		return Vector(self.x/scal, self.y/scal)
	def mod(self):
		return float(math.sqrt(self.scalar(self)))
	def __neg__(self):
		return (-self.x, -self.y)
	def scalar(self,vec2):
		return (self.x*vec2.x+self.y*vec2.y)
	def normalize(self):
		mod=self.mod()
		if mod==0:
			mod=1
		self.x/=mod
		self.y/=mod
		return
	def to_tuple(self):
		return (self.x,self.y)
	def int(self):
		return (round(self.x),round(self.y))
