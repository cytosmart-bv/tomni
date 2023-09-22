from dataclasses import asdict
from unittest import TestCase

from tomni.annotation_manager import Ellipse, Point, Polygon
from tomni.annotation_manager.main import AnnotationManager


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

    # Area
    def test_circular_area(self):
        expected = 14.0
        actual = self.circular_polygon.area

        self.assertEqual(expected, actual)

    def test_rectangular_area(self):
        expected = 16.0
        actual = self.rectangle_polygon.area

        self.assertEqual(expected, actual)

    def test_star_shaped_area(self):
        expected = 7.0
        actual = self.star_shaped_polygon.area

        self.assertEqual(expected, actual)

    # Circularity
    def test_circular_circularity(self):
        expected = 0.9432711611657616
        actual = self.circular_polygon.circularity

        self.assertEqual(expected, actual)

    def test_star_shaped_circularity(self):
        expected = 0.640254577329347
        actual = self.star_shaped_polygon.circularity

        self.assertEqual(expected, actual)

    def test_rectangular_circularity(self):
        expected = 0.7853981633974483
        actual = self.rectangle_polygon.circularity

        self.assertEqual(expected, actual)

    # Convex_hull_area
    def test_circular_convex_hull_area(self):
        expected = 14.0
        actual = self.circular_polygon.convex_hull_area

        self.assertEqual(expected, actual)

    def test_star_shaped_convex_hull_area(self):
        expected = 8.0
        actual = self.star_shaped_polygon.convex_hull_area

        self.assertEqual(expected, actual)

    def test_rectangular_convex_hull_area(self):
        expected = 16.0
        actual = self.rectangle_polygon.convex_hull_area

        self.assertEqual(expected, actual)

    # Perimeter
    def test_circular_perimeter(self):
        expected = 13.656854152679443
        actual = self.circular_polygon.perimeter

        self.assertEqual(expected, actual)

    def test_star_shaped_perimeter(self):
        expected = 11.721349239349365
        actual = self.star_shaped_polygon.perimeter

        self.assertEqual(expected, actual)

    def test_rectangular_perimeter(self):
        expected = 16.0
        actual = self.rectangle_polygon.perimeter

        self.assertEqual(expected, actual)

    # Minor Axis
    def test_circular_minor_axis(self):
        expected = 4.363824844360352
        actual = self.circular_polygon.minor_axis

        self.assertAlmostEqual(expected, actual)

    def test_rectangular_minor_axis(self):
        expected = 5.551115205843844e-18
        actual = self.rectangle_polygon.minor_axis

        self.assertAlmostEqual(expected, actual)

    def test_star_shaped_minor_axis(self):
        expected = 2.985952854156494
        actual = self.star_shaped_polygon.minor_axis

        self.assertAlmostEqual(expected, actual)

    # Major Axis
    def test_circular_major_axis(self):
        expected = 4.526668071746826
        actual = self.circular_polygon.major_axis

        self.assertEqual(expected, actual)

    def test_rectangular_major_axis(self):
        expected = 4.0
        actual = self.rectangle_polygon.major_axis

        self.assertEqual(expected, actual)

    def test_star_shaped_major_axis(self):
        expected = 7.537467002868652
        actual = self.star_shaped_polygon.major_axis

        self.assertEqual(expected, actual)

    # Average Diameter
    def test_circular_average_diameter(self):
        expected = 4.445246458053589
        actual = self.circular_polygon.average_diameter

        self.assertEqual(expected, actual)

    def test_rectangular_average_diameter(self):
        expected = 2.0
        actual = self.rectangle_polygon.average_diameter

        self.assertEqual(expected, actual)

    def test_star_shaped_average_diameter(self):
        expected = 5.261709928512573
        actual = self.star_shaped_polygon.average_diameter

        self.assertEqual(expected, actual)

    # Aspect ratio
    def test_circular_aspect_ratio(self):
        expected = 0.9640258077673378
        actual = self.circular_polygon.aspect_ratio

        self.assertEqual(expected, actual)

    def test_rectangular_aspect_ratio(self):
        expected = 1.387778801460961e-18
        actual = self.rectangle_polygon.aspect_ratio

        self.assertEqual(expected, actual)

    def test_star_shaped_aspect_ratio(self):
        expected = 0.39614804987140684
        actual = self.star_shaped_polygon.aspect_ratio

        self.assertEqual(expected, actual)

    # Roundness
    def test_circular_roundness(self):
        expected = 0.8911880248803259
        actual = self.circular_polygon.roundness

        self.assertEqual(expected, actual)

    def test_rectangular_roundness(self):
        expected = 0.6365748269154868
        actual = self.rectangle_polygon.roundness

        self.assertEqual(expected, actual)

    def test_star_shaped_roundness(self):
        expected = 0.5569866579216156
        actual = self.star_shaped_polygon.roundness

        self.assertEqual(expected, actual)

    def test_circular_to_dict(self):
        expected = {
            "id": "1234-1234-2134-1321",
            "label": "polygon_test",
            "children": [],
            "parents": [],
            "type": "polygon",
            "area": 14.0,
            "convexHullArea": 14.0,
            "majorAxis": 4.53,
            "minorAxis": 4.36,
            "averageDiameter": 4.45,
            "aspectRatio": 0.96,
            "circularity": 0.94,
            "perimeter": 13.66,
            "roundness": 0.89,
            "points": [asdict(point) for point in self.circular_points],
            "accuracy": 1,
            "inner_points": [],
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
            "majorAxis": 4.0,
            "minorAxis": 0.0,
            "averageDiameter": 2.0,
            "aspectRatio": 0.0,
            "circularity": 0.79,
            "convexHullArea": 16.0,
            "perimeter": 16.0,
            "roundness": 0.64,
            "points": [asdict(point) for point in self.rectangle_points],
            "accuracy": 1,
            "inner_points": [],
        }
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
            "minorAxis": 2.99,
            "majorAxis": 7.54,
            "averageDiameter": 5.26,
            "aspectRatio": 0.40,
            "circularity": 0.64,
            "convexHullArea": 8.0,
            "perimeter": 11.72,
            "roundness": 0.56,
            "points": [asdict(point) for point in self.star_shaped_points],
            "accuracy": 1,
            "inner_points": [],
        }
        actual = self.star_shaped_polygon.to_dict()

        self.assertDictEqual(expected, actual)

    def test_triangle_to_dict(self):
        self.triangle_points = [Point(1, 5), Point(3, 1), Point(5, 5)]
        with self.assertRaises(ValueError):
            Polygon(
                points=self.triangle_points,
                id="id",
                children=[],
                parents=[],
                label="label",
            )

    def test_accuracy_to_dict(self):
        expected = {
            "id": "1234-1234-2134-1321",
            "label": "polygon_test",
            "children": [],
            "parents": [],
            "type": "polygon",
            "area": 14.0,
            "convexHullArea": 14.0,
            "majorAxis": 4.53,
            "minorAxis": 4.36,
            "averageDiameter": 4.45,
            "aspectRatio": 0.96,
            "circularity": 0.94,
            "perimeter": 13.66,
            "roundness": 0.89,
            "points": [asdict(point) for point in self.circular_points],
            "accuracy": 0.5,
            "inner_points": [],
        }

        accuracy_test_object = Polygon(
            points=self.circular_points,
            id="1234-1234-2134-1321",
            children=[],
            parents=[],
            label="polygon_test",
            accuracy=0.5,
        )

        actual = accuracy_test_object.to_dict()
        self.assertDictEqual(expected, actual)

    def test_accuracy_to_dict2(self):
        expected = {
            "id": "1234-1234-2134-1321",
            "label": "polygon_test",
            "children": [],
            "parents": [],
            "type": "polygon",
            "area": 14.0,
            "convexHullArea": 14.0,
            "majorAxis": 4.53,
            "minorAxis": 4.36,
            "averageDiameter": 4.45,
            "aspectRatio": 0.96,
            "circularity": 0.94,
            "perimeter": 13.66,
            "roundness": 0.89,
            "points": [asdict(point) for point in self.circular_points],
            "accuracy": 0,
            "inner_points": [],
        }

        accuracy_test_object = Polygon(
            points=self.circular_points,
            id="1234-1234-2134-1321",
            children=[],
            parents=[],
            label="polygon_test",
            accuracy=0,
        )

        actual = accuracy_test_object.to_dict()
        self.assertDictEqual(expected, actual)

    def test_feasture_multiplier_to_dict(self):
        expected = {
            "id": "1234-1234-2134-1321",
            "label": "polygon_test",
            "children": [],
            "parents": [],
            "type": "polygon",
            "area": 56.0,
            "convexHullArea": 56.0,
            "majorAxis": 9.05,
            "minorAxis": 8.73,
            "averageDiameter": 8.89,
            "aspectRatio": 0.96,
            "circularity": 0.94,
            "perimeter": 27.31,
            "roundness": 0.89,
            "points": [asdict(point) for point in self.circular_points],
            "accuracy": 0.5,
            "inner_points": [],
        }

        accuracy_test_object = Polygon(
            points=self.circular_points,
            id="1234-1234-2134-1321",
            children=[],
            parents=[],
            label="polygon_test",
            accuracy=0.5,
        )

        actual = accuracy_test_object.to_dict(feature_multiplier=2)
        self.assertDictEqual(expected, actual)

    def test_to_dict_with_ellipse_mask(self):
        center = int(2072 / 2)
        rad = int(2072 / 3)

        mask = AnnotationManager(
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

        polygon1 = Polygon(
            points=[
                Point(center, center),
                Point(center + 200, center + 200),
                Point(center, center + 200),
                Point(center - 199, center + 200),
                Point(center - 200, center + 200),
            ],
            id="",
            label="",
            children=[],
            parents=[],
        )
        polygon2 = Polygon(
            points=[
                Point(center, center),
                Point(center - 300, center - 200),
                Point(center, center + 198),
                Point(center, center + 199),
                Point(center, center + 200),
            ],
            id="",
            label="",
            children=[],
            parents=[],
        )
        polygon3 = Polygon(
            points=[
                Point(center, center),
                Point(center + 500, center + 500),
                Point(center + 198, center),
                Point(center + 199, center),
                Point(center + 200, center),
            ],
            id="",
            label="",
            children=[],
            parents=[],
        )

        polygons_inside = [polygon1, polygon2, polygon3]
        polygons_outside = [
            self.star_shaped_polygon,
            self.rectangle_polygon,
        ]

        for polygon in polygons_inside:
            self.assertTrue(polygon.is_in_mask(mask, 0.9))

        for polygon in polygons_outside:
            self.assertFalse(polygon.is_in_mask(mask, 0.9))

    def test_to_dict_with_polygon_mask(self):
        center = 2072 / 2
        size = 2072
        quadrant = size / 4
        points = [
            Point(quadrant, quadrant),
            Point(quadrant, quadrant * 3),
            Point(quadrant * 3, quadrant * 3),
            Point(quadrant * 3, quadrant),
            Point(quadrant * 3, quadrant + 1),
        ]
        mask = AnnotationManager(
            [Polygon(points, id="", label="", children=[], parents=[])]
        ).to_dict()

        polygon1 = Polygon(
            points=[
                Point(center, center),
                Point(center + 200, center + 200),
                Point(center, center + 198),
                Point(center, center + 199),
                Point(center, center + 200),
            ],
            id="",
            label="",
            children=[],
            parents=[],
        )
        polygon2 = Polygon(
            points=[
                Point(center, center),
                Point(center - 300, center - 200),
                Point(center, center + 198),
                Point(center, center + 199),
                Point(center, center + 200),
            ],
            id="",
            label="",
            children=[],
            parents=[],
        )
        polygon3 = Polygon(
            points=[
                Point(center, center),
                Point(center + 500, center + 500),
                Point(center + 200, 198),
                Point(center + 200, 199),
                Point(center + 200, center),
            ],
            id="",
            label="",
            children=[],
            parents=[],
        )

        polygons_inside = [polygon1, polygon2, polygon3]
        polygons_outside = [
            self.star_shaped_polygon,
            self.rectangle_polygon,
        ]

        for polygon in polygons_inside:
            self.assertTrue(polygon.is_in_mask(mask, 0.9))

        for polygon in polygons_outside:
            self.assertFalse(polygon.is_in_mask(mask, 0.9))

    def test_raises(self):
        with self.assertRaises(SyntaxError):
            self.rectangle_polygon.points = self.circular_points

    def test_inner_points(self):
        id = "1234-1234-2134-1321"
        children = []
        parents = []
        label = "inner_point_test"

        self.maxDiff = None
        points = [
            Point(0, 0),
            Point(0, 100),
            Point(0, 200),
            Point(0, 300),
            Point(0, 400),
            Point(100, 400),
            Point(200, 400),
            Point(300, 400),
            Point(400, 400),
            Point(400, 0),
        ]
        inner_points = [
            [
                Point(50, 50),
                Point(50, 100),
                Point(50, 150),
                Point(100, 150),
                Point(150, 150),
                Point(150, 50),
            ]
        ]

        expected = {
            "accuracy": 1,
            "label": label,
            "id": id,
            "children": children,
            "parents": parents,
            "type": "polygon",
            "area": 150000.0,
            "points": [asdict(point) for point in points],
            "inner_points": [
                [asdict(point) for point in list_of_points]
                for list_of_points in inner_points
            ],
        }

        donut_polygon = Polygon(
            points=points,
            id=id,
            children=children,
            parents=parents,
            label=label,
            inner_points=inner_points,
        )
        actual = donut_polygon.to_dict(features=["area"])
        self.assertDictEqual(expected, actual)
