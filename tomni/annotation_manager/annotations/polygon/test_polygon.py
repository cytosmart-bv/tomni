from dataclasses import asdict
from unittest import TestCase

import cv2
import numpy as np

from tomni.annotation_manager import Ellipse, Point, Polygon
from tomni.annotation_manager.main import AnnotationManager


class TestPolygon(TestCase):
    def setUp(self) -> None:
        id_ = "1234-1234-2134-1321"
        children = []
        parents = []
        label = "polygon_test"

        self.maxDiff = None
        self.circular_points = [Point(1, 2), Point(1, 4), Point(2, 5), Point(4, 5), Point(5, 4), Point(5, 2), Point(4, 1), Point(3, 1), Point(2, 1)]
        self.circular_polygon = Polygon(points=self.circular_points, id=id_, children=children, parents=parents, label=label)
        self.circular_points_simplified = [Point(1, 2), Point(1, 4), Point(2, 5), Point(4, 5), Point(5, 4), Point(5, 2), Point(4, 1), Point(2, 1)]

        self.star_shaped_points = [Point(1, 3), Point(2, 3), Point(3, 5), Point(5, 3), Point(3, 1), Point(2, 2)]
        self.star_shaped_polygon = Polygon(points=self.star_shaped_points, id=id_, children=children, parents=parents, label=label)
        self.star_shaped_points_simplified = [Point(1, 3), Point(2, 3), Point(3, 5), Point(5, 3), Point(3, 1)]

        self.rectangle_points = [Point(1, 5), Point(3, 5), Point(5, 5), Point(5, 1), Point(3, 1), Point(1, 1)]
        self.rectangle_polygon = Polygon(points=self.rectangle_points, id=id_, children=children, parents=parents, label=label)
        self.rectangle_points_simplified = [Point(1, 5), Point(5, 5), Point(5, 1), Point(1, 1)]

        self.triangle_points = [Point(1, 5), Point(3, 1), Point(5, 5)]
        self.triangle_polygon = Polygon(points=self.triangle_points, id=id_, children=children, parents=parents, label=label)

    def test_circular_area(self):
        expected = 14.0
        actual = self.circular_polygon.area

        self.assertEqual(expected, actual)

    def test_circular_circularity(self):
        expected = 0.9432711611657616
        actual = self.circular_polygon.circularity

        self.assertEqual(expected, actual)

    def test_circular_convex_hull_area(self):
        expected = 14.0
        actual = self.circular_polygon.convex_hull_area

        self.assertEqual(expected, actual)

    def test_circular_perimeter(self):
        expected = 13.656854152679443
        actual = self.circular_polygon.perimeter

        self.assertEqual(expected, actual)

    def test_circular_roundness(self):
        expected = 0.8911880248803259
        actual = self.circular_polygon.roundness

        self.assertEqual(expected, actual)

    def test_star_shaped_area(self):
        expected = 7.0
        actual = self.star_shaped_polygon.area

        self.assertEqual(expected, actual)

    def test_star_shaped_circularity(self):
        expected = 0.640254577329347
        actual = self.star_shaped_polygon.circularity

        self.assertEqual(expected, actual)

    def test_star_shaped_convex_hull_area(self):
        expected = 8.0
        actual = self.star_shaped_polygon.convex_hull_area

        self.assertEqual(expected, actual)

    def test_star_shaped_perimeter(self):
        expected = 11.721349239349365
        actual = self.star_shaped_polygon.perimeter

        self.assertEqual(expected, actual)

    def test_star_shaped_roundness(self):
        expected = 0.5569866579216156
        actual = self.star_shaped_polygon.roundness

        self.assertEqual(expected, actual)

    def test_rectangular_area(self):
        expected = 16.0
        actual = self.rectangle_polygon.area

        self.assertEqual(expected, actual)

    def test_rectangular_circularity(self):
        expected = 0.7853981633974483
        actual = self.rectangle_polygon.circularity

        self.assertEqual(expected, actual)

    def test_rectangular_convex_hull_area(self):
        expected = 16.0
        actual = self.rectangle_polygon.convex_hull_area

        self.assertEqual(expected, actual)

    def test_rectangular_perimeter(self):
        expected = 16.0
        actual = self.rectangle_polygon.perimeter

        self.assertEqual(expected, actual)

    def test_rectangular_roundness(self):
        expected = 0.6365748269154868
        actual = self.rectangle_polygon.roundness

        self.assertEqual(expected, actual)

        self.assertEqual(expected, actual)

    def test_triangular_circularity(self):
        expected = 0.5999907952581642
        actual = self.triangle_polygon.circularity

        self.assertEqual(expected, actual)

    def test_triangular_convex_hull_area(self):
        expected = 8.0
        actual = self.triangle_polygon.convex_hull_area

        self.assertEqual(expected, actual)

    def test_triangular_perimeter(self):
        expected = 12.9442720413208
        actual = self.triangle_polygon.perimeter

        self.assertEqual(expected, actual)

    def test_triangular_roundness(self):
        expected = 0.4074040947818932
        actual = self.triangle_polygon.roundness

        self.assertEqual(expected, actual)

    def test_circular_to_dict(self):
        expected = {
            "id": "1234-1234-2134-1321",
            "label": "polygon_test",
            "children": [],
            "parents": [],
            "type": "polygon",
            "area": 14.0,
            "circularity": 0.94,
            "convex_hull_area": 14.0,
            "perimeter": 13.66,
            "points": [asdict(point) for point in self.circular_points_simplified],
            "roundness": 0.89,
        }
        actual = self.circular_polygon.to_dict()

        self.assertDictEqual(expected, actual)

    def test_rectangular_to_dict(self):
        expected = {
            "id": "1234-1234-2134-1321",
            "label": "polygon_test",
            "children": [],
            "parents": [],
            "type": "polygon",
            "area": 16.0,
            "circularity": 0.79,
            "convex_hull_area": 16.0,
            "perimeter": 16.0,
            "points": [asdict(point) for point in self.rectangle_points_simplified],
            "roundness": 0.64,
        }
        actual = self.rectangle_polygon.to_dict()

        self.assertDictEqual(expected, actual)
        actual = self.rectangle_polygon.to_dict()

        self.assertDictEqual(expected, actual)

    def test_star_shaped_to_dict(self):
        expected = {
            "id": "1234-1234-2134-1321",
            "label": "polygon_test",
            "children": [],
            "parents": [],
            "type": "polygon",
            "area": 7.0,
            "circularity": 0.64,
            "convex_hull_area": 8.0,
            "perimeter": 11.72,
            "points": [asdict(point) for point in self.star_shaped_points_simplified],
            "roundness": 0.56,
        }
        actual = self.star_shaped_polygon.to_dict()

        self.assertDictEqual(expected, actual)

    def test_triangle_to_dict(self):
        expected = {
            "id": "1234-1234-2134-1321",
            "label": "polygon_test",
            "children": [],
            "parents": [],
            "type": "polygon",
            "area": 8.0,
            "circularity": 0.6,
            "convex_hull_area": 8.0,
            "perimeter": 12.94,
            "points": [asdict(point) for point in self.triangle_points],
            "roundness": 0.41,
        }
        actual = self.triangle_polygon.to_dict()
        print(expected)
        print(actual)
        self.assertDictEqual(expected, actual)

    def test_to_dict_with_ellipse_mask(self):
        center = int(2072 / 2)
        rad = int(2072 / 3)

        mask = AnnotationManager(
            [Ellipse(center=Point(center, center), radius_x=rad, rotation=0, id="", label="", children=[], parents=[])]
        ).to_dict()[0]

        polygon1 = Polygon(
            points=[Point(center, center), Point(center + 200, center + 200), Point(center, center + 200)], id="", label="", children=[], parents=[]
        )
        polygon2 = Polygon(
            points=[Point(center, center), Point(center - 300, center - 200), Point(center, center + 200)], id="", label="", children=[], parents=[]
        )
        polygon3 = Polygon(
            points=[Point(center, center), Point(center + 500, center + 500), Point(center + 200, center)], id="", label="", children=[], parents=[]
        )

        polygons_inside = [polygon1, polygon2, polygon3]
        polygons_outside = [self.star_shaped_polygon, self.rectangle_polygon, self.triangle_polygon]

        for polygon in polygons_inside:
            self.assertTrue(polygon.is_in_mask(mask, 0.9))

        for polygon in polygons_outside:
            self.assertFalse(polygon.is_in_mask(mask, 0.9))

    def test_to_dict_with_polygon_mask(self):
        center = 2072 / 2
        size = 2072
        quadrant = size / 4
        points = [Point(quadrant, quadrant), Point(quadrant, quadrant * 3), Point(quadrant * 3, quadrant * 3), Point(quadrant * 3, quadrant)]
        mask = AnnotationManager([Polygon(points, id="", label="", children=[], parents=[])]).to_dict()[0]

        polygon1 = Polygon(
            points=[Point(center, center), Point(center + 200, center + 200), Point(center, center + 200)], id="", label="", children=[], parents=[]
        )
        polygon2 = Polygon(
            points=[Point(center, center), Point(center - 300, center - 200), Point(center, center + 200)], id="", label="", children=[], parents=[]
        )
        polygon3 = Polygon(
            points=[Point(center, center), Point(center + 500, center + 500), Point(center + 200, center)], id="", label="", children=[], parents=[]
        )

        polygons_inside = [polygon1, polygon2, polygon3]
        polygons_outside = [self.star_shaped_polygon, self.rectangle_polygon, self.triangle_polygon]

        for polygon in polygons_inside:
            self.assertTrue(polygon.is_in_mask(mask, 0.9))

        for polygon in polygons_outside:
            self.assertFalse(polygon.is_in_mask(mask, 0.9))

    def test_raises(self):
        with self.assertRaises(SyntaxError):
            self.triangle_polygon.points = self.circular_points
