from unittest import TestCase

import numpy as np

from .main import crop_image_by_dim


class TestCropByDim(TestCase):
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
        self.test_data_scale_succesful = [
            {
                "input_scale": 1 - 1e-5,
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
            {"input_scale": 1, "expected_image": self.input_image},
            {
                "input_scale": 0.5,
                "expected_image": [
                    [0, 0, 1, 1, 1],
                    [0, 0, 1, 1, 1],
                    [1, 1, 0, 0, 0],
                    [1, 1, 0, 0, 0],
                    [1, 1, 0, 0, 0],
                ],
            },
            {
                "input_scale": 0.9,
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
            {"input_scale": 0.1, "expected_image": [[0]],},
        ]

        self.test_data_dimensions_raises_error = [11, -1]

    def test_crop_image_by_dim_succesfull(self):
        for test_data in self.test_data_dimensions_succesfull:
            with self.subTest(test_data["input_dim"]):
                actual_image = crop_image_by_dim(
                    self.input_image, test_data["input_dim"]
                )
                np.testing.assert_array_equal(test_data["expected_image"], actual_image)

    def test_crop_image_by_dim_raise_error(self):
        for input_dim in self.test_data_dimensions_raises_error:
            with self.subTest(input_dim):
                self.assertRaises(
                    ValueError, lambda: crop_image_by_dim(self.input_image, input_dim)
                )
