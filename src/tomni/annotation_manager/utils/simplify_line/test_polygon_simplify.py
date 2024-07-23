from unittest import TestCase

from tomni.annotation_manager.annotations.point import Point

from .main import simplify_line


class TestPolygonSimplify(TestCase):
    def test_positive_squares_extra_points(self):
        line = [
            Point(1, 1),
            Point(1, 30),
            Point(15, 30),
            Point(30, 30),
            Point(30, 14),
            Point(30, 1),
        ]
        expected = [Point(1, 1), Point(1, 30), Point(30, 30), Point(30, 1)]
        result = simplify_line(line)

        self.assertListEqual(expected, result)

    def test_remove_first_and_last(self):
        line = [
            Point(10, 1),
            Point(1, 1),
            Point(1, 30),
            Point(15, 30),
            Point(30, 30),
            Point(30, 14),
            Point(30, 1),
            Point(20, 1),
        ]
        expected = [Point(1, 1), Point(1, 30), Point(30, 30), Point(30, 1)]
        result = simplify_line(line)

        self.assertListEqual(expected, result)

    def test_very_small_5_points(self):
        line = [
            Point(1, 1),
            Point(1, 30),
            Point(15, 30.000001),
            Point(30, 30),
            Point(30, 1),
        ]
        expected = [
            Point(1, 1),
            Point(1, 30),
            Point(15, 30.000001),
            Point(30, 30),
            Point(30, 1),
        ]
        result = simplify_line(line)

        self.assertListEqual(expected, result)

    def test_triangle(self):
        line = [
            Point(1, 5),
            Point(3, 1),
            Point(5, 5),
        ]
        expected = [
            Point(1, 5),
            Point(3, 1),
            Point(5, 5),
        ]
        result = simplify_line(line)

        self.assertListEqual(expected, result)

    def test_triangle_2(self):
        line = [
            Point(1, 5),
            Point(2, 3),
            Point(3, 1),
            Point(5, 5),
        ]
        expected = [
            Point(1, 5),
            Point(3, 1),
            Point(5, 5),
        ]
        result = simplify_line(line)

        self.assertListEqual(expected, result)

    def test_triangle_3(self):
        line = [
            Point(1, 5),
            Point(2, 3.000001),
            Point(3, 1),
            Point(5, 5),
        ]
        expected = [
            Point(1, 5),
            Point(2, 3.000001),
            Point(3, 1),
            Point(5, 5),
        ]
        result = simplify_line(line)

        self.assertListEqual(expected, result)

    def test_two_points(self):
        line = [
            Point(1, 1),
            Point(5, 5),
        ]
        expected = [
            Point(1, 1),
            Point(5, 5),
        ]
        actual = simplify_line(line)

        self.assertListEqual(expected, actual)
