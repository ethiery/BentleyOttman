import unittest

from Segment import Segment
from math import sqrt

class TestSegment(unittest.TestCase):

	def test__init__invalid(self):
		with self.assertRaises(ValueError) as cm:
			s = Segment(0, 0, 0, 0)
		self.assertTrue('Invalid coordinates (segment is a point)' 
						in cm.exception.args)

	def test__init__vertical_ordered(self):
		s = Segment(0, 0, 0, 1)
		self.assertEqual((s.x1, s.y1, s.x2, s.y2), (0, 0, 0, 1))

	def test__init__vertical_non_ordered(self):
		s = Segment(0, 1, 0, 0)
		self.assertEqual((s.x1, s.y1, s.x2, s.y2), (0, 0, 0, 1))

	def test__init__not_vertical_ordered(self):
		s = Segment(0, 0, 1, 1)
		self.assertEqual((s.x1, s.y1, s.x2, s.y2), (0, 0, 1, 1))

	def test__init__not_vertical_non_ordered(self):
		s = Segment(1, 1, 0, 0)
		self.assertEqual((s.x1, s.y1, s.x2, s.y2), (0, 0, 1, 1))

	def test__eq(self):
		s1 = Segment(0, 1, 2, 3)
		s2 = Segment(0, 1, 2, 3)
		self.assertEqual(s1, s2)

	def test__ne(self):
		s1 = Segment(0, 1, 2, 3)
		s2 = Segment(3, 2, 1, 0)
		self.assertNotEqual(s1, s2)

	def test__cmp__lower1_true(self):
		s1 = Segment(0, 0, 2, 2)
		s2 = Segment(1, 0, 2, 3)
		self.assertTrue(s2 < s1)

	def test__cmp__lower1_false(self):
		s1 = Segment(0, 0, 2, 2)
		s2 = Segment(1, 2, 2, 3)
		self.assertFalse(s2 < s1)

	def test__cmp__lower2_true(self):
		s1 = Segment(0, 0, 2, 2)
		s2 = Segment(0, -1, 2, 3)
		self.assertTrue(s2 < s1)

	def test__cmp__lower2_false(self):
		s1 = Segment(0, 0, 2, 2)
		s2 = Segment(0, 1, 2, 3)
		self.assertFalse(s2 < s1)

	def test__cmp__lower3_true(self):
		s1 = Segment(0, 0, 2, 2)
		s2 = Segment(1, 1, 3, 2)
		self.assertTrue(s2 < s1)

	def test__cmp__lower3_false(self):
		s1 = Segment(0, 0, 2, 2)
		s2 = Segment(1, 1, 2, 3)
		self.assertFalse(s2 < s1)

	def test__gradient__vertical(self):
		s = Segment(0, 0, 0, 1)
		with self.assertRaises(ZeroDivisionError) as cm:
			s.gradient

	def test__gradient__not_vertical(self):
		s = Segment(0, 0, 1, 1)
		self.assertEqual(s.gradient, 1)

	def test__yIntercept__vertical(self):
		s = Segment(0, 0, 0, 1)
		with self.assertRaises(ZeroDivisionError) as cm:
			s.yIntercept

	def test__yIntercept__not_vertical(self):
		s = Segment(1, 1, 2, 2)
		self.assertEqual(s.yIntercept, 0)

	def test__line_intersection__not_parallel_neither_vertical(self):
		s1 = Segment(0, 0, 1, 1)
		s2 = Segment(3, 1, 4, 0)
		self.assertEqual(s1.lineIntersectionWith(s2), (2,2))

	def test__line_intersection__not_parallel_first_vertical(self):
		s1 = Segment(1, 0, 1, 1)
		s2 = Segment(3, 1, 4, 0)
		self.assertEqual(s1.lineIntersectionWith(s2), (1,3))

	def test__line_intersection__not_parallel_second_vertical(self):
		s1 = Segment(0, 0, 1, 1)
		s2 = Segment(3, 0, 3, 1)
		self.assertEqual(s1.lineIntersectionWith(s2), (3,3))

	def test__line_intersection__parallel_not_mingled(self):
		s1 = Segment(0, 0, 0, 1)
		s2 = Segment(1, 0, 1, 1)
		self.assertEqual(s1.lineIntersectionWith(s2), None)

	def test__line_intersection__parallel_mingled_vertical(self):
		s1 = Segment(0, 0, 0, 2)
		s2 = Segment(0, 1, 0, 3)
		self.assertEqual(s1.lineIntersectionWith(s2), "line")

	def test__line_intersection__parallel_mingled_not_vertical(self):
		s1 = Segment(0, 0, 2, 2)
		s2 = Segment(1, 1, 3, 3)
		self.assertEqual(s1.lineIntersectionWith(s2), "line")

	def test__oldIntersection__empty(self):
		s1 = Segment(0, 0, 0, 1)
		s2 = Segment(1, 0, 1, 1)
		self.assertEqual(s1.oldIntersectionWith(s2), None)

	def test__oldIntersection__line_vertical_empty(self):
		s1 = Segment(0, 0, 0, 1)
		s2 = Segment(0, 2, 0, 3)
		self.assertEqual(s1.oldIntersectionWith(s2), None)

	def test__oldIntersection__line_vertical_single_point(self):
		s1 = Segment(0, 0, 0, 1)
		s2 = Segment(0, 1, 0, 2)
		self.assertEqual(s1.oldIntersectionWith(s2), (0,1))

	def test__oldIntersection__line_vertical_segment(self):
		s1 = Segment(0, 0, 0, 2)
		s2 = Segment(0, 1, 0, 3)
		self.assertEqual(s1.oldIntersectionWith(s2), Segment(0, 1, 0, 2))
 
	def test__oldIntersection__line_not_vertical_empty(self):
		s1 = Segment(0, 0, 1, 1)
		s2 = Segment(2, 2, 3, 3)
		self.assertEqual(s1.oldIntersectionWith(s2), None)

	def test__oldIntersection__line_vertical_single_point(self):
		s1 = Segment(0, 0, 1, 1)
		s2 = Segment(1, 1, 2, 2)
		self.assertEqual(s1.oldIntersectionWith(s2), (1,1))

	def test__oldIntersection__line_vertical_segment(self):
		s1 = Segment(0, 0, 2, 2)
		s2 = Segment(1, 1, 3, 3)
		self.assertEqual(s1.oldIntersectionWith(s2), Segment(1, 1, 2, 2))

	def test__oldIntersection__point_in(self):
		s1 = Segment(0, 0, 4, 4)
		s2 = Segment(0, 4, 4, 0)
		self.assertEqual(s1.oldIntersectionWith(s2), (2,2))

	def test__oldIntersection__point_out(self):
		s1 = Segment(0, 0, 1, 1)
		s2 = Segment(3, 1, 4, 0)
		self.assertEqual(s1.oldIntersectionWith(s2), None)

	def test__orthogonalProjection__vertical_in(self):
		s = Segment(0, 0, 0, 1)
		p = (1, 0.5)
		self.assertEqual(s.orthogonalProjectOf(p), (0, 0.5))

	def test__orthogonalProjection__vertical_out(self):
		s = Segment(0, 0, 0, 1)
		p = (1, 1.5)
		self.assertEqual(s.orthogonalProjectOf(p), None)

	def test__orthogonalProjection__not_vertical_in(self):
		s = Segment(0, 0, 1, 1)
		p = (0, 1)
		self.assertEqual(s.orthogonalProjectOf(p), (0.5, 0.5))

	def test__orthogonalProjection__not_vertical_out(self):
		s = Segment(0, 0, 1, 1)
		p = (0, 3)
		self.assertEqual(s.orthogonalProjectOf(p), None)

	def test__yAtX__in(self):
		s = Segment(0, 0, 1, 1)
		self.assertEqual(s.yAtX(0.5), 0.5)

	def test__yAtX__out(self):
		s = Segment(0, 0, 1, 1)
		self.assertEqual(s.yAtX(2), None)

	def test__intersection__empty(self):
		s1 = Segment(0, 0, 0, 1)
		s2 = Segment(1, 0, 1, 1)
		self.assertEqual(s1.intersectionWith(s2), None)

	def test__intersection__line_vertical_empty(self):
		s1 = Segment(0, 0, 0, 1)
		s2 = Segment(0, 2, 0, 3)
		self.assertEqual(s1.intersectionWith(s2), None)

	def test__intersection__line_vertical_single_point(self):
		s1 = Segment(0, 0, 0, 1)
		s2 = Segment(0, 1, 0, 2)
		self.assertEqual(s1.intersectionWith(s2), (0,1))

	def test__intersection__line_vertical_segment(self):
		s1 = Segment(0, 0, 0, 2)
		s2 = Segment(0, 1, 0, 3)
		self.assertEqual(s1.intersectionWith(s2), Segment(0, 1, 0, 2))
 
	def test__intersection__line_not_vertical_empty(self):
		s1 = Segment(0, 0, 1, 1)
		s2 = Segment(2, 2, 3, 3)
		self.assertEqual(s1.intersectionWith(s2), None)

	def test__intersection__line_vertical_single_point(self):
		s1 = Segment(0, 0, 1, 1)
		s2 = Segment(1, 1, 2, 2)
		self.assertEqual(s1.intersectionWith(s2), (1,1))

	def test__intersection__line_vertical_segment(self):
		s1 = Segment(0, 0, 2, 2)
		s2 = Segment(1, 1, 3, 3)
		self.assertEqual(s1.intersectionWith(s2), Segment(1, 1, 2, 2))

	def test__intersection__point_in(self):
		s1 = Segment(0, 0, 4, 4)
		s2 = Segment(0, 4, 4, 0)
		self.assertEqual(s1.intersectionWith(s2), (2,2))

	def test__intersection__point_out(self):
		s1 = Segment(0, 0, 1, 1)
		s2 = Segment(3, 1, 4, 0)
		self.assertEqual(s1.intersectionWith(s2), None)


from Circle import Circle

class TestCircle(unittest.TestCase):

	def test__init__valid_radius(self):
		c = Circle(0, 0, 1)
		self.assertEqual((c.xc, c.yc, c.r), (0, 0, 1))

	def test__init__invalid_radius(self):
		with self.assertRaises(ValueError) as cm:
			c = Circle(0, 0, -1)
		self.assertTrue('Invalid radius value (negative)' in cm.exception.args)

	def test__eq(self):
		c1 = Circle(0, 0, 1)
		c2 = Circle(0, 0, 1)
		self.assertEqual(c1, c2)

	def test__ne(self):
		c1 = Circle(0, 0, 1)
		c2 = Circle(0, 0, 2)
		self.assertNotEqual(c1, c2)

	def test__cmp__lower1(self):
		c1 = Circle(0, 0, 1)
		c2 = Circle(1, 1, 1)
		self.assertTrue(c1 < c2)

	def test__cmp__lower2(self):
		c1 = Circle(0, 0, 1)
		c2 = Circle(0, 1, 1)
		self.assertTrue(c1 < c2)

	def test__intersectionWithLine__vertical_empty(self):
		c1 = Circle(0, 0, 1)
		s1 = Segment(2, 0, 2, 1)
		self.assertEqual(c1.intersectionWithLine(s1), None)

	def test__intersectionWithLine__vertical_single_point(self):
		c1 = Circle(0, 0, 1)
		s1 = Segment(1, -1, 1, 1)
		self.assertEqual(c1.intersectionWithLine(s1), (1, 0))

	def test__intersectionWithLine__vertical_two_points(self):
		c1 = Circle(0, 0, 1)
		s1 = Segment(0, -2, 0, 2)
		self.assertEqual(c1.intersectionWithLine(s1), (0, -1, 0, 1))

	def test__intersectionWithLine_not_vertical_empty(self):
		c1 = Circle(0, 0, 1)
		s1 = Segment(2, 0, 3, 1)
		self.assertEqual(c1.intersectionWithLine(s1), None)

	def test__intersectionWithLine__not_vertical_single_point(self):
		c1 = Circle(0, 0, 1)
		s1 = Segment(0, sqrt(2), sqrt(2), 0)
		inter = c1.intersectionWithLine(s1)
		dx = abs(inter[0] - 1/sqrt(2))
		dy = abs(inter[1] - 1/sqrt(2))
		EPS = 0.001
		self.assertTrue(dx < EPS and dy < EPS) 

	def test__intersectionWithLine__not_vertical_two_points(self):
		c1 = Circle(0, 0, 1)
		s1 = Segment(-2, -1, 1, 2)
		self.assertEqual(c1.intersectionWithLine(s1), (-1, 0, 0, 1))


	def test__oldIntersectionWithSegment__empty(self):
		c1 = Circle(0, 0, 1)
		s1 = Segment(2, 0, 2, 1)
		self.assertEqual(c1.oldIntersectionWithSegment(s1), None)

	def test__oldIntersectionWithSegment__not_vertical_2_points_out(self):
		c1 = Circle(0, 0, 1)
		s1 = Segment(2, 0, 3, 0)
		self.assertEqual(c1.oldIntersectionWithSegment(s1), None)

	def test__oldIntersectionWithSegment__not_vertical_2_points_in(self):
		c1 = Circle(0, 0, 1)
		s1 = Segment(-2, 0, 2, 0)
		self.assertEqual(c1.oldIntersectionWithSegment(s1), (-1, 0, 1, 0))

	def test__oldIntersectionWithSegment__not_vertical_2_points_in_out(self):
		c1 = Circle(0, 0, 1)
		s1 = Segment(0, 0, 2, 0)
		self.assertEqual(c1.oldIntersectionWithSegment(s1), (1, 0))

	def test__oldIntersectionWithSegment__not_vertical_2_points_out_in(self):
		c1 = Circle(0, 0, 1)
		s1 = Segment(-2, 0, 0, 0)
		self.assertEqual(c1.oldIntersectionWithSegment(s1), (-1, 0))

	def test__oldIntersectionWithSegment__vertical_2_points_out(self):
		c1 = Circle(0, 0, 1)
		s1 = Segment(2, 0, 3, 0)
		self.assertEqual(c1.oldIntersectionWithSegment(s1), None)

	def test__oldIntersectionWithSegment__vertical_2_points_in(self):
		c1 = Circle(0, 0, 1)
		s1 = Segment(0, -2, 0, 2)
		self.assertEqual(c1.oldIntersectionWithSegment(s1), (0, -1, 0, 1))

	def test__oldIntersectionWithSegment__vertical_2_points_in_out(self):
		c1 = Circle(0, 0, 1)
		s1 = Segment(0, 0, 0, 2)
		self.assertEqual(c1.oldIntersectionWithSegment(s1), (0, 1))

	def test__oldIntersectionWithSegment__vertical_2_points_out_in(self):
		c1 = Circle(0, 0, 1)
		s1 = Segment(0, -2, 0, 0)
		self.assertEqual(c1.oldIntersectionWithSegment(s1), (0, -1))


	def test__intersectionWithSegment__empty(self):
		c1 = Circle(0, 0, 1)
		s1 = Segment(2, 0, 2, 1)
		self.assertEqual(c1.intersectionWithSegment(s1), [])

	def test__intersectionWithSegment__not_vertical_2_points_out(self):
		c1 = Circle(0, 0, 1)
		s1 = Segment(2, 0, 3, 0)
		self.assertEqual(c1.intersectionWithSegment(s1), [])

	def test__intersectionWithSegment__not_vertical_2_points_in(self):
		c1 = Circle(0, 0, 1)
		s1 = Segment(-2, 0, 2, 0)
		self.assertEqual(c1.intersectionWithSegment(s1), [(-1, 0), (1, 0)])

	def test__intersectionWithSegment__not_vertical_2_points_in_out(self):
		c1 = Circle(0, 0, 1)
		s1 = Segment(0, 0, 2, 0)
		self.assertEqual(c1.intersectionWithSegment(s1), [(1, 0)])

	def test__intersectionWithSegment__not_vertical_2_points_out_in(self):
		c1 = Circle(0, 0, 1)
		s1 = Segment(-2, 0, 0, 0)
		self.assertEqual(c1.intersectionWithSegment(s1), [(-1, 0)])

	def test__intersectionWithSegment__vertical_2_points_out(self):
		c1 = Circle(0, 0, 1)
		s1 = Segment(2, 0, 3, 0)
		self.assertEqual(c1.intersectionWithSegment(s1), [])

	def test__intersectionWithSegment__vertical_2_points_in(self):
		c1 = Circle(0, 0, 1)
		s1 = Segment(0, -2, 0, 2)
		self.assertEqual(c1.intersectionWithSegment(s1), [(0, -1), (0, 1)])

	def test__intersectionWithSegment__vertical_2_points_in_out(self):
		c1 = Circle(0, 0, 1)
		s1 = Segment(0, 0, 0, 2)
		self.assertEqual(c1.intersectionWithSegment(s1), [(0, 1)])

	def test__intersectionWithSegment__vertical_2_points_out_in(self):
		c1 = Circle(0, 0, 1)
		s1 = Segment(0, -2, 0, 0)
		self.assertEqual(c1.intersectionWithSegment(s1), [(0, -1)])

from BentleyOttmann import Event

class TestEvent(unittest.TestCase):

	def test__init__valid_obj(self):
		e = Event(0, 1)
		self.assertEqual((0, 1, [], [], []), 
						 (e.x, e.y, e.left, e.right, e.inter))

	def test__eq(self):
		e1 = Event(0, 1)
		e2 = Event(0, 1)
		self.assertEqual(e1, e2)

	def test__ne(self):
		e1 = Event(0, 1)
		e2 = Event(0, 0)
		self.assertNotEqual(e1, e2)

	def test__cmp__lower1(self):
		e1 = Event(0, 0)
		e2 = Event(1, 1)
		self.assertTrue(e1 < e2)

	def test__cmp__lower2(self):
		s = Segment(0, 0, 0, 1)
		e1 = Event(0, 1)
		e2 = Event(0, 2)
		self.assertTrue(e1 < e2)


from BentleyOttmann import EventQueue

class TestEventQueue(unittest.TestCase):

	def test__init__empty(self):
		q = EventQueue([])
		self.assertTrue(q.isEmpty())

	def test__init__vertical(self):
		s1 = Segment(0, 1, 0, 2)
		q = EventQueue([s1])
		e1 = q.nextEvent()
		self.assertEqual((e1.x, e1.y, e1.low, e1.high),
						 (0, 1, [s1], []))
		e2 = q.nextEvent()
		self.assertEqual((e2.x, e2.y, e2.low, e2.high),
						 (0, 2, [], [s1]))


	def test__init__ordered(self):
		s1 = Segment(0, 0, 1, 1)
		s2 = Segment(0, 0, 2, 2)
		s3 = Segment(1, 1, 3, 3)
		segments = [s1, s2, s3]
		q = EventQueue(segments)
		self.assertFalse(q.isEmpty())
		e1 = q.nextEvent()
		self.assertEqual((e1.x, e1.y, e1.left, e1.right),
						 (0, 0, [s1, s2], []))
		e2 = q.nextEvent()
		self.assertEqual((e2.x, e2.y, e2.left, e2.right),
						 (1, 1, [s3], [s1]))
		e3 = q.nextEvent()
		self.assertEqual((e3.x, e3.y, e3.left, e3.right),
						 (2, 2, [], [s2]))
		e4 = q.nextEvent()
		self.assertEqual((e4.x, e4.y, e4.left, e4.right),
						 (3, 3, [], [s3]))
		self.assertTrue(q.isEmpty())

	def test__init__not_ordered(self):
		s1 = Segment(0, 0, 1, 1)
		s2 = Segment(0, 0, 2, 2)
		s3 = Segment(1, 1, 3, 3)
		segments = [s3, s2, s1]
		q = EventQueue(segments)
		self.assertFalse(q.isEmpty())
		e1 = q.nextEvent()
		self.assertEqual((e1.x, e1.y, e1.left, e1.right, e1.inter),
						 (0, 0, [s2, s1], [], []))
		e2 = q.nextEvent()
		self.assertEqual((e2.x, e2.y, e2.left, e2.right, e2.inter),
						 (1, 1, [s3], [s1], []))
		e3 = q.nextEvent()
		self.assertEqual((e3.x, e3.y, e3.left, e3.right, e3.inter),
						 (2, 2, [], [s2], []))
		e4 = q.nextEvent()
		self.assertEqual((e4.x, e4.y, e4.left, e4.right, e4.inter),
						 (3, 3, [], [s3], []))
		self.assertTrue(q.isEmpty())

	def test__addInter_existing(self):
		s1 = Segment(1, 1, 2, 1)
		s2 = Segment(0, 0, 2, 2)
		s3 = Segment(0, 2, 2, 0)
		q = EventQueue([s1])
		q.addInter(1, 1, s2, s3)
		e = q.nextEvent()
		self.assertEqual((e.x, e.y, e.left, e.right, e.inter),
						 (1, 1, [s1], [], [s2, s3]))

	def test__addInter_non_existing(self):
		s2 = Segment(0, 0, 2, 2)
		s3 = Segment(0, 2, 2, 0)
		q = EventQueue([])
		q.addInter(1, 1, s2, s3)
		e = q.nextEvent()
		self.assertEqual((e.x, e.y, e.left, e.right, e.inter),
						 (1, 1, [], [], [s2, s3]))


from BentleyOttmann import SweepLine

class TestSweepLine(unittest.TestCase):

	def test__add__first(self):
		line = SweepLine()
		s1 = Segment(0, 0, 2, 2)
		line.add(s1)
		self.assertEqual(line.above(s1), None)
		self.assertEqual(line.below(s1), None)

	def test__add__below1(self):
		line = SweepLine()
		s1 = Segment(0, 0, 2, 2)
		s2 = Segment(1, 0, 2, 3)
		line.add(s1)
		line.add(s2)
		self.assertEqual(line.above(s1), None)
		self.assertEqual(line.below(s1), s2)
		self.assertEqual(line.above(s2), s1)
		self.assertEqual(line.below(s2), None)


	def test__add__above1(self):
		line = SweepLine()
		s1 = Segment(0, 0, 2, 2)
		s2 = Segment(1, 2, 2, 3)
		line.add(s1)
		line.add(s2)
		self.assertEqual(line.above(s2), None)
		self.assertEqual(line.below(s2), s1)
		self.assertEqual(line.above(s1), s2)
		self.assertEqual(line.below(s1), None)

	def test__add__below2(self):
		line = SweepLine()
		s1 = Segment(0, 0, 2, 2)
		s2 = Segment(1, 1, 3, 2)
		line.add(s1)
		line.add(s2)
		self.assertEqual(line.above(s1), None)
		self.assertEqual(line.below(s1), s2)
		self.assertEqual(line.above(s2), s1)
		self.assertEqual(line.below(s2), None)

	def test__add__above2(self):
		line = SweepLine()
		s1 = Segment(0, 0, 2, 2)
		s2 = Segment(1, 1, 2, 3)
		line.add(s1)
		line.add(s2)
		self.assertEqual(line.above(s2), None)
		self.assertEqual(line.below(s2), s1)
		self.assertEqual(line.above(s1), s2)
		self.assertEqual(line.below(s1), None)

	def test__remove(self):
		line = SweepLine()
		s1 = Segment(0, 0, 2, 2)
		line.add(s1)
		line.remove(s1)
		self.assertTrue(line.isEmpty)

	def test__swap(self):
		line = SweepLine()
		s1 = Segment(0, 0, 1, 1)
		s2 = Segment(0, 1, 1, 0)
		line.add(s1)
		line.add(s2)
		line.swap(0.5, 0.5, s1, s2)
		self.assertEqual(line.above(s1), None)
		self.assertEqual(line.below(s1), s2)
		self.assertEqual(line.above(s2), s1)
		self.assertEqual(line.below(s2), None)

from BentleyOttmann import intersection_list

class Test_intersection_list(unittest.TestCase):

	def test__1(self):
		s1 = Segment(0, 0, 1, 1)
		s2 = Segment(0, 1, 1, 0)
		s3 = Segment(0.5, 0, 0.5, 1)
		s4 = Segment(0, 0, 1, 0.5)
		intersections = intersection_list([s1,s2,s3, s4])







if __name__ == '__main__':
	unittest.main()