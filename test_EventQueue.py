import unittest
from ComparableSegment import ComparableSegment
from Event import Event
from EventQueue import EventQueue

class TestEventQueue(unittest.TestCase):

	# __init__

	def test__init__empty(self):
		q = EventQueue([])
		self.assertTrue(q.isEmpty())

	def test__init__single_not_vertical(self):
		s1 = ComparableSegment(0, 0, 1, 1)
		q = EventQueue([s1])
		self.assertFalse(q.isEmpty())
		e1 = q.nextEvent()
		self.assertEqual((e1.x, e1.y), (0, 0))
		self.assertEqual((e1.left, e1.right, e1.inner_inter, e1.low, e1.high), 
						 ([s1], [], [], [], []))
		e2 = q.nextEvent()
		self.assertEqual((e2.x, e2.y), (1, 1))
		self.assertEqual((e2.left, e2.right, e2.inner_inter, e2.low, e2.high), 
						 ([], [s1], [], [], []))
		self.assertTrue(q.isEmpty())

	def test__init__single_vertical(self):
		s1 = ComparableSegment(0, 0, 0, 1)
		q = EventQueue([s1])
		self.assertFalse(q.isEmpty())
		e1 = q.nextEvent()
		self.assertEqual((e1.x, e1.y), (0, 0))
		self.assertEqual((e1.left, e1.right, e1.inner_inter, e1.low, e1.high), 
						 ([], [], [], [s1], []))
		e2 = q.nextEvent()
		self.assertEqual((e2.x, e2.y), (0, 1))
		self.assertEqual((e2.left, e2.right, e2.inner_inter, e2.low, e2.high), 
						 ([], [], [], [], [s1]))
		self.assertTrue(q.isEmpty())

	def test__init__several(self):
		s1 = ComparableSegment(0, 1, 2, 2)
		s2 = ComparableSegment(0, 0, 1, 1)
		s3 = ComparableSegment(1, 1, 1, 3)
		s4 = ComparableSegment(0, 0, 2, 2)
		s5 = ComparableSegment(0, 1, 1, 3)
		segments = [s1, s2, s3, s4, s5]
		q = EventQueue(segments)
		self.assertFalse(q.isEmpty())
		e1 = q.nextEvent()
		self.assertEqual((e1.x, e1.y), (0, 0))
		self.assertEqual((e1.right, e1.inner_inter, e1.low, e1.high), 
						 ([], [], [], []))
		self.assertTrue(s2 in e1.left and s4 in e1.left)
		e2 = q.nextEvent()
		self.assertEqual((e2.x, e2.y), (0, 1))
		self.assertEqual((e2.left, e2.right, e2.inner_inter, e2.low, e2.high), 
						 ([s1, s5], [], [], [], []))
		e3 = q.nextEvent()
		self.assertEqual((e3.x, e3.y), (1, 1))
		self.assertEqual((e3.left, e3.right, e3.inner_inter, e3.low, e3.high), 
						 ([], [s2], [], [s3], []))
		e4 = q.nextEvent()
		self.assertEqual((e4.x, e4.y), (1, 3))
		self.assertEqual((e4.left, e4.right, e4.inner_inter, e4.low, e4.high), 
						 ([], [s5], [], [], [s3]))
		e5 = q.nextEvent()
		self.assertEqual((e5.x, e5.y), (2, 2))
		self.assertEqual((e5.left, e5.right, e5.inner_inter, e5.low, e5.high), 
						 ([], [s1, s4], [], [], []))
		self.assertTrue(q.isEmpty())

	# addIntersectingSegment

	def test__addIntersectingSegment__valid(self):
		s1 = ComparableSegment(1, 1, 1, 2)
		s2 = ComparableSegment(0, 0, 2, 2)
		q = EventQueue([s1, s2])
		q.addIntersectingSegment(s2, 1, 1)
		self.assertFalse(q.isEmpty())
		e1 = q.nextEvent()
		self.assertEqual((e1.x, e1.y), (0, 0))
		self.assertEqual((e1.left, e1.right, e1.inner_inter, e1.low, e1.high), 
						 ([s2], [], [], [], []))
		e2 = q.nextEvent()
		self.assertEqual((e2.x, e2.y), (1, 1))
		self.assertEqual((e2.left, e2.right, e2.inner_inter, e2.low, e2.high), 
						 ([], [], [s2], [s1], []))
		e3 = q.nextEvent()
		self.assertEqual((e3.x, e3.y), (1, 2))
		self.assertEqual((e3.left, e3.right, e3.inner_inter, e3.low, e3.high), 
						 ([], [], [], [], [s1]))
		e4 = q.nextEvent()
		self.assertEqual((e4.x, e4.y), (2, 2))
		self.assertEqual((e4.left, e4.right, e4.inner_inter, e4.low, e4.high), 
						 ([], [s2], [], [], []))
		self.assertTrue(q.isEmpty())

	def test__addIntersectingSegment__invalid(self):
		s1 = ComparableSegment(0, 0, 1, 1)
		q = EventQueue([s1])
		with self.assertRaises(ValueError) as cm:
			q.addIntersectingSegment(s1, 1, 1)
		self.assertTrue('One of this segment\'s endpoints belong to the event' 
						in cm.exception.args)


if __name__ == '__main__':
	unittest.main()