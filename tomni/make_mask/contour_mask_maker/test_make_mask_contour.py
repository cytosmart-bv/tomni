from __future__ import absolute_import
from unittest import TestCase
from .main import make_mask_contour
import numpy as np

class TestCircle_mask_selector(TestCase):    
    def test_happy_flow_open_points(self):
        contour = [[2, 3], [5, 3], [5, 5], [2, 5]]

        expected_img = np.array([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 1., 1., 1., 1., 0., 0., 0., 0.],
                                [0., 0., 1., 1., 1., 1., 0., 0., 0., 0.],
                                [0., 0., 1., 1., 1., 1., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]]).astype(np.uint8)

        result = make_mask_contour((10, 8), contour)

        np.testing.assert_array_equal(result, expected_img)
    
    def test_happy_flow_two_points(self):
        contour = [[2, 3], [5, 3]]

        expected_img = np.array([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 1., 1., 1., 1., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]]).astype(np.uint8)

        result = make_mask_contour((10, 8), contour)
        print(result)
        print(expected_img)
        np.testing.assert_array_equal(result, expected_img)
    
    def test_happy_flow_single_points(self):
        contour = [[2, 3]]

        expected_img = np.array([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 1., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]]).astype(np.uint8)

        result = make_mask_contour((10, 8), contour)
        print(result)
        print(expected_img)
        np.testing.assert_array_equal(result, expected_img)
    
    def test_happy_flow_closed_points(self):
        contour = [[2, 3], [5, 3], [5, 5], [2, 5], [2, 3]]

        expected_img = np.array([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 1., 1., 1., 1., 0., 0., 0., 0.],
                                [0., 0., 1., 1., 1., 1., 0., 0., 0., 0.],
                                [0., 0., 1., 1., 1., 1., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]]).astype(np.uint8)

        result = make_mask_contour((10, 8), contour)

        np.testing.assert_array_equal(result, expected_img)

    def test_hourglass_open_points(self):
        contour = [[1, 1], [7, 7], [7, 1], [1, 7]]

        expected_img = np.array([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 1., 0., 0., 0., 0., 0., 1., 0., 0.],
                                [0., 1., 1., 0., 0., 0., 1., 1., 0., 0.],
                                [0., 1., 1., 1., 0., 1., 1., 1., 0., 0.],
                                [0., 1., 1., 1., 1., 1., 1., 1., 0., 0.],
                                [0., 1., 1., 1., 0., 1., 1., 1., 0., 0.],
                                [0., 1., 1., 0., 0., 0., 1., 1., 0., 0.],
                                [0., 1., 0., 0., 0., 0., 0., 1., 0., 0.]]).astype(np.uint8)

        result = make_mask_contour((10, 8), contour)

        np.testing.assert_array_equal(result, expected_img)

    def test_diagnol_interpolation_points(self):
        contour = [[1, 1], [7, 3], [7, 5], [1, 5]]

        expected_img = np.array([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 1., 1., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 1., 1., 1., 1., 1., 0., 0., 0., 0.],
                                [0., 1., 1., 1., 1., 1., 1., 1., 0., 0.],
                                [0., 1., 1., 1., 1., 1., 1., 1., 0., 0.],
                                [0., 1., 1., 1., 1., 1., 1., 1., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]]).astype(np.uint8)

        result = make_mask_contour((10, 8), contour)

        np.testing.assert_array_equal(result, expected_img)

    def test_error_wrong_format(self):
        contour = [[2, 5, 5, 2, 2],
                   [3, 3, 5, 5, 3]]
        self.assertRaises(TypeError, make_mask_contour, (10, 8), contour)

    def test_error_to_big_shape(self):
        contour = [[[1, 1], [7, 3], [7, 5], [1, 5]]]
        self.assertRaises(TypeError, make_mask_contour, (10, 8), contour)

    def test_error_to_small_shape(self):
        contour = [1, 5]
        self.assertRaises(TypeError, make_mask_contour, (10, 8), contour)