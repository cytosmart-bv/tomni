from unittest import TestCase
from .main import crop_json

class TestRandomCropBbox(TestCase):
    def test_ellipse_x_movement(self):
        input_json = [
            {
                "type": "ellipse",
                "center": {"x": 2, "y": 3},
                "radiusX": 5,
                "radiusY": 5,
                "angleOfRotation": 0,
            },
            {"type": "ellipse", "center": {"x": 4, "y": 7}, "radiusX": 6, "radiusY": 6},
        ]

        inputDim = (5, 6)
        x_move = 2
        y_move = 0

        expected_json = [
            {
                "type": "ellipse",
                "center": {"x": 0, "y": 3},
                "radiusX": 5,
                "radiusY": 5,
                "angleOfRotation": 0,
            }
        ]

        result_json = crop_json(input_json,x_move, y_move, inputDim)
        self.assertListEqual(result_json, expected_json)

    def test_ellipse_xy_movement(self):
        

        input_json = [
            {
                "type": "ellipse",
                "center": {"x": 2, "y": 3},
                "radiusX": 5,
                "radiusY": 5,
                "angleOfRotation": 0,
            },
            {"type": "ellipse", "center": {"x": 4, "y": 8}, "radiusX": 6, "radiusY": 6},
        ]

        inputDim = (5, 6)
        x_move = 2 
        y_move = 1

        expected_json = [
            {
                "type": "ellipse",
                "center": {"x": 0, "y": 2},
                "radiusX": 5,
                "radiusY": 5,
                "angleOfRotation": 0,
            }
        ]

        result_json = crop_json(input_json,x_move, y_move, inputDim)

        self.assertListEqual(result_json, expected_json)

        expected_input_json = [
            {
                "type": "ellipse",
                "center": {"x": 2, "y": 3},
                "radiusX": 5,
                "radiusY": 5,
                "angleOfRotation": 0,
            },
            {"type": "ellipse", "center": {"x": 4, "y": 8}, "radiusX": 6, "radiusY": 6},
        ]

        self.assertListEqual(input_json, expected_input_json)
    
    def test_polygon_x_movement(self):
    
        # [p, bx, by, bw, bh, c1, c2, c3]
        input_json = [
            {
                "type": "polygon",
                "points": [
                    {"x": 0, "y": 2},
                    {"x": 2, "y": 2},
                    {"x": 2, "y": 0},
                    {"x": 0, "y": 2},
                ],
            },
            {
                "type": "polygon",
                "points": [
                    {"x": 4, "y": 6},
                    {"x": 6, "y": 6},
                    {"x": 6, "y": 4},
                    {"x": 4, "y": 6},
                ],
            },
        ]

        inputDim = (5, 6)
        x_move = 2 
        y_move = 0

        expected_json = [
            {
                "type": "polygon",
                "points": [
                    {"x": 2, "y": 6},
                    {"x": 4, "y": 6},
                    {"x": 4, "y": 4},
                    {"x": 2, "y": 6},
                ],
            }
        ]

        expected_input_json = [
            {
                "type": "polygon",
                "points": [
                    {"x": 0, "y": 2},
                    {"x": 2, "y": 2},
                    {"x": 2, "y": 0},
                    {"x": 0, "y": 2},
                ],
            },
            {
                "type": "polygon",
                "points": [
                    {"x": 4, "y": 6},
                    {"x": 6, "y": 6},
                    {"x": 6, "y": 4},
                    {"x": 4, "y": 6},
                ],
            },
        ]
        result_json = crop_json(input_json,x_move, y_move, inputDim)
        self.assertListEqual(result_json, expected_json)

        self.assertEqual(len(input_json), len(expected_input_json))
        for i in range(len(input_json)):
            self.assertDictEqual(input_json[i], expected_input_json[i])

    def test_polygon_xy_movement(self):

        input_json = [
            {
                "type": "polygon",
                "points": [
                    {"x": 0, "y": 2},
                    {"x": 2, "y": 2},
                    {"x": 2, "y": 0},
                    {"x": 0, "y": 2},
                ],
            },
            {
                "type": "polygon",
                "points": [
                    {"x": 4, "y": 6},
                    {"x": 6, "y": 6},
                    {"x": 6, "y": 4},
                    {"x": 4, "y": 6},
                ],
            },
        ]

        inputDim = (5, 6)
        x_move = 2
        y_move = 1
        
        expected_json = [
            {
                "type": "polygon",
                "points": [
                    {"x": 2, "y": 5},
                    {"x": 4, "y": 5},
                    {"x": 4, "y": 3},
                    {"x": 2, "y": 5},
                ],
            }
        ]

        result_json = crop_json(input_json,x_move, y_move,  inputDim)
        self.assertListEqual(result_json, expected_json)

    def test_expected_polygon_no_crop(self):

        input_json = [
            {
                "type": "polygon",
                "points": [
                    {"x": 0, "y": 2},
                    {"x": 2, "y": 2},
                    {"x": 2, "y": 0},
                    {"x": 0, "y": 2},
                ],
            },
            {
                "type": "polygon",
                "points": [
                    {"x": 4, "y": 6},
                    {"x": 6, "y": 6},
                    {"x": 6, "y": 4},
                    {"x": 4, "y": 6},
                ],
            },
        ]

        inputDim = (10, 10)
        x_move = 0
        y_move = 0

        expected_json = [
            {
                "type": "polygon",
                "points": [
                    {"x": 0, "y": 2},
                    {"x": 2, "y": 2},
                    {"x": 2, "y": 0},
                    {"x": 0, "y": 2},
                ],
            },
            {
                "type": "polygon",
                "points": [
                    {"x": 4, "y": 6},
                    {"x": 6, "y": 6},
                    {"x": 6, "y": 4},
                    {"x": 4, "y": 6},
                ],
            },
        ]

        result_json = crop_json(input_json, x_move, y_move, inputDim)
        self.assertListEqual(result_json, expected_json)

    def test_poly_GONE(self):
        input_json = [
            {
                "type": "polygon",
                "points": [
                    {"x": 0, "y": 2},
                    {"x": 2, "y": 2},
                    {"x": 2, "y": 0},
                    {"x": 0, "y": 2},
                ],
            },
            {
                "type": "polygon",
                "points": [
                    {"x": 4, "y": 6},
                    {"x": 6, "y": 6},
                    {"x": 6, "y": 4},
                    {"x": 4, "y": 6},
                ],
            },
        ]

        inputDim = (2, 2)
        x_move = 8
        y_move = 0

        expected_json = []

        result_json = crop_json(input_json,x_move, y_move,  inputDim)
        self.assertListEqual(result_json, expected_json)

