import unittest
import numpy as np
from .main import contour2bbox


class TestContour2Bbox(unittest.TestCase):
    def test_conversion_normal(self):
        # array( [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #         [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        #         [0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
        #         [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype=uint8)

        input_contour = np.array(
            [[[3, 3]], [[3, 5]], [[5, 5]], [[5, 3]]], dtype=np.int32
        )

        expected_result = (3, 3, 6, 6)
        result = contour2bbox(input_contour)
        self.assertTupleEqual(expected_result, result)

    def test_conversion_negative(self):
        input_contour = np.array(
            [[[-3, -3]], [[-3, -5]], [[-5, -5]], [[-5, -3]]], dtype=np.int32
        )
        expected_result = (-5, -5, -2, -2)
        result = contour2bbox(input_contour)
        self.assertTupleEqual(expected_result, result)
