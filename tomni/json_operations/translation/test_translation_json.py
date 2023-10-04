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

    def test_polygon_inner_contours(self):
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
            "inner_points": [
                [
                    {"x": 185.0, "y": 120.0},
                    {"x": 190.0, "y": 121.0},
                    {"x": 190.0, "y": 122.0},
                    {"x": 191.0, "y": 121.0},
                    {"x": 193.0, "y": 121.0},
                ],
                [
                    {"x": 250.0, "y": 521.0},
                    {"x": 250.0, "y": 522.0},
                    {"x": 250.0, "y": 524.0},
                    {"x": 251.0, "y": 521.0},
                ],
            ],
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
            "inner_points": [
                [
                    {"x": 35.0, "y": 130.0},
                    {"x": 40.0, "y": 131.0},
                    {"x": 40.0, "y": 132.0},
                    {"x": 41.0, "y": 131.0},
                    {"x": 43.0, "y": 131.0},
                ],
                [
                    {"x": 100.0, "y": 531.0},
                    {"x": 100.0, "y": 532.0},
                    {"x": 100.0, "y": 534.0},
                    {"x": 101.0, "y": 531.0},
                ],
            ],
        }

        result = translation_json(inputDict, translation_x, translation_y)

        self.assertDictEqual(result, expectedDict)

    def test_polygon_inner_contours_empty(self):
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
            "inner_points": [],
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
            "inner_points": [],
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
