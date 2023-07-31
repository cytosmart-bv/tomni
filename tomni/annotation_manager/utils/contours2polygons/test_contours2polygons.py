from unittest import TestCase

from tomni.annotation_manager.utils.contours2polygons import contours2polygons
from tomni.annotation_manager.annotations import Polygon, Point
import numpy as np
import uuid


class TestContours2Polygons(TestCase):
    def test_happy_flow(self) -> None:
        contours = np.array(
            [[[0, 0], [10, 0], [100, 0], [100, 100], [50, 100], [0, 100]]]
        )
        polygons = contours2polygons(contours, None)

        expected = [
            Polygon(
                label="",
                id=str(uuid.uuid4()),
                children=[],
                parents=[],
                points=[
                    Point(0, 0),
                    Point(10, 0),
                    Point(100, 0),
                    Point(100, 100),
                    Point(50, 100),
                    Point(0, 100),
                ],
                inner_points=[],
            )
        ]

        self.assertEqual(polygons, expected)

    def test_happy_flow_label(self) -> None:
        contours = np.array(
            [[[0, 0], [10, 0], [100, 0], [100, 100], [50, 100], [0, 100]]]
        )
        polygons = contours2polygons(contours, None, label="labelled")

        expected = [
            Polygon(
                label="labelled",
                id=str(uuid.uuid4()),
                children=[],
                parents=[],
                points=[
                    Point(0, 0),
                    Point(10, 0),
                    Point(100, 0),
                    Point(100, 100),
                    Point(50, 100),
                    Point(0, 100),
                ],
                inner_points=[],
            )
        ]

        self.assertEqual(polygons, expected)

    def test_happy_flow_hierarchy(self) -> None:
        contours = [
            np.array([[[1, 1]], [[1, 8]], [[7, 7]], [[7, 8]], [[7, 1]]]),
            [
                np.array(
                    [
                        [[2, 3]],
                        [[3, 2]],
                        [[5, 2]],
                        [[6, 3]],
                        [[6, 6]],
                        [[5, 7]],
                        [[3, 7]],
                        [[2, 6]],
                    ]
                )
            ],
        ]

        hierarchy = np.array(
            [
                [
                    [-1, -1, 1, -1],
                    [-1, -1, -1, 0],
                ]
            ]
        )

        polygons = contours2polygons(
            contours=contours, hierarchy=hierarchy, label="labelled"
        )

        expected = [
            Polygon(
                label="labelled",
                id=str(uuid.uuid4()),
                children=[],
                parents=[],
                points=[
                    Point(1, 1),
                    Point(1, 8),
                    Point(7, 7),
                    Point(7, 8),
                    Point(7, 1),
                ],
                inner_points=[
                    [
                        Point(2, 3),
                        Point(3, 2),
                        Point(5, 2),
                        Point(6, 3),
                        Point(6, 6),
                        Point(5, 7),
                        Point(3, 7),
                        Point(2, 6),
                    ]
                ],
            ),
        ]

        self.assertEqual(polygons, expected)

    def test_happy_flow_multiple_contours(self) -> None:
        contours = np.array(
            [
                [[0, 0], [10, 0], [100, 0], [100, 100], [50, 100], [0, 100]],
                [[0, 0], [10, 0], [200, 0], [200, 100], [50, 100], [0, 100]],
            ]
        )
        polygons = contours2polygons(contours, None, label="labelled")

        expected = [
            Polygon(
                label="labelled",
                id=str(uuid.uuid4()),
                children=[],
                parents=[],
                points=[
                    Point(0, 0),
                    Point(10, 0),
                    Point(100, 0),
                    Point(100, 100),
                    Point(50, 100),
                    Point(0, 100),
                ],
                inner_points=[],
            ),
            Polygon(
                label="labelled",
                id=str(uuid.uuid4()),
                children=[],
                parents=[],
                points=[
                    Point(0, 0),
                    Point(10, 0),
                    Point(200, 0),
                    Point(200, 100),
                    Point(50, 100),
                    Point(0, 100),
                ],
                inner_points=[],
            ),
        ]

        self.assertEqual(polygons, expected)

    def test_include_inner_and_hierarchy(self) -> None:
        contours = np.array(
            [[[0, 0], [10, 0], [100, 0], [100, 100], [50, 100], [0, 100]]]
        )
        hierarchy = np.array(
            [
                [
                    [-1, -1, 1, -1],
                    [-1, -1, -1, 0],
                ]
            ]
        )

        polygons = contours2polygons(
            contours=contours, include_inner_contours=False, hierarchy=hierarchy
        )

        expected = [
            Polygon(
                label="",
                id=str(uuid.uuid4()),
                children=[],
                parents=[],
                points=[
                    Point(0, 0),
                    Point(10, 0),
                    Point(100, 0),
                    Point(100, 100),
                    Point(50, 100),
                    Point(0, 100),
                ],
                inner_points=[],
            )
        ]

        self.assertEqual(polygons, expected)

    def test_external_hierarchy_include_inner_contours_true(self) -> None:
        contours = np.array(
            [[[0, 0], [10, 0], [100, 0], [100, 100], [50, 100], [0, 100]]]
        )
        hierarchy = np.array([[[1, -1, -1, -1]]])

        polygons = contours2polygons(
            contours=contours, include_inner_contours=True, hierarchy=hierarchy
        )

        expected = [
            Polygon(
                label="",
                id=str(uuid.uuid4()),
                children=[],
                parents=[],
                points=[
                    Point(0, 0),
                    Point(10, 0),
                    Point(100, 0),
                    Point(100, 100),
                    Point(50, 100),
                    Point(0, 100),
                ],
                inner_points=[],
            )
        ]

        self.assertEqual(polygons, expected)

    def test_include_inner_and_hierarchy_mismatch(self) -> None:
        contours = np.array(
            [[[0, 0], [10, 0], [100, 0], [100, 100], [50, 100], [0, 100]]]
        )

        self.assertRaises(
            ValueError,
            contours2polygons,
            contours,
            include_inner_contours=True,
            hierarchy=None,
        )

    def test_too_few_points(self) -> None:
        contours = np.array([[[0, 0], [10, 0], [100, 0], [100, 100]]])
        polygons = contours2polygons(contours, None)

        expected = []

        self.assertEqual(polygons, expected)
