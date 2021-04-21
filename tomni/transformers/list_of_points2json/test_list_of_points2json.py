from unittest import TestCase
import numpy as np
from .main import list_of_points2json

class TestContour2json(TestCase):
    def test_happy_flow_np_array(self):
        list_of_points = np.array([[500, 50], [500, 99], [539, 99], [539, 50]])

        expectedResult = {
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
        }

        result = list_of_points2json(list_of_points)
        result["id"] = "unicorn"

        self.assertDictEqual(result, expectedResult)

    def test_happy_flow_list(self):
        list_of_points = [[600, 50], [600, 99], [412, 99], [412, 50]]

        expectedResult = {
            "type": "polygon",
            "points": [
                {"x": 600, "y": 50},
                {"x": 600, "y": 99},
                {"x": 412, "y": 99},
                {"x": 412, "y": 50},
            ],
            "id": "unicorn",
            "parents": [],
            "children": [],
        }

        result = list_of_points2json(list_of_points)
        result["id"] = "unicorn"

        self.assertDictEqual(result, expectedResult)