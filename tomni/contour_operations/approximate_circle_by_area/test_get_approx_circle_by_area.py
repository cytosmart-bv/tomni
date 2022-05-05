from unittest import TestCase
from .main import approximate_circle_by_area
import numpy as np


class TestGetAppoxCircleArea(TestCase):
    def test_free_shape(self):
        contour = np.array([[[70, 120]], [[80, 80]], [[70, 40]], [[60, 80]]])

        expected_result = (70, 80, 15.9576912161)
        result = approximate_circle_by_area(contour)
        print(result)

        self.assertEqual(len(result), len(expected_result))
        for i in range(len(result)):
            self.assertAlmostEqual(result[i], expected_result[i], 4)
