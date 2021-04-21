from __future__ import absolute_import
from unittest import TestCase
from .main import make_mask_circle
import numpy as np

class TestCircle_mask_selector(TestCase):
    def test_5x5_5(self):
        expected = np.array([
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0]
        ])

        result = make_mask_circle((5, 5), 5)
        np.testing.assert_array_equal(result, expected)

    def test_5x7_5(self):
        expected = np.array([
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
        ])

        result = make_mask_circle((5, 7), 5)
        np.testing.assert_array_equal(result, expected)
    
    def test_7x7_5(self):
        expected = np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ])

        result = make_mask_circle((7, 7), 5)
        np.testing.assert_array_equal(result, expected)

    def test_7x10_6(self):
        expected = np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ])

        result = make_mask_circle((7, 10), 6)
        np.testing.assert_array_equal(result, expected)

    def test_big_301x201(self):
        result = make_mask_circle((301, 201),101)
        self.assertEqual(np.shape(result), (201, 301))
        self.assertEqual(result[0, 0], False)
        self.assertEqual(result[0, 150], False)
        self.assertEqual(result[25, 75], False)
        self.assertEqual(result[100, 150], True)
        self.assertEqual(result[63, 117], True)
        
    def test_overflow_5001(self):
        result = make_mask_circle((5001, 5001),5000)

        self.assertEqual(result[0, 0], False)
        self.assertEqual(result[5000, 5000], False)
        self.assertEqual(result[4300, 4300], False)
        self.assertEqual(result[2500, 2500], True)
        self.assertEqual(result[3300, 3300], True)

    # # RUN THIS LOCALY. This is to big for the build agent
    # def test_overflow_25001(self):
    #     result = make_mask_circle((25001, 25001),25000)
    #
    #     self.assertEqual(result[0, 0], False)
    #     self.assertEqual(result[25000, 25000], False)
    #     self.assertEqual(result[21400, 21400], False)
    #     self.assertEqual(result[21300, 21300], True)
    #     self.assertEqual(result[12500, 12500], True)
