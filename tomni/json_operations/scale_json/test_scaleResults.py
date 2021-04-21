from unittest import TestCase
from .main import scale_json


class TestScaleObject(TestCase):
    def test_scaling_ellipses(self):
        inputDict = {
            "type": "ellipse",
            "center": {"x": 20, "y": 30},
            "radiusX": 10,
            "radiusY": 10,
            "angleOfRotation": 0,
            "id": "unicorn",
        }
        inputScaling = 0.5

        expectedDict = {
            "type": "ellipse",
            "center": {"x": 10, "y": 15},
            "radiusX": 5,
            "radiusY": 5,
            "angleOfRotation": 0,
            "id": "unicorn",
        }

        result = scale_json(inputDict, inputScaling)

        self.assertDictEqual(result, expectedDict)

    def test_scaling_polygon(self):
        inputDict = {
            "type": "polygon",
            "points": [
                {"x": 500, "y": 52},
                {"x": 500, "y": 100},
                {"x": 540, "y": 100},
                {"x": 540, "y": 52},
            ],
            "id": "unicorn",
            "parents": [],
            "children": [],
        }
        inputScaling = 0.25

        expectedDict = {
            "type": "polygon",
            "points": [
                {"x": 125, "y": 13},
                {"x": 125, "y": 25},
                {"x": 135, "y": 25},
                {"x": 135, "y": 13},
            ],
            "id": "unicorn",
            "parents": [],
            "children": [],
        }

        result = scale_json(inputDict, inputScaling)

        self.assertDictEqual(result, expectedDict)

    def test_unknown_type(self):
        inputDict = {
            "type": "unicornType",
        }
        inputScaling = 1.02
        with self.assertRaises(ValueError):
            result = scale_json(inputDict, inputScaling)