from __future__ import absolute_import
from unittest import TestCase
import numpy as np
from .main import fluo_tophat


class TestIlluminationCorretionAlgorithm(TestCase):
    def test_grey_image(self):
        img = np.ones((1000, 1000)) * 128
        illum_img, _, _ = fluo_tophat(img)
        self.assertEqual(np.min(illum_img), 0)

    def test_white_image(self):
        img = np.ones((1000, 1000)) * 255
        illum_img, _, _ = fluo_tophat(img)
        self.assertEqual(np.min(illum_img), 0)

    def test_black_image(self):
        img = np.ones((1000, 1000)) * 0
        illum_img, _, _ = fluo_tophat(img)
        self.assertEqual(np.min(illum_img), 0)

    def test_random_image(self):
        img = np.random.randint(0, 255, (1000, 1000))
        img[0:400, 0:400] = np.zeros((400, 400))
        illum_img, _, _ = fluo_tophat(img)
        self.assertGreaterEqual(np.min(illum_img), 0)
        self.assertLessEqual(np.max(illum_img), 255)



