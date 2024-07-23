from unittest import TestCase

import numpy as np

from tomni.annotation_manager.annotations.point import Point

from .main import parse_points_to_contour


class TestUtils(TestCase):
    def setUp(self) -> None:
        self.epsilon = 0.9
        self.n_iter = 1
        self.circular_points = [
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
        self.star_shaped_points = [
            Point(1, 3),
            Point(2, 3),
            Point(3, 5),
            Point(5, 3),
            Point(3, 1),
            Point(2, 2),
        ]
        self.rectangle_points = [
            Point(1, 5),
            Point(3, 5),
            Point(5, 5),
            Point(5, 1),
            Point(3, 1),
            Point(1, 1),
        ]
        self.triangle_points = [
            Point(1, 5),
            Point(3, 1),
            Point(5, 5),
        ]

    def tearDown(self):
        pass

    def test_parse_points_to_contour_star(self):
        expected = np.array(
            [[[1, 3]], [[2, 3]], [[3, 5]], [[5, 3]], [[3, 1]], [[2, 2]]], dtype=np.int32
        )

        actual = parse_points_to_contour(self.star_shaped_points)

        np.testing.assert_array_equal(expected, actual)
        self.assertEqual(expected.dtype, actual.dtype)
