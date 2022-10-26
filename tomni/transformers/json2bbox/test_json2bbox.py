from unittest import TestCase
import numpy as np
from .main import json2bbox


class TestJson2bbox(TestCase):
    def test_happy_flow_polygon(self):
        expectedResult = (500, 50, 539, 99)

        inputContours = {
            "type": "polygon",
            "points": [
                {"x": 500, "y": 50},
                {"x": 500, "y": 99},
                {"x": 520, "y": 79},
                {"x": 539, "y": 99},
                {"x": 520, "y": 79},
                {"x": 539, "y": 50},
            ],
            "id": "unicorn",
            "parents": [],
            "children": [],
        }

        result = json2bbox(inputContours)

        np.testing.assert_equal(result, expectedResult)

    def test_happy_flow_ellipse(self):
        expectedResult = (0, 1, 12, 9)

        inputContours = {
            "type": "ellipse",
            "center": {"x": 6.0, "y": 5.0},
            "radiusX": 6.0,
            "radiusY": 4.0,
            "angleOfRotation": 0,
            "id": "unicorn",
        }

        result = json2bbox(inputContours)

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
            json2bbox(inputContours)

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

        with self.assertRaises(KeyError):
            json2bbox(inputContours)
