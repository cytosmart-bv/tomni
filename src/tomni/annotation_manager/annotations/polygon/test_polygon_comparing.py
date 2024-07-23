from unittest import TestCase

from tomni.annotation_manager.annotations.point import Point
from tomni.annotation_manager.annotations.polygon import Polygon


class TestPolygonCompare(TestCase):
    def test_positive_squares(self):
        poly1 = Polygon(
            [Point(1, 1), Point(1, 2), Point(1, 3), Point(2, 3), Point(2, 1)],
            id=1,
            label="square",
        )
        poly2 = Polygon(
            [Point(1, 1), Point(1, 2), Point(1, 3), Point(2, 3), Point(2, 1)],
            id=2,
            label="square",
        )

        self.assertTrue(poly1 == poly2)

    def test_flipped_squares(self):
        poly1 = Polygon(
            [Point(1, 1), Point(1, 2), Point(1, 3), Point(2, 3), Point(2, 1)],
            id=1,
            label="square",
        )
        poly2 = Polygon(
            [Point(2, 1), Point(2, 3), Point(1, 3), Point(1, 2), Point(1, 1)],
            id=2,
            label="flipped square",
        )

        self.assertTrue(poly1 == poly2)

    def test_rotated_squares(self):
        poly1 = Polygon(
            [Point(1, 1), Point(1, 2), Point(1, 3), Point(2, 3), Point(2, 1)],
            id=1,
            label="square",
        )
        poly2 = Polygon(
            [Point(2, 1), Point(1, 1), Point(1, 2), Point(1, 3), Point(2, 3)],
            id=2,
            label="rotated square",
        )

        self.assertTrue(poly1 == poly2)

    def test_rotated_and_flipped_squares(self):
        poly1 = Polygon(
            [Point(1, 1), Point(1, 2), Point(1, 3), Point(2, 3), Point(2, 1)],
            id=1,
            label="square",
        )
        poly2 = Polygon(
            [Point(2, 3), Point(1, 3), Point(1, 2), Point(1, 1), Point(2, 1)],
            id=2,
            label="flipped rotated square",
        )

        self.assertTrue(poly1 == poly2)

    def test_positive_squares_hourglass(self):
        poly1 = Polygon(
            [Point(1, 1), Point(1, 2), Point(1, 3), Point(2, 3), Point(2, 1)],
            id=1,
            label="square",
        )
        poly2 = Polygon(
            [Point(1, 1), Point(2, 3), Point(1, 3), Point(1, 2), Point(2, 1)],
            id=2,
            label="hourglass",
        )

        self.assertFalse(poly1 == poly2)

    def test_positive_wrong_type(self):
        poly1 = Polygon(
            [Point(1, 1), Point(1, 2), Point(1, 3), Point(2, 3), Point(2, 1)],
            id=1,
            label="square",
        )
        point2 = Point(1, 1)

        self.assertFalse(poly1 == point2)
