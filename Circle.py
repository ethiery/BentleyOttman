from Segment import Segment
from math import sqrt

class Circle(object):
	'''
	This class represents a circle.
	(xc, yc) is its center and r is its radius.

	Note that this circle's equation is
	(y-yc)^2 + (x-xc)^2 = r^2
	'''

	def __init__(self, xc, yc, r):
		if r < 0:
			raise ValueError('Invalid radius value (negative)')
		else:
			self.xc, self.yc, self.r = xc, yc, r

	def __eq__(self, other):
		'''
		Two circles are equals if they have the same center and radius
		'''
		return (self.xc, self.yc, self.r) == (other.xc, other.yc, other.r)

	def __ne__(self, other):
		return not self == other

	def __lt__(self, other):
		'''
		Circles are compared according to their left most point
		'''
		return (self.xc-self.r, self.yc) <= (other.xc-other.r, other.yc)

	def intersectionWithSegment(self, seg, eps=0.001):
		'''
		Computes the intersection between this circle and the segment 
		passed as argument, and returns them in a list
		'''
		# Computes the barycentric coordinate alpha, which is solution
		# of the system
		# | (y-yc)^2 + (x-xc)^2 = r^2
		# | y = alpha*y1 + (1-alpha)*y2
		# | x = alpha*x1 + (1-alpha)*x2
		# which is equivalent to : A*alpha^2 + B*alpha + C = 0 where:
		A = (seg.x1-seg.x2)**2 + (seg.y1-seg.y2)**2
		B = 2*((seg.x2-self.xc)*(seg.x1-seg.x2) + 
			   (seg.y2-self.yc)*(seg.y1-seg.y2))
		C = (seg.x2-self.xc)**2 + (seg.y2-self.yc)**2 - self.r**2
		delta = B**2 - 4*A*C
		alphas = []
		if delta > eps:
			sqrt_delta = sqrt(delta)
			alphas.extend([(sqrt_delta - B)/(2*A), (-sqrt_delta - B)/(2*A)])
		elif delta > -eps:
			alphas.append(-B / (2*A))
		# For each alpha, checks if the intersection point is in seg
		res = []
		for alpha in alphas:
			if 0 <= alpha <= 1:
				x = alpha*seg.x1 + (1-alpha)*seg.x2
				y = alpha*seg.y1 + (1-alpha)*seg.y2
				res.append((x,y))
		return res

	############################################
	# DEPRECIATED USE INTERSECTIONWITH INSTEAD #
	############################################

	# Use this method to measure how much slower this methods are
	@staticmethod
	def compareIntersectionMethods():
		from random import random
		from time import clock
		# Initializes 100 random segments in [0,1]x[0,1]
		segments = []
		for i in range(100):
			x1, y1, x2, y2 = random(), random(), random(), random()
			segments.append(Segment(x1, y1, x2, y2))
		# Initializes 100 random circles of center in [0,1]x[0,1]
		# and of radius in [0,1]
		circles = []
		for i in range(100):
			xc, yc, r = random(), random(), random()
			circles.append(Circle(xc, yc, r))
		# Times the old intersection function
		start = clock()
		for s in segments:
			for c in circles:
				inter = c.oldIntersectionWithSegment(s)
		old = clock()-start
		# Times the new intersection function
		start = clock()
		for s in segments:
			for c in circles:
				inter = c.intersectionWithSegment(s)
		new = clock()-start
		print("Computing the intersections between 100 random segments"+
			  " in [0,1]x[0,1].\n"+
			  " and 100 random circles in [0,1]x[0,1] of radius at most 1\n"
			  "Old function took {} s\n".format(old)+
			  "New function took {} s\n".format(new)+
			  "Speed up : x{}".format(old/new))

	
	def intersectionWithLine(self, seg, eps=0.001):
		'''
		Computes the intersection between this circle and the line
		containing the segment passed as argument.
		Returns :
		- None if the intersection is empty
		- (x, y) if the intersection is a point of coordinates (x, y)
		- (x1, y1, x2, y2) if the intersection is a set of 2 points
		of coordinates (x1, y1) and (x2, y2)
		'''
		# If the line is vertical:
		if seg.isVertical:
			x0 = seg.x1
			# The intersection points are the solutions of the system :
			# | (y-yc)^2 + (x-xc)^2 = r^2
			# | x = x0
			square = self.r**2 - (x0 - self.xc)**2
			if square < -eps:
				return None
			elif square > eps:
				sqrt_square = sqrt(square)
				y1 = self.yc - sqrt_square
				y2 = self.yc + sqrt_square
				return (x0, y1, x0, y2)
			else:
				return (x0, self.yc)
		# If the line is not vertical
		else:
			a, b = seg.gradient, seg.yIntercept
			# The intersection points are the solutions of the system:
			# | (y-yc)^2 + (x-xc)^2 = r^2
			# | y = a*x + b
			# x is solution of A*x² + B*x + C = 0 where:
			A = (1 + a**2)
			B = 2*(a*b - self.xc - a*self.yc)
			C = self.xc**2 + self.yc**2 + b**2 - self.r**2 - 2*b*self.yc
			delta = B**2 - 4*A*C
			if delta < -eps:
				return None
			elif delta > eps:
				sqrt_delta = sqrt(delta)
				x1 = (-sqrt_delta - B) / (2*A)
				y1 = a*x1 + b
				x2 = (sqrt_delta - B) / (2*A)
				y2 = a*x2 + b
				return (x1, y1, x2, y2)
			else:
				x = -B / (2*A)
				y = a*x + b
				return (x, y)

	def oldIntersectionWithSegment(self, seg):
		'''
		Computes the intersection between this circle 
		and a segment. Returns :
		- None if the intersection is empty
		- (x, y) if the intersection is a point of coordinates (x, y)
		- (x1, y1, x2, y2) if the intersection is a set of 2 points
		of coordinates (x1, y1) and (x2, y2)
		'''
		line_intersection = self.intersectionWithLine(seg)
		# If the corresponding lines' intersection is empty
		if line_intersection == None:
			return None
		else:
			points = [(line_intersection[2*i], line_intersection[2*i+1]) 
					  for i in range(round(len(line_intersection)/2))]
			segment_intersection = []
			# Checks if the intersection point belongs to the segment
			for x,y in points:
				if ((not seg.isVertical and seg.x1 <= x <= seg.x2) or
					(seg.isVertical and seg.y1 <= y <= seg.y2)):
						segment_intersection.extend([x, y])
			if len(segment_intersection) > 0:
				return tuple(segment_intersection)
			else:
				return None