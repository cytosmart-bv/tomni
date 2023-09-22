from unittest import TestCase

from tomni.annotation_manager.annotations.point import Point


class TestPointCompare(TestCase):
    def test_positive(self):
        point1 = Point(1, 2)
        point2 = Point(1, 2)

        self.assertTrue(point1 == point2)

    def test_positive_decimal(self):
        point1 = Point(1, 2)
        point2 = Point(1.0, 2.0)

        self.assertTrue(point1 == point2)

    def test_negative(self):
        point1 = Point(1, 2)
        point2 = Point(2, 1)

        self.assertFalse(point1 == point2)
