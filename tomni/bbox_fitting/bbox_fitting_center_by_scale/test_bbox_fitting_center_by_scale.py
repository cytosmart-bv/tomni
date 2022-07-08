from unittest import TestCase

import numpy as np

from .main import bbox_fitting_center_by_scale


class TestBboxFittingCenterByScale(TestCase):
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

        self.test_data_scale_raise_error = [-1e-5, -0.1, 0, 1.1, 1.000001]

    def test_bbox_fitting_center_by_scale_succesful(self):
        for test_data in self.test_data_scale_succesful:
            with self.subTest(test_data["input_scale"]):
                actual_image = bbox_fitting_center_by_scale(
                    self.input_image, test_data["input_scale"]
                )
                np.testing.assert_array_equal(test_data["expected_image"], actual_image)

    def test_bbox_fitting_center_by_scale_error(self):
        for input_scale in self.test_data_scale_raise_error:
            with self.subTest(input_scale):
                self.assertRaises(
                    ValueError,
                    lambda: bbox_fitting_center_by_scale(self.input_image, input_scale),
                )
