from __future__ import absolute_import
from unittest import TestCase
from . import bbox_fitting
import numpy as np

class TestBbox_fitting(TestCase):
    def test_raise_warning_image(self):
        input_array = [
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 2, 1],
            [1, 1, 1, 3, 1],
            [0, 1, 1, 1, 0]]
        with self.assertRaises(TypeError):
            result = bbox_fitting(input_array, 1, 1, 3, 3)

    def test_raise_warning_float_cor(self):
        input_array = np.array([
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 2, 1],
            [1, 1, 1, 3, 1],
            [0, 1, 1, 1, 0]
        ])
        with self.assertRaises(ValueError):
            result = bbox_fitting(input_array, 1.1, 1, 3, 3)
        with self.assertRaises(ValueError):
            result = bbox_fitting(input_array, 1, 1.3, 3, 3)
        with self.assertRaises(ValueError):
            result = bbox_fitting(input_array, 1, 1, 3.9, 3)
        with self.assertRaises(ValueError):
            result = bbox_fitting(input_array, 1, 1, 3, 3.0)

    def test_crop_5x5_3x3(self):
        input_array = np.array([
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 2, 1],
            [1, 1, 1, 3, 1],
            [0, 1, 1, 1, 0]
        ])

        expected = np.array([
            [1, 1, 1],
            [1, 1, 2],
            [1, 1, 3],
        ])

        result = bbox_fitting(input_array, 1, 1, 4, 4)
        np.testing.assert_array_equal(expected, result)

    def test_crop_7x5_3x3(self):
        input_array = np.array([
            [0, 1, 0, 1, 0],
            [0, 1, 1, 1, 0],
            [1, 1, 4, 1, 1],
            [1, 1, 5, 1, 1],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0],
            [0, 1, 0, 1, 0]
        ])

        expected = np.array([
            [1, 4, 1],
            [1, 5, 1],
            [1, 1, 1],
        ])

        result = bbox_fitting(input_array, 1, 2, 4, 5)
        np.testing.assert_array_equal(expected, result)

    
    def test_padding_3x3_5x5(self):
        input_array = np.array([
            [5, 1, 1],
            [1, 1, 2],
            [1, 1, 3],
        ])
        
        expected = np.array([
            [0, 0, 0, 0, 0],
            [0, 5, 1, 1, 0],
            [0, 1, 1, 2, 0],
            [0, 1, 1, 3, 0],
            [0, 0, 0, 0, 0]
        ])

        result = bbox_fitting(input_array, -1, -1, 4, 4)
        np.testing.assert_array_equal(expected, result)

    def test_padding_3x3_5x7(self):
        input_array = np.array([
            [5, 1, 1],
            [1, 1, 2],
            [1, 1, 3],
        ])
        
        expected = np.array([
            [0, 0, 0, 0, 0],
            [0, 5, 1, 1, 0],
            [0, 1, 1, 2, 0],
            [0, 1, 1, 3, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ])

        result = bbox_fitting(input_array, -1, -1, 4, 6)
        np.testing.assert_array_equal(expected, result)

    def test_padding_and_cropping_3x3_3x4(self):
        input_array = np.array([
            [5, 1, 1],
            [1, 1, 2],
            [1, 1, 3],
        ])
        
        expected = np.array([
            [1, 1, 0],
            [1, 2, 0],
            [1, 3, 0],
            [0, 0, 0]
        ])

        result = bbox_fitting(input_array, 1, 0, 4, 4)
        np.testing.assert_array_equal(expected, result)

    def test_padding_and_cropping_3x3_3x4_color(self):
        input_array = np.array([
            [[5, 4, 3], [1, 9, 2], [1, 8, 2]],
            [[1, 2, 2],[1, 1, 2], [1, 7, 2]],
            [[1, 4, 2], [1, 5, 2], [1, 6, 2]],
        ])
        
        expected = np.array([
            [[1, 9, 2], [1, 8, 2], [0, 0, 0]],
            [[1, 1, 2], [1, 7, 2], [0, 0, 0]],
            [[1, 5, 2], [1, 6, 2], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        ])

        result = bbox_fitting(input_array, 1, 0, 4, 4)
        np.testing.assert_array_equal(expected, result)
    
    def test_underflow_left(self):
        input_array = np.array([
            [5, 1, 1],
            [1, 1, 2],
            [1, 1, 3],
        ])
        
        expected = np.array([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ])

        result = bbox_fitting(input_array, -5, 1, -1, 6)
        np.testing.assert_array_equal(expected, result)
    
    def test_overflow_right(self):
        input_array = np.array([
            [5, 1, 1],
            [1, 1, 2],
            [1, 1, 3],
        ])
        
        expected = np.array([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ])

        result = bbox_fitting(input_array, 3, 1, 7, 6)
        np.testing.assert_array_equal(expected, result)
    def test_overflow_down(self):
        input_array = np.array([
            [5, 1, 1],
            [1, 1, 2],
            [1, 1, 3],
        ])
        
        expected = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])

        result = bbox_fitting(input_array, 1, 9, 4, 13)
        np.testing.assert_array_equal(expected, result)
    
    def test_underflow_up(self):
        input_array = np.array([
            [5, 1, 1],
            [1, 1, 2],
            [1, 1, 3],
        ])
        
        expected = np.array([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ])

        result = bbox_fitting(input_array, 1, -7, 5, -2)
        np.testing.assert_array_equal(expected, result)

    def test_padding_3x3_5x7_different_color(self):
        '''
        Don't argure about how color is writen. It is color without, because I don't like u.
        '''
        input_array = np.array([
            [5, 1, 1],
            [1, 1, 2],
            [1, 1, 3],
        ])
        
        expected = np.array([
            [255, 255, 255, 255, 255],
            [255, 5, 1, 1, 255],
            [255, 1, 1, 2, 255],
            [255, 1, 1, 3, 255],
            [255, 255, 255, 255, 255],
            [255, 255, 255, 255, 255],
            [255, 255, 255, 255, 255],
        ])

        result = bbox_fitting(input_array, -1, -1, 4, 6, padding_value=255)
        np.testing.assert_array_equal(expected, result)