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
                    points=[Point(1, 3), Point(2, 3), Point(3, 5), Point(5, 3), Point(3, 1), Point(2, 2)],
                    id="132132132123132",
                    children=[],
                    parents=[],
                    label="star",
                ),
                Polygon(
                    points=[Point(10, 30), Point(20, 30), Point(30, 50), Point(50, 30), Point(30, 10), Point(20, 20)],
                    id="132132132123132",
                    children=[],
                    parents=[],
                    label="star",
                ),
                Polygon(
                    points=[Point(100, 300), Point(200, 300), Point(300, 500), Point(500, 300), Point(300, 100), Point(200, 200)],
                    id="132132132123132",
                    children=[],
                    parents=[],
                    label="star",
                ),
                Polygon(
                    points=[Point(1000, 3000), Point(2000, 3000), Point(3000, 5000), Point(5000, 3000), Point(3000, 1000), Point(2000, 2000)],
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

    def tearDown(self):
        del self.manager

    def test_filter_single(self):
        actual = self.manager.filter(feature="area", min_val=500, max_val=5000000)
        expected_n_items = 2

        self.assertIsInstance(actual, list)
        self.assertEqual(len(actual), expected_n_items)

    def test_filter_single_inplace(self):
        actual = self.manager.filter(feature="area", min_val=500, max_val=5000000, inplace=True)
        expected_n_items = 2

        self.assertIsInstance(actual, AnnotationManager)
        self.assertEqual(len(self.manager), expected_n_items)
        self.assertEqual(len(self.manager), expected_n_items)

    def test_filter_chained(self):
        actual = self.manager.filter(feature="area", min_val=0, max_val=500, inplace=True).filter(
            feature="perimeter", min_val=11, max_val=12, inplace=True
        )
        expected_n_items = 1

        self.assertIsInstance(actual, AnnotationManager)
        self.assertEqual(len(self.manager), expected_n_items)

    def test_from_json_to_bin_mask_back_to_json(self):
        im_shape = (2072, 2072)
        quadrant_size = im_shape[0] / 4

        am = AnnotationManager(
            [
                Polygon(
                    points=[
                        Point(quadrant_size, quadrant_size),
                        Point(quadrant_size, 2 * quadrant_size),
                        Point(2 * quadrant_size, quadrant_size),
                        Point(2 * quadrant_size, 2 * quadrant_size),
                    ],
                    id="132132132123132",
                    children=[],
                    parents=[],
                    label="star",
                ),
                Polygon(
                    points=[
                        Point(3 * quadrant_size, quadrant_size),
                        Point(3 * quadrant_size, 2 * quadrant_size),
                        Point(4 * quadrant_size, 3 * quadrant_size),
                        Point(4 * quadrant_size, 2 * quadrant_size),
                    ],
                    id="132132132123132",
                    children=[],
                    parents=[],
                    label="star",
                ),
                Polygon(
                    points=[
                        Point(quadrant_size, 3 * quadrant_size),
                        Point(quadrant_size, 4 * quadrant_size),
                        Point(2 * quadrant_size, 4 * quadrant_size),
                        Point(2 * quadrant_size, 3 * quadrant_size),
                    ],
                    id="132132132123132",
                    children=[],
                    parents=[],
                    label="star",
                ),
            ]
        )

        bin_mask = am.to_binary_mask(im_shape)

    def test_to_dict_with_polygon_mask(self):
        mask = {"type": "polygon", "points": [{"x": 0, "y": 0}, {"x": 0, "y": 4000}, {"x": 4000, "y": 4000}, {"x": 4000, "y": 0}]}
        expected = [
            {
                "id": "132132132123132",
                "label": "star",
                "children": [],
                "parents": [],
                "area": 7.0,
                "circularity": 0.64,
                "convex_hull_area": 8.0,
                "perimeter": 11.72,
                "roundness": 0.56,
                "type": "polygon",
                "points": [{"x": 1, "y": 3}, {"x": 2, "y": 3}, {"x": 3, "y": 5}, {"x": 5, "y": 3}, {"x": 3, "y": 1}],
            },
            {
                "id": "132132132123132",
                "label": "star",
                "children": [],
                "parents": [],
                "area": 700.0,
                "circularity": 0.64,
                "convex_hull_area": 800.0,
                "perimeter": 117.21,
                "roundness": 0.56,
                "type": "polygon",
                "points": [{"x": 10, "y": 30}, {"x": 20, "y": 30}, {"x": 30, "y": 50}, {"x": 50, "y": 30}, {"x": 30, "y": 10}],
            },
            {
                "id": "132132132123132",
                "label": "star",
                "children": [],
                "parents": [],
                "area": 70000.0,
                "circularity": 0.64,
                "convex_hull_area": 80000.0,
                "perimeter": 1172.13,
                "roundness": 0.56,
                "type": "polygon",
                "points": [{"x": 100, "y": 300}, {"x": 200, "y": 300}, {"x": 300, "y": 500}, {"x": 500, "y": 300}, {"x": 300, "y": 100}],
            },
        ]
        actual = self.manager.to_dict(mask_json=mask)

        self.assertEqual(expected, actual)

    def test_to_dict_with_ellipse_mask(self):
        mask = AnnotationManager([Ellipse(center=Point(50, 50), radius_x=100, rotation=0, id="", label="", children=[], parents=[])]).to_dict()[0]

        expected = [
            {
                "id": "132132132123132",
                "label": "star",
                "children": [],
                "parents": [],
                "area": 7.0,
                "circularity": 0.64,
                "convex_hull_area": 8.0,
                "perimeter": 11.72,
                "roundness": 0.56,
                "type": "polygon",
                "points": [{"x": 1, "y": 3}, {"x": 2, "y": 3}, {"x": 3, "y": 5}, {"x": 5, "y": 3}, {"x": 3, "y": 1}],
            },
            {
                "id": "132132132123132",
                "label": "star",
                "children": [],
                "parents": [],
                "area": 700.0,
                "circularity": 0.64,
                "convex_hull_area": 800.0,
                "perimeter": 117.21,
                "roundness": 0.56,
                "type": "polygon",
                "points": [{"x": 10, "y": 30}, {"x": 20, "y": 30}, {"x": 30, "y": 50}, {"x": 50, "y": 30}, {"x": 30, "y": 10}],
            },
        ]

        actual = self.manager.to_dict(mask_json=mask)

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
        shape = data.shape
        manager = AnnotationManager.from_labeled_mask(data)

        n_labels = 3
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

        # n_labels = 1
        # self.assertEqual(len(manager), n_labels)

        actual = manager.to_labeled_mask(shape)
        cv2.imwrite("actual.png", actual)

        np.testing.assert_array_equal(actual, data)

    def test_init_from_non_binary_mask_raises(self):
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
        self.assertRaises(AssertionError, AnnotationManager.from_binary_mask, data)

    def test_init_from_labeled_mask_to_binary_mask(self):
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

        n_labels = 3
        self.assertEqual(len(manager), n_labels)

        actual = manager.to_binary_mask(shape)

        np.testing.assert_array_equal(actual, expected)

    def test_to_binary_mask(self):
        polygons = [
            Polygon(
                points=[Point(1, 3), Point(2, 3), Point(3, 5), Point(5, 3), Point(3, 1), Point(2, 2)],
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

    def test_to_labeled_mask(self):
        polygons = [
            Polygon(points=[Point(1, 1), Point(1, 2), Point(2, 2), Point(2, 1)], id="132132132123132", children=[], parents=[], label="star"),
            Polygon(points=[Point(3, 3), Point(3, 5), Point(5, 5), Point(5, 3)], id="132132132123132", children=[], parents=[], label="star"),
        ]

        expected = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0, 0, 0],
                [0, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 2, 2, 2, 0],
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
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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

        manager = AnnotationManager.from_binary_mask(input_mask)
        actual = manager.to_binary_mask(input_mask.shape)

        np.testing.assert_array_equal(input_mask, actual)

    def test_binary_mask_multiple_objects_not_connected_to_labeled_mask_connectivity_4(self):
        connectivity = 4
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
                [0, 0, 0, 0, 0, 2, 2, 2, 0, 0],
                [0, 0, 0, 0, 0, 2, 2, 2, 0, 0],
                [0, 0, 0, 0, 0, 2, 2, 2, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            dtype=np.uint8,
        )

        manager = AnnotationManager.from_binary_mask(input_mask, connectivity=connectivity)
        actual = manager.to_labeled_mask(input_mask.shape)

        np.testing.assert_array_equal(expected, actual)

    def test_binary_mask_multiple_objects_not_connected_to_labeled_mask_connectivity_8(self):
        connectivity = 8
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

        manager = AnnotationManager.from_binary_mask(input_mask, connectivity=connectivity)
        actual = manager.to_labeled_mask(input_mask.shape)

        np.testing.assert_array_equal(expected, actual)
