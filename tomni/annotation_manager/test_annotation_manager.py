from unittest import TestCase

import numpy as np

from tomni.annotation_manager.annotations.point.main import Point
from tomni.annotation_manager.annotations.polygon.main import Polygon

from .main import AnnotationManager


class TestAnnotationManager(TestCase):
    def setUp(self) -> None:
        self.cdf = AnnotationManager(
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
        del self.cdf

    def test_filter_single(self):
        actual = self.cdf.filter(feature="area", min_val=500, max_val=5000000)
        expected_n_items = 2

        self.assertIsInstance(actual, list)
        self.assertEqual(len(actual), expected_n_items)

    def test_filter_single_inplace(self):
        actual = self.cdf.filter(
            feature="area", min_val=500, max_val=5000000, inplace=True
        )
        expected_n_items = 2

        self.assertIsInstance(actual, AnnotationManager)
        self.assertEqual(len(self.cdf), expected_n_items)
        self.assertEqual(len(self.cdf), expected_n_items)

    def test_filter_chained(self):
        actual = self.cdf.filter(
            feature="area", min_val=0, max_val=500, inplace=True
        ).filter(feature="perimeter", min_val=11, max_val=12, inplace=True)
        expected_n_items = 1

        self.assertIsInstance(actual, AnnotationManager)
        self.assertEqual(len(self.cdf), expected_n_items)
