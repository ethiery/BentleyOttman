import unittest
from ComparableSegment import ComparableSegment
from BentleyOttmann import intersectionsList

class TestBentleyOttman(unittest.TestCase):

	# only vertical segments

	# def test__2_overlapping_vertical_segments(self):
	# 	s1 = ComparableSegment(0, 0, 0, 2)
	# 	s2 = ComparableSegment(0, 1, 0, 3)
	# 	self.assertEqual(intersectionsList([s1, s2]),
	# 					 [((s2, s1), ComparableSegment(0, 1, 0, 2))])

	# def test__2_disjoint_vertical_segments(self):
	# 	s1 = ComparableSegment(0, 0, 0, 1)
	# 	s2 = ComparableSegment(0, 2, 0, 3)
	# 	self.assertEqual(intersectionsList([s1, s2]), [])

	# def test__one_vertical_one_normal(self):
	# 	s1 = ComparableSegment(0, 0, 0, 2)
	# 	s2 = ComparableSegment(0, 1, 1, 2)
	# 	self.assertEqual(intersectionsList([s1, s2]), 
	# 					 [((s2, s1), (0, 1))])

	# def test__one_normal_one_vertical(self):
	# 	s1 = ComparableSegment(0, 1, 1, 2)
	# 	s2 = ComparableSegment(1, 0, 1, 2)
	# 	self.assertEqual(intersectionsList([s1, s2]), 
	# 					 [((s2, s1), (1, 2))])

	# def test__two_with_same_leftpoint_not_overlapping(self):
	# 	s1 = ComparableSegment(0, 0, 1, 1)
	# 	s2 = ComparableSegment(0, 0, 1, 2)
	# 	self.assertEqual(intersectionsList([s1, s2]), 
	# 					 [((s1, s2), (0, 0))])

	# def test__two_with_same_leftpoint_overlapping(self):
	# 	s1 = ComparableSegment(0, 0, 1, 1)
	# 	s2 = ComparableSegment(0, 0, 2, 2)
	# 	self.assertEqual(intersectionsList([s1, s2]), 
	# 					 [((s1, s2), ComparableSegment(0, 0, 1, 1))])

	# def test__two_leftpoint_rightpoint(self):
	# 	s1 = ComparableSegment(0, 0, 1, 1)
	# 	s2 = ComparableSegment(1, 1, 2, 2)
	# 	self.assertEqual(intersectionsList([s1, s2]), 
	# 					 [((s1, s2), (1, 1))])

	# def test_2_normal_intersecting_single_point(self):
	# 	s1 = ComparableSegment(0, 0, 1, 1)
	# 	s2 = ComparableSegment(0, 1, 1, 0)
	# 	self.assertEqual(intersectionsList([s1, s2]),
	# 					 [((s2, s1), (0.5, 0.5))])

	def test_2_normal_overlapping(self):
		s1 = ComparableSegment(0, 0, 2, 2)
		s2 = ComparableSegment(1, 1, 3, 3)
		self.assertEqual(intersectionsList([s1, s2]),
						 [((s1, s2), ComparableSegment(1, 1, 2, 2))])



if __name__ == '__main__':
	unittest.main()