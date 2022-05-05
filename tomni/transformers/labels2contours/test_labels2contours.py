from __future__ import absolute_import
from unittest import TestCase
import numpy as np
from numpy import array
from .main import labels2contours


class TestSelect_labels2Contours(TestCase):
    def assert_output(self, expected_output, result):
        self.assertEqual(len(expected_output), len(result))
        for i in range(len(expected_output)):
            result_external = result[i][0]
            print(result_external)
            np.testing.assert_array_equal(result_external, expected_output[i][0])

            # Test inner contours
            result_internal_list = result[i][1]
            expected_internal_list = expected_output[i][1]
            self.assertEqual(len(expected_internal_list), len(result_internal_list))
            for result_internal, expected_internal in zip(
                result_internal_list, expected_internal_list
            ):
                np.testing.assert_array_equal(result_internal, expected_internal)

    def test_happy_flow(self):
        data = array(
            [
                [0, 5, 5, 0, 0, 0],
                [0, 5, 5, 0, 0, 0],
                [1, 1, 1, 0, 0, 0],
                [0, 2, 0, 0, 0, 0],
                [0, 2, 2, 0, 0, 0],
                [0, 2, 2, 2, 0, 0],
                [0, 2, 2, 2, 2, 0],
            ]
        )

        expected_output = [
            [[[0, 2]], [[2, 2]]],  # 1
            [[[1, 3]], [[1, 6]], [[4, 6]]],  # 2
            [[[1, 0]], [[1, 1]], [[2, 1]], [[2, 0]]],  # 5
        ]

        result = labels2contours(data)

        self.assert_output(expected_output, result)

    def test_return_inner_no_inner(self):
        data = array(
            [
                [0, 5, 5, 0, 0, 0],
                [0, 5, 5, 0, 0, 0],
                [1, 1, 1, 0, 0, 0],
                [0, 2, 0, 0, 0, 0],
                [0, 2, 2, 0, 0, 0],
                [0, 2, 2, 2, 0, 0],
                [0, 2, 2, 2, 2, 0],
            ]
        )

        expected_output = [
            [[[[0, 2]], [[2, 2]]], []],  # 1
            [[[[1, 3]], [[1, 6]], [[4, 6]]], []],  # 2
            [[[[1, 0]], [[1, 1]], [[2, 1]], [[2, 0]]], []],  # 5
        ]

        result = labels2contours(data, return_inner_contours=True)
        self.assert_output(expected_output, result)

    def test_donut(self):
        data = array(
            [
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 2, 2, 2, 2, 0],
                [0, 2, 0, 0, 2, 0],
                [0, 2, 0, 0, 2, 0],
                [0, 2, 2, 2, 2, 0],
            ]
        )

        expected_output = [
            [
                # External contour
                [[[1, 3]], [[1, 6]], [[4, 6]], [[4, 3]]],
                # All the internal contours
                [
                    # Corners are interpolated as being diagonal
                    # hench the 8 points for something that looks like a square
                    [
                        [[1, 4]],
                        [[2, 3]],
                        [[3, 3]],
                        [[4, 4]],
                        [[4, 5]],
                        [[3, 6]],
                        [[2, 6]],
                        [[1, 5]],
                    ]
                ],
            ],
        ]

        result = labels2contours(data, return_inner_contours=True)
        self.assert_output(expected_output, result)

    def test_deprated_warning(self):
        data = array(
            [
                [0, 5, 5, 0, 0, 0],
                [0, 5, 5, 0, 0, 0],
                [1, 1, 1, 0, 0, 0],
                [0, 2, 0, 0, 0, 0],
                [0, 2, 2, 0, 0, 0],
                [0, 2, 2, 2, 0, 0],
                [0, 2, 2, 2, 2, 0],
            ]
        )

        with self.assertRaises(DeprecationWarning):
            labels2contours(data, simplify_error=0.1)
