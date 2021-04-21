from unittest import TestCase
from .main import translation_json


class TestScaleObject(TestCase):
    def test_ellipses(self):
        inputDict = {
            "type": "ellipse",
            "center": {"x": 20, "y": 30},
            "radiusX": 10,
            "radiusY": 10,
            "angleOfRotation": 0,
            "id": "unicorn",
        }
        translation_x = 50
        translation_y = -100

        expectedDict = {
            "type": "ellipse",
            "center": {"x": 70, "y": -70},
            "radiusX": 10,
            "radiusY": 10,
            "angleOfRotation": 0,
            "id": "unicorn",
        }

        result = translation_json(inputDict, translation_x, translation_y)

        self.assertDictEqual(result, expectedDict)

    def test_polygon(self):
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
        translation_x = -150
        translation_y = 10

        expectedDict = {
            "type": "polygon",
            "points": [
                {"x": 350, "y": 62},
                {"x": 350, "y": 110},
                {"x": 390, "y": 110},
                {"x": 390, "y": 62},
            ],
            "id": "unicorn",
            "parents": [],
            "children": [],
        }

        result = translation_json(inputDict, translation_x, translation_y)

        self.assertDictEqual(result, expectedDict)

    def test_unknown_type(self):
        inputDict = {
            "type": "unicornType",
        }
        translation_x = -150
        translation_y = 10
        with self.assertRaises(ValueError):
            result = translation_json(inputDict, translation_x, translation_y)
