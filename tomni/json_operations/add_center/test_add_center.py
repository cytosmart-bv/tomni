from unittest import TestCase
import numpy as np
from .main import add_center


class TestAddCenterJson(TestCase):
    def test_happy_flow(self):
        json_object = {
            "type": "polygon",
            "points": [
                {"x": 500, "y": 50},
                {"x": 500, "y": 99},
                {"x": 539, "y": 99},
                {"x": 539, "y": 50},
            ],
            "id": "unicorn",
            "parents": [],
            "children": [],
        }

        expected_result = {
            "type": "polygon",
            "points": [
                {"x": 500, "y": 50},
                {"x": 500, "y": 99},
                {"x": 539, "y": 99},
                {"x": 539, "y": 50},
            ],
            "id": "unicorn",
            "parents": [],
            "children": [],
            "center": {"x": 519, "y": 74},
        }

        add_center(json_object)

        self.assertDictEqual(json_object, expected_result)

    def test_single_point(self):
        json_object = {
            "type": "polygon",
            "points": [{"x": 500, "y": 50},],
            "id": "unicorn",
            "parents": [],
            "children": [],
        }

        expected_result = {
            "type": "polygon",
            "points": [{"x": 500, "y": 50},],
            "id": "unicorn",
            "parents": [],
            "children": [],
            "center": {"x": 500, "y": 50},
        }

        add_center(json_object)

        self.assertDictEqual(json_object, expected_result)

    def test_circle(self):
        json_object = {
            "type": "ellipse",
            "center": {"x": 20, "y": 30},
            "radiusX": 10,
            "radiusY": 10,
            "angleOfRotation": 0,
            "id": "unicorn",
        }

        expected_result = {
            "type": "ellipse",
            "center": {"x": 20, "y": 30},
            "radiusX": 10,
            "radiusY": 10,
            "angleOfRotation": 0,
            "id": "unicorn",
        }

        add_center(json_object)

        self.assertDictEqual(json_object, expected_result)
