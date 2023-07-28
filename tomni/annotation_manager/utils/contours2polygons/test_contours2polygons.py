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
