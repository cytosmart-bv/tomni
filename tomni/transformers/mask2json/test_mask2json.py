import numpy as np
import cv2

from unittest import TestCase

from .main import mask2json


class TestMask2Json(TestCase):
    def compare_result_to_expected(self, expected_result, result):
        assert len(result) == len(expected_result)
        for json_object, result_object in zip(expected_result, result):
            self.assertListEqual(json_object["points"], result_object["points"])

            # Inner objects
            result_inner = result_object.get("innerObjects", [])
            expected_result_inner = json_object.get("innerObjects", [])
            assert len(result_inner) == len(expected_result_inner)
            for json_object_inner, result_object_inner in zip(
                expected_result_inner, result_inner
            ):
                self.assertListEqual(
                    json_object_inner["points"], result_object_inner["points"]
                )

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
                    {"x": 2, "y": 3},
                    {"x": 3, "y": 2},
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

        self.json_objects_multi_connected = [
            {
                "type": "polygon",
                "points": [
                    {"x": 2, "y": 2},
                    {"x": 2, "y": 4},
                    {"x": 4, "y": 4},
                    {"x": 5, "y": 5},
                    {"x": 5, "y": 7},
                    {"x": 7, "y": 7},
                    {"x": 7, "y": 5},
                    {"x": 5, "y": 5},
                    {"x": 4, "y": 4},
                    {"x": 4, "y": 2},
                ],
            },
        ]

    def test_single_object(self):
        input_mask = (
            np.array(
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
            * 255
        )
        result = mask2json(input_mask)
        print(result)

        self.compare_result_to_expected(result, self.json_objects)

    def test_single_donut(self):
        input_mask = (
            np.array(
                [
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                ],
                dtype=np.uint8,
            )
            * 255
        )

        expected_result = [
            {
                "type": "polygon",
                "points": [
                    {"x": 2, "y": 2},
                    {"x": 2, "y": 5},
                    {"x": 5, "y": 5},
                    {"x": 5, "y": 2},
                ],
                "innerObjects": [
                    {
                        "type": "polygon",
                        "points": [
                            {"x": 2, "y": 3},
                            {"x": 3, "y": 2},
                            {"x": 4, "y": 2},
                            {"x": 5, "y": 3},
                            {"x": 5, "y": 4},
                            {"x": 4, "y": 5},
                            {"x": 3, "y": 5},
                            {"x": 2, "y": 4},
                        ],
                    }
                ],
            }
        ]

        result = mask2json(input_mask, return_inner_contours=True)
        print(result)

        self.compare_result_to_expected(result, expected_result)

    def test_double_donut(self):
        input_mask = (
            np.array(
                [
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
                    [0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
                    [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                ],
                dtype=np.uint8,
            )
            * 255
        )

        expected_result = [
            {
                "type": "polygon",
                "points": [
                    {"x": 2, "y": 2},
                    {"x": 2, "y": 5},
                    {"x": 8, "y": 5},
                    {"x": 8, "y": 2},
                ],
                "innerObjects": [
                    {
                        "type": "polygon",
                        "points": [
                            {"x": 5, "y": 3},
                            {"x": 6, "y": 2},
                            {"x": 7, "y": 2},
                            {"x": 8, "y": 3},
                            {"x": 8, "y": 4},
                            {"x": 7, "y": 5},
                            {"x": 6, "y": 5},
                            {"x": 5, "y": 4},
                        ],
                    },
                    {
                        "type": "polygon",
                        "points": [
                            {"x": 2, "y": 3},
                            {"x": 3, "y": 2},
                            {"x": 4, "y": 2},
                            {"x": 5, "y": 3},
                            {"x": 5, "y": 4},
                            {"x": 4, "y": 5},
                            {"x": 3, "y": 5},
                            {"x": 2, "y": 4},
                        ],
                    },
                ],
            }
        ]

        result = mask2json(input_mask, return_inner_contours=True)
        print(result)

        self.compare_result_to_expected(result, expected_result)

    def test_double_donut_and_friend(self):
        input_mask = (
            np.array(
                [
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
                    [0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
                    [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                ],
                dtype=np.uint8,
            )
            * 255
        )

        expected_result = [
            {
                "type": "polygon",
                "points": [
                    {"x": 2, "y": 2},
                    {"x": 2, "y": 5},
                    {"x": 8, "y": 5},
                    {"x": 8, "y": 2},
                ],
                "innerObjects": [
                    {
                        "type": "polygon",
                        "points": [
                            {"x": 5, "y": 3},
                            {"x": 6, "y": 2},
                            {"x": 7, "y": 2},
                            {"x": 8, "y": 3},
                            {"x": 8, "y": 4},
                            {"x": 7, "y": 5},
                            {"x": 6, "y": 5},
                            {"x": 5, "y": 4},
                        ],
                    },
                    {
                        "type": "polygon",
                        "points": [
                            {"x": 2, "y": 3},
                            {"x": 3, "y": 2},
                            {"x": 4, "y": 2},
                            {"x": 5, "y": 3},
                            {"x": 5, "y": 4},
                            {"x": 4, "y": 5},
                            {"x": 3, "y": 5},
                            {"x": 2, "y": 4},
                        ],
                    },
                ],
            },
            {
                "type": "polygon",
                "points": [
                    {"x": 1, "y": 7},
                    {"x": 1, "y": 9},
                    {"x": 2, "y": 9},
                    {"x": 2, "y": 7},
                ],
            },
        ]

        result = mask2json(input_mask, return_inner_contours=True)
        print(result)

        self.compare_result_to_expected(result, expected_result)

    def test_single_tri(self):
        input_mask = (
            np.array(
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
            * 255
        )

        result = mask2json(input_mask)

        self.compare_result_to_expected(result, self.json_objects_tri)

    def test_single_tri2(self):
        input_mask = (
            np.array(
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
            * 255
        )

        result = mask2json(input_mask)
        print(result)

        self.compare_result_to_expected(result, self.json_objects_tri2)

    def test_multiple_objects_not_connected(self):
        input_mask = (
            np.array(
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
            * 255
        )

        result = mask2json(input_mask, is_diagonal_connected=False)
        print(result)

        self.compare_result_to_expected(result, self.json_objects_multi)

    def test_multiple_objects(self):
        input_mask = (
            np.array(
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
            * 255
        )

        result = mask2json(input_mask, is_diagonal_connected=True)
        print(result)

        self.compare_result_to_expected(result, self.json_objects_multi_connected)

    def test_no_mask(self):
        input_mask = np.zeros((10, 10), dtype=np.uint8)

        result = mask2json(input_mask)

        self.compare_result_to_expected(result, [])

    def test_to_small_objects(self):
        input_mask = (
            np.array(
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
            * 255
        )

        result = mask2json(input_mask)

        self.compare_result_to_expected(result, [])

    def test_to_small_objects_lim0(self):
        input_mask = (
            np.array(
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
            * 255
        )

        result = mask2json(input_mask, 0)

        self.compare_result_to_expected(result, self.json_objects_small)
