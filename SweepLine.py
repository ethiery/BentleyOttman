from math import floor
from sortedcontainers import SortedList
from ComparableSegment import ComparableSegment

class SweepLine(object):
	'''
	This class represents the vertical sweep line which sweeps over 
	the set of segments in the Bentley-Ottmann algorithm.

	At any moment, it contains a sorted list of all the 
	ComparableSegments which intersect with the sweep line in its 
	current position.

	Note that if 2 segments s1 and s2 are overlapping, you cannot 
	assume anything about their order in the sorted queue, as 
	s1 < s2 and s1 > s2 are both false

	Such sorted list would usually rely on a balanced binary search 
	tree data structure in order to have O(log(N)) insertion, 
	deletion and swapping.

	Instead, I chose to use a SortedList of Grant Jenks' SortedContainers 
	module, which has several advantages that you can discover by browsing
	its page. It allows O(log(N)) insertion, deletion and swapping, and I
	find it to be faster in practice.
	'''

	def __init__(self):
		'''
		Initializes an empty sweep line.
		'''
		self.l = SortedList()

	def isEmpty(self):
		'''
		Returns true if and only if the sweep line is empty.
		'''
		return len(self.l) == 0

	def addSegment(self, seg):
		'''
		Adds seg to the sweep line.
		'''
		ComparableSegment.currentX = seg.x1 
		self.l.add(seg)

	def removeSegment(self, seg):
		'''
		Removes seg from the sweep line.
		'''
		self.l.remove(seg)

	def belowSegments(self, seg):
		'''
		Returns a list containing :
		- The highest segment s_below contained in the sweep line 
		such as s_below.isBelow(seg)
		- All the segments s contained before s_below in the sweep 
		line but such as s.isBelow(s_below) is false, (i.e. which have the 
		same y-coordinate at ComparableSegment.currentX and gradient).
		'''
		res = []
		# i = index of seg
		i = self.l.index(seg)
		# Passes segments which have same y-coordinate and gradient
		# to find s_below
		while i-1 >= 0:
			prev = self.l[i-1]
			i -= 1
			if prev.isBelow(seg):
				res.append(prev)
				break
		# Appends all the segments which have same y-coordinate and 
		# gradient as s_below
		while i-1 >= 0:
			prev = self.l[i-1]
			if prev.isBelow(res[0]):
				break
			res.append(prev)
			i -= 1
		return res

	def aboveSegments(self, seg):
		'''
		Returns a list containing :
		- The lowest segment s_above contained in the sweep line 
		such as seg < s_above
		- All the segments s contained after s_above in the sweep 
		line but such as s_below < s is false, (i.e. which have the 
		same y-coordinate at ComparableSegment.currentX and gradient).
		'''
		res = []
		# i = index of seg
		i = self.l.index(seg)
		# Passes segments which have same y-coordinate and gradient
		# to find s_above
		while i+1 < len(self.l):
			succ = self.l[i+1]
			i += 1
			if seg.isBelow(succ):
				res.append(succ)
				break
		# Appends all the segments which have same y-coordinate and 
		# gradient as s_above
		while i+1 < len(self.l):
			succ = self.l[i+1]
			if res[0].isBelow(succ):
				break
			res.append(succ)
			i += 1
		return res

	def sameLevelAs(self, seg):
		'''
		Returns a list containing the segments s of the line
		such as s.aboveSegments(seg) and seg.aboveSegments(s) are
		both false, i.e. all the segments with same y-coordinate at 
		ComparableSegment.currentX and gradient as seg.
		'''
		i = self.l.index(seg)
		res = [self.l[i]]
		# Looks for same level segments above
		j = i + 1
		while j < len(self.l) and not seg.isBelow(self.l[j]):
			res.append(self.l[j])
			j += 1
		# Looks for same level segments below
		j = i - 1
		while j >= 0 and not self.l[j].isBelow(seg):
			res.append(self.l[j])
			j -= 1
		return res

	def betweenY(self, y_inf, y_sup, x):
		'''
		Returns a list of all the segments intersecting the sweep line
		between y-coordinates y_inf and y_sup included, at 
		x-coordinate x
		'''
		ComparableSegment.currentX = x
		res = []
		i = 0
		# Passes segments whose y-coordinate is < y_inf
		while i < len(self.l) and self.l[i].yAtX(x) < y_inf:
			i += 1
		while i < len(self.l) and self.l[i].yAtX(x) <= y_sup:
			res.append(self.l[i])
			i += 1

		return res

	def revertOrder(self, x, segments):
		'''
		Reverse the order of segments in the sweep line, at coord (x, y).
		'''
		indices = []
		for seg in segments:
			ComparableSegment.currentX = seg.x1
			indices.append(self.l.index(seg))
		# Update segments currentX so that the swap keep sort order
		ComparableSegment.currentX = x
		# Swaps the segments
		for i in range(floor(len(segments)/2)):
			i1 = indices[i]
			i2 = indices[-i-1]
			self.l[i1] = segments[-i-1]
			self.l[i2] = segments[i]