from __future__ import absolute_import
from unittest import TestCase
from . import bbox_fitting_center
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
            bbox_fitting_center(input_array, [3, 3])

    def test_raise_warning_float_cor(self):
        input_array = np.array([
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 2, 1],
            [1, 1, 1, 3, 1],
            [0, 1, 1, 1, 0]
        ])
        with self.assertRaises(ValueError):
            bbox_fitting_center(input_array, [3.9, 3])
        with self.assertRaises(ValueError):
            bbox_fitting_center(input_array, [3, 3.0])

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

        result = bbox_fitting_center(input_array, (3, 3))
        np.testing.assert_array_equal(expected, result)

    def test_crop_5x5_5x3(self):
        input_array = np.array([
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 2, 1],
            [1, 1, 1, 3, 1],
            [0, 1, 1, 1, 0]
        ])

        expected = np.array([
            [1, 1, 1, 1, 1],
            [1, 1, 1, 2, 1],
            [1, 1, 1, 3, 1],
        ])

        result = bbox_fitting_center(input_array, (5, 3))
        np.testing.assert_array_equal(expected, result)

    def test_padding_and_cropping_5x5_7x3(self):
        input_array = np.array([
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 2, 1],
            [1, 1, 1, 3, 1],
            [0, 1, 1, 1, 0]
        ])

        expected = np.array([
            [0, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 2, 1, 0],
            [0, 1, 1, 1, 3, 1, 0],
        ])

        result = bbox_fitting_center(input_array, (7, 3))
        np.testing.assert_array_equal(expected, result)

    def test_padding_and_cropping_5x5_6x3(self):
        input_array = np.array([
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 2, 1],
            [1, 1, 1, 3, 1],
            [0, 1, 1, 1, 0]
        ])

        expected = np.array([
            [1, 1, 1, 1, 1, 0],
            [1, 1, 1, 2, 1, 0],
            [1, 1, 1, 3, 1, 0],
        ])

        result = bbox_fitting_center(input_array, (6, 3))
        np.testing.assert_array_equal(expected, result)

    def test_padding_and_cropping_4x4_6x3(self):
        input_array = np.array([
            [0, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 2],
            [1, 1, 1, 3],
        ])

        expected = np.array([
            [0, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 2, 0],
            [0, 1, 1, 1, 3, 0],
        ])

        result = bbox_fitting_center(input_array, (6, 3))
        np.testing.assert_array_equal(expected, result)