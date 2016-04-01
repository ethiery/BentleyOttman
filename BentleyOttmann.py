from Segment import Segment
from ComparableSegment import ComparableSegment
from Event import Event
from EventQueue import EventQueue
from SweepLine import SweepLine

def intersectionsList(segments):

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

		################## Handles vertical low endpoints ################
		# It this event contains a vertical low endpoints, the 
		# corresponding segment must be added to vertical_segments 
		# before handling other segments.
		#
		# Also, it intersects with :
		# - all the other vertical lines passing through this event
		# - all the segments currently in the sweep line, whose 
		# y-coordinate is between its low endpoint's and its high endpoint's 
		# 
		for seg in event.low:
			# Computes intersections
			for other in (vertical_segments +
						  sweep_line.betweenY(seg.y1, seg.y2, seg.x1)):
				inter = seg.intersectionWith(other)
				if inter != None:
					intersections.append(((seg, other), inter))
					#print("appened inter 1")
			# adds to vertical lines
			vertical_segments.append(seg)

		#################### Handles right endpoints #####################
		# It this event contains right endpoints, the corresponding 
		# segments must be removed from the sweep line.
		# These segments intersects with :
		# - all segments in vertical_segments (dealt with while adding them)
		# - all segments in event.left
		# - all segments in event.inner_inter
		# - each other 
		#
		for i in range(len(event.right)):
			seg = event.right[i]
			# Adds intersections
			for other in event.left:
				intersections.append(((seg, other), (event.x, event.y)))
				#print("appened inter 2")
			for j in range(i+1, len(event.right)):
				other = event.right[j]
				intersections.append(((seg, other), (event.x, event.y)))
				#print("appened inter 3")
			for other in event.inner_inter:
				intersections.append(((seg, other), (event.x, event.y)))
				#print("appened inter 4")
			# removes it to the sweep line
			sweep_line.removeSegment(seg)
		
		# ############## Handles non vertical intersections ###############
		# It this event contains inner intersection points, the order of
		# the corresponding segments in the sweep line but me reversed
		# (to express the crossing of the segments)
		# 
		# Also these segments intersects with :
		# - all segments in vertical_segments (dealt with while adding them)
		# - all segments in event.right (dealt with when removing them)
		# - all segments in event.left
		# - each other 
		for i in range(len(event.inner_inter)):
			seg = event.inner_inter[i]
			for other in event.left:
				inter = seg.intersectionWith(other)
				if inter != None:
					intersections.append(((seg, other), inter))
					#print("appened inter 5")
			for j in range(i+1, len(event.inner_inter)):
				other = event.inner_inter[j]
				intersections.append(((seg, other), (event.x, event.y)))
				#print("appened inter 6")

		# Inverses the order of intersections segments in the sweep line
		if event.inner_inter != []:
			sweep_line.revertOrder(event.x, event.inner_inter)
		
		# #################### Handles left endpoints #####################
		# It this event contains left endpoints, the corresponding 
		# segments must be added to the sweep line.
		# These segments intersects with :
		# - all segments in vertical_segments
		# - all segments in event.right (already delt with)
		# - all segments in event.inner_inter (already delt with)
		# - each other
		#
		for i in range(len(event.left)):
			seg = event.left[i]
			# Adds it to the sweep line
			sweep_line.addSegment(seg)
			# Adds sure intersections
			for other in vertical_segments:
				intersections.append(((seg, other), (seg.x1, seg.y1)))
				#print("appened inter 7")
			for j in range(i+1, len(event.left)):
				other = event.left[j]
				inter = seg.intersectionWith(other)
				if inter != None:
					intersections.append(((seg, other), inter))
					#print("appened inter 8")
			
		
		# ############# Computes following intersections ################
		# Now that we've added new segments, and removed some segments,
		# the segments with highest gradient of event.left + even.inner_inter
		# might intersect with the segments just above in the sweep line
		# and the segments with lowest gradient might intersect with the
		# segments below in the sweep line
		greatest = None
		if event.left != []:
			greatest = event.left[-1]
		if ((event.inner_inter != []) and 
			(greatest == None or greatest < event.inner_inter[-1])):
				greatest = event.inner_inter[-1]
		if greatest != None:
			highest_segments = sweep_line.sameLevelAs(greatest)
			above_segments = sweep_line.aboveSegments(greatest)
			for seg in highest_segments:
				for other in above_segments:
					inter = seg.intersectionWith(other)
					if (isinstance(inter, Segment) or
						inter == (event.x, event.y)):
							intersections.append(((seg, other), inter))
							#print("appened inter 9")
					elif inter != None:
						x, y = inter
						#print("found new inner inter above")
						event_queue.addIntersectingSegment(seg, x, y)
						event_queue.addIntersectingSegment(other, x, y)
		smallest = None
		if event.left != []:
			smallest = event.left[0]
		if ((event.inner_inter != []) and 
			(smallest == None or smallest < event.inner_inter[-1])):
				smallest = event.inner_inter[0]
		if smallest != None:
			lowest_segments = sweep_line.sameLevelAs(smallest)
			below_segments = sweep_line.belowSegments(smallest)
			for seg in lowest_segments:
				for other in below_segments:
					inter = seg.intersectionWith(other)
					if (isinstance(inter, Segment) or
						inter == (event.x, event.y)):
							intersections.append(((seg, other), inter))
							#print("appened inter 10")
					elif inter != None:
						x, y = inter
						#print("found new inner inter below")
						event_queue.addIntersectingSegment(seg, x, y)
						event_queue.addIntersectingSegment(other, x, y)

		
		################# Handles vertical high endpoints ################
		# It this event contains a vertical high endpoints, the 
		# corresponding segment must removed from vertical_segments 
		# after handling other segments, once all the intersections
		# with it have been computed.,
		for seg in event.high:
			vertical_segments.remove(seg)

	return intersections
