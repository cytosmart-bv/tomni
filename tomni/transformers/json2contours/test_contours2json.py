from unittest import TestCase
import numpy as np
from .main import json2contours

class TestJson2contours(TestCase):
    def test_happy_flow(self):
        expectedResult  = np.array([[[500, 50]], [[500, 99]], [[539, 99]], [[539, 50]]])

        inputContours = {
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

        result = json2contours(inputContours)

        np.testing.assert_equal(result, expectedResult)

    def test_value_error_unsupported_type(self):
        inputContours = {
            "type": "unicorn",
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

        with self.assertRaises(ValueError):
            json2contours(inputContours)

    def test_value_error_no_type_given(self):
        inputContours = {
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

        with self.assertRaises(ValueError):
            json2contours(inputContours)