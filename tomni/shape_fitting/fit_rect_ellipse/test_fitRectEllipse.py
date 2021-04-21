from __future__ import absolute_import
from unittest import TestCase
from .main import fit_rect_around_ellipse
import numpy as np

class Testfit_rect_around_ellipse(TestCase):
    def test_fit_circle(self):
        x = 0
        y = 100
        r1 = 900
        r2 = 900
        alpha = 0

        expectedX1 = -900
        expectedY1 = -800
        expectedX2 = 900
        expectedY2 = 1000

        x1, y1, x2, y2 = fit_rect_around_ellipse(x, y, r1, r2, alpha)

        self.assertEqual(x1, expectedX1)
        self.assertEqual(y1, expectedY1)
        self.assertEqual(x2, expectedX2)
        self.assertEqual(y2, expectedY2)

    def test_fit_ellipse_no_rotation(self):
        x = 0
        y = 100
        r1 = 900
        r2 = 500
        alpha = 0

        expectedX1 = -900
        expectedY1 = -400
        expectedX2 = 900
        expectedY2 = 600

        x1, y1, x2, y2 = fit_rect_around_ellipse(x, y, r1, r2, alpha)

        self.assertEqual(x1, expectedX1)
        self.assertEqual(y1, expectedY1)
        self.assertEqual(x2, expectedX2)
        self.assertEqual(y2, expectedY2)


    def test_fit_ellipse_with_rotation(self):
        '''
        These number where measured using InkScape 
        '''
        x = 108
        y = 185
        r1 = 79
        r2 = 50
        alpha = 30

        expectedX1 = 35
        expectedY1 = 126
        expectedX2 = 181
        expectedY2 = 244

        x1, y1, x2, y2 = fit_rect_around_ellipse(x, y, r1, r2, alpha)

        print(x1, y1, x2, y2)
        print("width {} expected width {}".format(x2 - x1, expectedX2 - expectedX1))
        print("height {} expected height {}".format(y2 - y1, expectedY2 - expectedY1))
        self.assertAlmostEqual(x1, expectedX1, 0)
        self.assertAlmostEqual(y1, expectedY1, 0)
        self.assertAlmostEqual(x2, expectedX2, 0)
        self.assertAlmostEqual(y2, expectedY2, 0)