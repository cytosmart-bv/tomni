from __future__ import absolute_import
from unittest import TestCase
from .main import json2dict


class TestJson2Dict(TestCase):
    def test_default(self):
        input_json_list = [
            {
                "type": "polygon",
                "accuracy": 0.45455,
                "parents": [],
                "children": [],
                "id": "unicorn",
                "points": [
                    {"x": 505, "y": 745},
                    {"x": 478, "y": 756},
                ],
                "area": 300,
            },
            {
                "type": "ellipse",
                "accuracy": 0.443,
                "id": "unicorn",
                "center": {"x": 769, "y": 649},
                "radiusX": 24,
                "radiusY": 23,
                "angleOfRotation": 0,
                "area": 3,
            },
        ]

        expected_output = {
            "type": ["polygon", "ellipse"],
            "area": [300, 3],
            "id": ["unicorn", "unicorn"],
            "center": [None, [769, 649]],
            "index": [0, 1],
        }

        result = json2dict(input_json_list)

        self.assertDictEqual(result, expected_output)

    def test_singel_keyword(self):
        input_json_list = [
            {
                "type": "polygon",
                "accuracy": 0.45455,
                "parents": [],
                "children": [],
                "id": "unicorn",
                "points": [
                    {"x": 505, "y": 745},
                    {"x": 478, "y": 756},
                ],
                "area": 300,
            },
            {
                "type": "ellipse",
                "accuracy": 0.443,
                "id": "unicorn",
                "center": {"x": 769, "y": 649},
                "radiusX": 24,
                "radiusY": 23,
                "angleOfRotation": 0,
                "area": 3,
            },
        ]

        expected_output = {
            "radiusX": [None, 24],
            "index": [0, 1],
        }

        result = json2dict(input_json_list, ["radiusX"])

        self.assertDictEqual(result, expected_output)

    def test_multi_keyword(self):
        input_json_list = [
            {
                "type": "polygon",
                "accuracy": 0.45455,
                "parents": [],
                "children": [],
                "id": "unicorn",
                "points": [
                    {"x": 505, "y": 745},
                    {"x": 478, "y": 756},
                ],
                "area": 300,
            },
            {
                "type": "ellipse",
                "accuracy": 0.443,
                "id": "unicorn",
                "center": {"x": 769, "y": 649},
                "radiusX": 24,
                "radiusY": 23,
                "angleOfRotation": 0,
                "area": 3,
            },
        ]

        expected_output = {
            "points": [
                [
                    {"x": 505, "y": 745},
                    {"x": 478, "y": 756},
                ],
                None,
            ],
            "radiusX": [None, 24],
            "index": [0, 1],
        }

        result = json2dict(input_json_list, ["radiusX", "points"])

        self.assertDictEqual(result, expected_output)

    def test_unknown_keyword(self):
        input_json_list = [
            {
                "type": "polygon",
                "accuracy": 0.45455,
                "parents": [],
                "children": [],
                "id": "unicorn",
                "points": [
                    {"x": 505, "y": 745},
                    {"x": 478, "y": 756},
                ],
                "area": 300,
            },
            {
                "type": "ellipse",
                "accuracy": 0.443,
                "id": "unicorn",
                "center": {"x": 769, "y": 649},
                "radiusX": 24,
                "radiusY": 23,
                "angleOfRotation": 0,
                "area": 3,
            },
        ]

        expected_output = {
            "cytosmart": [None, None],
            "index": [0, 1],
        }

        result = json2dict(input_json_list, ["cytosmart"])

        self.assertDictEqual(result, expected_output)