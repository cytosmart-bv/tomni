from __future__ import absolute_import

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

    def test_scaling_polygon_inner_contours(self):
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
                    {"x": 140.0, "y": 520.0},
                    {"x": 160.0, "y": 524.0},
                    {"x": 160.0, "y": 528.0},
                    {"x": 164.0, "y": 524.0},
                    {"x": 172.0, "y": 524.0},
                ],
                [
                    {"x": 400.0, "y": 124.0},
                    {"x": 400.0, "y": 128.0},
                    {"x": 400.0, "y": 136.0},
                    {"x": 404.0, "y": 124.0},
                ],
            ],
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
            "inner_points": [
                [
                    {"x": 35.0, "y": 130.0},
                    {"x": 40.0, "y": 131.0},
                    {"x": 40.0, "y": 132.0},
                    {"x": 41.0, "y": 131.0},
                    {"x": 43.0, "y": 131.0},
                ],
                [
                    {"x": 100.0, "y": 31.0},
                    {"x": 100.0, "y": 32.0},
                    {"x": 100.0, "y": 34.0},
                    {"x": 101.0, "y": 31.0},
                ],
            ],
        }

        result = scale_json(inputDict, inputScaling)

        self.assertDictEqual(result, expectedDict)

    def test_scaling_polygon_inner_contours_empty(self):
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
            "inner_points": [],
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
