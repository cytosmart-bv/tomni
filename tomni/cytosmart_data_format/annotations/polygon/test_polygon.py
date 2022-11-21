from dataclasses import asdict
from unittest import TestCase

from tomni.cytosmart_data_format import Point, Polygon


class TestPolygon(TestCase):
    def setUp(self) -> None:
        id_ = "1234-1234-2134-1321"
        children = []
        parents = []
        label = "polygon_test"

        self.maxDiff = None
        self.circular_points = [
            Point(1, 2),
            Point(1, 4),
            Point(2, 5),
            Point(4, 5),
            Point(5, 4),
            Point(5, 2),
            Point(4, 1),
            Point(3, 1),
            Point(2, 1),
        ]
        self.circular_polygon = Polygon(
            points=self.circular_points,
            id=id_,
            children=children,
            parents=parents,
            label=label,
        )

        self.star_shaped_points = [
            Point(1, 3),
            Point(2, 3),
            Point(3, 5),
            Point(5, 3),
            Point(3, 1),
            Point(2, 2),
        ]
        self.star_shaped_polygon = Polygon(
            points=self.star_shaped_points,
            id=id_,
            children=children,
            parents=parents,
            label=label,
        )

        self.rectangle_points = [
            Point(1, 5),
            Point(3, 5),
            Point(5, 5),
            Point(5, 1),
            Point(3, 1),
            Point(1, 1),
        ]
        self.rectangle_polygon = Polygon(
            points=self.rectangle_points,
            id=id_,
            children=children,
            parents=parents,
            label=label,
        )

        self.triangle_points = [
            Point(1, 5),
            Point(3, 1),
            Point(5, 5),
        ]
        self.triangle_polygon = Polygon(
            points=self.triangle_points,
            id=id_,
            children=children,
            parents=parents,
            label=label,
        )

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
        expected = None
        actual = self.triangle_polygon.circularity

        self.assertEqual(expected, actual)

    def test_triangular_convex_hull_area(self):
        expected = None
        actual = self.triangle_polygon.convex_hull_area

        self.assertEqual(expected, actual)

    def test_triangular_perimeter(self):
        expected = 12.9442720413208
        actual = self.triangle_polygon.perimeter

        self.assertEqual(expected, actual)

    def test_triangular_roundness(self):
        expected = None
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
            "circularity": 0.9432711611657616,
            "convex_hull_area": 14.0,
            "perimeter": 13.656854152679443,
            "points": [asdict(point) for point in self.circular_points],
            "roundness": 0.8911880248803259,
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
            "circularity": 0.7853981633974483,
            "convex_hull_area": 16.0,
            "perimeter": 16.0,
            "points": [asdict(point) for point in self.rectangle_points],
            "roundness": 0.6365748269154868,
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
            "circularity": 0.640254577329347,
            "convex_hull_area": 8.0,
            "perimeter": 11.721349239349365,
            "points": [asdict(point) for point in self.star_shaped_points],
            "roundness": 0.5569866579216156,
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
            "area": None,
            "circularity": None,
            "convex_hull_area": None,
            "perimeter": 12.9442720413208,
            "points": [asdict(point) for point in self.triangle_points],
            "roundness": None,
        }
        actual = self.triangle_polygon.to_dict()

        self.assertDictEqual(expected, actual)