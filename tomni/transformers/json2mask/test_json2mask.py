import numpy as np

from numpy.testing import assert_array_equal
from unittest import TestCase

from .main import json2mask
from ...make_mask import make_mask_circle

class TestJson2Mask(TestCase):
    @classmethod
    def setUp(self):
        self.json_objects = [
            {
                "type": "polygon",
                "points": [
                    {"x": 2, "y": 2},
                    {"x": 2, "y": 4},
                    {"x": 4, "y": 4},
                    {"x": 4, "y": 2},
                ],
            }
        ]
        self.json_objects_small = [
            {
                "type": "polygon",
                "points": [
                    {"x": 2, "y": 2},
                    {"x": 4, "y": 2},
                ],
            }
        ]
        self.json_objects_tri = [
            {
                "type": "polygon",
                "points": [
                    {"x": 2, "y": 2},
                    {"x": 3, "y": 2},
                    {"x": 2, "y": 3},
                ],
            }
        ]
        self.json_objects_tri2 = [
            {
                "type": "polygon",
                "points": [
                    {"x": 2, "y": 2},
                    {"x": 5, "y": 5},
                    {"x": 8, "y": 2},
                ],
            }
        ]
        self.json_objects_multi = [
            {
                "type": "polygon",
                "points": [
                    {"x": 2, "y": 2},
                    {"x": 2, "y": 4},
                    {"x": 4, "y": 4},
                    {"x": 4, "y": 2},
                ],
            },
            {
                "type": "polygon",
                "points": [
                    {"x": 5, "y": 5},
                    {"x": 5, "y": 7},
                    {"x": 7, "y": 7},
                    {"x": 7, "y": 5},
                ],
            },
        ]
        self.json_objects_multi_overlap = [
            {
                "type": "polygon",
                "points": [
                    {"x": 2, "y": 2},
                    {"x": 2, "y": 4},
                    {"x": 4, "y": 4},
                    {"x": 4, "y": 2},
                ],
            },
            {
                "type": "polygon",
                "points": [
                    {"x": 4, "y": 4},
                    {"x": 4, "y": 7},
                    {"x": 7, "y": 7},
                    {"x": 7, "y": 4},
                ],
            },
        ]
        self.img_dim = (10, 10)

    def test_single_object(self):
        expected_result = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            dtype=np.uint8,
        )
        result = json2mask(self.json_objects, self.img_dim)

        assert_array_equal(expected_result, result)

    def test_single_tri(self):
        expected_result = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            dtype=np.uint8,
        )

        result = json2mask(self.json_objects_tri, self.img_dim)

        assert_array_equal(expected_result, result)

    def test_single_tri2(self):
        expected_result = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            dtype=np.uint8,
        )

        result = json2mask(self.json_objects_tri2, self.img_dim)
        print(result)

        assert_array_equal(expected_result, result)

    def test_multiple_objects(self):
        expected_result = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            dtype=np.uint8,
        )

        result = json2mask(self.json_objects_multi, self.img_dim)

        assert_array_equal(expected_result, result)

    def test_multiple_objects_overlap(self):
        expected_result = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            dtype=np.uint8,
        )

        result = json2mask(self.json_objects_multi_overlap, self.img_dim)
        assert_array_equal(expected_result, result)

    def test_to_small_objects(self):
        expected_result = np.zeros((10, 10), dtype=np.uint8)

        result = json2mask(self.json_objects_small, self.img_dim)

        assert_array_equal(expected_result, result)

    def test_to_small_objects_lim0(self):
        expected_result = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            dtype=np.uint8,
        )

        result = json2mask(self.json_objects_small, self.img_dim, 0)

        assert_array_equal(expected_result, result)

    def test_circle_floats(self):
        size = (11, 13)
        json_objects = [
            {
                "type": "ellipse",
                "center": {"x": 6., "y": 4.},
                "radiusX": 6.,
                "radiusY": 4.,
                "angleOfRotation": 0,
                "id": "unicorn",
            }
        ]

        expected = np.array(
            [
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )

        result = json2mask(json_objects, size, 0)
        assert_array_equal(result, expected)

    def test_big_circle(self):
        size = (10000, 10001)

        json_objects = [
            {
                "type": "ellipse",
                "center": {"x": 5000, "y": 2467},
                "radiusX": 3200,
                "radiusY": 1692,
                "angleOfRotation": 0,
                "id": "unicorn",
            }
        ]    

        mask = json2mask(json_objects, size, 0)
        self.assertEqual(True, mask[2467][5000])
        self.assertEqual(True, mask[3000][5000])

        # X minimum
        self.assertEqual(False, mask[2467][1798])
        self.assertEqual(True, mask[2467][1801])

        # X Maximum
        self.assertEqual(True, mask[2467][8198])
        self.assertEqual(False, mask[2467][8201])
        
        # Y minimum
        self.assertEqual(False, mask[773][5000])
        self.assertEqual(True, mask[777][5000])

        # Y maximum
        self.assertEqual(True, mask[4157][5000])
        self.assertEqual(False, mask[4161][5000])

    def test_big_circle_floats(self):
        size = (10000, 10001)

        json_objects = [
            {
                "type": "ellipse",
                "center": {"x": 5000., "y": 2467.},
                "radiusX": 3200.,
                "radiusY": 1692.,
                "angleOfRotation": 0,
                "id": "unicorn",
            }
        ]    

        mask = json2mask(json_objects, size, 0)
        self.assertEqual(True, mask[2467][5000])
        self.assertEqual(True, mask[3000][5000])

        # X minimum
        self.assertEqual(False, mask[2467][1798])
        self.assertEqual(True, mask[2467][1801])

        # X Maximum
        self.assertEqual(True, mask[2467][8198])
        self.assertEqual(False, mask[2467][8201])
        
        # Y minimum
        self.assertEqual(False, mask[773][5000])
        self.assertEqual(True, mask[777][5000])

        # Y maximum
        self.assertEqual(True, mask[4157][5000])
        self.assertEqual(False, mask[4161][5000])

    def test_circle(self):
        size = (11, 13)
        json_objects = [
            {
                "type": "ellipse",
                "center": {"x": 6, "y": 4},
                "radiusX": 6,
                "radiusY": 4,
                "angleOfRotation": 0,
                "id": "unicorn",
            }
        ]

        expected = np.array(
            [
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )

        result = json2mask(json_objects, size, 0)
        assert_array_equal(result, expected)

    def test_big_image_ellipse(self):
        size = (500, 500)
        json_objects = [
            {
                "type": "ellipse",
                "center": {"x": 100, "y": 100},
                "radiusX": 25,
                "radiusY": 25,
                "angleOfRotation": 0,
                "id": "48881bfa-59bb-42a8-bb6a-8fb91486b023",
                "accuracy": 0.59511399269104,
                "label": "organoid",
                "area": 1134.1149479459152,
                "diameter": 38.0,
                "aspect_ratio": 1.0,
                "roundness": 4.0,
                "circularity": 1.0,
                "created_using": "organoid_run_16_v0_3",
            }
        ]

        expected = np.zeros((500, 500), dtype=np.uint8)
        expected[75:126, 75:126] = make_mask_circle((51, 51), 50)

        result = json2mask(json_objects, size, 0)
        assert_array_equal(result, expected)