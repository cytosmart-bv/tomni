from __future__ import absolute_import
from unittest import TestCase
from . import make_mask_ellipse
from ..circlair_mask.main import make_mask_circle
import numpy as np
from numpy.testing import assert_array_equal
import cv2

class TestMakeMaskEllipse(TestCase):
    def test_MMESmall_small_radii(self):
        size = (8, 4)
        x = 3
        y = 1
        r1 = 0
        r2 = -1

        self.assertRaises(ValueError, make_mask_ellipse, size, x, y, r1, r2)

    def test_5x5_5(self):
        size = (5, 5)
        x = 2
        y = 2
        r1 = 2
        r2 = 2

        expected = np.array([
            [0, 0, 1, 0, 0],
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0],
            [0, 0, 1, 0, 0]
        ])

        result = make_mask_ellipse(size, x, y, r1, r2)
        np.testing.assert_array_equal(result, expected)

    def test_5x5_5_float_radius(self):
        size = (5, 5)
        x = 2
        y = 2
        r1 = 2.
        r2 = 2.

        expected = np.array([
            [0, 0, 1, 0, 0],
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0],
            [0, 0, 1, 0, 0]
        ])

        result = make_mask_ellipse(size, x, y, r1, r2)
        np.testing.assert_array_equal(result, expected)

    def test_5x5_5_all_float(self):
        size = (5, 5)
        x = 2.
        y = 2.
        r1 = 2.
        r2 = 2.

        expected = np.array([
            [0, 0, 1, 0, 0],
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0],
            [0, 0, 1, 0, 0]
        ])

        result = make_mask_ellipse(size, x, y, r1, r2)
        np.testing.assert_array_equal(result, expected)

    def test_5x5_1(self):
        size = (5, 5)
        x = 2
        y = 2
        r1 = 1
        r2 = 1

        expected = np.array([
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0]
        ])

        result = make_mask_ellipse(size, x, y, r1, r2)
        np.testing.assert_array_equal(result, expected)

    def test_MMESmall_even_radii_length(self):
        size = (13, 11)
        x = 6
        y = 4
        r1 = 6
        r2 = 4

        expected = np.array([
            [0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 1., 1., 1., 1., 1., 1., 1., 0., 0., 0.],
            [0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0.],
            [0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0.],
            [1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
            [0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0.],
            [0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0.],
            [0., 0., 0., 1., 1., 1., 1., 1., 1., 1., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]])

        mask = make_mask_ellipse(size, x, y, r1, r2)
        assert_array_equal(mask, expected)

    def test_MMESmall_odd_radii_length(self):
        size = (13, 11)
        x = 6
        y = 4
        r1 = 5
        r2 = 3

        expected = np.array([
            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 1., 1., 1., 1., 1., 1., 1., 0., 0., 0.],
            [0., 0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0., 0.],
            [0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0.],
            [0., 0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0., 0.],
            [0., 0., 0., 1., 1., 1., 1., 1., 1., 1., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]])

        mask = make_mask_ellipse(size, x, y, r1, r2)
        assert_array_equal(mask, expected)

    def test_MMESmall_combined(self):
        size = (16, 17)
        x = 9
        y = 9
        rx = 3
        ry = 6

        expected = np.array([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 0., 0., 1., 1., 1., 0., 0., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 0., 1., 1., 1., 1., 1., 0., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 0., 1., 1., 1., 1., 1., 0., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 0., 1., 1., 1., 1., 1., 0., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 0., 1., 1., 1., 1., 1., 0., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 1., 1., 1., 1., 1., 1., 1., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 0., 1., 1., 1., 1., 1., 0., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 0., 1., 1., 1., 1., 1., 0., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 0., 1., 1., 1., 1., 1., 0., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 0., 1., 1., 1., 1., 1., 0., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 0., 0., 1., 1., 1., 0., 0., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]])

        mask = make_mask_ellipse(size, x, y, rx, ry)
        assert_array_equal(expected, mask)

    def test_mask_ellipse_no_rotation_16X16(self):
        expected = np.array([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 1., 1., 1., 1., 1., 1., 1., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0., 0.],
                             [0., 0., 0., 0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0.],
                             [0., 0., 0., 0., 0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 1., 1., 1., 1., 1., 1., 1., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                             [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]])

        size = (16, 16)
        x = 9
        y = 9
        r1 = 5
        r2 = 3
        mask = make_mask_ellipse(size, x, y, r1, r2)
        assert_array_equal(mask, expected)

    def test_make_mask_small_radii(self):
        expected_array = np.array([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                   [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                   [0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0.],
                                   [0., 0., 0., 1., 1., 1., 1., 1., 1., 1., 0., 0., 0., 0., 0.],
                                   [0., 0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0., 0., 0., 0.],
                                   [0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0., 0., 0.],
                                   [0., 0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0., 0., 0., 0.],
                                   [0., 0., 0., 1., 1., 1., 1., 1., 1., 1., 0., 0., 0., 0., 0.],
                                   [0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0.],
                                   [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                   [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                   [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                   [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                   [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                   [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                   ])
        size = (15, 15)
        x = 6
        y = 5
        r1 = 5
        r2 = 3

        mask = make_mask_ellipse(size, x, y, r1, r2)
        assert_array_equal(expected_array, mask)

    def test_15x15_5(self):
        expected = np.array([
            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 1., 1., 1., 1., 1., 1., 1., 0., 0., 0., 0., 0.],
            [0., 0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0., 0., 0., 0.],
            [0., 0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0., 0., 0., 0.],
            [0., 0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0., 0., 0., 0.],
            [0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0., 0., 0.],
            [0., 0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0., 0., 0., 0.],
            [0., 0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0., 0., 0., 0.],
            [0., 0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0., 0., 0., 0.],
            [0., 0., 0., 1., 1., 1., 1., 1., 1., 1., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]])

        size = (15, 15)
        x = 6
        y = 6
        r1 = 5
        r2 = 5

        mask = make_mask_ellipse(size, x, y, r1, r2)
        assert_array_equal(mask, expected)

    def test_compare_circle_with_ellipse(self):
        size = (101, 101)
        x = 50
        y = 50
        r1 = 25
        r2 = 25

        mask_ell = make_mask_ellipse(size, x, y, r1, r2)
        mask_cir = make_mask_circle(size, r1*2)
        assert_array_equal(mask_cir, mask_ell)

    def test_MMEBig_expected(self):
        size = (700, 700)
        x = 300
        y = 300
        rx = 250
        ry = 150

        mask = make_mask_ellipse(size, x, y, rx, ry)

        # X minimum
        self.assertEqual(False, mask[300][48])
        self.assertEqual(True, mask[300][52])

        # X Maximum
        self.assertEqual(True, mask[300][548])
        self.assertEqual(False, mask[300][552])
        
        # Y minimum
        self.assertEqual(False, mask[148][300])
        self.assertEqual(True, mask[152][300])

        # Y maximum
        self.assertEqual(True, mask[448][300])
        self.assertEqual(False, mask[452][300])



    def test_MMEBig_expected_odd_size(self):
        size = (10000, 10001)
        x = 5000
        y = 2467
        rx = 3200
        ry = 1692

        mask = make_mask_ellipse(size, x, y, rx, ry)
        self.assertEqual(True, mask[2467][5000])
        self.assertEqual(True, mask[3000][5000])

        # X minimum
        self.assertEqual(False, mask[2467][1798])
        self.assertEqual(True, mask[2467][1801])

        # X Maximum
        self.assertEqual(True, mask[2467][8198])
        self.assertEqual(False, mask[2467][8201])
        
        # Y minimum
        self.assertEqual(False, mask[773][5000])
        self.assertEqual(True, mask[777][5000])

        # Y maximum
        self.assertEqual(True, mask[4157][5000])
        self.assertEqual(False, mask[4161][5000])

    def test_MMEBig_expected_odd_size_floats(self):
        size = (10000, 10001)
        x = 5000.
        y = 2467.
        rx = 3200.
        ry = 1692.

        mask = make_mask_ellipse(size, x, y, rx, ry)
        self.assertEqual(True, mask[2467][5000])
        self.assertEqual(True, mask[3000][5000])

        # X minimum
        self.assertEqual(False, mask[2467][1798])
        self.assertEqual(True, mask[2467][1801])

        # X Maximum
        self.assertEqual(True, mask[2467][8198])
        self.assertEqual(False, mask[2467][8201])
        
        # Y minimum
        self.assertEqual(False, mask[773][5000])
        self.assertEqual(True, mask[777][5000])

        # Y maximum
        self.assertEqual(True, mask[4157][5000])
        self.assertEqual(False, mask[4161][5000])

    def test_500x500_bufferoverflow(self):
        size = (500, 500)
        x = 100
        y = 100
        r1 = 25
        r2 = 25

        expected = np.zeros(size)
        expected[75:126, 75:126] = make_mask_ellipse((51, 51), 25, 25, r1, r2)

        result = make_mask_ellipse(size, x, y, r1, r2)
        np.testing.assert_array_equal(result, expected)

    def test_1000x1000_bufferoverflow(self):
        image_size = (1000, 1000)
        x1 = 800
        y1 = 800
        rx = 99
        ry = 99

        expected = np.zeros(image_size)
        expected[701:900, 701:900] = make_mask_ellipse((199, 199), 99, 99, rx, ry)

        result = make_mask_ellipse(image_size, x1, y1, rx, ry)
        np.testing.assert_array_equal(result, expected)

        # Check the corners
        self.assertEqual(False, result[899][899])
        self.assertEqual(False, result[899][701])
        self.assertEqual(False, result[701][899])
        self.assertEqual(False, result[701][701])
