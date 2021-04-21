from unittest import TestCase
import numpy as np
from .main import get_center

class TestGetCenterContour(TestCase):
    def test_happy_flow(self):
        contour = np.array([[[500, 50]], [[500, 99]], [[539, 99]], [[539, 50]]])

        expectedResult = (519, 74)

        result = get_center(contour=contour)

        self.assertEqual(len(result), len(expectedResult))
        for i in range(len(result)):
            self.assertEqual(result[i], expectedResult[i])

    def test_single_point(self):
        contour = np.array([[[500, 50]]])

        expectedResult = (500, 50)

        result = get_center(contour=contour)

        self.assertEqual(len(result), len(expectedResult))
        for i in range(len(result)):
            self.assertEqual(result[i], expectedResult[i])