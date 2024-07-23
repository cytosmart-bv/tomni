from unittest import TestCase

from .main import iterative_downsampling


class TestIterativeDownsampling(TestCase):
    def setUp(self) -> None:
        self.n_iter = 1
        self.circular_points = [
            {"x": 1, "y": 2},
            {"x": 1, "y": 4},
            {"x": 2, "y": 5},
            {"x": 4, "y": 5},
            {"x": 5, "y": 4},
            {"x": 5, "y": 2},
            {"x": 4, "y": 1},
            {"x": 3, "y": 1},
            {"x": 2, "y": 1},
        ]
        self.star_shaped_points = [
            {"x": 1, "y": 3},
            {"x": 2, "y": 3},
            {"x": 3, "y": 5},
            {"x": 5, "y": 3},
            {"x": 3, "y": 1},
            {"x": 2, "y": 2},
        ]
        self.rectangle_points = [
            {"x": 1, "y": 5},
            {"x": 3, "y": 5},
            {"x": 5, "y": 5},
            {"x": 5, "y": 1},
            {"x": 3, "y": 1},
            {"x": 1, "y": 1},
        ]
        self.triangle_points = [
            {"x": 1, "y": 5},
            {"x": 3, "y": 1},
            {"x": 5, "y": 5},
        ]

    def test_iterative_downsampling_rectangle(self):
        expected = [{"x": 1, "y": 5}, {"x": 5, "y": 5}, {"x": 3, "y": 1}]

        actual = iterative_downsampling(self.rectangle_points, self.n_iter)

        self.assertEqual(expected, actual)

    def test_iterative_downsampling_star(self):
        expected = [{"x": 1, "y": 3}, {"x": 3, "y": 5}, {"x": 3, "y": 1}]

        actual = iterative_downsampling(self.star_shaped_points, self.n_iter)

        self.assertEqual(expected, actual)

    def test_iterative_downsampling_circular(self):
        expected = [
            {"x": 1, "y": 2},
            {"x": 2, "y": 5},
            {"x": 5, "y": 4},
            {"x": 4, "y": 1},
            {"x": 2, "y": 1},
        ]

        actual = iterative_downsampling(self.circular_points, self.n_iter)

        self.assertEqual(expected, actual)

    def test_iterative_downsampling_zero(self):
        actual = iterative_downsampling(self.circular_points, 0)
        self.assertEqual(self.circular_points, actual)

    def test_raises_assertion(self):
        self.assertRaises(AssertionError, iterative_downsampling, [], -1)
