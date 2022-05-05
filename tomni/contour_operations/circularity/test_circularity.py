from unittest import TestCase
import numpy as np
from .main import circularity


class TestCircularity(TestCase):
    def test_perfect_square(self):
        contour = np.array([[[500, 50]], [[500, 99]], [[549, 99]], [[549, 50]]])

        expected_result = np.pi / 4

        result = circularity(contour)

        self.assertAlmostEqual(result, expected_result)

    def test_octagon(self):
        # Octagon is rounder then a square
        # This is not perfect but okay
        contour = np.array(
            [
                [[500, 50]],
                [[490, 75]],
                [[500, 99]],
                [[525, 109]],
                [[549, 99]],
                [[559, 75]],
                [[549, 50]],
                [[525, 40]],
            ]
        )

        expected_result = 0.9479813831233634

        result = circularity(contour)

        self.assertAlmostEqual(result, expected_result)

    def test_flat_rectangle(self):
        # A rectangle of 450 by 50
        contour = np.array([[[0, 50]], [[0, 100]], [[450, 100]], [[450, 50]]])

        expected_result = 9 * np.pi / 100

        result = circularity(contour)

        self.assertAlmostEqual(result, expected_result)

    def test_square_with_dent(self):
        """
        A dent has a big impact on circularity because the perimeter get a lot bigger but the area gets smaller
        """
        contour = np.array(
            [
                [[500, 50]],
                [[500, 100]],
                # start dent
                [[524, 100]],
                [[524, 51]],
                [[525, 51]],
                [[525, 100]],
                # end ent
                [[550, 100]],
                [[550, 50]],
            ]
        )

        A = 50 * 50 - 49
        P = 50 * 4 + 2 * 49
        expected_result = (np.pi * 4 * A) / (P**2)  # 0.34683318742167396

        result = circularity(contour)

        self.assertAlmostEqual(result, expected_result, 5)
