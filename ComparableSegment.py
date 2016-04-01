from Segment import Segment

class ComparableSegment(Segment):
	'''
	This class represents segments that are compared in a special way
	to be sorted in a Sweep Line.
	'''

	# X-coordinate used to compare 2 segments
	currentX = 0

	def __lt__(self, other):
		'''
		Returns true if and only if self < other.
		s1 < s2 if : 
		- s1's y-coordinate < s2's y-coordinate at currentX
		- s1's y-coordinate = s2's y-coordinate at currentX 
		and s1.gradient < s2.gradient
		- s1's y-coordinate = s2's y-coordinate at currentX 
		, s1.gradient = s2.gradient
		and (s1.x1, s1.y1, s1.x2, s1.y2) < (s2.x1, s2.y1, s2.x2, s2.y2)

		WARNING : this method raises ZeroDivisionError when called 
		on a vertical segment.
		'''
		self_y = self.yAtX(ComparableSegment.currentX)
		other_y = other.yAtX(ComparableSegment.currentX)

		return ((self_y, self.gradient(), self.x1, self.y1, self.x2, self.y2) < 
				(other_y, other.gradient(), other.x1, other.y1, other.x2, other.y2))

	def isBelow(self, other):
		'''
		Returns true if and only if self is below other.
		A segment s1 is below a segment s2 if : 
		- s1's y-coordinate < s2's y-coordinate at currentX
		- s1's y-coordinate = s2's y-coordinate at currentX 
		and s1.gradient < s2.gradient
		
		WARNING : this method raises ZeroDivisionError when called 
		on a vertical segment.
		'''
		self_y = self.yAtX(ComparableSegment.currentX)
		other_y = other.yAtX(ComparableSegment.currentX)

		return (self_y, self.gradient()) < (other_y, other.gradient())
