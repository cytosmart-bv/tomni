from unittest import TestCase
import numpy as np
from .main import contours2json

class TestContour2json(TestCase):
    def test_happy_flow(self):
        inputContours = np.array([[[[500, 50]], [[500, 99]], [[539, 99]], [[539, 50]]]])

        expectedResult = [{
            "type": "polygon",
            "points": [
                {"x": 500, "y": 50},
                {"x": 500, "y": 99},
                {"x": 539, "y": 99},
                {"x": 539, "y": 50},
            ],
            "id": "unicorn",
            "parents": [],
            "children": [],
        }]

        result = contours2json(inputContours)
        result[0]["id"] = "unicorn"

        self.assertEqual(len(result), len(expectedResult))
        for i in range(len(result)):
            print(f"future {i}: \n input \n {result[i]} \n expected \n {expectedResult[i]}")
            self.assertDictEqual(result[i], expectedResult[i])