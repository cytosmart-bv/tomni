from unittest import TestCase

import numpy as np

from .main import crop_image_by_scale


class TestCropByScale(TestCase):
    @classmethod
    def setUp(self):

        # single object data
        self.input_image = np.array(
            [
                [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            ]
        )
        self.test_data_dimensions_succesful = [
            {
                "input_dim": 5,
                "expected_image": [
                    [0, 0, 1, 1, 1],
                    [0, 0, 1, 1, 1],
                    [1, 1, 0, 0, 0],
                    [1, 1, 0, 0, 0],
                    [1, 1, 0, 0, 0],
                ],
            },
            {"input_dim": 1, "expected_image": [[0]]},
            {"input_dim": 0, "expected_image": None},
            {"input_dim": 10, "expected_image": self.input_image},
            {
                "input_dim": 9,
                "expected_image": [
                    [0, 0, 0, 0, 1, 1, 1, 1, 1],
                    [0, 0, 0, 0, 1, 1, 1, 1, 1],
                    [0, 0, 0, 0, 1, 1, 1, 1, 1],
                    [0, 0, 0, 0, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 0, 0, 0, 0, 0],
                    [1, 1, 1, 1, 0, 0, 0, 0, 0],
                    [1, 1, 1, 1, 0, 0, 0, 0, 0],
                    [1, 1, 1, 1, 0, 0, 0, 0, 0],
                    [1, 1, 1, 1, 0, 0, 0, 0, 0],
                ],
            },
        ]
        self.test_data_dimensions_raises_error = [11, -1]

    def test_crop_image_by_scale_succesfull(self):
        for test_data in self.test_data_scale_succesful:
            with self.subTest(test_data["input_scale"]):
                actual_image = crop_image_by_scale(
                    self.input_image, test_data["input_scale"]
                )
                np.testing.assert_array_equal(test_data["expected_image"], actual_image)

    def test_crop_image_by_scale_raise_error(self):
        for input_scale in self.test_data_scale_raise_error:
            with self.subTest(input_scale):
                self.assertRaises(
                    ValueError,
                    lambda: crop_image_by_scale(self.input_image, input_scale),
                )
