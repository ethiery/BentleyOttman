import heapq
from Event import Event

class EventQueue(object):
	''' 
	This class represents a queue containing Events, and which is
	maintained ordered throughout the execution of the Bentley-Ottmann
	algorithm.

	It relies on the python heapq module, which allows insertion in
	O(lg(S)) (where S is the current size of the queue), and access to
	the smallest element (i.e. the next Event) in O(1).

	Note : when computing the intersections of a set of N segments,
	at any moment the size of the queue is S <= 2*N + N^2
	2*N events being the endpoints of the N segments and
	N^2 events being the N^2 potential intersection points. 
	'''

	def __init__(self, segments):
		'''
		Initializes the list of events corresponding to a list of 
		ComparableSegments
		'''
		self.event_finder = {}
		self.queue = []
		# Adds endpoints one by one, creating a new Event when needed
		for s in segments:
			e1 = self.getOrCreate(s.x1, s.y1)
			e1.addSegment(s)
			e2 = self.getOrCreate(s.x2, s.y2)
			e2.addSegment(s)

	def getOrCreate(self, x, y):
		'''
		Looks for the event of coordinates (x, y) in the queue,
		creates it if it does not exist yet, and returns it
		'''
		e = self.event_finder.get((x, y), None)
		if e == None:
			e = Event(x, y)
			heapq.heappush(self.queue, e)
			self.event_finder[(x, y)] = e
		return e

	def addIntersectingSegment(self, seg, x, y):
		'''
		Let e be the event of coordinates (x, y) in the queue,
		newly created if necessary.
		If seg is not already in the inner intersecting segments
		of this event, adds it to the list.

		Raises ValueError if one of segment's endpoints
		is (x, y).
		'''
		if (x, y) in [(seg.x1, seg.y1), (seg.x2, seg.y2)]:
			raise ValueError('One of this segment\'s endpoints belong to the event')
		else:
			e = self.getOrCreate(x, y)
			if seg not in e.inner_inter:
				e.addSegment(seg)

	def nextEvent(self):
		'''
		Removes the next Event from the queue and returns it.
		'''
		e = heapq.heappop(self.queue)
		del self.event_finder[(e.x, e.y)]
		return e

	def isEmpty(self):
		'''
		Returns true if and only if the queue is empty.
		'''
		return len(self.queue) == 0