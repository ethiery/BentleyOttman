import heapq
from sys import maxsize
from math import floor
from sortedcontainers import SortedList
from Segment import Segment

class Event(object):
	''' 
	This class represents an event encountered by the sweep line
	in the Bentley-Ottmann algorithm. It has 3 attributes :
	- its 2 coordinates (x,y)
	- a sorted list of non vertical segments whose left endpoints have 
	this coordinates
	- a sorted list of non vertical segments whose right endpoints have 
	this coordinates
	- a sorted list of segments which intersect at this coordinates 
	(not on their endpoints)
	- a list of verticals segment whose left endpoints have 
	this coordinates
	- a list of verticals segment whose right endpoints have 
	this coordinates
	'''

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.left = []
		self.right = []
		self.inter = []
		self.low = []
		self.high = []


	def __eq__(self, other):
		'''
		Two events are equals if they have the same coordinates
		'''
		if other == None:
			return False
		elif not isinstance(other, Event):
			raise TypeError()
		else:
			return (self.x, self.y) == (other.x, other.y)

	def __ne__(self, other):
		return not self == other

	def __lt__(self, other):
		'''
		Events are compared according to their coordinates
		'''
		return (self.x, self.y) < (other.x, other.y)


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
		Initializes the list of events corresponding to a list of segments
		'''
		self.event_finder = {}
		# Computes events
		for s in segments:
			# finds or creates the left endpoint event
			e1 = self.event_finder.get((s.x1, s.y1), None)
			if e1 == None:
				e1 = Event(s.x1, s.y1)
				self.event_finder[(s.x1, s.y1)] = e1
			# finds or creates the right endpoint event
			e2 = self.event_finder.get((s.x2, s.y2), None)
			if e2 == None:
				e2 = Event(s.x2, s.y2)
				self.event_finder[(s.x2, s.y2)] = e2
			# Adds the endpoints in the right list
			if s.isVertical:
				e1.low.append(s)
				e2.high.append(s)
			else:
				heapq.heappush(e1.left, s)
				heapq.heappush(e2.right, s)
		# Sorts events in the queue
		self.q = []
		for event in self.event_finder.values():
			heapq.heappush(self.q, event)

	def addInter(self, x, y, seg1, seg2):
		'''
		Adds an intersection between seg1 and seg2 at the 
		coordinates (x, y) to the eventQueue.
		'''
		e = self.event_finder.get((x, y), None)
		# finds or creates the intersection event
		if e == None:
			e = Event(x, y)
			self.event_finder[(x, y)] = e
			heapq.heappush(self.q, e)
		# Adds the segments to this to this event
		for s in (seg1, seg2):
			if s not in e.inter:
				heapq.heappush(e.inter, s)

	def nextEvent(self):
		'''
		Removes the next Event from the queue and returns it.
		'''
		e = heapq.heappop(self.q)
		del self.event_finder[(e.x, e.y)]
		return e

	def isEmpty(self):
		'''
		Returns true if and only if the queue is empty.
		'''
		return len(self.q) == 0


class SweepLine(object):
	'''
	This class represents the vertical sweep line which sweeps over 
	the set of segments in the Bentley-Ottmann algorithm.

	At any moment, it contains a sorted list of all the segments 
	which intersect with the sweep line in its current position, 

	It would usually rely on a balanced binary search tree data 
	structure in order to have O(log(N)) insertion, deletion and swapping.

	Instead, I chose to use a SortedList of Grant Jenks' SortedContainers 
	module, which has several advantages that you can discover by browsing
	its page. It allows O(log(N)) insertion, deletion and swapping, and I
	find it to be faster in practice.
	'''

	def __init__(self):
		'''
		Initializes the Sorted List
		'''
		self.l = SortedList()

	def add(self, seg):
		'''
		Adds seg to the sweep line
		Note that seg is placed below any segment which passes above
		its left endpoint, and above any segment which passes on or below
		its left endpoint
		'''
		self.l.add(seg)

	def remove(self, seg):
		'''
		Removes seg from the sweep line.
		'''
		self.l.remove(seg)

	def below(self, seg):
		'''
		Returns the segment which is just below seg or None if it
		does not exists.
		seg does not necessarily have to be in the sweep line.
		'''
		i = self.l.bisect_left(seg)
		if i-1 >= 0:
			return self.l[i-1]
		else:
			return None

	def above(self, seg):
		'''
		Returns the segment which is just above seg or None if it
		does not exists.
		seg does not necessarily have to be in the sweep line.
		'''
		i = self.l.bisect_right(seg)
		if i < len(self.l):
			return self.l[i]
		else:
			return None

	def between(self, seg_inf, seg_sup):
		'''
		Returns a list of all the segments in the sweep line
		between seg_inf and seg_sup not included
		'''
		i_sup = self.l.bisect_left(seg_sup)
		i_inf = self.l.bisect_right(seg_inf)
		if i_sup < i_inf:
			return []
		else:
			return self.l[i_inf:i_sup]

	def swap(self, x, y, seg1, seg2):
		'''
		Swaps seg1 and seg2 in the sweep line, at coord (x, y).
		'''
		i1 = self.l.index(seg1)
		i2 = self.l.index(seg2)
		# Change the segments left end points so that the 
		# following swap keep sort order
		seg1.x1, seg1.y1 = x, y
		seg2.x1, seg2.y1 = x, y
		# Swaps the segments
		self.l[i1] = seg2
		self.l[i2] = seg1

	def isEmpty(self):
		'''
		Returns true if and only if the sweep line is empty.
		'''
		return len(self.l) == 0

	def iter(self):
		'''
		Returns an iterator over the segments in the sweep line.
		Segments must to be added or deleted while iterating
		'''
		return iter(self.l)


def intersection_list(segments):

	# Initializes sorted event queue 
	event_queue = EventQueue(segments)
	# Initializes empty sweep line
	sweep_line = SweepLine()
	# Initializes empty output intersection list
	intersections = []

	# Initializes empty list of vertical segments being swept
	vertical_segments = []

	while not event_queue.isEmpty():
		event = event_queue.nextEvent()
		print("event {}, {} :".format(event.x, event.y))

		################## Handles vertical low endpoints ################
		for vert_seg in event.low:
			vertical_segments.append(vert_seg)

		#################### Handles right endpoints #####################
		if len(event.right) > 0: 
			# computes intersection between segments above et below 
			# the ones that are going to be removed
			above = sweep_line.above(event.right[0])
			below = sweep_line.below(event.right[-1])
			if below != None and above != None:
				inter = below.intersectionWith(above)
				if inter != None:
					x, y = inter
					event_queue.addInter(x, y, below, above)
		for seg in event.right:
			# removes it from the sweep line
			sweep_line.remove(seg)
			# Adds its intersection with vertical segments
			for vert_seg in vertical_segments:
				print("add inter {} {} right endpoint".format(seg.x2, seg.y2))
				intersections.append((seg.x2, seg.y2, seg, vert_seg))

		############## Handles non vertical intersections ###############
		nb_segs = len(event.inter)
		# Adds all the intersections between segments intersecting here
		for i in range(nb_segs):
			for j in range(i+1, nb_segs):
				intersections.append((event.x, event.y, 
									  event.inter[i], event.inter[j]))
				print("add inter {} {} intersection".format(event.x, event.y))

		# Inverse the order of intersections segments in the sweep line
		for i in range(floor(len(event.inter)/2)):
			sweep_line.swap(event.x, event.y, event.inter[i], event.inter[-i-1])
		if len(event.inter) > 0:
			# Computes the intersection between the new highest and the
			# segment above it
			highest = event.inter[0]
			above = sweep_line.above(highest)
			if above != None:
				inter = highest.intersectionWith(above)
				if inter != None:
					x, y = inter
					event_queue.addInter(x, y, highest, above)


			# Computes the intersection between the new lowest and the
			# segment below it
			lowest = event.inter[-1]
			below = sweep_line.below(lowest)
			if below != None:
				inter = lowest.intersectionWith(below)
				if inter != None:
					x, y = inter
					event_queue.addInter(x, y, lowest, below)


		#################### Handles left endpoints ##################### 
		for seg in event.left:
			# Adds it to the sweep line
			#print("adding segment {} to the sweep line".format(seg))
			sweep_line.add(seg)
			# Adds its intersection with vertical segments
			for vert_seg in vertical_segments:
				intersections.append((seg.x1, seg.y1, seg, vert_seg))
				print("add inter {} {} left endpoint".format(seg.x1, seg.y1))

		if len(event.left) > 0:
			# Computes the  intersection between the highest new 
			# segment and the one above it
			highest = event.left[-1]
			above = sweep_line.above(highest)
			if above != None:
				inter = highest.intersectionWith(above)
				if inter != None:
					x, y = inter
					event_queue.addInter(x, y, highest, above)

			# Computes the intersection between the lowest new 
			# segment and the one below it
			lowest = event.left[0]
			below = sweep_line.below(lowest)
			if below != None:
				inter = lowest.intersectionWith(below)
				if inter != None:
					x, y = inter
					event_queue.addInter(x, y, lowest, below)

		
		################# Handles vertical high endpoints ################
		for vert_seg in event.high:
			x = vert_seg.x1
			y_inf, y_sup = vert_seg.y1, vert_seg.y2
			seg_inf = Segment(x, y_inf, x+1, y_inf)
			seg_sup = Segment(x, y_sup, x+1, y_sup)
			l = sweep_line.between(seg_inf, seg_sup)
			for seg in l:
				y = seg.yAtX(x)
				intersections.append((x, y, seg, vert_seg))
				print("add inter {} {} vertical".format(x, y))

			vertical_segments.remove(vert_seg)

	return intersections
