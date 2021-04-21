from unittest import TestCase
from .main import rotate_json


class TestRotatePatch(TestCase):
    def test_rotation_expected_0(self):
        input_json = {
            "type": "ellipse",
            "center": {"x": 9, "y": 3},
            "radiusX": 5,
            "radiusY": 5,
            "angleOfRotation": 0,
        }

        expected_json = {
            "type": "ellipse",
            "center": {"x": 9, "y": 3},
            "radiusX": 5,
            "radiusY": 5,
            "angleOfRotation": 0,
        }

        true_json = rotate_json(input_json, 0, (5, 5))
        self.assertDictEqual(true_json, expected_json)

    def test_rotation_expected_0_polygon(self):
        input_json = {
            "type": "polygon",
            "points": [{"x": 1, "y": 1}, {"x": 1, "y": 5}],
        }

        expected_json = {
            "type": "polygon",
            "points": [{"x": 1, "y": 1}, {"x": 1, "y": 5}],
        }

        true_json = rotate_json(input_json, 0, (5, 5))
        self.assertDictEqual(true_json, expected_json)

    def test_rotation_expected_90(self):
        input_json = {
            "type": "ellipse",
            "center": {"x": 0, "y": 2},
            "radiusX": 5,
            "radiusY": 5,
            "angleOfRotation": 0,
        }

        expected_json = {
            "type": "ellipse",
            "center": {"x": 3, "y": 0},
            "radiusX": 5,
            "radiusY": 5,
            "angleOfRotation": 0,
        }
        true_json = rotate_json(input_json, 90, (6, 5))
        self.assertDictEqual(true_json, expected_json)

    def test_rotation_expected_90_polygon(self):

        input_json = {
            "type": "polygon",
            "points": [{"x": 1, "y": 1}, {"x": 1, "y": 5}],
        }

        expected_json = {
            "type": "polygon",
            "points": [{"x": 4, "y": 1}, {"x": 0, "y": 1}],
        }
        true_json = rotate_json(input_json, 90, (6, 5))

        self.assertDictEqual(true_json, expected_json)

    def test_rotation_expected_180(self):
        input_json = {
            "type": "ellipse",
            "center": {"x": 0, "y": 2},
            "radiusX": 5,
            "radiusY": 5,
            "angleOfRotation": 0,
        }

        expected_json = {
            "type": "ellipse",
            "center": {"x": 4, "y": 3},
            "radiusX": 5,
            "radiusY": 5,
            "angleOfRotation": 0,
        }

        true_json = rotate_json(input_json, 180, (6, 5))
        self.assertDictEqual(true_json, expected_json)

    def test_rotation_expected_180_polygon(self):
        input_json = {
            "type": "polygon",
            "points": [{"x": 1, "y": 1}, {"x": 1, "y": 5}],
        }

        expected_json = {
            "type": "polygon",
            "points": [{"x": 3, "y": 4}, {"x": 3, "y": 0}],
        }
        true_json = rotate_json(input_json, 180, (6, 5))
        self.assertDictEqual(true_json, expected_json)

    def test_rotation_expected_270_polygon(self):
        input_json = {
            "type": "polygon",
            "points": [{"x": 1, "y": 1}, {"x": 1, "y": 4}],
        }

        expected_json = {
            "type": "polygon",
            "points": [{"x": 1, "y": 3}, {"x": 4, "y": 3}],
        }

        true_json = rotate_json(input_json, 270, (6, 5))

        self.assertDictEqual(true_json, expected_json)

    def test_rotation_expected_270(self):
        input_json = {
            "type": "ellipse",
            "center": {"x": 0, "y": 4},
            "radiusX": 5,
            "radiusY": 5,
            "angleOfRotation": 0,
        }

        expected_json = {
            "type": "ellipse",
            "center": {"x": 4, "y": 4},
            "radiusX": 5,
            "radiusY": 5,
            "angleOfRotation": 0,
        }

        true_json = rotate_json(input_json, 270, (6, 5))
        self.assertDictEqual(true_json, expected_json)

    def test_angle_not_multiple_90(self):
        input_json = {
            "type": "ellipse",
            "center": {"x": 9, "y": 3},
            "radiusX": 5,
            "radiusY": 5,
            "angleOfRotation": 0,
        }
        angle = 80
        self.assertRaises(ValueError, rotate_json, input_json, angle, (5, 5))
