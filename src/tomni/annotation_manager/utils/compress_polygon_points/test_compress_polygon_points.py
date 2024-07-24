from unittest import TestCase

import numpy as np

from tomni.annotation_manager.annotations.point.main import Point

from .main import compress_polygon_points


class TestCompressPolygonPoints(TestCase):
    def setUp(self) -> None:
        self.points = [
            Point(1, 2),
            Point(1, 4),
            Point(2, 5),
            Point(4, 5),
            Point(5, 4),
            Point(5, 2),
            Point(4, 1),
            Point(3, 1),
            Point(2, 1),
        ]

    def test_compress_happy_flow(self):
        expected = [
            Point(x=1, y=2),
            Point(x=2, y=5),
            Point(x=5, y=4),
            Point(x=4, y=1),
            Point(x=2, y=1),
        ]
        actual = compress_polygon_points(self.points, 1)

        self.assertEqual(expected, actual)

    def test_compress_to_much_so_return_same(self):
        expected = [
            Point(1, 2),
            Point(1, 4),
            Point(2, 5),
            Point(4, 5),
            Point(5, 4),
            Point(5, 2),
            Point(4, 1),
            Point(3, 1),
            Point(2, 1),
        ]
        actual = compress_polygon_points(self.points, 3)

        self.assertEqual(expected, actual)
