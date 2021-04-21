from unittest import TestCase
from .main import add_circularity
import math


class TestScaleObject(TestCase):
    def test_square(self):
        input_json_object = {
            "type": "polygon",
            "points": [
                {"x": 5000, "y": 0},
                {"x": 5000, "y": 10000},
                {"x": 15000, "y": 10000},
                {"x": 15000, "y": 0},
            ],
            "id": "unicorn",
        }

        expected_json_object = {
            "type": "polygon",
            "points": [
                {"x": 5000, "y": 0},
                {"x": 5000, "y": 10000},
                {"x": 15000, "y": 10000},
                {"x": 15000, "y": 0},
            ],
            "id": "unicorn",
            "circularity": 2 / math.pi,
        }

        add_circularity(input_json_object)
        self.assertAlmostEqual(
            input_json_object["circularity"], expected_json_object["circularity"], 5
        )

        # check everything except circularity
        input_json_object["circularity"] = 0
        expected_json_object["circularity"] = 0
        self.assertDictEqual(input_json_object, expected_json_object)

    def test_unknown_type(self):
        input_json_object = {
            "type": "unicornType",
        }
        with self.assertRaises(ValueError):
            add_circularity(input_json_object)
