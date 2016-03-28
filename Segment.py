class Segment(object):
	'''
	This class represents a segment.

	(x1, y1) and (x2, y2) are its 2 endpoints.
	They are orderer from left to right then top to bottom,
	at instanciation i.e.
	x1 <= x2 and if x1 == x2 then y1 <= y2 

	Note that the corresponding infinite line equation is
	y = gradient * x + yIntercept
	'''

	def __init__(self, x1, y1, x2, y2):
		if x1 == x2 and y1 == y2:
			raise ValueError('Invalid coordinates (segment is a point)')
		elif (x1, y1) <= (x2, y2):
			self.x1, self.y1 = x1, y1
			self.x2, self.y2 = x2, y2
		else:
			self.x1, self.y1 = x2, y2
			self.x2, self.y2 = x1, y1

	def __eq__(self, seg):
		'''
		Two segments are equals if they have the same endpoints
		'''
		if seg == None:
			return False
		elif not isinstance(seg, Segment):
			raise TypeError()
		else:
			return ((self.x1,self.y1,self.x2,self.y2) == 
					(seg.x1,seg.y1,seg.x2,seg.y2))

	def __ne__(self, seg):
		return not self == seg

	def __lt__(self, seg):
		'''
		A segment s1 is < to another segment s2 if : 
		- s1's left endpoint is below s2
		- s1's left endpoint is on s2, and s1.gradient < s2.gradient 

		MUST NOT be used on a vertical segment
		(raises ZeroDivisionError)
		'''
		if (self.x1, self.y1) < (seg.x1, seg.y1):
			return (self.yAtX(seg.x1), self.gradient) < (seg.y1, seg.gradient)
		else:
			return (self.y1, self.gradient) < (seg.yAtX(self.x1), seg.gradient)

	@property
	def isVertical(self, EPS=0.001):
		'''
		Returns true if and only if this segment is vertical, with
		EPS precision.
		'''
		return abs(self.x1 - self.x2) < EPS

	@property
	def yIntercept(self):
		'''
		Returns the coordinates (x,y) of the y-intercept of the line
		containing this segment.

		MUST NOT be used for a vertical segment 
		(raises ZeroDivisionError)
		'''
		return self.y1 - self.gradient * self.x1

	@property
	def gradient(self):
		'''
		Returns the gradient of the segment, 
		
		MUST NOT be used for a vertical segment 
		(raises ZeroDivisionError)
		'''
		return (self.y2 - self.y1) / (self.x2 - self.x1)
		

	def orthogonalProjectOf(self, p):
		'''
		Computes the orthogonal projection of point p on
		this segment and returns it, or None if it does not exist.

		MUST NOT be used if this segment is a point (i.e. x1=x2 
		and y1=y2).
		'''
		xp, yp = p
		# Lets name A and B the endpoint of our segment
		# Computes vecAB . vecAP / vecAB . vecAB
		ratio = (((self.x2-self.x1)*(xp-self.x1) + 
				  (self.y2-self.y1)*(yp-self.y1))
				 /((self.x2-self.x1)**2 + (self.y2-self.y1)**2))
		# If the orthogonal projection is inside this segment
		if 0 <= ratio <= 1:
			x = self.x1 + ratio*(self.x2-self.x1)
			y = self.y1 + ratio*(self.y2-self.y1)
			return (x,y)
		else:
			return None

	def yAtX(self, x):
		'''
		Returns the y-coordinate of the point of this segment
		which has a x-coordinate x, or None if it does not
		exist.

		MUST NOT be used for a vertical segment
		(raises ZeroDivisionError)
		'''
		# Computes the barycentric coordinates of the point
		alpha = (x-self.x2)/(self.x1-self.x2)
		if 0 <= alpha <= 1:
			return alpha*self.y1 + (1-alpha)*self.y2
		else:
			return None 

	def intersectionWith(self, seg):
		'''
		Computes the intersection between this segment and another 
		segment. Returns :
		- None if the intersection is empty
		- (x, y) if the intersection is a point of coordinates (x, y)
		- a segment if the intersection is this segment

		The only difference with intersectionWith() is that it is
		optimized by using orthogonal projections and barycentric
		coordinates which allows to compute the result after
		2 branchements instead of 4 if the lines are not parallel
		'''
		x1, x2, x3, x4 = self.x1, self.x2, seg.x1, seg.x2
		y1, y2, y3, y4 = self.y1, self.y2, seg.y1, seg.y2

		gradient_ratio = (y1-y2)*(x3-x4) - (x1-x2)*(y3-y4)
		# If lines are parallel:
		if gradient_ratio == 0:
			# if they are not on top of each other
			if (self.isVertical and seg.isVertical or
				self.yIntercept != seg.yIntercept):
					return None
			else:
				# Computes the orthogonal projections of each pair of 
				# endpoints on the other segment
				onself1 = self.orthogonalProjectOf((seg.x1, seg.y1))
				onseg1 = seg.orthogonalProjectOf((self.x1, self.y1))
				p1 = onseg1 if onself1 == None else onself1
				if p1 == None:
					return None
				else:
					onself2 = self.orthogonalProjectOf((seg.x2, seg.y2))
					onseg2 = seg.orthogonalProjectOf((self.x2, self.y2))
					p2 = onseg2 if onself2 == None else onself2
					if p1 == p2:
						return p1
					else:
						return Segment(*p1, *p2)
		else:
			# Computes barycentric coordinates of the intersection
			alpha = ((y1-y2)*(x2-x4) - (x1-x2)*(y2-y4)) / gradient_ratio
			beta = ((y3-y4)*(x2-x4) - (x3-x4)*(y2-y4)) / gradient_ratio
			# Checks the intersection is in both segment
			if (0 <= alpha <= 1) and (0 <= beta <= 1):
				x = alpha*x1 + (1-alpha)*x2
				y = alpha*y1 + (1-alpha)*y2
				return (x, y)
			else:
				return None

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
		# Times the old intersection function
		start = clock()
		for s1 in segments:
			for s2 in segments:
				inter = s1.oldIntersectionWith(s2)
		old = clock()-start
		# Times the new intersection function
		start = clock()
		for s1 in segments:
			for s2 in segments:
				inter = s1.intersectionWith(s2)
		new = clock()-start
		print("Computing the intersections between 100 random segments"+
			  " in [0,1]x[0,1].\n"+
			  "Old function took {} s\n".format(old)+
			  "New function took {} s\n".format(new)+
			  "Speed up : x{}".format(old/new))

	def lineIntersectionWith(self, seg):
		'''
		Computes the intersection between the line containing this 
		segment, and the line containing another segment.
		Returns :
		- None if the intersection is empty
		- (x, y) if the intersection is a point of coordinates (x, y)
		- "line" if the intersection is a line
		'''
		a1, a2 = self.isVertical, seg.isVertical
		a1 = None if a1 else self.gradient
		a2 = None if a2 else seg.gradient
		b1 = None if a1 == None else self.yIntercept
		b2 = None if a2 == None else seg.yIntercept

		# if the 2 lines aren't parallel
		if a1 != a2:
			x, y = None, None
			# if neither of the 2 lines is vertical
			if a1 != None and a2 != None:
				x = (b2-b1) / (a1-a2)
				y = a1*x + b1
			# if this line is vertical but not the other
			elif a1 != None:
				x = seg.x1
				y = a1*x + b1
			# if this line isn't vertical but the other one is
			else:
				x = self.x1
				y = a2*x + b2
			return (x,y)
		# if the 2 lines are parallel but not mingled
		elif (b1 != b2) or (b1 == None and self.x1 != seg.x2): 
			return None
		# if the 2 lines are parallel and mingled
		else:
			return 'line'

	def oldIntersectionWith(self, seg):
		'''
		Computes the intersection between this segment and another 
		segment. Returns :
		- None if the intersection is empty
		- (x, y) if the intersection is a point of coordinates (x, y)
		- a segment if the intersection is this segment
		'''
		line_intersection = self.lineIntersectionWith(seg)
		# If the corresponding lines' intersection is empty
		if line_intersection == None:
			return None
		# If the corresponding lines' intersection is a line
		elif line_intersection == 'line':
			# Computes the endpoints of a potential intersection
			if self.isVertical:
				cmp_k = lambda x: x[1]
			else:
				cmp_k = lambda x: x[0]
			xmin, ymin = max((self.x1, self.y1), (seg.x1, seg.y1), key=cmp_k)
			xmax, ymax = min((self.x2, self.y2), (seg.x2, seg.y2), key=cmp_k)
			# If the intersection is empty
			if (xmin > xmax) or (xmin == xmax and ymin > ymax):
				return None
			# If the intersection is a single point
			elif (xmin, ymin) == (xmax, ymax):
				return (xmin, ymin)
			# If the intersection is a segment
			else:
				return Segment(xmin, ymin, xmax, ymax)
		# If the corresponding lines' intersection is a point
		else:
			x, y = line_intersection
			# Checks if the intersection point belongs to both segments
			if (self.x1 <= x <= self.x2) and (seg.x1 <= x <= seg.x2):
				return (x, y)
			else:
				return None
