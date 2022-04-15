from unittest import TestCase
import numpy as np
from .main import circularity


class TestCircularity(TestCase):
    def test_perfect_square(self):
        contour = np.array([[[500, 50]], [[500, 99]], [[549, 99]], [[549, 50]]])

        expectedResult = np.pi / 4

        result = circularity(contour)

        self.assertAlmostEqual(result, expectedResult)

    def test_octagon(self):
        # Octagon is rounder then a square
        # This is not perfect but okay
        contour = np.array([
            [[500, 50]], [[490, 75]], 
            [[500, 99]], [[525, 109]], 
            [[549, 99]], [[559, 75]], 
            [[549, 50]], [[525, 40]], 
            ])

        expectedResult = 0.9479813831233634

        result = circularity(contour)

        self.assertAlmostEqual(result, expectedResult)

    def test_flat_rectangle(self):
        # A rectangle of 450 by 50
        contour = np.array([[[0, 50]], [[0, 100]], [[450, 100]], [[450, 50]]])

        expectedResult = 9 * np.pi / 100

        result = circularity(contour)

        self.assertAlmostEqual(result, expectedResult)