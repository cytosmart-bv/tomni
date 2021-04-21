from unittest import TestCase
from .main import json2labels
import numpy as np

class Test_json2labels(TestCase):    
    def test_ellipse(self):
        objects = [{"type": "ellipse",
                    "center": {"x": 5,
                               "y": 4},
                    "radiusX": 2,
                    "radiusY": 3,
                    "angleOfRotation": 0.0}]
        imgSize = (10,10)
        expOut =   [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                    [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
                    [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
                    [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
                    [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
                    [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
                    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        segMap = json2labels(objects, imgSize)
        print(segMap)
        np.testing.assert_array_equal(segMap, expOut)
    
    def test_polygon(self):
        objects = [{"type": "polygon",
                     "points": [
                                {
                                    "x": 2,
                                    "y": 3
                                },
                                {
                                    "x": 5,
                                    "y": 6
                                },
                                {
                                    "x": 2,
                                    "y": 5
                                },
                                {
                                    "x": 7,
                                    "y": 9
                                },
                                {
                                    "x": 4,
                                    "y": 2
                                }
                                ]}]
        imgSize = (10,10)
        expOut =   [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                    [0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
                    [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
                    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]]
        segMap = json2labels(objects, imgSize)
        print(segMap)
        np.testing.assert_array_equal(segMap, expOut)

    def test_rectangle_output(self):
        objects = [{"type": "ellipse",
                    "center": {"x": 5,
                               "y": 4},
                    "radiusX": 2,
                    "radiusY": 3,
                    "angleOfRotation": 0.0}]
        imgSize = (10,11)
        expOut =   [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                    [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
                    [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
                    [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
                    [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
                    [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
                    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        segMap = json2labels(objects, imgSize)
        print(segMap)
        np.testing.assert_array_equal(segMap, expOut)

    def test_unknown(self):
        objects = [{"type": "random",
                    "center": {"x": 2,
                               "y": 3},
                    "radius": 4}]
        imgSize = (10,10)
        self.assertRaises(ValueError, json2labels, objects, imgSize)

