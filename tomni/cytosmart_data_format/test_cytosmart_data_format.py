from dataclasses import asdict
from unittest import TestCase

import numpy as np

from tomni.cytosmart_data_format import CytoSmartDataFormat
from tomni.cytosmart_data_format.annotations.point.main import Point
from tomni.cytosmart_data_format.annotations.polygon.main import Polygon

from .main import CytoSmartDataFormat


class TestCytoSmartDataFormat(TestCase):
    def setUp(self) -> None:
        self.cdf = CytoSmartDataFormat(
            [
                Polygon(
                    points=[
                        Point(1, 3),
                        Point(2, 3),
                        Point(3, 5),
                        Point(5, 3),
                        Point(3, 1),
                        Point(2, 2),
                    ],
                    id="132132132123132",
                    children=[],
                    parents=[],
                    label="star",
                ),
                Polygon(
                    points=[
                        Point(10, 30),
                        Point(20, 30),
                        Point(30, 50),
                        Point(50, 30),
                        Point(30, 10),
                        Point(20, 20),
                    ],
                    id="132132132123132",
                    children=[],
                    parents=[],
                    label="star",
                ),
                Polygon(
                    points=[
                        Point(100, 300),
                        Point(200, 300),
                        Point(300, 500),
                        Point(500, 300),
                        Point(300, 100),
                        Point(200, 200),
                    ],
                    id="132132132123132",
                    children=[],
                    parents=[],
                    label="star",
                ),
                Polygon(
                    points=[
                        Point(1000, 3000),
                        Point(2000, 3000),
                        Point(3000, 5000),
                        Point(5000, 3000),
                        Point(3000, 1000),
                        Point(2000, 2000),
                    ],
                    id="132132132123132",
                    children=[],
                    parents=[],
                    label="star",
                ),
                Polygon(
                    points=[
                        Point(10000, 30000),
                        Point(20000, 30000),
                        Point(30000, 50000),
                        Point(50000, 30000),
                        Point(30000, 10000),
                        Point(20000, 20000),
                    ],
                    id="132132132123132",
                    children=[],
                    parents=[],
                    label="star",
                ),
            ]
        )

        id_ = "2"
        children = []
        parents = []
        label = "polygon_test"
        self.rectangle_points = [
            Point(1, 5),
            Point(3, 5),
            Point(5, 5),
            Point(5, 1),
            Point(3, 1),
            Point(1, 1),
        ]
        self.polygon_annotation = Polygon(
            points=self.rectangle_points,
            id=id_,
            children=children,
            parents=parents,
            label=label,
        )

        self.ellipse_dict = {
            "area": 3.14,
            "aspect_ratio": 1.0,
            "center": {"x": 0, "y": 0},
            "children": [],
            "circularity": 1.0,
            "id": "1",
            "label": "ellipse_test",
            "parents": [],
            "perimeter": 6.28,
            "radiusX": 1,
            "radiusY": 1,
            "angleOfRotation": 0,
            "type": "ellipse",
        }
        self.polygon_dict = {
            "id": "2",
            "label": "polygon_test",
            "children": [],
            "parents": [],
            "type": "polygon",
            "area": 16.0,
            "circularity": 0.79,
            "convex_hull_area": 16.0,
            "perimeter": 16.0,
            "points": [asdict(point) for point in self.rectangle_points],
            "roundness": 0.64,
        }
        self.list_of_dict = [self.ellipse_dict, self.polygon_dict]
        self.cdf1 = CytoSmartDataFormat.from_dicts([self.ellipse_dict])
        self.cdf2 = CytoSmartDataFormat.from_dicts([self.polygon_dict])
        self.cdf_combined = CytoSmartDataFormat.from_dicts(
            [self.ellipse_dict, self.polygon_dict]
        )
        self.cdf_combined2 = CytoSmartDataFormat.from_dicts(
            [self.ellipse_dict] + self.list_of_dict
        )

    def tearDown(self):
        del self.cdf

    def test_filter_single(self):
        actual = self.cdf.filter(feature="area", min_val=500, max_val=5000000)
        expected_n_items = 2

        self.assertIsInstance(actual, list)
        self.assertEqual(len(actual), expected_n_items)

    def test_filter_single_inplace(self):
        actual = self.cdf.filter(
            feature="area", min_val=500, max_val=5000000, inplace=True
        )
        expected_n_items = 2

        self.assertIsInstance(actual, CytoSmartDataFormat)
        self.assertEqual(len(self.cdf), expected_n_items)
        self.assertEqual(len(self.cdf), expected_n_items)

    def test_filter_chained(self):
        actual = self.cdf.filter(
            feature="area", min_val=0, max_val=500, inplace=True
        ).filter(feature="perimeter", min_val=11, max_val=12, inplace=True)
        expected_n_items = 1

        self.assertIsInstance(actual, CytoSmartDataFormat)
        self.assertEqual(len(self.cdf), expected_n_items)

    def test_cdf_add(self):
        assert (
            len(self.cdf1) == 1
        ), f"Length changed during testing is now {len(self.cdf1)}"
        assert (
            len(self.cdf2) == 1
        ), f"Length changed during testing is now {len(self.cdf2)}"

        new_cdf = self.cdf1 + self.cdf2

        assert len(new_cdf) == 2
        assert new_cdf.to_dict() == self.cdf_combined.to_dict()

    def test_cdf_add_dict(self):
        assert (
            len(self.cdf1) == 1
        ), f"Length changed during testing is now {len(self.cdf1)}"
        assert (
            len(self.cdf2) == 1
        ), f"Length changed during testing is now {len(self.cdf2)}"

        new_cdf = self.cdf1 + self.polygon_dict
        assert len(new_cdf) == 2
        assert new_cdf.to_dict() == self.cdf_combined.to_dict()

    def test_cdf_add_annotation(self):
        assert (
            len(self.cdf1) == 1
        ), f"Length changed during testing is now {len(self.cdf1)}"
        assert (
            len(self.cdf2) == 1
        ), f"Length changed during testing is now {len(self.cdf2)}"

        new_cdf = self.cdf1 + self.polygon_annotation
        assert len(new_cdf) == 2
        assert new_cdf.to_dict() == self.cdf_combined.to_dict()

    def test_cdf_add_list(self):
        assert (
            len(self.cdf1) == 1
        ), f"Length changed during testing is now {len(self.cdf1)}"
        assert (
            len(self.cdf2) == 1
        ), f"Length changed during testing is now {len(self.cdf2)}"

        new_cdf = self.cdf1 + self.list_of_dict
        assert len(new_cdf) == 3
        assert new_cdf.to_dict() == self.cdf_combined2.to_dict()

    def test_cdf_radd_dict(self):
        assert (
            len(self.cdf1) == 1
        ), f"Length changed during testing is now {len(self.cdf1)}"
        assert (
            len(self.cdf2) == 1
        ), f"Length changed during testing is now {len(self.cdf2)}"

        new_cdf = self.polygon_dict + self.cdf1
        assert len(new_cdf) == 2
        assert new_cdf.to_dict() == self.cdf_combined.to_dict()

    def test_cdf_radd_annotation(self):
        assert (
            len(self.cdf1) == 1
        ), f"Length changed during testing is now {len(self.cdf1)}"
        assert (
            len(self.cdf2) == 1
        ), f"Length changed during testing is now {len(self.cdf2)}"

        new_cdf = self.polygon_annotation + self.cdf1
        assert len(new_cdf) == 2
        assert new_cdf.to_dict() == self.cdf_combined.to_dict()

    def test_cdf_radd_list(self):
        assert (
            len(self.cdf1) == 1
        ), f"Length changed during testing is now {len(self.cdf1)}"
        assert (
            len(self.cdf2) == 1
        ), f"Length changed during testing is now {len(self.cdf2)}"

        new_cdf = self.list_of_dict + self.cdf1
        assert len(new_cdf) == 3
        assert new_cdf.to_dict() == self.cdf_combined2.to_dict()

    def test_fail_add_dict(self):
        a = {
            "area": 3.14,
            "aspect_ratio": 1.0,
            "center": {"x": 0, "y": 0},
            "children": [],
            "circularity": 1.0,
            "id": "1",
            "label": "ellipse_test",
            "parents": [],
            "perimeter": 6.28,
            "radiusX": 1,
            "radiusY": 1,
            "angleOfRotation": 0,
            "type": "ellipsesss",
        }
        with self.assertRaises(Exception) as context:
            test = self.cdf1 + a
        self.assertTrue(
            "CDF cannot be created. Dict with id 1 misses type-key with value ellipse or polygon."
            in str(context.exception)
        )

    def test_fail_add_list(self):
        a = {
            "area": 3.14,
            "aspect_ratio": 1.0,
            "center": {"x": 0, "y": 0},
            "children": [],
            "circularity": 1.0,
            "id": "1",
            "label": "ellipse_test",
            "parents": [],
            "perimeter": 6.28,
            "radiusX": 1,
            "radiusY": 1,
            "angleOfRotation": 0,
            "type": "ellipsesss",
        }
        b = {
            "area": 3.14,
            "aspect_ratio": 1.0,
            "center": {"x": 0, "y": 0},
            "children": [],
            "circularity": 1.0,
            "id": "1",
            "label": "ellipse_test",
            "parents": [],
            "perimeter": 6.28,
            "radiusX": 1,
            "radiusY": 1,
            "angleOfRotation": 0,
            "type": "ellipse",
        }
        c = [b, a]
        with self.assertRaises(Exception) as context:
            test = self.cdf1 + c
        self.assertTrue(
            "CDF cannot be created. Dict with id 1 misses type-key with value ellipse or polygon."
            in str(context.exception)
        )
