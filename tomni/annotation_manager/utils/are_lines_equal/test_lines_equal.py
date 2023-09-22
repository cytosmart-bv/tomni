from unittest import TestCase

from tomni.annotation_manager.annotations.point import Point
from .main import are_lines_equal


class TestLineEqual(TestCase):
    def test_happy_flow(self):
        line_1 = [Point(1, 1), Point(1, 30), Point(30, 30), Point(30, 1)]
        line_2 = [Point(1, 1), Point(1, 30), Point(30, 30), Point(30, 1)]

        self.assertTrue(are_lines_equal(line_1, line_2))

    def test_rotated(self):
        line_1 = [Point(1, 1), Point(1, 30), Point(30, 30), Point(30, 1)]
        line_2 = [Point(30, 30), Point(30, 1), Point(1, 1), Point(1, 30)]

        self.assertTrue(are_lines_equal(line_1, line_2))

    def test_different(self):
        line_1 = [Point(1, 1), Point(1, 30), Point(30, 30), Point(30, 1)]
        line_2 = [Point(30, 30), Point(30, 1), Point(1, 2), Point(1, 30)]

        self.assertFalse(are_lines_equal(line_1, line_2))

    def test_different_length(self):
        line_1 = [Point(1, 1), Point(1, 30), Point(30, 30), Point(30, 1)]
        line_2 = [Point(30, 30), Point(30, 1), Point(1, 1), Point(1, 1), Point(1, 30)]

        self.assertFalse(are_lines_equal(line_1, line_2))
