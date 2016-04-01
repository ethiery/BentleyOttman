import unittest
from Segment import Segment
from math import sqrt

class TestSegment(unittest.TestCase):

	# __init__

	def test__init__valid_args_correct_order(self):
		s = Segment(0, 0, 1, 1)
		self.assertEqual((s.x1, s.y1, s.x2, s.y2), (0, 0, 1, 1))

	def test__init__valid_args_wrong_order(self):
		s = Segment(1, 1, 0, 0)
		self.assertEqual((s.x1, s.y1, s.x2, s.y2), (0, 0, 1, 1))

	def test__init__invalid_args(self):
		with self.assertRaises(ValueError) as cm:
			s = Segment(0, 0, 0, 0)
		self.assertTrue('Invalid coordinates (segment is a point)' 
						in cm.exception.args)

	# __eq__

	def test__eq__equal_segments(self):
		s1 = Segment(0, 0, 1, 1)
		s2 = Segment(0, 0, 1, 1)
		self.assertEqual(s1, s2)

	def test__eq__not_equal_segments(self):
		s1 = Segment(0, 0, 1, 1)
		s2 = Segment(0, 0, 2, 2)
		self.assertNotEqual(s1, s2)

	def test__eq__None(self):
		s1 = Segment(0, 0, 1, 1)
		s2 = None
		self.assertNotEqual(s1, s2)

	# __str__

	def test__str(self):
		s1 = Segment(0, 0, 1, 1)
		self.assertEqual(str(s1), 'Segment [(0, 0);(1, 1)]')

	# gradient

	def test__gradient__normal_segment(self):
		s = Segment(0, 0, 1, 1)
		self.assertEqual(s.gradient(), 1)

	def test__gradient__vertical_segment(self):
		s = Segment(0, 0, 0, 1)
		with self.assertRaises(ZeroDivisionError) as cm:
			s.gradient()

	# yIntercept

	def test__yIntercept__normal_segment(self):
		s = Segment(1, 1, 2, 2)
		self.assertEqual(s.yIntercept(), 0)

	def test__yIntercept__vertical_segment(self):
		s = Segment(0, 0, 0, 1)
		with self.assertRaises(ZeroDivisionError) as cm:
			s.yIntercept()

	# yAtX

	def test__yAtX__in(self):
		s = Segment(0, 0, 1, 1)
		self.assertEqual(s.yAtX(0.5), 0.5)

	def test__yAtX__out(self):
		s = Segment(0, 0, 1, 1)
		self.assertEqual(s.yAtX(2), None)

	# orthogonalProjectionOf

	def test__orthogonalProjectionOf__normal_segment_in(self):
		s = Segment(0, 0, 1, 1)
		p = (0, 1)
		self.assertEqual(s.orthogonalProjectionOf(p), (0.5, 0.5))

	def test__orthogonalProjectionOf__normal_segment_out(self):
		s = Segment(0, 0, 1, 1)
		p = (0, 3)
		self.assertEqual(s.orthogonalProjectionOf(p), None)

	def test__orthogonalProjectionOf__vertical_segment_in(self):
		s = Segment(0, 0, 0, 1)
		p = (1, 0.5)
		self.assertEqual(s.orthogonalProjectionOf(p), (0, 0.5))

	def test__orthogonalProjectionOf__vertical_segment_out(self):
		s = Segment(0, 0, 0, 1)
		p = (1, 1.5)
		self.assertEqual(s.orthogonalProjectionOf(p), None)

	# isVertical

	def test__isVertical__normal_segment(self):
		s = Segment(0, 0, 1, 1)
		self.assertFalse(s.isVertical())

	def test__isVertical__vertical_segment(self):
		s = Segment(0, 0, 0, 1)
		self.assertTrue(s.isVertical())

	# intersection_With	

	def test__intersectionWith__parallel_normal_different_lines(self):
		s1 = Segment(0, 0, 1, 1)
		s2 = Segment(0, 1, 1, 2)
		self.assertEqual(s1.intersectionWith(s2), None)

	def test__intersectionWith__parallel_vertical_different_lines(self):
		s1 = Segment(0, 0, 0, 1)
		s2 = Segment(1, 0, 1, 1)
		self.assertEqual(s1.intersectionWith(s2), None)

	def test__intersectionWith__parallel_normal_not_overlapping(self):
		s1 = Segment(0, 0, 1, 1)
		s2 = Segment(2, 2, 3, 3)
		self.assertEqual(s1.intersectionWith(s2), None)

	def test__intersectionWith__parallel_vertical_not_overlapping(self):
		s1 = Segment(0, 0, 0, 1)
		s2 = Segment(0, 2, 0, 3)
		self.assertEqual(s1.intersectionWith(s2), None)
 
	def test__intersectionWith__parallel_normal_overlapping_segment(self):
		s1 = Segment(0, 0, 2, 2)
		s2 = Segment(1, 1, 3, 3)
		self.assertEqual(s1.intersectionWith(s2), Segment(1, 1, 2, 2))

	def test__intersectionWith__parallel_vertical_overlapping_segment(self):
		s1 = Segment(0, 0, 0, 2)
		s2 = Segment(0, 1, 0, 3)
		self.assertEqual(s1.intersectionWith(s2), Segment(0, 1, 0, 2))

	def test__intersectionWith__parallel_normal_overlapping_point(self):
		s1 = Segment(0, 0, 1, 1)
		s2 = Segment(1, 1, 2, 2)
		self.assertEqual(s1.intersectionWith(s2), (1, 1))

	def test__intersectionWith__parallel_vertical_overlapping_point(self):
		s1 = Segment(0, 0, 0, 1)
		s2 = Segment(0, 1, 0, 2)
		self.assertEqual(s1.intersectionWith(s2), (0, 1))

	def test__intersectionWith__not_parallel_one_vertical_in(self):
		s1 = Segment(1, 0, 1, 2)
		s2 = Segment(0, 0, 2, 2)
		self.assertEqual(s1.intersectionWith(s2), (1, 1))

	def test__intersectionWith__not_parallel_one_vertical_out(self):
		s1 = Segment(1, 0, 1, 2)
		s2 = Segment(2, 2, 4, 4)
		self.assertEqual(s1.intersectionWith(s2), None)

	def test__intersectionWith__not_parallel_one_vertical_endpoint(self):
		s1 = Segment(0, 0, 0, 2)
		s2 = Segment(0, 1, 2, 2)
		self.assertEqual(s1.intersectionWith(s2), (0, 1))

	def test__intersectionWith_not_parallel_not_vertical_in(self):
		s1 = Segment(0, 0, 2, 2)
		s2 = Segment(0, 1, 1, 0)
		self.assertEqual(s1.intersectionWith(s2), (0.5, 0.5))

	def test__intersectionWith_not_parallel_not_vertical_out(self):
		s1 = Segment(1, 1, 2, 2)
		s2 = Segment(0, 1, 1, 0)
		self.assertEqual(s1.intersectionWith(s2), None)

	def test__intersectionWith_not_parallel_not_vertical_endpoint(self):
		s1 = Segment(0, 2, 2, 0)
		s2 = Segment(0, 0, 1, 1)
		self.assertEqual(s1.intersectionWith(s2), (1, 1))


if __name__ == '__main__':
	unittest.main()