from unittest import TestCase

from tomni.cytosmart_data_format import Point, Polygon


class TestPolygonSimplify(TestCase):
    def test_positive_squares_extra_points(self):
        poly = Polygon(
            [
                Point(1, 1),
                Point(1, 30),
                Point(15, 30),
                Point(30, 30),
                Point(30, 14),
                Point(30, 1),
            ],
            id=2,
            label="square",
        )
        expected = [Point(1, 1), Point(1, 30), Point(30, 30), Point(30, 1)]
        result = poly.points

        self.assertListEqual(expected, result)

    def test_remove_first_and_last(self):
        poly = Polygon(
            [
                Point(10, 1),
                Point(1, 1),
                Point(1, 30),
                Point(15, 30),
                Point(30, 30),
                Point(30, 14),
                Point(30, 1),
                Point(20, 1),
            ],
            id=2,
            label="square",
        )
        expected = [Point(1, 1), Point(1, 30), Point(30, 30), Point(30, 1)]
        result = poly.points

        self.assertListEqual(expected, result)

    def test_very_small_5_points(self):
        poly = Polygon(
            [
                Point(1, 1),
                Point(1, 30),
                Point(15, 30.000001),
                Point(30, 30),
                Point(30, 1),
            ],
            id=2,
            label="square",
        )
        expected = [
            Point(1, 1),
            Point(1, 30),
            Point(15, 30.000001),
            Point(30, 30),
            Point(30, 1),
        ]
        result = poly.points

        self.assertListEqual(expected, result)

    def test_triangle(self):
        poly = Polygon(
            [
                Point(1, 5),
                Point(3, 1),
                Point(5, 5),
            ],
            id=2,
            label="square",
        )
        expected = [
            Point(1, 5),
            Point(3, 1),
            Point(5, 5),
        ]
        result = poly.points

        self.assertListEqual(expected, result)

    def test_triangle_2(self):
        poly = Polygon(
            [
                Point(1, 5),
                Point(2, 3),
                Point(3, 1),
                Point(5, 5),
            ],
            id=2,
            label="square",
        )
        expected = [
            Point(1, 5),
            Point(3, 1),
            Point(5, 5),
        ]
        result = poly.points

        self.assertListEqual(expected, result)

    def test_triangle_3(self):
        poly = Polygon(
            [
                Point(1, 5),
                Point(2, 3.000001),
                Point(3, 1),
                Point(5, 5),
            ],
            id=2,
            label="square",
        )
        expected = [
            Point(1, 5),
            Point(2, 3.000001),
            Point(3, 1),
            Point(5, 5),
        ]
        result = poly.points

        self.assertListEqual(expected, result)
