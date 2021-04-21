from __future__ import absolute_import
from unittest import TestCase
import numpy as np
from numpy import array, uint8, uint16, uint32, int64
from .main import labels2contours


class TestSelect_labels2Contours(TestCase):
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
            [[[0, 2]], [[2, 2]]], #1
            [[[1, 3]], [[1, 6]], [[4, 6]]], #2
            [[[1, 0]], [[1, 1]], [[2, 1]], [[2, 0]]], #5
        ]

        result = labels2contours(data)

        self.assertEqual(len(expected_output), len(result))

        for i in range(len(expected_output)):
            x = result[i]
            print(x)
            np.testing.assert_array_equal(x, expected_output[i])

