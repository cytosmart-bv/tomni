from unittest import TestCase

from tomni.annotation_manager.utils.contours2polygons.main import (
    _is_approx_rectangle,
    _add_point,
    contours2polygons,
)
from tomni.annotation_manager.annotations import Polygon, Point
import numpy as np
import uuid


class TestContours2Polygons(TestCase):
    def test_happy_flow(self) -> None:
        contours = (
            np.array(
                [[[0, 0]], [[10, 0]], [[100, 0]], [[100, 100]], [[50, 100]], [[0, 100]]]
            ),
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
        contours = (
            np.array(
                [[[0, 0]], [[10, 0]], [[100, 0]], [[100, 100]], [[50, 100]], [[0, 100]]]
            ),
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
        contours = (
            np.array([[[1, 1]], [[1, 8]], [[7, 7]], [[7, 8]], [[7, 1]]]),
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
                ],
            ),
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
            contours=contours,
            hierarchy=hierarchy,
            include_inner_contours=True,
            label="labelled",
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
        contours = (
            np.array(
                [[[0, 0]], [[10, 0]], [[100, 0]], [[100, 100]], [[50, 100]], [[0, 100]]]
            ),
            np.array(
                [[[0, 0]], [[10, 0]], [[200, 0]], [[200, 100]], [[50, 100]], [[0, 100]]]
            ),
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
        contours = (
            np.array(
                [[[0, 0]], [[10, 0]], [[100, 0]], [[100, 100]], [[50, 100]], [[0, 100]]]
            ),
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
        contours = (
            np.array(
                [[[0, 0]], [[10, 0]], [[100, 0]], [[100, 100]], [[50, 100]], [[0, 100]]]
            ),
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
        contours = (
            np.array(
                [[[0, 0]], [[10, 0]], [[100, 0]], [[100, 100]], [[50, 100]], [[0, 100]]]
            ),
        )

        self.assertRaises(
            ValueError,
            contours2polygons,
            contours,
            include_inner_contours=True,
            hierarchy=None,
        )

    def test_too_few_points(self) -> None:
        contours = np.array(
            [[[0, 0]], [[5, 0]], [[5, 5]], [[0, 5]]],
        )
        polygons = contours2polygons(contours, None)

        expected = []

        self.assertEqual(polygons, expected)

    def test_is_approx_rectangle_true(self) -> None:
        contours = np.array(
            [
                [[0, 0]],
                [[100, 0]],
                [[100, 100]],
                [[0, 100]],
            ],
        )
        polygons = _is_approx_rectangle(contours)

        expected = True

        self.assertEqual(polygons, expected)

    def test_is_approx_rectangle_false(self) -> None:
        contour = np.array(
            [
                [[0, 0]],
                [[50, 25]],
                [[100, 125]],
                [[50, 100]],
            ],
        )
        polygons = _is_approx_rectangle(contour)

        expected = False

        self.assertEqual(polygons, expected)

    def test_is_approx_rectangle_false_diamond(self) -> None:
        contour = np.array(
            [
                [[50, 0]],
                [[0, 50]],
                [[50, 100]],
                [[100, 50]],
            ],
        )
        polygons = _is_approx_rectangle(contour)

        expected = False

        self.assertEqual(polygons, expected)

    def test_add_point(self) -> None:
        contour = np.array(
            [
                [[0, 0]],
                [[50, 0]],
                [[50, 50]],
                [[0, 50]],
            ],
        )
        output = _add_point(contour)

        expected = np.array(
            [
                [[0, 0]],
                [[25, 0]],
                [[50, 0]],
                [[50, 50]],
                [[0, 50]],
            ],
        )

        np.testing.assert_array_equal(output, expected)

    def test_add_point_2(self) -> None:
        contour = np.array(
            [
                [[0, 0]],
                [[100, 0]],
                [[100, 100]],
                [[0, 100]],
            ],
        )
        output = _add_point(contour)

        expected = np.array(
            [
                [[0, 0]],
                [[50, 0]],
                [[100, 0]],
                [[100, 100]],
                [[0, 100]],
            ],
        )

        np.testing.assert_array_equal(output, expected)
