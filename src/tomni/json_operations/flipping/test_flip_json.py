from unittest import TestCase

from .main import flip_json


class TestFlipPatch(TestCase):
    def test_flips(self):
        input_json = {
            "type": "ellipse",
            "center": {"x": 9, "y": 3},
            "radiusX": 5,
            "radiusY": 5,
            "angleOfRotation": 0,
        }

        result_json = flip_json(input_json, 10)
        expected_json = {
            "type": "ellipse",
            "center": {"x": 9, "y": 6},
            "radiusX": 5,
            "radiusY": 5,
            "angleOfRotation": 0,
        }

        self.assertDictEqual(result_json, expected_json)

    def test_flips_polygon(self):
        input_json = {
            "type": "polygon",
            "points": [{"x": 7, "y": 2}, {"x": 7, "y": 6}, {"x": 12, "y": 5}],
        }
        result_json = flip_json(input_json, 10)
        expected_json = {
            "type": "polygon",
            "points": [{"x": 7, "y": 7}, {"x": 7, "y": 3}, {"x": 12, "y": 4}],
        }
        self.assertDictEqual(result_json, expected_json)

    def test_flips_polygon_inner_points(self):
        input_json = {
            "type": "polygon",
            "points": [{"x": 7, "y": 2}, {"x": 7, "y": 6}, {"x": 12, "y": 5}],
            "inner_points": [
                [{"x": 1, "y": 1}, {"x": 1, "y": 5}],
                [{"x": 2, "y": 1}, {"x": 1, "y": 2}],
            ],
        }
        result_json = flip_json(input_json, 10)
        expected_json = {
            "type": "polygon",
            "points": [{"x": 7, "y": 7}, {"x": 7, "y": 3}, {"x": 12, "y": 4}],
            "inner_points": [
                [{"x": 1, "y": 8}, {"x": 1, "y": 4}],
                [{"x": 2, "y": 8}, {"x": 1, "y": 7}],
            ],
        }
        self.assertDictEqual(result_json, expected_json)

    def test_flips_polygon_inner_points_empty(self):
        input_json = {
            "type": "polygon",
            "points": [{"x": 7, "y": 2}, {"x": 7, "y": 6}, {"x": 12, "y": 5}],
            "inner_points": [],
        }
        result_json = flip_json(input_json, 10)
        expected_json = {
            "type": "polygon",
            "points": [{"x": 7, "y": 7}, {"x": 7, "y": 3}, {"x": 12, "y": 4}],
            "inner_points": [],
        }
        self.assertDictEqual(result_json, expected_json)
