from __future__ import absolute_import
from unittest import TestCase
import numpy as np
from numpy import array, uint8, uint16, uint32, int64
from .main import labels2listsOfPoints


class TestSelect_labels2ListOfPoints(TestCase):
    def test_select_labels_as_indices(self):
        data = array(
            [
                [0, 5, 5, 0, 3, 3],
                [0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 7, 7],
                [0, 2, 0, 0, 7, 7],
                [0, 2, 2, 0, 0, 7],
                [0, 2, 2, 0, 0, 0],
                [0, 2, 2, 0, 8, 0],
            ]
        )

        expected_output = [
            [[0, 2]],
            [[1, 3], [1, 4], [2, 4], [1, 5], [2, 5], [1, 6], [2, 6]],
            [[4, 0], [5, 0]],
            [[1, 0], [2, 0]],
            [[4, 2], [5, 2], [4, 3], [5, 3], [5, 4]],
            [[4, 6]],
        ]

        result = labels2listsOfPoints(data)

        self.assertEqual(len(expected_output), len(result))

        for i in range(len(expected_output)):
            x = result[i]
            print(x)
            np.testing.assert_array_equal(x, expected_output[i])
