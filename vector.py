import math
from cmath import phase # argument of a complex number

class Vector(object):
	"""2D vectors"""
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def __repr__(self):
		return "(%f, %f)" % (self.x, self.y)
	def __add__(self, other):
		return Vector(self.x + other.x, self.y + other.y)
	def __sub__(self, other):
		return Vector(self.x - other.x, self.y - other.y)
	def __mul__(self, other):
		if isinstance(other, int) or isinstance(other, float): # vector * scalar -> vector
			return Vector(self.x * other, self.y * other)
		else: # vector * vector -> scalar (scalar product) 
			return self.x*other.x + self.y*other.y
	def __rmul__(self, other):
		return Vector(self.x * other, self.y * other)
	def __div__(self, other):
		return Vector(self.x / other, self.y / other)
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y
	def pair(self):
		"""convert to tuple"""
		return (self.x, self.y)
	def norm(self):
		return math.sqrt(self.x*self.x + self.y*self.y)
	def is_null(self):
		return self.x == 0 and self.y == 0
	def angle(self):
		"""angle in radians defined by the vector"""
		return phase(complex(self.x, self.y))
	def distance(self, other):
		"""distance between two points"""
		return Vector(other.x - self.x, other.y - self.y).norm()
	def normalize(self, scale):
		"""returns a scaled copy of the vector of norm scale"""
		n = self.norm()
		if n == 0:
			return Vector(0,0)
		else:
			return Vector(self.x*scale/n, self.y*scale/n)

def bresenham(p1, p2):
	"""Returns the path of integer points from p1 to p2 (Vectors)"""
	dw, dh = 1, 1
	x1, y1, x2, y2 = p1.x, p1.y, p2.x, p2.y
	if x1 > x2:
		dw = -1
	if y1 > y2:
		dh = -1
	if x1 == x2:
		return [Vector(x1, i) for i in range(y1, y2+dh, dh)]
	elif y1 == y2:
		return [Vector(i, y1) for i in range(x1, x2+dw, dw)]
	width = abs(x2 - x1) # width and height are the constant dimensions of the segment
	height = abs(y2 - y1)
	w, h = width, height # w and h are the "current" width and height
	x, y = (x1, y1) # (x, y) is the current point in the path
	path = [Vector(x, y)]
	while (x, y) != (x2, y2):
		if w > h:
			x += dw
			w -= h
			h = height
		elif h > w:
			y += dh
			h -= w
			w = width
		else:
			x += dw
			y += dh
			w, h = width, height
		path.append(Vector(x, y))
	return path