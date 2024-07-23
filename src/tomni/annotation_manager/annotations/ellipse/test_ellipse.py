from unittest import TestCase

import cv2
import numpy as np

from tomni.annotation_manager import Ellipse, Point, Polygon
from tomni.annotation_manager.main import AnnotationManager


def assertAlmostEqualDictEqual(testcase, expected, actual, percentage_tolerance):
    testcase.assertIsInstance(expected, dict)
    testcase.assertIsInstance(actual, dict)

    testcase.assertSetEqual(set(expected.keys()), set(actual.keys()))

    for key in expected:
        if isinstance(expected[key], dict) and isinstance(actual[key], dict):
            assertAlmostEqualDictEqual(
                testcase, expected[key], actual[key], percentage_tolerance
            )
        elif isinstance(expected[key], (int, float)) and isinstance(
            actual[key], (int, float)
        ):
            if expected[key] == 0:
                testcase.assertAlmostEqual(expected[key], actual[key], places=0)
            else:
                percentage_diff = (
                    abs((expected[key] - actual[key]) / expected[key]) * 100
                )
                testcase.assertLessEqual(
                    percentage_diff,
                    percentage_tolerance,
                    msg=f"Percentage difference for {key}: {percentage_diff:.2f}%",
                )
        else:
            testcase.assertEqual(expected[key], actual[key])


class TestEllipse(TestCase):
    def setUp(self) -> None:
        id_ = "1234-1234-2134-1321"
        children = []
        parents = []
        label = "ellipse_test"

        self.zero_ellipse = Ellipse(
            radius_x=0,
            radius_y=0,
            center=Point(0, 0),
            rotation=0,
            id=id_,
            children=children,
            parents=parents,
            label=label,
        )
        self.circle = Ellipse(
            radius_x=1,
            radius_y=1,
            center=Point(0, 0),
            rotation=0,
            id=id_,
            children=children,
            parents=parents,
            label=label,
        )
        self.oval = Ellipse(
            radius_x=1,
            radius_y=3,
            center=Point(0, 0),
            rotation=0,
            id=id_,
            children=children,
            parents=parents,
            label=label,
        )
        # self.circle_features = Ellipse(radius_x=1, radius_y=1, center=Point(0, 0), rotation=0, id=id_, children=children, parents=parents, label=label, features=["area", "minor_axis", "perimeter"])

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

    def test_zero_average_diameter(self):
        expected = 0
        actual = self.zero_ellipse.average_diameter
        self.assertEqual(expected, actual)

    def test_circle_average_diameter(self):
        expected = 2
        actual = self.circle.average_diameter
        self.assertEqual(expected, actual)

    def test_oval_average_diameter(self):
        expected = 4
        actual = self.oval.average_diameter
        self.assertEqual(expected, actual)

    def test_zero_minor_axis(self):
        expected = 0
        actual = self.zero_ellipse.minor_axis
        self.assertEqual(expected, actual)

    def test_circle_minor_axis(self):
        expected = 2
        actual = self.circle.minor_axis
        self.assertEqual(expected, actual)

    def test_oval_minor_axis(self):
        expected = 2
        actual = self.oval.minor_axis
        self.assertEqual(expected, actual)

    def test_zero_major_axis(self):
        expected = 0
        actual = self.zero_ellipse.major_axis
        self.assertEqual(expected, actual)

    def test_circle_major_axis(self):
        expected = 2
        actual = self.circle.major_axis
        self.assertEqual(expected, actual)

    def test_oval_major_axis(self):
        expected = 6
        actual = self.oval.major_axis
        self.assertEqual(expected, actual)

    def test_zero_convex_hull_area(self):
        expected = 0.0
        actual = self.zero_ellipse.convex_hull_area
        self.assertEqual(expected, actual)

    def test_circle_convex_hull_area(self):
        expected = np.pi
        actual = self.circle.convex_hull_area
        self.assertEqual(expected, actual)

    def test_oval_convex_hull_area(self):
        expected = 9.42477796076938
        actual = self.oval.convex_hull_area
        self.assertEqual(expected, actual)

    def test_circle_roundness(self):
        expected = 1
        actual = self.circle.roundness
        self.assertEqual(expected, actual)

    def test_oval_roundness(self):
        expected = 1 / 3
        actual = self.oval.roundness
        self.assertEqual(expected, actual)

    def test_zero_ellipse_roundness(self):
        expected = 0
        actual = self.zero_ellipse.roundness
        self.assertEqual(expected, actual)

    def test_zero_ellipse_to_dict(self):
        expected = {
            "area": 0.0,
            "aspectRatio": 1.0,
            "averageDiameter": 0,
            "center": {"x": 0, "y": 0},
            "children": [],
            "circularity": np.nan,
            "convexHullArea": 0.0,
            "id": "1234-1234-2134-1321",
            "label": "ellipse_test",
            "majorAxis": 0,
            "minorAxis": 0,
            "parents": [],
            "perimeter": 0.0,
            "roundness": 0,
            "radiusX": 0.0,
            "radiusY": 0.0,
            "angleOfRotation": 0,
            "type": "ellipse",
            "accuracy": 1,
        }
        actual = self.zero_ellipse.to_dict()

        # Have to use np testing because of verifying nan values.
        np.testing.assert_equal(expected, actual)

    def test_circle_to_dict(self):
        expected = {
            "area": 3.14,
            "aspectRatio": 1.0,
            "averageDiameter": 2,
            "center": {"x": 0, "y": 0},
            "children": [],
            "circularity": 1.0,
            "convexHullArea": 3.14,
            "id": "1234-1234-2134-1321",
            "label": "ellipse_test",
            "majorAxis": 2,
            "minorAxis": 2,
            "parents": [],
            "perimeter": 6.28,
            "radiusX": 1,
            "radiusY": 1,
            "angleOfRotation": 0,
            "type": "ellipse",
            "accuracy": 1,
            "roundness": 1.0,
        }
        actual = self.circle.to_dict()
        self.assertDictEqual(expected, actual)

    def test_oval_to_dict(self):
        expected = {
            "area": 9.42,
            "aspectRatio": 0.33,
            "averageDiameter": 4,
            "center": {"x": 0, "y": 0},
            "children": [],
            "circularity": 0.6,
            "convexHullArea": 9.42,
            "id": "1234-1234-2134-1321",
            "label": "ellipse_test",
            "majorAxis": 6,
            "minorAxis": 2,
            "parents": [],
            "perimeter": 14.05,
            "radiusX": 1,
            "radiusY": 3,
            "angleOfRotation": 0,
            "type": "ellipse",
            "accuracy": 1,
            "roundness": 0.33,
        }
        actual = self.oval.to_dict()

        self.assertDictEqual(expected, actual)

    def test_oval_to_dict_accuracy_05(self):
        expected = {
            "area": 9.42,
            "aspectRatio": 0.33,
            "averageDiameter": 4,
            "center": {"x": 0, "y": 0},
            "children": [],
            "circularity": 0.6,
            "convexHullArea": 9.42,
            "id": "",
            "label": "",
            "majorAxis": 6,
            "minorAxis": 2,
            "parents": [],
            "perimeter": 14.05,
            "radiusX": 1,
            "radiusY": 3,
            "angleOfRotation": 0,
            "type": "ellipse",
            "accuracy": 0.5,
            "roundness": 0.33,
        }
        oval1 = Ellipse(
            radius_x=1,
            radius_y=3,
            center=Point(0, 0),
            rotation=0,
            id="",
            children=[],
            parents=[],
            label="",
            accuracy=0.5,
        )
        actual = oval1.to_dict()

        self.assertDictEqual(expected, actual)

    def test_oval_to_dict_accuracy_0(self):
        expected = {
            "area": 9.42,
            "aspectRatio": 0.33,
            "averageDiameter": 4,
            "center": {"x": 0, "y": 0},
            "children": [],
            "circularity": 0.6,
            "convexHullArea": 9.42,
            "id": "",
            "label": "",
            "majorAxis": 6,
            "minorAxis": 2,
            "parents": [],
            "perimeter": 14.05,
            "radiusX": 1,
            "radiusY": 3,
            "angleOfRotation": 0,
            "type": "ellipse",
            "accuracy": 0,
            "roundness": 0.33,
        }
        oval1 = Ellipse(
            radius_x=1,
            radius_y=3,
            center=Point(0, 0),
            rotation=0,
            id="",
            children=[],
            parents=[],
            label="",
            accuracy=0,
        )
        actual = oval1.to_dict()

        self.assertDictEqual(expected, actual)

    def test_to_dict_with_ellipse_mask(self):
        size = 2072
        quadrant = int(size / 4)
        center = int(size / 2)
        rad = int(size / 3)

        mask_json = AnnotationManager(
            [
                Ellipse(
                    center=Point(center, center),
                    radius_x=rad,
                    rotation=0,
                    id="",
                    label="",
                    children=[],
                    parents=[],
                )
            ]
        ).to_dict()
        ellipse1 = Ellipse(
            radius_x=quadrant,
            center=Point(center, center),
            rotation=0,
            id="",
            label="",
            children=[],
            parents=[],
        )
        ellipse2 = Ellipse(
            radius_x=quadrant - 100,
            center=Point(center + 100, center - 100),
            rotation=0,
            id="",
            label="",
            children=[],
            parents=[],
        )
        ellipse3 = Ellipse(
            radius_x=quadrant - 150,
            center=Point(center - 100, center + 150),
            rotation=0,
            id="",
            label="",
            children=[],
            parents=[],
        )

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
        points = [
            Point(quadrant, quadrant),
            Point(quadrant, quadrant * 3),
            Point(quadrant * 3, quadrant * 3),
            Point(quadrant * 3, quadrant),
            Point(quadrant * 3, quadrant + 1),
        ]
        mask = AnnotationManager(
            [Polygon(points=points, id="", label="", children=[], parents=[])]
        ).to_dict()

        ellipse1 = Ellipse(
            radius_x=quadrant,
            center=Point(center, center),
            rotation=0,
            id="",
            label="",
            children=[],
            parents=[],
        )
        ellipse2 = Ellipse(
            radius_x=quadrant - 100,
            center=Point(center + 100, center - 100),
            rotation=0,
            id="",
            label="",
            children=[],
            parents=[],
        )
        ellipse3 = Ellipse(
            radius_x=quadrant - 150,
            center=Point(center - 100, center + 150),
            rotation=0,
            id="",
            label="",
            children=[],
            parents=[],
        )

        ellipses_inside = [ellipse1, ellipse2, ellipse3]
        ellipses_outside = [self.circle, self.oval]

        for ellipse in ellipses_inside:
            self.assertTrue(ellipse.is_in_mask(mask, 0.9))

        for ellipse in ellipses_outside:
            self.assertFalse(ellipse.is_in_mask(mask, 0.9))

        oval_features = Ellipse(
            radius_x=1,
            radius_y=3,
            center=Point(0, 0),
            rotation=0,
            id="id",
            children=[],
            parents=[],
            label="label",
        )
        expected = {
            "area": 9.42,
            "averageDiameter": 4,
            "center": {"x": 0, "y": 0},
            "children": [],
            "circularity": 0.6,
            "id": "id",
            "label": "label",
            "minorAxis": 2,
            "parents": [],
            "radiusX": 1,
            "radiusY": 3,
            "angleOfRotation": 0,
            "type": "ellipse",
            "accuracy": 1,
        }

        actual = oval_features.to_dict(
            features=["area", "circularity", "minor_axis", "average_diameter"]
        )
        self.assertDictEqual(expected, actual)

    def test_feature_selection_empty(self):
        oval_features = Ellipse(
            radius_x=1,
            radius_y=3,
            center=Point(0, 0),
            rotation=0,
            id="id",
            children=[],
            parents=[],
            label="label",
        )
        expected = {
            "center": {"x": 0, "y": 0},
            "children": [],
            "id": "id",
            "label": "label",
            "parents": [],
            "radiusX": 1,
            "radiusY": 3,
            "angleOfRotation": 0,
            "type": "ellipse",
            "accuracy": 1,
        }

        actual = oval_features.to_dict(features=[])
        self.assertDictEqual(expected, actual)

    def test_feature_selection_None(self):
        oval_features = Ellipse(
            radius_x=1,
            radius_y=3,
            center=Point(0, 0),
            rotation=0,
            id="id",
            children=[],
            parents=[],
            label="label",
        )
        expected = {
            "area": 9.42,
            "aspectRatio": 0.33,
            "averageDiameter": 4,
            "center": {"x": 0, "y": 0},
            "children": [],
            "circularity": 0.6,
            "convexHullArea": 9.42,
            "id": "id",
            "label": "label",
            "majorAxis": 6,
            "minorAxis": 2,
            "parents": [],
            "perimeter": 14.05,
            "radiusX": 1,
            "radiusY": 3,
            "angleOfRotation": 0,
            "type": "ellipse",
            "accuracy": 1,
            "roundness": 0.33,
        }

        actual = oval_features.to_dict(features=None)
        self.assertDictEqual(expected, actual)

    def test_feature_multiplier(self):
        feature_multiplier = 742
        oval_features = Ellipse(
            radius_x=1,
            radius_y=3,
            center=Point(0, 0),
            rotation=0,
            id="id",
            children=[],
            parents=[],
            label="label",
        )
        expected = {
            "area": round(9.42 * feature_multiplier**2, 2),
            "aspectRatio": 0.33,
            "averageDiameter": round(4 * feature_multiplier, 2),
            "center": {"x": 0, "y": 0},
            "children": [],
            "circularity": 0.6,
            "convexHullArea": round(9.42 * feature_multiplier**2, 2),
            "id": "id",
            "label": "label",
            "majorAxis": round(6 * feature_multiplier, 2),
            "minorAxis": round(2 * feature_multiplier, 2),
            "parents": [],
            "perimeter": round(14.05 * feature_multiplier, 2),
            "radiusX": 1,
            "radiusY": 3,
            "angleOfRotation": 0,
            "type": "ellipse",
            "accuracy": 1,
            "roundness": 0.33,
        }

        actual = oval_features.to_dict(feature_multiplier=742)
        assertAlmostEqualDictEqual(self, expected, actual, 1)

    def test_metric_unit(self):
        oval_features = Ellipse(
            radius_x=1,
            radius_y=3,
            center=Point(0, 0),
            rotation=0,
            id="id",
            children=[],
            parents=[],
            label="label",
        )
        expected = {
            "areaPm": 9.42,
            "aspectRatio": 0.33,
            "averageDiameterPm": 4,
            "center": {"x": 0, "y": 0},
            "children": [],
            "circularity": 0.6,
            "convexHullAreaPm": 9.42,
            "id": "id",
            "label": "label",
            "majorAxisPm": 6,
            "minorAxisPm": 2,
            "parents": [],
            "perimeterPm": 14.05,
            "radiusX": 1,
            "radiusY": 3,
            "angleOfRotation": 0,
            "type": "ellipse",
            "accuracy": 1,
            "roundness": 0.33,
        }

        actual = oval_features.to_dict(features=None, metric_unit="pm")
        self.assertDictEqual(expected, actual)
