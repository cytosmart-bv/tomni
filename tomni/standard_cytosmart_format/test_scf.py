import unittest
from .main import SCFJson


class TestSCFJson(unittest.TestCase):
    def setUp(self) -> None:
        self.scf_json1 = SCFJson(
            [
                {
                    "type": "polygon",
                    "points": [
                        {"x": 0, "y": 10},
                        {"x": 10, "y": 10},
                        {"x": 10, "y": 0},
                        {"x": 0, "y": 0},
                    ],
                    "id": "unicorn",
                },
                {
                    "type": "ellipse",
                    "center": {"x": 20, "y": 30},
                    "radiusX": 10,
                    "radiusY": 12,
                    "angleOfRotation": 0,
                    "id": "unicorn1",
                },
            ]
        )
        self.scf_json2 = SCFJson(
            [
                {
                    "type": "polygon",
                    "points": [
                        {"x": 0, "y": 10},
                        {"x": 10, "y": 10},
                        {"x": 10, "y": 0},
                        {"x": 0, "y": 0},
                    ],
                    "id": "unicorn2",
                },
                {
                    "type": "ellipse",
                    "center": {"x": 20, "y": 30},
                    "radiusX": 10,
                    "radiusY": 12,
                    "angleOfRotation": 0,
                    "id": "unicorn3",
                },
            ]
        )

        self.scf_json3 = SCFJson(
            [
                {
                    "type": "polygon",
                    "points": [
                        {"x": 0, "y": 20},
                        {"x": 20, "y": 20},
                        {"x": 20, "y": 0},
                        {"x": 0, "y": 0},
                    ],
                    "id": "unicorn4",
                },
                {
                    "type": "ellipse",
                    "center": {"x": 20, "y": 30},
                    "radiusX": 20,
                    "radiusY": 40,
                    "angleOfRotation": 0,
                    "id": "unicorn5",
                },
            ]
        )

    def test_validate_incorrect_both(self):
        with self.assertRaises(ValueError) as context:
            SCFJson(
                [
                    {
                        "points": [
                            {"x": 0, "y": 20},
                            {"x": 20, "y": 20},
                            {"x": 20, "y": 0},
                            {"x": 0, "y": 0},
                        ],
                        "id": "unicorn4",
                    }
                ]
            )
            self.assertTrue(
                "object is not in the Standard CytoSMART Format", context.exception
            )

    def test_len(self):
        assert len(self.scf_json1) == 2
        assert len(self.scf_json2) == 2
        assert len(self.scf_json3) == 2

    def test_add(self):
        expected_scf = SCFJson(
            [
                {
                    "type": "polygon",
                    "points": [
                        {"x": 0, "y": 10},
                        {"x": 10, "y": 10},
                        {"x": 10, "y": 0},
                        {"x": 0, "y": 0},
                    ],
                    "area": 100,
                },
                {
                    "type": "polygon",
                    "points": [
                        {"x": 0, "y": 10},
                        {"x": 10, "y": 10},
                        {"x": 10, "y": 0},
                        {"x": 0, "y": 0},
                    ],
                    "area": 100,
                },
                {
                    "type": "ellipse",
                    "center": {"x": 20, "y": 30},
                    "radiusX": 10,
                    "radiusY": 12,
                    "angleOfRotation": 0,
                    "area": 376.99111843077515,
                },
                {
                    "type": "ellipse",
                    "center": {"x": 20, "y": 30},
                    "radiusX": 10,
                    "radiusY": 12,
                    "angleOfRotation": 0,
                    "area": 376.99111843077515,
                },
            ]
        )
        new_scf = self.scf_json1 + self.scf_json2
        assert new_scf == expected_scf

    def test_equal(self):
        assert self.scf_json1 == self.scf_json1
        assert self.scf_json1 == self.scf_json2
        assert self.scf_json2 == self.scf_json2
        assert self.scf_json3 == self.scf_json3

    def test_not_equal(self):
        assert self.scf_json1 != self.scf_json3
        assert self.scf_json2 != self.scf_json3
