from unittest import TestCase
import numpy as np
from .main import ellipse2json

class TestEllipse2json(TestCase):
    def test_happy_flow_circle(self):
        expectedResult = {
        "type": "ellipse",
        "center": {"x": 20, "y": 30},
        "radiusX": 10,
        "radiusY": 10,
        "angleOfRotation": 0,
        "id": "unicorn",
    }

        result = ellipse2json(20, 30, 10)
        result["id"] = "unicorn"

        self.assertDictEqual(result, expectedResult)

    def test_happy_flow_ellipse(self):
        expectedResult = {
        "type": "ellipse",
        "center": {"x": 20, "y": 30},
        "radiusX": 10,
        "radiusY": 15,
        "angleOfRotation": 0.98,
        "id": "unicorn",
    }

        result = ellipse2json(20, 30, 10, 15, 0.98)
        result["id"] = "unicorn"

        self.assertDictEqual(result, expectedResult)