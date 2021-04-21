from __future__ import absolute_import
from unittest import TestCase
import numpy as np
from .main import absolute_difference


class TestIlluminationCorretionAlgorithm(TestCase):
    def test_grey_image(self):
        img = np.ones((1000, 1000)) * 128
        illum_img = absolute_difference(img)
        self.assertGreaterEqual(np.min(illum_img), 0)
        self.assertLessEqual(np.max(illum_img), 255)

    def test_white_image(self):
        img = np.ones((1000, 1000)) * 255
        illum_img = absolute_difference(img)
        self.assertGreaterEqual(np.min(illum_img), 0)
        self.assertLessEqual(np.max(illum_img), 255)

    def test_black_image(self):
        img = np.ones((1000, 1000)) * 0
        illum_img = absolute_difference(img)
        self.assertGreaterEqual(np.min(illum_img), 0)
        self.assertLessEqual(np.max(illum_img), 255)

    def test_illumination_black_white(self):
        # BLACK GREY WHITE TEST
        xx, yy = np.mgrid[:300, :300]
        dist = xx
        img = (dist >= 100) * 128 + (dist >= 200) * 128
        illum_img = absolute_difference(img, gauss_size=21)
        self.assertGreaterEqual(np.min(illum_img), 0)
        self.assertLessEqual(np.max(illum_img), 255)

    def test_illumination_3_shades_of_grey(self):
        print("\nSTART 3 SHADES OF GREY TEST")
        xx, yy = np.mgrid[:300, :300]
        dist = xx
        img = (dist >= 100) * 50 + (dist >= 200) * 50 + 50
        illum_img = absolute_difference(img, gauss_size=21)
        self.assertGreaterEqual(np.min(illum_img), 0)
        self.assertLessEqual(np.max(illum_img), 255)

    def test_fractal(self):
        np.random.seed(931224)
        img = np.random.randint(0, 255, (1000, 1000))
        img[0:400, 0:400] = np.zeros((400, 400))
        cent_img = img[400:600, 400:600]

        full_illum_img = absolute_difference(img, gauss_size=21, new_median=128)
        small_illum_img = absolute_difference(cent_img, gauss_size=21, new_median=128)

        np.testing.assert_array_equal(
            small_illum_img[50:150, 50:150], full_illum_img[450:550, 450:550]
        )

    def test_warning(self):
        # BLACK GREY WHITE TEST
        xx, yy = np.mgrid[:300, :300]
        dist = xx
        img = (dist >= 100) * 128 + (dist >= 200) * 128

        with self.assertWarns(SyntaxWarning):
            illum_img = absolute_difference(img, gauss_size=20)

        self.assertGreaterEqual(np.min(illum_img), 0)
        self.assertLessEqual(np.max(illum_img), 255)