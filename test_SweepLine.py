import unittest
from SweepLine import SweepLine
from ComparableSegment import ComparableSegment

class TestSweepLine(unittest.TestCase):

	# __init__

	def test__init__empty(self):
		line = SweepLine()
		self.assertTrue(line.isEmpty())

	# addSegment

	def test__addSegment__first(self):
		line = SweepLine()
		s1 = ComparableSegment(0, 0, 2, 2)
		line.addSegment(s1)
		self.assertEqual(line.aboveSegments(s1), [])
		self.assertEqual(line.belowSegments(s1), [])

	def test__addSegment__equal(self):
		line = SweepLine()
		s1 = ComparableSegment(0, 0, 2, 2)
		s2 = ComparableSegment(1, 1, 2, 2)
		line.addSegment(s1)
		line.addSegment(s2)
		self.assertEqual(line.aboveSegments(s1), [])
		self.assertEqual(line.belowSegments(s1), [])
		self.assertEqual(line.aboveSegments(s2), [])
		self.assertEqual(line.belowSegments(s2), [])

	def test__addSegment__above_different_y(self):
		line = SweepLine()
		s1 = ComparableSegment(0, 0, 2, 2)
		s2 = ComparableSegment(1, 2, 2, 2)
		line.addSegment(s1)
		line.addSegment(s2)
		self.assertEqual(line.aboveSegments(s2), [])
		self.assertEqual(line.belowSegments(s2), [s1])
		self.assertEqual(line.aboveSegments(s1), [s2])
		self.assertEqual(line.belowSegments(s1), [])

	def test__addSegment__above_same_y_different_gradient(self):
		line = SweepLine()
		s1 = ComparableSegment(0, 0, 2, 2)
		s2 = ComparableSegment(1, 1, 2, 3)
		line.addSegment(s1)
		line.addSegment(s2)
		self.assertEqual(line.aboveSegments(s2), [])
		self.assertEqual(line.belowSegments(s2), [s1])
		self.assertEqual(line.aboveSegments(s1), [s2])
		self.assertEqual(line.belowSegments(s1), [])

	def test__addSegment__below_different_y(self):
		line = SweepLine()
		s1 = ComparableSegment(0, 0, 2, 2)
		s2 = ComparableSegment(1, 0, 2, 2)
		line.addSegment(s1)
		line.addSegment(s2)
		self.assertEqual(line.aboveSegments(s1), [])
		self.assertEqual(line.belowSegments(s1), [s2])
		self.assertEqual(line.aboveSegments(s2), [s1])
		self.assertEqual(line.belowSegments(s2), [])

	def test__addSegment__below_same_y_different_gradient(self):
		line = SweepLine()
		s1 = ComparableSegment(0, 0, 2, 2)
		s2 = ComparableSegment(1, 1, 2, 1)
		line.addSegment(s1)
		line.addSegment(s2)
		self.assertEqual(line.aboveSegments(s1), [])
		self.assertEqual(line.belowSegments(s1), [s2])
		self.assertEqual(line.aboveSegments(s2), [s1])
		self.assertEqual(line.belowSegments(s2), [])

	# remove

	def test__remove__single(self):
		line = SweepLine()
		s1 = ComparableSegment(0, 0, 2, 2)
		line.addSegment(s1)
		line.removeSegment(s1)
		self.assertTrue(line.isEmpty)

	def test__remove__multiple_not_equals(self):
		line = SweepLine()
		s1 = ComparableSegment(1, 2, 2, 2)
		s2 = ComparableSegment(0, 0, 2, 2)
		s3 = ComparableSegment(1, 0, 2, 2)
		line.addSegment(s2)
		line.addSegment(s1)
		line.addSegment(s3)
		self.assertEqual(line.aboveSegments(s1), [])
		self.assertEqual(line.belowSegments(s1), [s2])
		self.assertEqual(line.aboveSegments(s2), [s1])
		self.assertEqual(line.belowSegments(s2), [s3])
		self.assertEqual(line.aboveSegments(s3), [s2])
		self.assertEqual(line.belowSegments(s3), [])
		line.removeSegment(s2)
		self.assertEqual(line.aboveSegments(s1), [])
		self.assertEqual(line.belowSegments(s1), [s3])
		self.assertEqual(line.aboveSegments(s3), [s1])
		self.assertEqual(line.belowSegments(s3), [])

	def test__remove__multiple_equals(self):
		line = SweepLine()
		s1 = ComparableSegment(0, 0, 3, 3)
		s2 = ComparableSegment(0, 0, 2, 2)
		s3 = ComparableSegment(1, 1, 3, 3)
		line.addSegment(s1)
		line.addSegment(s2)
		line.addSegment(s3)
		self.assertEqual(len(line.l), 3)
		self.assertTrue(s1 in line.l)
		self.assertTrue(s2 in line.l)
		self.assertTrue(s3 in line.l)
		line.removeSegment(s2)
		self.assertEqual(len(line.l), 2)
		self.assertTrue(s1 in line.l)
		self.assertFalse(s2 in line.l)
		self.assertTrue(s3 in line.l)
		
	# sameLevelAs
	def test__sameLevelAs__one_on_one(self):
		line = SweepLine()
		s1 = ComparableSegment(0, 0, 2, 2)
		line.addSegment(s1)
		self.assertEqual(line.sameLevelAs(s1), [s1])

	# sameLevelAs
	def test__sameLevelAs__one_on_several(self):
		line = SweepLine()
		s1 = ComparableSegment(0, 0, 1, 1)
		s2 = ComparableSegment(0, 0, 1, 2)
		s3 = ComparableSegment(0, 0, 1, 3)
		line.addSegment(s1)
		line.addSegment(s2)
		line.addSegment(s3)
		self.assertEqual(line.sameLevelAs(s2), [s2])

	# sameLevelAs
	def test__sameLevelAs__all_on_several(self):
		line = SweepLine()
		s1 = ComparableSegment(0, 0, 1, 1)
		s2 = ComparableSegment(0, 0, 2, 2)
		s3 = ComparableSegment(0, 0, 3, 3)
		line.addSegment(s1)
		line.addSegment(s2)
		line.addSegment(s3)
		res = line.sameLevelAs(s2)
		self.assertEqual(len(res), 3)
		self.assertTrue(s1 in res and s2 in res and s3 in res)

	# sameLevelAs
	def test__sameLevelAs__several_on_several(self):
		line = SweepLine()
		s1 = ComparableSegment(0, 0, 1, 1)
		s2 = ComparableSegment(0, 0, 2, 2)
		s3 = ComparableSegment(0, 0, 3, 3)
		s4 = ComparableSegment(0, 0, 3, 2)
		s5 = ComparableSegment(0, 0, 2, 3)
		line.addSegment(s4)
		line.addSegment(s1)
		line.addSegment(s2)
		line.addSegment(s3)
		line.addSegment(s5)
		res = line.sameLevelAs(s2)
		self.assertEqual(len(res), 3)
		self.assertTrue(s1 in res and s2 in res and s3 in res)

	# betweenY

	def test__betweenY__empty(self):
		line = SweepLine()
		self.assertEqual(line.betweenY(0, 1, 0), [])

	def test__betweenY__all_in(self):
		line = SweepLine()
		s1 = ComparableSegment(0, 0, 2, 2)
		s2 = ComparableSegment(0, 1, 2, 3)
		s3 = ComparableSegment(0, 2, 2, 4)
		line.addSegment(s1)
		line.addSegment(s2)
		line.addSegment(s3)
		self.assertEqual(line.betweenY(1, 3, 1), [s1, s2, s3])
			
	def test_betweenY__few_in(self):
		line = SweepLine()
		s1 = ComparableSegment(0, 0, 1, 0)
		s2 = ComparableSegment(0, 1, 1, 1)
		s3 = ComparableSegment(0, 2, 1, 2)
		s4 = ComparableSegment(0, 3, 1, 3)
		s5 = ComparableSegment(0, 4, 1, 4)
		line.addSegment(s1)
		line.addSegment(s2)
		line.addSegment(s3)
		line.addSegment(s4)
		line.addSegment(s5)
		self.assertEqual(line.betweenY(1, 3, 0), [s2, s3, s4])

	def test_betweenY__none_in(self):
		line = SweepLine()
		s1 = ComparableSegment(0, 0, 1, 0)
		s2 = ComparableSegment(0, 1, 1, 1)
		s3 = ComparableSegment(0, 2, 1, 2)
		line.addSegment(s1)
		line.addSegment(s2)
		line.addSegment(s3)
		self.assertEqual(line.betweenY(1.5, 1.75, 0), [])

	# revertOrder

	def test__revertOrder_nothing_in_between(self):
		line = SweepLine()
		s1 = ComparableSegment(0, 0, 1, 1)
		s2 = ComparableSegment(0, 1, 1, 0)
		line.addSegment(s1)
		line.addSegment(s2)
		self.assertEqual(line.aboveSegments(s2), [])
		self.assertEqual(line.belowSegments(s2), [s1])
		self.assertEqual(line.aboveSegments(s1), [s2])
		self.assertEqual(line.belowSegments(s1), [])
		line.revertOrder(0.5, [s1, s2])
		self.assertEqual(line.aboveSegments(s1), [])
		self.assertEqual(line.belowSegments(s1), [s2])
		self.assertEqual(line.aboveSegments(s2), [s1])
		self.assertEqual(line.belowSegments(s2), [])

	def test__revertOrder__2_segments(self):
		line = SweepLine()
		s1 = ComparableSegment(0, 0, 1, 1)
		s2 = ComparableSegment(0, 1, 1, 0)
		line.addSegment(s1)
		line.addSegment(s2)
		self.assertEqual(line.aboveSegments(s2), [])
		self.assertEqual(line.belowSegments(s2), [s1])
		self.assertEqual(line.aboveSegments(s1), [s2])
		self.assertEqual(line.belowSegments(s1), [])
		line.revertOrder(0.5, [s1, s2])
		self.assertEqual(line.aboveSegments(s1), [])
		self.assertEqual(line.belowSegments(s1), [s2])
		self.assertEqual(line.aboveSegments(s2), [s1])
		self.assertEqual(line.belowSegments(s2), [])

	def test__revertOrder__3_segments(self):
		line = SweepLine()
		s1 = ComparableSegment(0, 0, 1, 1)
		s2 = ComparableSegment(0, 0.5, 1, 0.5)
		s3 = ComparableSegment(0, 1, 1, 0)
		line.addSegment(s1)
		line.addSegment(s2)
		line.addSegment(s3)
		self.assertEqual(line.aboveSegments(s3), [])
		self.assertEqual(line.belowSegments(s3), [s2])
		self.assertEqual(line.aboveSegments(s2), [s3])
		self.assertEqual(line.belowSegments(s2), [s1])
		self.assertEqual(line.aboveSegments(s1), [s2])
		self.assertEqual(line.belowSegments(s1), [])
		line.revertOrder(0.5, [s1, s2, s3])
		self.assertEqual(line.aboveSegments(s1), [])
		self.assertEqual(line.belowSegments(s1), [s2])
		self.assertEqual(line.aboveSegments(s2), [s1])
		self.assertEqual(line.belowSegments(s2), [s3])
		self.assertEqual(line.aboveSegments(s3), [s2])
		self.assertEqual(line.belowSegments(s3), [])

	def test__revertOrder__4_segments(self):
		line = SweepLine()
		s1 = ComparableSegment(0, 0, 1, 1)
		s2 = ComparableSegment(0, 0.25, 1, 0.75)
		s3 = ComparableSegment(0, 0.75, 1, 0.25)
		s4 = ComparableSegment(0, 1, 1, 0)
		line.addSegment(s1)
		line.addSegment(s2)
		line.addSegment(s3)
		line.addSegment(s4)
		self.assertEqual(line.aboveSegments(s4), [])
		self.assertEqual(line.belowSegments(s4), [s3])
		self.assertEqual(line.aboveSegments(s3), [s4])
		self.assertEqual(line.belowSegments(s3), [s2])
		self.assertEqual(line.aboveSegments(s2), [s3])
		self.assertEqual(line.belowSegments(s2), [s1])
		self.assertEqual(line.aboveSegments(s1), [s2])
		self.assertEqual(line.belowSegments(s1), [])
		line.revertOrder(0.5, [s1, s2, s3, s4])
		self.assertEqual(line.aboveSegments(s1), [])
		self.assertEqual(line.belowSegments(s1), [s2])
		self.assertEqual(line.aboveSegments(s2), [s1])
		self.assertEqual(line.belowSegments(s2), [s3])
		self.assertEqual(line.aboveSegments(s3), [s2])
		self.assertEqual(line.belowSegments(s3), [s4])
		self.assertEqual(line.aboveSegments(s4), [s3])
		self.assertEqual(line.belowSegments(s4), [])


if __name__ == '__main__':
	unittest.main()