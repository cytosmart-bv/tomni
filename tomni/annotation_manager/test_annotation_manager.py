from unittest import TestCase

import cv2
import numpy as np

from tomni.annotation_manager.annotations import Ellipse, Point, Polygon
from tomni.annotation_manager.utils import overlap_object

from .main import AnnotationManager


class TestAnnotationManager(TestCase):
    def setUp(self) -> None:
        self.manager = AnnotationManager(
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
                    accuracy=0.5,
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
                    accuracy=0,
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
                    accuracy=0,
                ),
            ]
        )

    def tearDown(self):
        del self.manager

    def test_filter_single(self):
        actual = self.manager.filter(feature="area", min_val=500, max_val=5000000)
        expected_n_items = 3

        self.assertIsInstance(actual, list)
        self.assertEqual(len(actual), expected_n_items)

    def test_filter_accuracy_big_range(self):
        actual = self.manager.filter(feature="accuracy", min_val=0, max_val=5)
        expected_n_items = 6

        self.assertIsInstance(actual, list)
        self.assertEqual(len(actual), expected_n_items)

    def test_filter_accuracy_tight_range(self):
        actual = self.manager.filter(feature="accuracy", min_val=0.8, max_val=1)
        expected_n_items = 3

        self.assertIsInstance(actual, list)
        self.assertEqual(len(actual), expected_n_items)

    def test_filter_single_inplace(self):
        actual = self.manager.filter(
            feature="area", min_val=500, max_val=5000000, inplace=True
        )
        expected_n_items = 3

        self.assertIsInstance(actual, AnnotationManager)
        self.assertEqual(len(self.manager), expected_n_items)

    def test_filter_chained(self):
        actual = self.manager.filter(
            feature="area", min_val=0, max_val=500, inplace=True
        ).filter(feature="circularity", min_val=0.5, max_val=1, inplace=True)
        expected_n_items = 1

        self.assertIsInstance(actual, AnnotationManager)
        self.assertEqual(len(self.manager), expected_n_items)

    def test_filter_feature_multiplier(self):
        temp_manager = AnnotationManager(
            [
                Polygon(
                    points=[
                        Point(0, 0),
                        Point(0, 5),
                        Point(0, 10),
                        Point(10, 10),
                        Point(10, 5),
                        Point(10, 0),
                    ],
                    id="132132132123132",
                    children=[],
                    parents=[],
                    label="star",
                )
            ]
        )
        manager1 = temp_manager.filter(
            feature="area", min_val=0, max_val=500, inplace=True, feature_multiplier=1
        )
        expected_n_items1 = 1

        self.assertIsInstance(manager1, AnnotationManager)
        self.assertEqual(len(manager1), expected_n_items1)

        manager2 = temp_manager.filter(
            feature="area",
            min_val=0,
            max_val=500,
            inplace=True,
            feature_multiplier=742,
        )
        expected_n_items2 = 0
        self.assertIsInstance(manager2, AnnotationManager)
        self.assertEqual(len(manager2), expected_n_items2)

    def test_to_dict_with_polygon_mask(self):
        mask = [
            {
                "type": "polygon",
                "points": [
                    {"x": 0, "y": 0},
                    {"x": 0, "y": 4000},
                    {"x": 4000, "y": 4000},
                    {"x": 4000, "y": 2000},
                    {"x": 4000, "y": 0},
                ],
            }
        ]
        expected = [
            {
                "id": "132132132123132",
                "label": "star",
                "children": [],
                "parents": [],
                "areaUm": 7.0,
                "circularity": 0.64,
                "convexHullAreaUm": 8.0,
                "type": "polygon",
                "points": [
                    {"x": 1, "y": 3},
                    {"x": 2, "y": 3},
                    {"x": 3, "y": 5},
                    {"x": 5, "y": 3},
                    {"x": 3, "y": 1},
                    {"x": 2, "y": 2},
                ],
                "accuracy": 1,
                "inner_points": [],
            },
            {
                "id": "132132132123132",
                "label": "star",
                "children": [],
                "parents": [],
                "areaUm": 700.0,
                "circularity": 0.64,
                "convexHullAreaUm": 800.0,
                "type": "polygon",
                "points": [
                    {"x": 10, "y": 30},
                    {"x": 20, "y": 30},
                    {"x": 30, "y": 50},
                    {"x": 50, "y": 30},
                    {"x": 30, "y": 10},
                    {"x": 20, "y": 20},
                ],
                "accuracy": 1,
                "inner_points": [],
            },
            {
                "id": "132132132123132",
                "label": "star",
                "children": [],
                "parents": [],
                "areaUm": 70000.0,
                "circularity": 0.64,
                "convexHullAreaUm": 80000.0,
                "type": "polygon",
                "points": [
                    {"x": 100, "y": 300},
                    {"x": 200, "y": 300},
                    {"x": 300, "y": 500},
                    {"x": 500, "y": 300},
                    {"x": 300, "y": 100},
                    {"x": 200, "y": 200},
                ],
                "accuracy": 1,
                "inner_points": [],
            },
            {
                "id": "132132132123132",
                "label": "star",
                "children": [],
                "parents": [],
                "areaUm": 700.0,
                "circularity": 0.64,
                "convexHullAreaUm": 800.0,
                "type": "polygon",
                "points": [
                    {"x": 10, "y": 30},
                    {"x": 20, "y": 30},
                    {"x": 30, "y": 50},
                    {"x": 50, "y": 30},
                    {"x": 30, "y": 10},
                    {"x": 20, "y": 20},
                ],
                "accuracy": 0,
                "inner_points": [],
            },
        ]
        actual = self.manager.to_dict(
            mask_json=mask,
            features=["area", "convex_hull_area", "circularity"],
            metric_unit="Um",
        )

        self.assertEqual(expected, actual)

    def test_to_dict_with_ellipse_mask(self):
        mask = AnnotationManager(
            [
                Ellipse(
                    center=Point(50, 50),
                    radius_x=100,
                    rotation=0,
                    id="",
                    label="",
                    children=[],
                    parents=[],
                )
            ]
        ).to_dict()

        expected = [
            {
                "id": "132132132123132",
                "label": "star",
                "children": [],
                "parents": [],
                "areaUm": 7.0,
                "circularity": 0.64,
                "convexHullAreaUm": 8.0,
                "type": "polygon",
                "points": [
                    {"x": 1, "y": 3},
                    {"x": 2, "y": 3},
                    {"x": 3, "y": 5},
                    {"x": 5, "y": 3},
                    {"x": 3, "y": 1},
                    {"x": 2, "y": 2},
                ],
                "accuracy": 1,
                "inner_points": [],
            },
            {
                "id": "132132132123132",
                "label": "star",
                "children": [],
                "parents": [],
                "areaUm": 700.0,
                "circularity": 0.64,
                "convexHullAreaUm": 800.0,
                "type": "polygon",
                "points": [
                    {"x": 10, "y": 30},
                    {"x": 20, "y": 30},
                    {"x": 30, "y": 50},
                    {"x": 50, "y": 30},
                    {"x": 30, "y": 10},
                    {"x": 20, "y": 20},
                ],
                "accuracy": 1,
                "inner_points": [],
            },
            {
                "id": "132132132123132",
                "label": "star",
                "children": [],
                "parents": [],
                "areaUm": 700.0,
                "circularity": 0.64,
                "convexHullAreaUm": 800.0,
                "type": "polygon",
                "points": [
                    {"x": 10, "y": 30},
                    {"x": 20, "y": 30},
                    {"x": 30, "y": 50},
                    {"x": 50, "y": 30},
                    {"x": 30, "y": 10},
                    {"x": 20, "y": 20},
                ],
                "accuracy": 0,
                "inner_points": [],
            },
        ]

        actual = self.manager.to_dict(
            mask_json=mask,
            features=["area", "convex_hull_area", "circularity"],
            metric_unit="Um",
        )

        self.assertEqual(expected, actual)

    def test_to_dict_compression_few_points(self):
        self.manager = AnnotationManager(
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
                    inner_points=[
                        [
                            Point(1, 3),
                            Point(2, 3),
                            Point(3, 5),
                            Point(5, 3),
                            Point(4, 3),
                        ]
                    ],
                )
            ]
        )
        expected = [
            {
                "id": "132132132123132",
                "label": "star",
                "children": [],
                "parents": [],
                "type": "polygon",
                "points": [
                    {"x": 1, "y": 3},
                    {"x": 2, "y": 3},
                    {"x": 3, "y": 5},
                    {"x": 5, "y": 3},
                    {"x": 3, "y": 1},
                    {"x": 2, "y": 2},
                ],
                "accuracy": 1,
                "inner_points": [
                    [
                        {"x": 1, "y": 3},
                        {"x": 2, "y": 3},
                        {"x": 3, "y": 5},
                        {"x": 5, "y": 3},
                        {"x": 4, "y": 3},
                    ]
                ],
            }
        ]
        actual = self.manager.to_dict(
            features=[], metric_unit="Um", do_compress=True, epsilon=3
        )

        self.assertEqual(expected, actual)

    def test_to_dict_inner_points_compression_lots_of_points(self):
        self.manager = AnnotationManager(
            [
                Polygon(
                    points=[
                        Point(1, 3),
                        Point(2, 3),
                        Point(3, 3),
                        Point(4, 3),
                        Point(5, 3),
                        Point(6, 3),
                        Point(7, 3),
                        Point(8, 3),
                        Point(9, 3),
                        Point(10, 3),
                        Point(11, 3),
                        Point(11, 11),
                        Point(5, 6),
                        Point(3, 11),
                    ],
                    id="132132132123132",
                    children=[],
                    parents=[],
                    label="star",
                    inner_points=[
                        [
                            Point(1, 2),
                            Point(1, 3),
                            Point(1, 4),
                            Point(1, 5),
                            Point(1, 6),
                            Point(1, 7),
                            Point(1, 8),
                            Point(1, 9),
                            Point(1, 10),
                            Point(10, 10),
                            Point(5, 5),
                            Point(10, 1),
                        ]
                    ],
                )
            ]
        )
        expected = [
            {
                "id": "132132132123132",
                "label": "star",
                "children": [],
                "parents": [],
                "type": "polygon",
                "points": [
                    {"x": 1.0, "y": 3.0},
                    {"x": 11.0, "y": 3.0},
                    {"x": 11.0, "y": 11.0},
                    {"x": 5.0, "y": 6.0},
                    {"x": 3.0, "y": 11.0},
                ],
                "accuracy": 1,
                "inner_points": [
                    [
                        {"x": 1.0, "y": 2.0},
                        {"x": 1.0, "y": 10.0},
                        {"x": 10.0, "y": 10.0},
                        {"x": 5.0, "y": 5.0},
                        {"x": 10.0, "y": 1.0},
                    ]
                ],
            }
        ]
        actual = self.manager.to_dict(
            features=[], metric_unit="Um", do_compress=True, epsilon=3
        )

        self.assertEqual(expected, actual)

    def test_init_from_labeled_to_labeled_mask(self):
        data = np.array(
            [
                [0, 3, 3, 0, 0, 0],
                [0, 3, 3, 0, 0, 0],
                [1, 1, 1, 0, 0, 0],
                [0, 2, 0, 0, 0, 0],
                [0, 2, 2, 0, 0, 0],
                [0, 2, 2, 2, 0, 0],
                [0, 2, 2, 2, 2, 0],
            ]
        )

        expected = np.array(
            [
                [0, 1, 1, 0, 0, 0],
                [0, 1, 1, 0, 0, 0],
                [1, 1, 1, 0, 0, 0],
                [0, 1, 0, 0, 0, 0],
                [0, 1, 1, 0, 0, 0],
                [0, 1, 1, 1, 0, 0],
                [0, 1, 1, 1, 1, 0],
            ]
        )

        shape = data.shape
        manager = AnnotationManager.from_labeled_mask(data)

        n_labels = 1
        self.assertEqual(len(manager), n_labels)

        actual = manager.to_labeled_mask(shape)

        np.testing.assert_array_equal(actual, expected)

    def test_init_from_labeled_to_labeled_mask_big_contours(self):
        data = np.array(
            [
                [2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [2, 2, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 2, 2, 0, 1, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
                [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
        shape = data.shape
        manager = AnnotationManager.from_labeled_mask(data)

        n_labels = 2
        self.assertEqual(len(manager), n_labels)

        actual = manager.to_labeled_mask(shape)

        np.testing.assert_array_equal(actual, data)

    def test_init_from_binary_to_labeled_mask(self):
        data = np.array(
            [
                [0, 1, 1, 0, 0, 0],
                [0, 1, 1, 0, 0, 0],
                [1, 1, 1, 0, 0, 0],
                [0, 1, 0, 0, 0, 0],
                [0, 1, 1, 0, 0, 0],
                [0, 1, 1, 1, 0, 0],
                [0, 1, 1, 1, 1, 0],
            ]
        )

        shape = data.shape
        manager = AnnotationManager.from_binary_mask(data)

        n_labels = 1
        self.assertEqual(len(manager), n_labels)

        actual = manager.to_labeled_mask(shape)
        cv2.imwrite("actual.png", actual)

        np.testing.assert_array_equal(actual, data)

    def test_init_from_labeled_mask_to_binary_mask(self):
        data = np.array(
            [
                [2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [2, 2, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 2, 2, 0, 1, 1, 1, 1, 1, 1, 1],
                [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
                [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
        expected = np.array(
            [
                [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )

        shape = data.shape
        manager = AnnotationManager.from_labeled_mask(data)

        n_labels = 2
        self.assertEqual(len(manager), n_labels)

        actual = manager.to_binary_mask(shape)

        np.testing.assert_array_equal(actual, expected)

    def test_to_binary_mask(self):
        polygons = [
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
            )
        ]

        expected = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
            ]
        )
        manager = AnnotationManager(polygons)

        actual = manager.to_binary_mask((7, 7))

        np.testing.assert_array_equal(actual, expected)

    def test_to_binary_mask_inner_points(self):
        polygons = [
            Polygon(
                points=[
                    Point(0, 0),
                    Point(4, 0),
                    Point(6, 0),
                    Point(6, 6),
                    Point(3, 6),
                    Point(0, 6),
                ],
                id="132132132123132",
                children=[],
                parents=[],
                label="star",
                inner_points=[
                    [
                        Point(2, 1),
                        Point(4, 1),
                        Point(5, 2),
                        Point(5, 4),
                        Point(4, 5),
                        Point(2, 5),
                        Point(1, 4),
                        Point(1, 2),
                    ]
                ],
            )
        ]

        expected = np.array(
            [
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 0, 0, 0, 1, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 1, 0, 0, 0, 1, 1],
                [1, 1, 1, 1, 1, 1, 1],
            ]
        )
        manager = AnnotationManager(polygons)

        actual = manager.to_binary_mask((7, 7))

        np.testing.assert_array_equal(actual, expected)

    def test_to_labeled_mask(self):
        polygons = [
            Polygon(
                points=[
                    Point(1, 1),
                    Point(2, 3),
                    Point(1, 3),
                    Point(2, 3),
                    Point(2, 1),
                ],
                id="132132132123132",
                children=[],
                parents=[],
                label="star",
            ),
            Polygon(
                points=[
                    Point(3, 3),
                    Point(3, 5),
                    Point(5, 5),
                    Point(5, 4),
                    Point(5, 3),
                ],
                id="132132132123132",
                children=[],
                parents=[],
                label="star",
            ),
        ]

        expected = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0, 0, 0],
                [0, 1, 1, 0, 0, 0, 0],
                [0, 1, 1, 2, 2, 2, 0],
                [0, 0, 0, 2, 2, 2, 0],
                [0, 0, 0, 2, 2, 2, 0],
                [0, 0, 0, 0, 0, 0, 0],
            ]
        )
        manager = AnnotationManager(polygons)

        actual = manager.to_labeled_mask((7, 7))

        np.testing.assert_array_equal(actual, expected)

    def test_binary_mask_double_donut(self):
        input_mask = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
                [0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
                [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            dtype=np.uint8,
        )

        expected = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            dtype=np.uint8,
        )

        manager = AnnotationManager.from_binary_mask(input_mask)
        actual = manager.to_binary_mask(input_mask.shape)

        np.testing.assert_array_equal(expected, actual)

    def test_binary_mask_no_object(self):
        input_mask = np.zeros((10, 10))
        expected = np.zeros((10, 10))
        manager = AnnotationManager.from_binary_mask(input_mask)
        actual = manager.to_binary_mask(input_mask.shape)

        np.testing.assert_array_equal(expected, actual)

    def test_binary_mask_all_1_object_small(self):
        input_mask = np.ones((10, 10))
        expected = np.zeros((10, 10))
        manager = AnnotationManager.from_binary_mask(input_mask)
        actual = manager.to_binary_mask(input_mask.shape)

        np.testing.assert_array_equal(expected, actual)

    def test_binary_mask_all_1_object_big(self):
        input_mask = np.ones((100, 100))
        expected = np.ones((100, 100))
        manager = AnnotationManager.from_binary_mask(input_mask)
        actual = manager.to_binary_mask(input_mask.shape)

        np.testing.assert_array_equal(expected, actual)

    def test_labeled_mask_all_1_object(self):
        input_mask = np.ones((100, 100))
        expected = np.ones((100, 100))
        manager = AnnotationManager.from_binary_mask(input_mask)
        actual = manager.to_binary_mask(input_mask.shape)

        np.testing.assert_array_equal(expected, actual)

    def test_labeled_mask_no_object(self):
        input_mask = np.zeros((10, 10))

        expected = np.zeros((10, 10))
        manager = AnnotationManager.from_binary_mask(input_mask)
        actual = manager.to_binary_mask(input_mask.shape)

        np.testing.assert_array_equal(expected, actual)

    def test_binary_mask_small_object(self):
        input_mask = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            dtype=np.uint8,
        )
        expected = np.zeros((10, 10))
        manager = AnnotationManager.from_binary_mask(input_mask)
        actual = manager.to_binary_mask(input_mask.shape)

        np.testing.assert_array_equal(expected, actual)

    def test_binary_mask_multiple_objects(
        self,
    ):
        input_mask = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            dtype=np.uint8,
        )

        expected = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            dtype=np.uint8,
        )

        manager = AnnotationManager.from_binary_mask(
            input_mask, include_inner_contours=False
        )
        actual = manager.to_labeled_mask(input_mask.shape)

        np.testing.assert_array_equal(expected, actual)

    def test_from_binary_mask_to_dict_donut(self):
        data = np.array(
            [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1],
                [1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1],
                [1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1],
                [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            ]
        )

        expected = [
            {
                "label": "",
                "children": [],
                "parents": [],
                "type": "polygon",
                "points": [
                    {"x": 0, "y": 0},
                    {"x": 0, "y": 9},
                    {"x": 1, "y": 9},
                    {"x": 5, "y": 5},
                    {"x": 7, "y": 5},
                    {"x": 11, "y": 9},
                    {"x": 12, "y": 9},
                    {"x": 12, "y": 0},
                ],
                "inner_points": [
                    [
                        {"x": 1, "y": 2},
                        {"x": 2, "y": 1},
                        {"x": 10, "y": 1},
                        {"x": 11, "y": 2},
                        {"x": 11, "y": 6},
                        {"x": 10, "y": 7},
                        {"x": 7, "y": 4},
                        {"x": 5, "y": 4},
                        {"x": 2, "y": 7},
                        {"x": 1, "y": 6},
                    ]
                ],
                "accuracy": 1,
            }
        ]

        manager = AnnotationManager.from_binary_mask(data, include_inner_contours=True)
        actual = manager.to_dict(features=[])
        for dict_object in actual:
            dict_object.pop("id")

        np.testing.assert_array_equal(actual, expected)

    def test_from_binary_mask_to_dict_donut_labelled(self):
        data = np.array(
            [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1],
                [1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1],
                [1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1],
                [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            ]
        )

        expected = [
            {
                "label": "dead",
                "children": [],
                "parents": [],
                "type": "polygon",
                "points": [
                    {"x": 0, "y": 0},
                    {"x": 0, "y": 9},
                    {"x": 1, "y": 9},
                    {"x": 5, "y": 5},
                    {"x": 7, "y": 5},
                    {"x": 11, "y": 9},
                    {"x": 12, "y": 9},
                    {"x": 12, "y": 0},
                ],
                "inner_points": [
                    [
                        {"x": 1, "y": 2},
                        {"x": 2, "y": 1},
                        {"x": 10, "y": 1},
                        {"x": 11, "y": 2},
                        {"x": 11, "y": 6},
                        {"x": 10, "y": 7},
                        {"x": 7, "y": 4},
                        {"x": 5, "y": 4},
                        {"x": 2, "y": 7},
                        {"x": 1, "y": 6},
                    ]
                ],
                "accuracy": 1,
            }
        ]
        label = "dead"
        manager = AnnotationManager.from_binary_mask(
            data, include_inner_contours=True, label=label
        )
        actual = manager.to_dict(features=[])
        for dict_object in actual:
            dict_object.pop("id")

        np.testing.assert_array_equal(actual, expected)

    def test_from_binary_mask_to_dict_polygon_inside_donut(self):
        data = np.array(
            [
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            ]
        )

        expected = [
            {
                "label": "",
                "children": [],
                "parents": [],
                "type": "polygon",
                "points": [
                    {"x": 4, "y": 3},
                    {"x": 4, "y": 5},
                    {"x": 5, "y": 6},
                    {"x": 8, "y": 6},
                    {"x": 9, "y": 5},
                    {"x": 9, "y": 3},
                ],
                "inner_points": [],
                "accuracy": 1,
            },
            {
                "label": "",
                "children": [],
                "parents": [],
                "type": "polygon",
                "points": [
                    {"x": 1, "y": 0},
                    {"x": 1, "y": 8},
                    {"x": 12, "y": 8},
                    {"x": 12, "y": 3},
                    {"x": 13, "y": 2},
                    {"x": 14, "y": 2},
                    {"x": 14, "y": 0},
                ],
                "inner_points": [
                    [
                        {"x": 1, "y": 1},
                        {"x": 2, "y": 0},
                        {"x": 11, "y": 0},
                        {"x": 12, "y": 1},
                        {"x": 12, "y": 7},
                        {"x": 11, "y": 8},
                        {"x": 2, "y": 8},
                        {"x": 1, "y": 7},
                    ]
                ],
                "accuracy": 1,
            },
        ]

        manager = AnnotationManager.from_binary_mask(data, include_inner_contours=True)
        actual = manager.to_dict(features=[])
        for dict_object in actual:
            dict_object.pop("id")
        np.testing.assert_array_equal(actual, expected)

    def test_from_binary_mask_to_dict_polygon_inside_donut_inner_contour_false(self):
        data = np.array(
            [
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            ]
        )

        expected = [
            {
                "label": "",
                "children": [],
                "parents": [],
                "type": "polygon",
                "points": [
                    {"x": 1, "y": 0},
                    {"x": 1, "y": 8},
                    {"x": 12, "y": 8},
                    {"x": 12, "y": 3},
                    {"x": 13, "y": 2},
                    {"x": 14, "y": 2},
                    {"x": 14, "y": 0},
                ],
                "inner_points": [],
                "accuracy": 1,
            },
        ]

        manager = AnnotationManager.from_binary_mask(data, include_inner_contours=False)
        actual = manager.to_dict(features=[])
        for dict_object in actual:
            dict_object.pop("id")
        np.testing.assert_array_equal(actual, expected)

    def test_labeled_mask_classes_to_dict_without_inner(self):
        data = np.array(
            [
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            ]
        )

        expected = [
            {
                "label": "alive",
                "children": [],
                "parents": [],
                "type": "polygon",
                "points": [
                    {"x": 1, "y": 0},
                    {"x": 1, "y": 8},
                    {"x": 12, "y": 8},
                    {"x": 12, "y": 3},
                    {"x": 13, "y": 2},
                    {"x": 14, "y": 2},
                    {"x": 14, "y": 0},
                ],
                "inner_points": [],
                "accuracy": 1,
            },
            {
                "label": "dead",
                "children": [],
                "parents": [],
                "type": "polygon",
                "points": [
                    {"x": 4, "y": 3},
                    {"x": 4, "y": 5},
                    {"x": 5, "y": 6},
                    {"x": 8, "y": 6},
                    {"x": 9, "y": 5},
                    {"x": 9, "y": 3},
                ],
                "inner_points": [],
                "accuracy": 1,
            },
        ]

        labels = ["alive", "dead"]
        manager = AnnotationManager.from_labeled_mask(
            data, labels=labels, include_inner_contours=False
        )
        actual = manager.to_dict(features=[])
        for dict_object in actual:
            dict_object.pop("id")
        np.testing.assert_array_equal(actual, expected)

    def test_labeled_mask_classes_to_dict_with_inner(self):
        data = np.array(
            [
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            ]
        )

        expected = [
            {
                "label": "alive",
                "children": [],
                "parents": [],
                "type": "polygon",
                "points": [
                    {"x": 1, "y": 0},
                    {"x": 1, "y": 8},
                    {"x": 12, "y": 8},
                    {"x": 12, "y": 3},
                    {"x": 13, "y": 2},
                    {"x": 14, "y": 2},
                    {"x": 14, "y": 0},
                ],
                "inner_points": [
                    [
                        {"x": 1, "y": 1},
                        {"x": 2, "y": 0},
                        {"x": 11, "y": 0},
                        {"x": 12, "y": 1},
                        {"x": 12, "y": 7},
                        {"x": 11, "y": 8},
                        {"x": 2, "y": 8},
                        {"x": 1, "y": 7},
                    ]
                ],
                "accuracy": 1,
            },
            {
                "label": "dead",
                "children": [],
                "parents": [],
                "type": "polygon",
                "points": [
                    {"x": 4, "y": 3},
                    {"x": 4, "y": 5},
                    {"x": 5, "y": 6},
                    {"x": 8, "y": 6},
                    {"x": 9, "y": 5},
                    {"x": 9, "y": 3},
                ],
                "inner_points": [],
                "accuracy": 1,
            },
        ]

        labels = ["alive", "dead"]
        manager = AnnotationManager.from_labeled_mask(
            data, labels=labels, include_inner_contours=True
        )
        actual = manager.to_dict(features=[])
        for dict_object in actual:
            dict_object.pop("id")
        np.testing.assert_array_equal(actual, expected)

    def test_single_label_include_inner(self):
        data = np.array(
            [
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            ]
        )

        expected = [
            {
                "label": "alive",
                "children": [],
                "parents": [],
                "type": "polygon",
                "points": [
                    {"x": 4, "y": 3},
                    {"x": 4, "y": 5},
                    {"x": 5, "y": 6},
                    {"x": 8, "y": 6},
                    {"x": 9, "y": 5},
                    {"x": 9, "y": 3},
                ],
                "inner_points": [],
                "accuracy": 1,
            },
            {
                "label": "alive",
                "children": [],
                "parents": [],
                "type": "polygon",
                "points": [
                    {"x": 1, "y": 0},
                    {"x": 1, "y": 8},
                    {"x": 12, "y": 8},
                    {"x": 12, "y": 3},
                    {"x": 13, "y": 2},
                    {"x": 14, "y": 2},
                    {"x": 14, "y": 0},
                ],
                "inner_points": [
                    [
                        {"x": 1, "y": 1},
                        {"x": 2, "y": 0},
                        {"x": 11, "y": 0},
                        {"x": 12, "y": 1},
                        {"x": 12, "y": 7},
                        {"x": 11, "y": 8},
                        {"x": 2, "y": 8},
                        {"x": 1, "y": 7},
                    ]
                ],
                "accuracy": 1,
            },
        ]

        label = "alive"
        manager = AnnotationManager.from_labeled_mask(
            data, include_inner_contours=True, labels=label
        )
        actual = manager.to_dict(features=[])
        for dict_object in actual:
            dict_object.pop("id")
        np.testing.assert_array_equal(actual, expected)

    def test_single_label_exclude_inner(self):
        data = np.array(
            [
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            ]
        )

        expected = [
            {
                "label": "alive",
                "children": [],
                "parents": [],
                "type": "polygon",
                "points": [
                    {"x": 1, "y": 0},
                    {"x": 1, "y": 8},
                    {"x": 12, "y": 8},
                    {"x": 12, "y": 3},
                    {"x": 13, "y": 2},
                    {"x": 14, "y": 2},
                    {"x": 14, "y": 0},
                ],
                "inner_points": [],
                "accuracy": 1,
            },
        ]

        label = "alive"
        manager = AnnotationManager.from_labeled_mask(
            data, include_inner_contours=False, labels=label
        )
        actual = manager.to_dict(features=[])
        for dict_object in actual:
            dict_object.pop("id")
        np.testing.assert_array_equal(actual, expected)

    def test_labeled_mask_labels_mismatch(self):
        data = np.array(
            [
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            ]
        )

        labels = ["alive"]

        self.assertRaises(
            ValueError,
            AnnotationManager.from_labeled_mask,
            data,
            labels=labels,
            include_inner_contours=True,
        )

    def test_labeled_mask_multiple_labels_happy_flow(self):
        data = np.array(
            [
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            ]
        )

        labels = ["alive", "dead"]

        expected = [
            {
                "label": "alive",
                "children": [],
                "parents": [],
                "type": "polygon",
                "points": [
                    {"x": 1, "y": 0},
                    {"x": 1, "y": 8},
                    {"x": 12, "y": 8},
                    {"x": 12, "y": 3},
                    {"x": 13, "y": 2},
                    {"x": 14, "y": 2},
                    {"x": 14, "y": 0},
                ],
                "inner_points": [
                    [
                        {"x": 1, "y": 1},
                        {"x": 2, "y": 0},
                        {"x": 11, "y": 0},
                        {"x": 12, "y": 1},
                        {"x": 12, "y": 7},
                        {"x": 11, "y": 8},
                        {"x": 2, "y": 8},
                        {"x": 1, "y": 7},
                    ]
                ],
                "accuracy": 1,
            },
            {
                "label": "dead",
                "children": [],
                "parents": [],
                "type": "polygon",
                "points": [
                    {"x": 4, "y": 3},
                    {"x": 4, "y": 5},
                    {"x": 5, "y": 6},
                    {"x": 8, "y": 6},
                    {"x": 9, "y": 5},
                    {"x": 9, "y": 3},
                ],
                "inner_points": [],
                "accuracy": 1,
            },
        ]

        manager = AnnotationManager.from_labeled_mask(
            data, include_inner_contours=True, labels=labels
        )
        actual = manager.to_dict(features=[])
        for dict_object in actual:
            dict_object.pop("id")
        np.testing.assert_array_equal(actual, expected)

    def test_labeled_mask_multiple_labels_but_missing_unique_values(self):
        data = np.array(
            [
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            ]
        )

        labels = ["alive", "dead", "more"]

        expected = [
            {
                "label": "alive",
                "children": [],
                "parents": [],
                "type": "polygon",
                "points": [
                    {"x": 1, "y": 0},
                    {"x": 1, "y": 8},
                    {"x": 12, "y": 8},
                    {"x": 12, "y": 3},
                    {"x": 13, "y": 2},
                    {"x": 14, "y": 2},
                    {"x": 14, "y": 0},
                ],
                "inner_points": [
                    [
                        {"x": 1, "y": 1},
                        {"x": 2, "y": 0},
                        {"x": 11, "y": 0},
                        {"x": 12, "y": 1},
                        {"x": 12, "y": 7},
                        {"x": 11, "y": 8},
                        {"x": 2, "y": 8},
                        {"x": 1, "y": 7},
                    ]
                ],
                "accuracy": 1,
            },
            {
                "label": "dead",
                "children": [],
                "parents": [],
                "type": "polygon",
                "points": [
                    {"x": 4, "y": 3},
                    {"x": 4, "y": 5},
                    {"x": 5, "y": 6},
                    {"x": 8, "y": 6},
                    {"x": 9, "y": 5},
                    {"x": 9, "y": 3},
                ],
                "inner_points": [],
                "accuracy": 1,
            },
        ]

        manager = AnnotationManager.from_labeled_mask(
            data, include_inner_contours=True, labels=labels
        )
        actual = manager.to_dict(features=[])
        for dict_object in actual:
            dict_object.pop("id")
        np.testing.assert_array_equal(actual, expected)

    def test_labeled_mask_multiple_labels_but_missing_unique_values_with_gap(self):
        data = np.array(
            [
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 1, 0, 0, 3, 3, 3, 3, 3, 3, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 3, 3, 3, 3, 3, 3, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 3, 3, 3, 3, 3, 3, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            ]
        )

        labels = ["alive", "gap", "dead"]

        expected = [
            {
                "label": "alive",
                "children": [],
                "parents": [],
                "type": "polygon",
                "points": [
                    {"x": 1, "y": 0},
                    {"x": 1, "y": 8},
                    {"x": 12, "y": 8},
                    {"x": 12, "y": 3},
                    {"x": 13, "y": 2},
                    {"x": 14, "y": 2},
                    {"x": 14, "y": 0},
                ],
                "inner_points": [
                    [
                        {"x": 1, "y": 1},
                        {"x": 2, "y": 0},
                        {"x": 11, "y": 0},
                        {"x": 12, "y": 1},
                        {"x": 12, "y": 7},
                        {"x": 11, "y": 8},
                        {"x": 2, "y": 8},
                        {"x": 1, "y": 7},
                    ]
                ],
                "accuracy": 1,
            },
            {
                "label": "dead",
                "children": [],
                "parents": [],
                "type": "polygon",
                "points": [
                    {"x": 4, "y": 3},
                    {"x": 4, "y": 5},
                    {"x": 5, "y": 6},
                    {"x": 8, "y": 6},
                    {"x": 9, "y": 5},
                    {"x": 9, "y": 3},
                ],
                "inner_points": [],
                "accuracy": 1,
            },
        ]

        manager = AnnotationManager.from_labeled_mask(
            data, include_inner_contours=True, labels=labels
        )
        actual = manager.to_dict(features=[])
        for dict_object in actual:
            dict_object.pop("id")
        np.testing.assert_array_equal(actual, expected)
