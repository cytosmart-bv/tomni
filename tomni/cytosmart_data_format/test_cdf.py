from unittest import TestCase

from dataclasses import asdict

from tomni.cytosmart_data_format import CytoSmartDataFormat
from tomni.cytosmart_data_format import Point, Polygon


class TestCDFAdding(TestCase):
    def setUp(self) -> None:
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
