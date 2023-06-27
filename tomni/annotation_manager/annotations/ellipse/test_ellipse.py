from unittest import TestCase

import cv2
import numpy as np

from tomni.annotation_manager import Ellipse, Point, Polygon
from tomni.annotation_manager.main import AnnotationManager


class TestEllipse(TestCase):
    def setUp(self) -> None:
        id_ = "1234-1234-2134-1321"
        children = []
        parents = []
        label = "ellipse_test"

        self.zero_ellipse = Ellipse(radius_x=0, radius_y=0, center=Point(0, 0), rotation=0, id=id_, children=children, parents=parents, label=label)
        self.circle = Ellipse(radius_x=1, radius_y=1, center=Point(0, 0), rotation=0, id=id_, children=children, parents=parents, label=label)
        self.oval = Ellipse(radius_x=1, radius_y=3, center=Point(0, 0), rotation=0, id=id_, children=children, parents=parents, label=label)

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

    def test_zero_ellipse_to_dict(self):
        expected = {
            "area": 0.0,
            "aspect_ratio": 1.0,
            "center": {"x": 0, "y": 0},
            "children": [],
            "circularity": np.nan,
            "id": "1234-1234-2134-1321",
            "label": "ellipse_test",
            "parents": [],
            "perimeter": 0.0,
            "radiusX": 0.0,
            "radiusY": 0.0,
            "angleOfRotation": 0,
            "type": "ellipse",
        }
        actual = self.zero_ellipse.to_dict()

        # Have to use np testing because of verifying nan values.
        np.testing.assert_equal(expected, actual)

    def test_circle_to_dict(self):
        expected = {
            "area": 3.14,
            "aspect_ratio": 1.0,
            "center": {"x": 0, "y": 0},
            "children": [],
            "circularity": 1.0,
            "id": "1234-1234-2134-1321",
            "label": "ellipse_test",
            "parents": [],
            "perimeter": 6.28,
            "radiusX": 1,
            "radiusY": 1,
            "angleOfRotation": 0,
            "type": "ellipse",
        }
        actual = self.circle.to_dict()
        self.assertDictEqual(expected, actual)

    def test_oval_to_dict(self):
        expected = {
            "area": 9.42,
            "aspect_ratio": 0.33,
            "center": {"x": 0, "y": 0},
            "children": [],
            "circularity": 0.6,
            "id": "1234-1234-2134-1321",
            "label": "ellipse_test",
            "parents": [],
            "perimeter": 14.05,
            "radiusX": 1,
            "radiusY": 3,
            "angleOfRotation": 0,
            "type": "ellipse",
        }
        actual = self.oval.to_dict()

        self.assertDictEqual(expected, actual)

    def test_to_dict_with_ellipse_mask(self):
        size = 2072
        quadrant = int(size / 4)
        center = int(size / 2)
        rad = int(size / 3)

        mask_json = AnnotationManager(
            [Ellipse(center=Point(center, center), radius_x=rad, rotation=0, id="", label="", children=[], parents=[])]
        ).to_dict()[0]
        ellipse1 = Ellipse(radius_x=quadrant, center=Point(center, center), rotation=0, id="", label="", children=[], parents=[])
        ellipse2 = Ellipse(radius_x=quadrant - 100, center=Point(center + 100, center - 100), rotation=0, id="", label="", children=[], parents=[])
        ellipse3 = Ellipse(radius_x=quadrant - 150, center=Point(center - 100, center + 150), rotation=0, id="", label="", children=[], parents=[])

        ellipses_inside = [ellipse1, ellipse2, ellipse3]
        ellipses_outside = [self.circle, self.oval]

        for ellipse in ellipses_inside:
            self.assertTrue(ellipse.is_in_mask(mask_json=mask_json, min_overlap=0.9))

        for ellipse in ellipses_outside:
            self.assertFalse(ellipse.is_in_mask(mask_json=mask_json, min_overlap=0.9))

    def test_to_dict_with_polygon_mask(self):
        center = int(2072 / 2)
        size = 2072
        quadrant = int(size / 4)
        points = [Point(quadrant, quadrant), Point(quadrant, quadrant * 3), Point(quadrant * 3, quadrant * 3), Point(quadrant * 3, quadrant)]
        mask = AnnotationManager([Polygon(points=points, id="", label="", children=[], parents=[])]).to_dict()[0]

        ellipse1 = Ellipse(radius_x=quadrant, center=Point(center, center), rotation=0, id="", label="", children=[], parents=[])
        ellipse2 = Ellipse(radius_x=quadrant - 100, center=Point(center + 100, center - 100), rotation=0, id="", label="", children=[], parents=[])
        ellipse3 = Ellipse(radius_x=quadrant - 150, center=Point(center - 100, center + 150), rotation=0, id="", label="", children=[], parents=[])

        ellipses_inside = [ellipse1, ellipse2, ellipse3]
        ellipses_outside = [self.circle, self.oval]

        for ellipse in ellipses_inside:
            self.assertTrue(ellipse.is_in_mask(mask, 0.9))

        for ellipse in ellipses_outside:
            self.assertFalse(ellipse.is_in_mask(mask, 0.9))
