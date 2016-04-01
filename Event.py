from ComparableSegment import ComparableSegment
import heapq

class Event(object):
	''' 
	This class represents an event encountered by the sweep line
	in the Bentley-Ottmann algorithm. An event can either be:
	- one or more segment's endpoint ;
	- an inner intersection point between 2 or more segments ;
	- a combination of the 2 above.

	An event properties are its coordinates (x, y), and 5 set of 
	ComparableSegments named left, right, inner_inter, low and high, 
	which contains respectively:
	- non vertical segments whose left endpoints belong to the event ;
	- non vertical segments whose right endpoints belong to the event ;
	- non vertical segments whose endpoints do not belong to the event, 
	but intersect at this coordinates ;
	- vertical segments whose lower endpoint belong to the event ;
	- vertical segments whose higher endpoints belong to the event.

	Non vertical segments lists are kept ordered by increasing 
	gradient, and vertical segments lists are not ordered.

	Be aware that for performance purposes, accessing one of these
	lists will not create a copy, so you should not modify it 
	directly if you want to use the Event again later.

	Implementation notes :
	- non vertical segments lists are kept ordered thanks to python
	heapq module, which allows insertion in O(lg(N))
	- vertical segments lists are not ordered, so insertion is 
	in O(lg(N))
	'''

	def __init__(self, x, y):
		'''
		Initializes a new Event with coordinates (x, y),
		and an empty set of segment
		'''
		self.x, self.y = x, y
		self.left, self.right = [], []
		self.inner_inter = []
		self.low, self.high = [],[]

	def __eq__(self, other):
		'''
		Returns true if and only if self and other are equals.
		Two events are equals if they have the exact same coordinates.
		'''
		if other == None:
			return False
		elif not isinstance(other, Event):
			raise TypeError()
		else:
			return (self.x, self.y) == (other.x, other.y)

	def __lt__(self, other):
		'''
		Returns true if and only if self is below other.
		An event e1 is below an event e2 if
		e1.x < e2.x or e1.x = e2.x and e1.y < e2.y.
		'''
		return (self.x, self.y) < (other.x, other.y)

	def __str__(self):
		return ('Event at ({}, {}), contains:'.format(self.x, self.y) +
		'\nleft endpoints of : ' + 
		', '.join([str(s) for s in self.left]) +
		'\nright endpoints of : ' + 
		', '.join([str(s) for s in self.right]) +
		'\ninner intersection points of : ' + 
		', '.join([str(s) for s in self.inner_inter]) +
		'\nlow endpoints of : ' + 
		', '.join([str(s) for s in self.low]) +
		'\nhigh endpoints of : ' + 
		', '.join([str(s) for s in self.high]))
			

	def addSegment(self, segment):
		'''
		Adds segment to the right list of segments.
		segment must be a ComparableSegment, or a TypeError
		will be raised.
		'''
		if not isinstance(segment, ComparableSegment):
			raise TypeError('Event can only contain ComparableSegments')
		else:
			ComparableSegment.currentX = self.x
			if (segment.x1, segment.y1) == (self.x, self.y):
				if segment.isVertical():
					self.low.append(segment)
				else:
					heapq.heappush(self.left, segment)
			elif (segment.x2, segment.y2) == (self.x, self.y):
				if segment.isVertical():
					self.high.append(segment)
				else:
					heapq.heappush(self.right, segment)
			else:
				heapq.heappush(self.inner_inter, segment)