import numpy as np
import cv2

from unittest import TestCase

from .main import mask2json


class TestMask2Json(TestCase):
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

        assert len(result) == len(self.json_objects)
        for json_object, result_object in zip(self.json_objects, result):
            self.assertCountEqual(json_object["points"], result_object["points"])

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

        assert len(result) == len(self.json_objects_tri)
        for json_object, result_object in zip(self.json_objects_tri, result):
            self.assertCountEqual(json_object["points"], result_object["points"])

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

        assert len(result) == len(self.json_objects_tri2)
        for json_object, result_object in zip(self.json_objects_tri2, result):
            self.assertCountEqual(json_object["points"], result_object["points"])

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

        assert len(result) == len(self.json_objects_multi)
        for json_object, result_object in zip(self.json_objects_multi, result):
            self.assertCountEqual(json_object["points"], result_object["points"])

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

        assert len(result) == len(self.json_objects_multi_connected)
        for json_object, result_object in zip(
            self.json_objects_multi_connected, result
        ):
            self.assertCountEqual(json_object["points"], result_object["points"])

    def test_no_mask(self):
        input_mask = np.zeros((10, 10), dtype=np.uint8)

        result = mask2json(input_mask)

        assert len(result) == len({}) == 0

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

        assert len(result) == len({}) == 0

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

        assert len(result) == len(self.json_objects_small)
        for json_object, result_object in zip(self.json_objects_small, result):
            self.assertCountEqual(json_object["points"], result_object["points"])
