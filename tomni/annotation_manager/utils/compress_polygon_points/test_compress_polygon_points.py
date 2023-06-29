from unittest import TestCase

import numpy as np

from tomni.annotation_manager.annotations.point.main import Point

from .main import compress_polygon_points


class TestCompressPolygonPoints(TestCase):
    def setUp(self) -> None:
        self.epsilon = 3
        self.circular_points = [Point(1, 2), Point(1, 4), Point(2, 5), Point(4, 5), Point(5, 4), Point(5, 2), Point(4, 1), Point(3, 1), Point(2, 1)]
        self.star_shaped_points = [Point(1, 3), Point(2, 3), Point(3, 5), Point(5, 3), Point(3, 1), Point(2, 2)]
        self.rectangle_points = [Point(1, 5), Point(3, 5), Point(5, 5), Point(5, 1), Point(3, 1), Point(1, 1)]
        self.triangle_points = [Point(1, 5), Point(3, 1), Point(5, 5)]

    def test_rdp_compression_circular(self):
        expected = [Point(x=1, y=2), Point(x=5, y=4), Point(x=2, y=1)]
        actual = compress_polygon_points(self.circular_points, self.epsilon)

        self.assertEqual(expected, actual)

    def test_compress_polygon_star(self):
        expected = [Point(x=1, y=3), Point(x=5, y=3), Point(x=2, y=2)]
        actual = compress_polygon_points(self.star_shaped_points, self.epsilon)

        self.assertEqual(expected, actual)

    def test_rdp_compression_triangle(self):
        expected = [Point(x=1, y=5), Point(x=3, y=1), Point(x=5, y=5)]

        actual = compress_polygon_points(self.triangle_points, self.epsilon)

        self.assertEqual(expected, actual)

    def test_rdp_compression_rectangle(self):
        expected = [Point(x=1, y=5), Point(x=5, y=1), Point(x=1, y=1)]

        actual = compress_polygon_points(self.rectangle_points, self.epsilon)

        self.assertEqual(expected, actual)

    def test_recursive_compression_triangle(self):
        expected = [Point(x=1, y=5), Point(x=3, y=1), Point(x=5, y=5)]

        actual = compress_polygon_points(self.triangle_points, self.epsilon)

        self.assertEqual(expected, actual)

    def test_recursive_compression_rectangle(self):
        expected = [Point(x=1, y=5), Point(x=5, y=1), Point(x=1, y=1)]

        actual = compress_polygon_points(self.rectangle_points, self.epsilon)

        self.assertEqual(expected, actual)

    def test_recursive_compression_star(self):
        expected = [Point(x=1, y=3), Point(x=5, y=3), Point(x=2, y=2)]

        actual = compress_polygon_points(self.star_shaped_points, self.epsilon)

        self.assertEqual(expected, actual)

    def test_recursive_compression_circular(self):
        expected = [Point(x=1, y=2), Point(x=5, y=4), Point(x=2, y=1)]

        actual = compress_polygon_points(self.circular_points, self.epsilon)

        self.assertEqual(expected, actual)
