import unittest
from ComparableSegment import ComparableSegment

class TestComparableSegment(unittest.TestCase):

	# __lt__

	def test__lt__different_y_coordinates(self):
		s1 = ComparableSegment(0, 0, 2, 2)
		s2 = ComparableSegment(0, 2, 2, 0)
		ComparableSegment.currentX = 0
		self.assertTrue(s1 < s2)

	def test__lt__different_y_coordinates2(self):
		s1 = ComparableSegment(0, 0, 2, 2)
		s2 = ComparableSegment(0, 2, 2, 0)
		ComparableSegment.currentX = 2
		self.assertTrue(s1 > s2)

	def test__lt__different_gradient(self):
		s1 = ComparableSegment(0, 0, 2, 2)
		s2 = ComparableSegment(0, 2, 2, 0)
		ComparableSegment.currentX = 1
		self.assertTrue(s1 > s2)

	def test__lt__different_left_endpoints(self):
		s1 = ComparableSegment(0, 0, 2, 2)
		s2 = ComparableSegment(1, 1, 2, 2)
		ComparableSegment.currentX = 1
		self.assertTrue(s1 < s2)

	def test__lt__different_right_endpoints(self):
		s1 = ComparableSegment(0, 0, 2, 2)
		s2 = ComparableSegment(0, 0, 3, 3)
		ComparableSegment.currentX = 1
		self.assertTrue(s1 < s2)

	def test__lt__equals(self):
		s1 = ComparableSegment(0, 0, 2, 2)
		s2 = ComparableSegment(0, 0, 2, 2)
		ComparableSegment.currentX = 1
		self.assertFalse(s1 < s2)
		self.assertFalse(s2 < s1)
		self.assertEqual(s1, s2)

	# isBelow

	def test__isBelow__different_y_coordinates(self):
		s1 = ComparableSegment(0, 0, 2, 1)
		s2 = ComparableSegment(0, 0, 2, 2)
		ComparableSegment.currentX = 1
		self.assertTrue(s1.isBelow(s2))

	def test__isBelow__different_gradient(self):
		s1 = ComparableSegment(0, 0, 2, 2)
		s2 = ComparableSegment(0, 2, 2, 0)
		ComparableSegment.currentX = 1
		self.assertTrue(s2.isBelow(s1))

	def test__isBelow__false(self):
		s1 = ComparableSegment(0, 0, 3, 3)
		s2 = ComparableSegment(1, 1, 3, 3)
		ComparableSegment.currentX = 2
		self.assertFalse(s2.isBelow(s1) or s1.isBelow(s2))




if __name__ == '__main__':
	unittest.main()