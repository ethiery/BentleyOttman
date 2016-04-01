from math import sqrt

class Segment(object):
	'''
	This class represents a segment by the coordinates of its
	2 endpoints : (x1, y1) and (x2, y2).

	Such segment is always initialized so that
	(x1, y1) is the left endpoint and (x2, y2) the right endpoint.
	In other words,
	x1 < x2 or x1 = x2 and y1 < y2

	Note that the equation of the line that contains the segment is
	y = gradient * x + yIntercept
	'''

	def __init__(self, x1, y1, x2, y2):
		'''
		x1, y1, x2, y2 must be numbers.
		(x1, y1) must be different than (x2, y2), otherwise a ValueError
		will be raised, as this class does not allow to represent a point.
		'''
		endpoint1, endpoint2 = (x1, y1), (x2, y2)
		if endpoint1 == endpoint2:
			raise ValueError('Invalid coordinates (segment is a point)')
		else:
			self.x1, self.y1 = min(endpoint1, endpoint2)			
			self.x2, self.y2 = max(endpoint1, endpoint2)

	def __eq__(self, other):
		'''
		Returns true if and only if self and other are equal segments.
		Two segments are equals if they have the exact same endpoints
		'''
		if other == None:
			return False
		elif not isinstance(other, Segment):
			raise TypeError()
		else:
			return ((self.x1, self.y1, self.x2, self.y2) == 
					(other.x1,other.y1,other.x2,other.y2))

	def __str__(self):
		'''
		Returns a human readable string describing self.
		'''
		return 'Segment [({}, {});({}, {})]'.format(self.x1, 
			self.y1, self.x2, self.y2)



	def gradient(self):
		'''
		Returns the gradient of self. 
		
		WARNING : this method raises ZeroDivisionError when called 
		on a vertical segment.
		'''
		return (self.y2-self.y1) / (self.x2-self.x1)

	def yIntercept(self):
		'''
		Returns the coordinates (x,y) of the y-intercept of the line
		containing self.

		WARNING : this method raises ZeroDivisionError when called 
		on a vertical segment
		'''
		return self.y1 - self.gradient()*self.x1

	def yAtX(self, x):
		'''
		Returns the y-coordinate of self's point of x-coordinate x,
		or None if it does not exist.

		WARNING : this method raises ZeroDivisionError when called 
		on a vertical segment
		'''
		# Computes the barycentric coordinate of the point
		alpha = (x-self.x2) / (self.x1-self.x2)
		if 0 <= alpha <= 1:
			return alpha*self.y1 + (1-alpha)*self.y2
		else:
			return None 

	def orthogonalProjectionOf(self, p):
		'''
		Computes the orthogonal projection of point p on self and
		returns its coordinate (x, y), or None if it does not exist.
		'''
		xp, yp = p
		# Let self be [AB]
		ABx, ABy = self.x2 - self.x1, self.y2 - self.y1
		APx, APy = xp - self.x1, yp - self.y1
		# Computes (vecAB . vecAP) / (vecAB . vecAB)
		ratio = (ABx*APx + ABy*APy) / (ABx**2 + ABy**2)
		# Checks if the orthogonal projection is inside self
		if 0 <= ratio <= 1:
			return (self.x1 + ratio*ABx, self.y1 + ratio*ABy)
		else:
			return None

	def isVertical(self):
		'''
		Returns true if and only if self is vertical
		'''
		return self.x1 == self.x2

	def intersectionWith(self, other):
		'''
		Computes the intersection between self and another segment, 
		which can be :
		- None if the intersection is empty
		- a point of coordinates (x, y)
		- a Segment [(x1,y1);(x2;y2)]
		'''
		x1, x2, x3, x4 = self.x1, self.x2, other.x1, other.x2
		y1, y2, y3, y4 = self.y1, self.y2, other.y1, other.y2

		gradient_ratio = (y1-y2)*(x3-x4) - (x1-x2)*(y3-y4)
		# If the segments are parallel:
		if gradient_ratio == 0:
			# If the segments are not on the same line:
			vert = self.isVertical()
			if ((vert and self.x1 != other.x1) or
				(not vert and self.yIntercept() != other.yIntercept())):
					return None
			# If they do: 
			else:
				# computes the endpoints of the intersection
				# by projecting the segment's endpoints on one another.
				ep1 = self.orthogonalProjectionOf((other.x1, other.y1))
				if ep1 == None:
					ep1 = other.orthogonalProjectionOf((self.x1, self.y1))
				if ep1 == None:
					return None
				ep2 = self.orthogonalProjectionOf((other.x2, other.y2))
				if ep2 == None:
					ep2 = other.orthogonalProjectionOf((self.x2, self.y2))
				if ep2 == None:
					return None
				# If both endpoints exist, returns the corresponding point
				# or segment.
				if ep1 == ep2:
					return ep1
				else:
					return Segment(ep1[0], ep1[1], ep2[0], ep2[1])
		# If the segments are not parallel:
		else:
			# Computes the barycentric coordinates of the intersection.
			alpha = ((y3-y4)*(x2-x4) - (x3-x4)*(y2-y4)) / gradient_ratio
			beta = ((y1-y2)*(x2-x4) - (x1-x2)*(y2-y4)) / gradient_ratio
			# Checks if the intersection is inside both segments.
			if (0 <= alpha <= 1) and (0 <= beta <= 1):
				x = alpha*x1 + (1-alpha)*x2
				y = alpha*y1 + (1-alpha)*y2
				return (x, y)
			else:
				return None