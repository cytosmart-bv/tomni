from __future__ import absolute_import
from unittest import TestCase
import math
from .main import summary_json


class TestSummaryJson(TestCase):
    def test_summary(self):
        input_json_list = [
            {
                "type": "polygon",
                "accuracy": 0.45455,
                "parents": [],
                "children": [],
                "id": "unicorn",
                "points": [
                    {"x": 0, "y": 10},
                    {"x": 10, "y": 10},
                    {"x": 10, "y": 0},
                    {"x": 0, "y": 0},
                ],
            },
            {
                "type": "ellipse",
                "accuracy": 0.443,
                "id": "unicorn",
                "center": {"x": 769, "y": 649},
                "radiusX": 10,
                "radiusY": 20,
                "angleOfRotation": 0,
            },
        ]

        copy_json_list = [
            {
                "type": "polygon",
                "accuracy": 0.45455,
                "parents": [],
                "children": [],
                "id": "unicorn",
                "points": [
                    {"x": 0, "y": 10},
                    {"x": 10, "y": 10},
                    {"x": 10, "y": 0},
                    {"x": 0, "y": 0},
                ],
            },
            {
                "type": "ellipse",
                "accuracy": 0.443,
                "id": "unicorn",
                "center": {"x": 769, "y": 649},
                "radiusX": 10,
                "radiusY": 20,
                "angleOfRotation": 0,
            },
        ]

        expected_output = (
            2,
            round(math.pi * 10 * 20 + 100, 2),
            round((math.pi * 10 * 20 + 100) / 2, 2),
            round(math.pi * 10 * 20, 2),
            100.0,
        )

        result = summary_json(input_json_list, "area")

        self.assertTupleEqual(result, expected_output)

        self.assertListEqual(input_json_list, copy_json_list)

    def test_summary_copy_false(self):
        input_json_list = [
            {
                "type": "polygon",
                "accuracy": 0.45455,
                "parents": [],
                "children": [],
                "id": "unicorn",
                "points": [
                    {"x": 0, "y": 10},
                    {"x": 10, "y": 10},
                    {"x": 10, "y": 0},
                    {"x": 0, "y": 0},
                ],
            },
            {
                "type": "ellipse",
                "accuracy": 0.443,
                "id": "unicorn",
                "center": {"x": 769, "y": 649},
                "radiusX": 10,
                "radiusY": 20,
                "angleOfRotation": 0,
            },
        ]

        expected_json_list = [
            {
                "type": "polygon",
                "accuracy": 0.45455,
                "parents": [],
                "children": [],
                "id": "unicorn",
                "points": [
                    {"x": 0, "y": 10},
                    {"x": 10, "y": 10},
                    {"x": 10, "y": 0},
                    {"x": 0, "y": 0},
                ],
                "area": 100,
            },
            {
                "type": "ellipse",
                "accuracy": 0.443,
                "id": "unicorn",
                "center": {"x": 769, "y": 649},
                "radiusX": 10,
                "radiusY": 20,
                "angleOfRotation": 0,
                "area": math.pi * 10 * 20,
            },
        ]

        expected_output = (
            2,
            round(math.pi * 10 * 20 + 100, 2),
            round((math.pi * 10 * 20 + 100) / 2, 2),
            round(math.pi * 10 * 20, 2),
            100.0,
        )

        result = summary_json(input_json_list, "area", do_copy=False)

        self.assertTupleEqual(result, expected_output)

        self.assertListEqual(input_json_list, expected_json_list)

    def test_summary_rounding3(self):
        input_json_list = [
            {
                "type": "polygon",
                "accuracy": 0.45455,
                "parents": [],
                "children": [],
                "id": "unicorn",
                "points": [
                    {"x": 0, "y": 10},
                    {"x": 10, "y": 10},
                    {"x": 10, "y": 0},
                    {"x": 0, "y": 0},
                ],
            },
            {
                "type": "ellipse",
                "accuracy": 0.443,
                "id": "unicorn",
                "center": {"x": 769, "y": 649},
                "radiusX": 10,
                "radiusY": 20,
                "angleOfRotation": 0,
            },
        ]

        copy_json_list = [
            {
                "type": "polygon",
                "accuracy": 0.45455,
                "parents": [],
                "children": [],
                "id": "unicorn",
                "points": [
                    {"x": 0, "y": 10},
                    {"x": 10, "y": 10},
                    {"x": 10, "y": 0},
                    {"x": 0, "y": 0},
                ],
            },
            {
                "type": "ellipse",
                "accuracy": 0.443,
                "id": "unicorn",
                "center": {"x": 769, "y": 649},
                "radiusX": 10,
                "radiusY": 20,
                "angleOfRotation": 0,
            },
        ]

        expected_output = (
            2,
            round(math.pi * 10 * 20 + 100, 3),
            round((math.pi * 10 * 20 + 100) / 2, 3),
            round(math.pi * 10 * 20, 3),
            100.0,
        )

        result = summary_json(input_json_list, "area", rounding=3)

        self.assertTupleEqual(result, expected_output)

        self.assertListEqual(input_json_list, copy_json_list)

    def test_value_error(self):
        input_json_list = [
            {
                "type": "polygon",
                "accuracy": 0.45455,
                "parents": [],
                "children": [],
                "id": "unicorn",
                "points": [
                    {"x": 0, "y": 10},
                    {"x": 10, "y": 10},
                    {"x": 10, "y": 0},
                    {"x": 0, "y": 0},
                ],
            },
            {
                "type": "ellipse",
                "accuracy": 0.443,
                "id": "unicorn",
                "center": {"x": 769, "y": 649},
                "radiusX": 10,
                "radiusY": 20,
                "angleOfRotation": 0,
            },
        ]
        self.assertRaises(ValueError, summary_json, input_json_list, "aea")
