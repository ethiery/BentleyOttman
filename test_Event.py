import unittest
from ComparableSegment import ComparableSegment
from Event import Event

class TestEvent(unittest.TestCase):

	# __init__

	def test__init(self):
		e = Event(0, 1)
		self.assertEqual((e.x, e.y), (0, 1))
		self.assertEqual((e.left, e.right, e.inner_inter, e.low, e.high), 
						 ([], [], [], [], []))

	# __eq__

	def test__eq__equal_events(self):
		e1 = Event(0, 0)
		e2 = Event(0, 0)
		self.assertEqual(e1, e2)

	def test__eq__not_equal_events(self):
		e1 = Event(0, 0)
		e2 = Event(0, 1)
		self.assertNotEqual(e1, e2)

	def test__eq__None(self):
		e1 = Event(0, 0)
		e2 = None
		self.assertNotEqual(e1, e2)

	# __cmp__

	def test__cmp_different_x(self):
		e1 = Event(0, 0)
		e2 = Event(1, 1)
		self.assertTrue(e1 < e2)

	def test__cmp_same_x(self):
		e1 = Event(0, 0)
		e2 = Event(0, 1)
		self.assertTrue(e1 < e2)

	# __str__

	def test__str(self):
		e = Event(1, 1)
		s1 = ComparableSegment(1, 1, 2, 2)
		s2 = ComparableSegment(0, 0, 1, 1)
		s3 = ComparableSegment(0, 0, 2, 2)
		s4 = ComparableSegment(1, 1, 1, 2)
		s5 = ComparableSegment(1, 0, 1, 1)
		e.addSegment(s1)
		e.addSegment(s2)
		e.addSegment(s3)
		e.addSegment(s4)
		e.addSegment(s5)
		self.assertEqual(str(e),
			('Event at (1, 1), contains:' +
			'\nleft endpoints of : ' + str(s1) +
			'\nright endpoints of : ' + str(s2) +
			'\ninner intersection points of : ' + str(s3) +
			'\nlow endpoints of : ' + str(s4) +
			'\nhigh endpoints of : ' + str(s5)))

	# addSegment

	def test__addSegment__left_first(self):
		e = Event(0, 0)
		s = ComparableSegment(0, 0, 1, 1)
		e.addSegment(s)
		self.assertEqual(e.left, [s])
		self.assertEqual((e.right, e.inner_inter, e.low, e.high), 
						 ([], [], [], []))

	def test__addSegment__left_before(self):
		e = Event(0, 0)
		s1 = ComparableSegment(0, 0, 1, 1)
		s2 = ComparableSegment(0, 0, 1, 0)
		e.addSegment(s1)
		e.addSegment(s2)
		self.assertEqual(e.left, [s2, s1])
		self.assertEqual((e.right, e.inner_inter, e.low, e.high), 
						 ([], [], [], []))

	def test__addSegment__left_after(self):
		e = Event(0, 0)
		s1 = ComparableSegment(0, 0, 1, 1)
		s2 = ComparableSegment(0, 0, 1, 2)
		e.addSegment(s1)
		e.addSegment(s2)
		self.assertEqual(e.left, [s1, s2])
		self.assertEqual((e.right, e.inner_inter, e.low, e.high), 
						 ([], [], [], []))

	def test__addSegment__right_first(self):
		e = Event(1, 1)
		s = ComparableSegment(0, 0, 1, 1)
		e.addSegment(s)
		self.assertEqual(e.right, [s])
		self.assertEqual((e.left, e.inner_inter, e.low, e.high), 
						 ([], [], [], []))

	def test__addSegment__right_before(self):
		e = Event(1, 1)
		s1 = ComparableSegment(0, 0, 1, 1)
		s2 = ComparableSegment(0, 1, 1, 1)
		e.addSegment(s1)
		e.addSegment(s2)
		self.assertEqual(e.right, [s2, s1])
		self.assertEqual((e.left, e.inner_inter, e.low, e.high), 
						 ([], [], [], []))

	def test__addSegment__right_after(self):
		e = Event(1, 1)
		s1 = ComparableSegment(0, 0, 1, 1)
		s2 = ComparableSegment(0, -1, 1, 1)
		e.addSegment(s1)
		e.addSegment(s2)
		self.assertEqual(e.right, [s1, s2])
		self.assertEqual((e.left, e.inner_inter, e.low, e.high), 
						 ([], [], [], []))

	def test__addSegment__inner_inter_first(self):
		e = Event(0.5, 0.5)
		s = ComparableSegment(0, 0.5, 1, 0.5)
		e.addSegment(s)
		self.assertEqual(e.inner_inter, [s])
		self.assertEqual((e.left, e.right, e.low, e.high), 
						 ([], [], [], []))

	def test__addSegment__inner_inter_before(self):
		e = Event(0.5, 0.5)
		s1 = ComparableSegment(0, 0.5, 1, 0.5)
		s2 = ComparableSegment(0, 1, 1, 0)
		e.addSegment(s1)
		e.addSegment(s2)
		self.assertEqual(e.inner_inter, [s2, s1])
		self.assertEqual((e.left, e.right, e.low, e.high), 
						 ([], [], [], []))

	def test__addSegment__inner_inter_after(self):
		e = Event(0.5, 0.5)
		s1 = ComparableSegment(0, 0.5, 1, 0.5)
		s2 = ComparableSegment(0, 0, 1, 1)
		e.addSegment(s1)
		e.addSegment(s2)
		self.assertEqual(e.inner_inter, [s1, s2])
		self.assertEqual((e.left, e.right, e.low, e.high), 
						 ([], [], [], []))

	def test__addSegment__low_first(self):
		e = Event(0, 0)
		s = ComparableSegment(0, 0, 0, 1)
		e.addSegment(s)
		self.assertEqual(e.low, [s])
		self.assertEqual((e.left, e.right, e.inner_inter, e.high), 
						 ([], [], [], []))

	def test__addSegment__low_more(self):
		e = Event(0, 0)
		s1 = ComparableSegment(0, 0, 0, 1)
		s2 = ComparableSegment(0, 0, 0, 2)
		e.addSegment(s1)
		e.addSegment(s2)
		self.assertEqual(len(e.low), 2)
		self.assertTrue(s1 in e.low)
		self.assertTrue(s2 in e.low)
		self.assertEqual((e.left, e.right, e.inner_inter, e.high), 
						 ([], [], [], []))

	def test__addSegment__high_first(self):
		e = Event(1, 1)
		s = ComparableSegment(1, 0, 1, 1)
		e.addSegment(s)
		self.assertEqual(e.high, [s])
		self.assertEqual((e.left, e.right, e.inner_inter, e.low), 
						 ([], [], [], []))

	def test__addSegment__high_more(self):
		e = Event(1, 1)
		s1 = ComparableSegment(1, 0, 1, 1)
		s2 = ComparableSegment(1, -1, 1, 1)
		e.addSegment(s1)
		e.addSegment(s2)
		self.assertEqual(len(e.high), 2)
		self.assertTrue(s1 in e.high)
		self.assertTrue(s2 in e.high)
		self.assertEqual((e.left, e.right, e.inner_inter, e.low), 
						 ([], [], [], []))

if __name__ == '__main__':
	unittest.main()