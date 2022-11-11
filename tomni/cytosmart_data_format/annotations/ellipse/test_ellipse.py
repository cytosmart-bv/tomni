from unittest import TestCase

import numpy as np

from tomni.cytosmart_data_format import Ellipse, Point


class TestEllipse(TestCase):
    def setUp(self) -> None:
        id_ = "1234-1234-2134-1321"
        children = []
        parents = []
        label = "ellipse_test"

        # self.zero_ellipse = Ellipse(
        #     radius=Point(0, 0),
        #     center=Point(0, 0),
        #     rotation=0,
        #     # id=id,
        #     # children=children,
        #     # parents=parents,
        #     # label=label,
        # )
        # self.circle = Ellipse(
        #     radius=Point(1, 1),
        #     center=Point(0, 0),
        #     rotation=0,
        #     # id=id,
        #     # children=children,
        #     # parents=parents,
        #     # label=label,
        # )
        self.oval = Ellipse(
            radius=Point(1, 3),
            center=Point(0, 0),
            rotation=0,
            id_=id_,
            children=children,
            parents=parents,
            label=label,
        )

    def test_zero_area(self):
        expected = 0.0
        actual = self.zero_ellipse.area

        self.assertEqual(expected, actual)

    def test_circle_area(self):
        expected = np.pi
        actual = self.circle.area

        self.assertAlmostEqual(expected, actual)

    def test_oval_area(self):
        expected = 9.42477796076938
        actual = self.oval.area

        self.assertEqual(expected, actual)

    def test_zero_circularity(self):
        self.assertTrue(np.isnan(self.zero_ellipse.circularity))

    def test_circle_circularity(self):
        expected = 1.0
        actual = self.circle.circularity

        self.assertEqual(expected, actual)

    def test_oval_circularity(self):
        expected = 0.5999999999999999
        actual = self.oval.circularity

        self.assertEqual(expected, actual)

    def test_zero_aspect_ratio(self):
        expected = 1.0
        actual = self.zero_ellipse.aspect_ratio

        self.assertEqual(expected, actual)

    def test_circle_aspect_ratio(self):
        expected = 1.0
        actual = self.circle.aspect_ratio

        self.assertEqual(expected, actual)

    def test_oval_aspect_ratio(self):
        expected = 0.3333333333333333
        actual = self.oval.aspect_ratio

        self.assertEqual(expected, actual)

    def test_zero_perimeter(self):
        expected = 0.0
        actual = self.zero_ellipse.perimeter

        self.assertEqual(expected, actual)

    def test_circle_perimeter(self):
        expected = 6.283185307179586
        actual = self.circle.perimeter

        self.assertEqual(expected, actual)

    def test_oval_perimeter(self):
        expected = 14.049629462081453
        actual = self.oval.perimeter
        self.assertEqual(expected, actual)

    def test_oval_to_dict(self):

        expected = {}
        actual = self.oval.to_dict()

        self.assertDictEqual(expected, actual)
