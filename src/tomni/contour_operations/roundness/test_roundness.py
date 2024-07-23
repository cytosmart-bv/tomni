from unittest import TestCase
import numpy as np
from .main import roundness


class TestRoundness(TestCase):
    def test_square(self):
        contour = np.array([[[500, 50]], [[500, 100]], [[550, 100]], [[550, 50]]])

        expectedResult = (50 * 50) / (25 * 25 * 2 * np.pi)

        result = roundness(contour)

        self.assertAlmostEqual(result, expectedResult, 5)

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

        expectedResult = 0.8964594850343249

        result = roundness(contour)

        self.assertAlmostEqual(result, expectedResult, 5)

    def test_square_with_dent(self):
        """
        A dent should not impact roundness to much as long as the area of the dent is relatively small
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

        expectedResult = (50 * 50 - 49) / (25 * 25 * 2 * np.pi)

        result = roundness(contour)

        self.assertAlmostEqual(result, expectedResult, 5)

    def test_flat_rectangle(self):
        # A rectangle of 450 by 50
        contour = np.array([[[0, 50]], [[0, 100]], [[450, 100]], [[450, 50]]])

        expectedResult = 0.13974567201687108

        result = roundness(contour)

        self.assertAlmostEqual(result, expectedResult)
