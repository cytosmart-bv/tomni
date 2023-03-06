from unittest import TestCase

import cv2
import numpy as np

from tomni.annotation_manager.annotations.point.main import Point
from tomni.annotation_manager.annotations.polygon.main import Polygon

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
        actual = self.manager.filter(
            feature="area", min_val=500, max_val=5000000, inplace=True
        )
        expected_n_items = 2

        self.assertIsInstance(actual, AnnotationManager)
        self.assertEqual(len(self.manager), expected_n_items)
        self.assertEqual(len(self.manager), expected_n_items)

    def test_filter_chained(self):
        actual = self.manager.filter(
            feature="area", min_val=0, max_val=500, inplace=True
        ).filter(feature="perimeter", min_val=11, max_val=12, inplace=True)
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
        mask = np.ones((3000, 3000), dtype=np.uint8)

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
                "points": [
                    {"x": 1, "y": 3},
                    {"x": 2, "y": 3},
                    {"x": 3, "y": 5},
                    {"x": 5, "y": 3},
                    {"x": 3, "y": 1},
                ],
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
                "points": [
                    {"x": 10, "y": 30},
                    {"x": 20, "y": 30},
                    {"x": 30, "y": 50},
                    {"x": 50, "y": 30},
                    {"x": 30, "y": 10},
                ],
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
                "points": [
                    {"x": 100, "y": 300},
                    {"x": 200, "y": 300},
                    {"x": 300, "y": 500},
                    {"x": 500, "y": 300},
                    {"x": 300, "y": 100},
                ],
            },
            {
                "id": "132132132123132",
                "label": "star",
                "children": [],
                "parents": [],
                "area": 7000000.0,
                "circularity": 0.64,
                "convex_hull_area": 8000000.0,
                "perimeter": 11721.35,
                "roundness": 0.56,
                "type": "polygon",
                "points": [
                    {"x": 1000, "y": 3000},
                    {"x": 2000, "y": 3000},
                    {"x": 3000, "y": 5000},
                    {"x": 5000, "y": 3000},
                    {"x": 3000, "y": 1000},
                ],
            },
        ]
        actual = self.manager.to_dict(mask=mask)

        self.assertEqual(expected, actual)

    def test_to_dict_with_ellipse_mask(self):
        mask = np.zeros((3000, 3000), dtype=np.uint8)
        mask = cv2.ellipse(
            mask,
            center=(50, 50),
            axes=(100, 100),
            angle=0,
            startAngle=0,
            endAngle=360,
            color=1,
            thickness=-1,
        )

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
                "points": [
                    {"x": 1, "y": 3},
                    {"x": 2, "y": 3},
                    {"x": 3, "y": 5},
                    {"x": 5, "y": 3},
                    {"x": 3, "y": 1},
                ],
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
                "points": [
                    {"x": 10, "y": 30},
                    {"x": 20, "y": 30},
                    {"x": 30, "y": 50},
                    {"x": 50, "y": 30},
                    {"x": 30, "y": 10},
                ],
            },
        ]

        actual = self.manager.to_dict(mask=mask)

        self.assertEqual(expected, actual)

    # def assert_output(self, expected_output, result):
    #     # TODO: FIGURE OUT input params
    #     self.assertEqual(len(expected_output), len(result))
    #     for i in range(len(expected_output)):
    #         result_external = result[i][0]
    #         print(result_external)
    #         np.testing.assert_array_equal(result_external, expected_output[i][0])

    #         # Test inner contours
    #         result_internal_list = result[i][1]
    #         expected_internal_list = expected_output[i][1]
    #         self.assertEqual(len(expected_internal_list), len(result_internal_list))
    #         for result_internal, expected_internal in zip(
    #             result_internal_list, expected_internal_list
    #         ):
    #     np.testing.assert_array_equal(result_internal, expected_internal)

    def test_init_from_labeled_to_labeled_mask_wo_inner_contours(self):
        data = np.array(
            [
                [0, 5, 5, 0, 0, 0],
                [0, 5, 5, 0, 0, 0],
                [1, 1, 1, 0, 0, 0],
                [0, 2, 0, 0, 0, 0],
                [0, 2, 2, 0, 0, 0],
                [0, 2, 2, 2, 0, 0],
                [0, 2, 2, 2, 2, 0],
            ]
        )
        manager = AnnotationManager.from_labeled_mask(data)

        n_labels = 5
        self.assertEqual(len(manager), n_labels)

        expected_output = [
            [[[0, 2]], [[2, 2]]],  # 1
            [[[1, 3]], [[1, 6]], [[4, 6]]],  # 2
            [[[1, 0]], [[1, 1]], [[2, 1]], [[2, 0]]],  # 5
        ]
        actual = manager.to_labeled_mask()

        np.testing.assert_array_equal(actual, data)

    # def init_from_labeled_test_return_inner_no_inner(self):
    #     data = array(
    #         [
    #             [0, 5, 5, 0, 0, 0],
    #             [0, 5, 5, 0, 0, 0],
    #             [1, 1, 1, 0, 0, 0],
    #             [0, 2, 0, 0, 0, 0],
    #             [0, 2, 2, 0, 0, 0],
    #             [0, 2, 2, 2, 0, 0],
    #             [0, 2, 2, 2, 2, 0],
    #         ]
    #     )

    #     expected_output = [
    #         [[[[0, 2]], [[2, 2]]], []],  # 1
    #         [[[[1, 3]], [[1, 6]], [[4, 6]]], []],  # 2
    #         [[[[1, 0]], [[1, 1]], [[2, 1]], [[2, 0]]], []],  # 5
    #     ]

    #     result = labels2contours(data, return_inner_contours=True)
    #     self.assert_output(expected_output, result)

    # def init_from_labeled_test_donut(self):
    #     data = array(
    #         [
    #             [0, 0, 0, 0, 0, 0],
    #             [0, 0, 0, 0, 0, 0],
    #             [0, 0, 0, 0, 0, 0],
    #             [0, 2, 2, 2, 2, 0],
    #             [0, 2, 0, 0, 2, 0],
    #             [0, 2, 0, 0, 2, 0],
    #             [0, 2, 2, 2, 2, 0],
    #         ]
    #     )

    #     expected_output = [
    #         [
    #             # External contour
    #             [[[1, 3]], [[1, 6]], [[4, 6]], [[4, 3]]],
    #             # All the internal contours
    #             [
    #                 # Corners are interpolated as being diagonal
    #                 # hench the 8 points for something that looks like a square
    #                 [
    #                     [[1, 4]],
    #                     [[2, 3]],
    #                     [[3, 3]],
    #                     [[4, 4]],
    #                     [[4, 5]],
    #                     [[3, 6]],
    #                     [[2, 6]],
    #                     [[1, 5]],
    #                 ]
    #             ],
    #         ],
    #     ]

    #     result = labels2contours(data, return_inner_contours=True)
    #     self.assert_output(expected_output, result)
