from __future__ import absolute_import
from unittest import TestCase
from .main import vgg2json


class TestVGG2Json(TestCase):
    def test_select_vgg_2_Json_one_file(self):
        input_vgg_json = {
            "test1.jpg": {
                "filename": "test1.jpg",
                "size": 151409,
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
                        "region_attributes": {"name": "organoid"},
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
            },
        }

        expected_output = [
            [
                {
                    "type": "polygon",
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
                    "id": "unicorn",
                    "center": {"x": 769, "y": 649},
                    "radiusX": 24,
                    "radiusY": 23,
                    "angleOfRotation": 0,
                },
            ]
        ]

        result = vgg2json(input_vgg_json)
        result[0][0]["id"] = "unicorn"
        result[0][1]["id"] = "unicorn"

        self.assertEqual(len(result), len(expected_output))
        for i in range(len(result)):
            self.assertDictEqual(result[i][0], expected_output[i][0])
            self.assertDictEqual(result[i][1], expected_output[i][1])

    def test_circle(self):
        input_vgg_json = {
            "test1.jpg": {
                "filename": "test1.jpg",
                "size": 151409,
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
                        "region_attributes": {"name": "organoid"},
                    },
                    {
                        "shape_attributes": {
                            "name": "circle",
                            "cx": 769,
                            "cy": 649,
                            "r": 24
                        },
                        "region_attributes": {},
                    },
                ],
            },
        }

        expected_output = [
            [
                {
                    "type": "polygon",
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
                    "id": "unicorn",
                    "center": {"x": 769, "y": 649},
                    "radiusX": 24,
                    "radiusY": 24,
                    "angleOfRotation": 0,
                },
            ]
        ]

        result = vgg2json(input_vgg_json)
        result[0][0]["id"] = "unicorn"
        result[0][1]["id"] = "unicorn"

        self.assertEqual(len(result), len(expected_output))
        for i in range(len(result)):
            self.assertDictEqual(result[i][0], expected_output[i][0])
            self.assertDictEqual(result[i][1], expected_output[i][1])

    def test_select_vgg_2_Json_multi_file(self):
        input_vgg_json = {
            "test1.jpg": {
                "filename": "test1.jpg",
                "size": 151409,
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
                        "region_attributes": {"name": "organoid"},
                    },
                ],
            },
            "test2.jpg": {
                "filename": "test2.jpg",
                "size": 151409,
                "regions": [
                    {
                        "shape_attributes": {
                            "name": "polygon",
                            "all_points_x": [
                                502,
                                472,
                            ],
                            "all_points_y": [
                                742,
                                752,
                            ],
                        },
                        "region_attributes": {"name": "organoid"},
                    },
                ],
            },
        }

        expected_output = [
            [
                {
                    "type": "polygon",
                    "parents": [],
                    "children": [],
                    "id": "unicorn",
                    "points": [
                        {"x": 505, "y": 745},
                        {"x": 478, "y": 756},
                    ],
                },
            ],
            [
                {
                    "type": "polygon",
                    "parents": [],
                    "children": [],
                    "id": "unicorn",
                    "points": [
                        {"x": 502, "y": 742},
                        {"x": 472, "y": 752},
                    ],
                },
            ],
        ]

        result = vgg2json(input_vgg_json)
        result[0][0]["id"] = "unicorn"
        result[1][0]["id"] = "unicorn"

        self.assertEqual(len(result), len(expected_output))
        for i in range(len(result)):
            for j in range(len(result[i])):
                self.assertDictEqual(result[i][j], expected_output[i][j])


