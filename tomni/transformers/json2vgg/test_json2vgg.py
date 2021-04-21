from __future__ import absolute_import
from unittest import TestCase
from .main import json2vgg


class TestJson2VGG(TestCase):
    def test_select_vgg_2_Json_one_file(self):
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
            },
            {
                "type": "ellipse",
                "accuracy": 0.443,
                "id": "unicorn",
                "center": {"x": 769, "y": 649},
                "radiusX": 24,
                "radiusY": 23,
                "angleOfRotation": 0,
            },
        ]

        expected_vgg_json_output = {
            "test1.jpg": {
                "filename": "test1.jpg",
                "regions": [
                    {
                        "shape_attributes": {
                            "name": "polygon",
                            "all_points_x": [
                                505,
                                478,
                            ],
                            "all_points_y": [
                                745,
                                756,
                            ],
                        },
                        "region_attributes": {"accuracy": 0.45455},
                    },
                    {
                        "shape_attributes": {
                            "name": "ellipse",
                            "cx": 769,
                            "cy": 649,
                            "rx": 24,
                            "ry": 23,
                            "theta": 0,
                        },
                        "region_attributes": {"accuracy": 0.443},
                    },
                ],
                "file_attributes": {},
            },
        }

        result = json2vgg(input_json_list, "test1")

        for i in range(len(result)):
            self.assertDictEqual(result, expected_vgg_json_output)

    def test_select_vgg_2_Json_one_file_no_accuracy(self):
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
            },
            {
                "type": "ellipse",
                "accuracy": 0.443,
                "id": "unicorn",
                "center": {"x": 769, "y": 649},
                "radiusX": 24,
                "radiusY": 23,
                "angleOfRotation": 0,
            },
        ]

        expected_vgg_json_output = {
            "test1.jpg": {
                "filename": "test1.jpg",
                "regions": [
                    {
                        "shape_attributes": {
                            "name": "polygon",
                            "all_points_x": [
                                505,
                                478,
                            ],
                            "all_points_y": [
                                745,
                                756,
                            ],
                        },
                        "region_attributes": {},
                    },
                    {
                        "shape_attributes": {
                            "name": "ellipse",
                            "cx": 769,
                            "cy": 649,
                            "rx": 24,
                            "ry": 23,
                            "theta": 0,
                        },
                        "region_attributes": {},
                    },
                ],
                "file_attributes": {},
            },
        }

        result = json2vgg(input_json_list, "test1", add_accuracy=False)

        for i in range(len(result)):
            self.assertDictEqual(result, expected_vgg_json_output)
