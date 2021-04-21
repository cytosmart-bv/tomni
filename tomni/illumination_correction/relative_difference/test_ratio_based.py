from __future__ import absolute_import
from unittest import TestCase
import numpy as np
from .main import relative_difference


class TestIlluminationCorretionRatioBased(TestCase):
    def test_grey_image(self):
        img = np.ones((1000, 1000)) * 128
        illum_img = relative_difference(img)
        self.assertGreaterEqual(np.min(illum_img), 0)
        self.assertLessEqual(np.max(illum_img), 255)

    def test_white_image(self):
        img = np.ones((1000, 1000)) * 255
        illum_img = relative_difference(img)
        self.assertGreaterEqual(np.min(illum_img), 0)
        self.assertLessEqual(np.max(illum_img), 255)

    def test_black_image(self):
        img = np.ones((1000, 1000)) * 0
        illum_img = relative_difference(img)
        self.assertGreaterEqual(np.min(illum_img), 0)
        self.assertLessEqual(np.max(illum_img), 255)


    def test_illumination_black_white(self):
        # BLACK GREY WHITE TEST
        xx, yy = np.mgrid[:300, :300]
        dist = xx
        img = (dist >= 100) * 128 + (dist >= 200) * 128
        illum_img = relative_difference(img, gauss_size=21)
        self.assertGreaterEqual(np.min(illum_img), 0)
        self.assertLessEqual(np.max(illum_img), 255)

    def test_illumination_3_shades_of_grey(self):
        print("\nSTART 3 SHADES OF GREY TEST")
        xx, yy = np.mgrid[:300, :300]
        dist = xx
        img = (dist >= 100) * 50 + (dist >= 200) * 50 + 50
        illum_img = relative_difference(img, gauss_size=21)
        self.assertGreaterEqual(np.min(illum_img), 0)
        self.assertLessEqual(np.max(illum_img), 255)

    def test_grey_image_adj(self):
        img = np.ones((1000, 1000)) * 128
        illum_img = relative_difference(img, smooth_size=3, do_normalize=True, resize_ratio=0.125)
        self.assertGreaterEqual(np.min(illum_img), 0)
        self.assertLessEqual(np.max(illum_img), 255)

    def test_white_image_adj(self):
        img = np.ones((1000, 1000)) * 255
        illum_img = relative_difference(img, smooth_size=3, do_normalize=True, resize_ratio=0.125)
        self.assertGreaterEqual(np.min(illum_img), 0)
        self.assertLessEqual(np.max(illum_img), 255)

    def test_black_image_adj(self):
        img = np.ones((1000, 1000)) * 0
        illum_img = relative_difference(img,smooth_size=3, do_normalize=True, resize_ratio=0.125)
        self.assertGreaterEqual(np.min(illum_img), 0)
        self.assertLessEqual(np.max(illum_img), 255)


    def test_illumination_black_white_adj(self):
        # BLACK GREY WHITE TEST
        xx, yy = np.mgrid[:300, :300]
        dist = xx
        img = (dist >= 100) * 128 + (dist >= 200) * 128
        illum_img = relative_difference(img, gauss_size=21, smooth_size=3, do_normalize=True, resize_ratio=0.125)
        self.assertGreaterEqual(np.min(illum_img), 0)
        self.assertLessEqual(np.max(illum_img), 255)

    def test_illumination_3_shades_of_grey_adj(self):
        print("\nSTART 3 SHADES OF GREY TEST")
        xx, yy = np.mgrid[:300, :300]
        dist = xx
        img = (dist >= 100) * 50 + (dist >= 200) * 50 + 50
        illum_img = relative_difference(img, gauss_size=21, smooth_size=3, do_normalize=True, resize_ratio=0.125)
        self.assertGreaterEqual(np.min(illum_img), 0)
        self.assertLessEqual(np.max(illum_img), 255)

