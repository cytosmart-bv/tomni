from unittest import TestCase
from .main import overlap_object


class Test_overlap_object(TestCase):
    def test_ellipse(self):
        object1 = {
            "type": "ellipse",
            "center": {"x": 4, "y": 4},
            "radiusX": 3,
            "radiusY": 3,
            "angleOfRotation": 0.0,
        }
        object2 = {
            "type": "ellipse",
            "center": {"x": 6, "y": 4},
            "radiusX": 7,
            "radiusY": 3,
            "angleOfRotation": 50,
        }

        overlap = overlap_object(object1, object2)
        expOverlap = 0.772
        self.assertAlmostEqual(overlap, expOverlap, places=1)

    def test_completeOverlap(self):
        object1 = {
            "type": "ellipse",
            "center": {"x": 30000, "y": 5000},
            "radiusX": 7,
            "radiusY": 3,
            "angleOfRotation": 0.0,
        }
        object2 = {
            "type": "ellipse",
            "center": {"x": 30000, "y": 5000},
            "radiusX": 3000,
            "radiusY": 2000,
            "angleOfRotation": 50,
        }

        overlap = overlap_object(object1, object2)
        expOverlap = 1
        self.assertAlmostEqual(overlap, expOverlap, places=1)

    def test_noOverlap(self):
        object1 = {
            "type": "ellipse",
            "center": {"x": 30000, "y": 5000},
            "radiusX": 7,
            "radiusY": 3,
            "angleOfRotation": 0.0,
        }
        object2 = {
            "type": "ellipse",
            "center": {"x": 3, "y": 5},
            "radiusX": 3,
            "radiusY": 20,
            "angleOfRotation": 50,
        }

        overlap = overlap_object(
            object1,
            object2,
        )
        expOverlap = 0
        self.assertAlmostEqual(overlap, expOverlap, places=1)

    def test_noArea(self):
        object1 = {
            "type": "ellipse",
            "center": {"x": 30000, "y": 5000},
            "radiusX": 0,
            "radiusY": 0,
            "angleOfRotation": 0.0,
        }
        object2 = {
            "type": "ellipse",
            "center": {"x": 3000, "y": 5000},
            "radiusX": 0,
            "radiusY": 0,
            "angleOfRotation": 0,
        }

        overlap = overlap_object(object1, object2)
        expOverlap = 0
        self.assertAlmostEqual(overlap, expOverlap, places=1)

    def test_polypon(self):
        object1 = {
            "type": "polygon",
            "points": [
                {"x": 2, "y": 3},
                {"x": 5, "y": 6},
                {"x": 2, "y": 5},
                {"x": 7, "y": 9},
                {"x": 4, "y": 2},
            ],
        }
        object2 = {
            "type": "polygon",
            "points": [
                {"x": 5, "y": 3},
                {"x": 10, "y": 10},
                {"x": 4, "y": 5},
                {"x": 4, "y": 2},
            ],
        }

        overlap = overlap_object(object1, object2)
        expOverlap = 0.286
        self.assertAlmostEqual(overlap, expOverlap, places=1)

    def test_polygon_ellipse(self):
        object1 = {
            "type": "polygon",
            "points": [
                {"x": 2, "y": 3},
                {"x": 5, "y": 6},
                {"x": 2, "y": 5},
                {"x": 7, "y": 9},
                {"x": 4, "y": 2},
            ],
        }
        object2 = {
            "type": "ellipse",
            "center": {"x": 6, "y": 4},
            "radiusX": 7,
            "radiusY": 3,
            "angleOfRotation": 50,
        }

        overlap = overlap_object(object1, object2)
        expOverlap = 0.899
        self.assertAlmostEqual(overlap, expOverlap, places=1)

    def test_ellipse_polygon(self):
        object1 = {
            "type": "ellipse",
            "center": {"x": 4, "y": 4},
            "radiusX": 3,
            "radiusY": 3,
            "angleOfRotation": 0.0,
        }

        object2 = {
            "type": "polygon",
            "points": [
                {"x": 5, "y": 3},
                {"x": 10, "y": 10},
                {"x": 4, "y": 5},
                {"x": 4, "y": 2},
            ],
        }

        overlap = overlap_object(object1, object2)
        expOverlap = 0.215
        self.assertAlmostEqual(overlap, expOverlap, places=1)

    def test_unknown_type(self):
        object1 = {"type": "square", "x1": 4, "y1": 4, "x2": 3, "y2": 3}
        object2 = {
            "type": "ellipse",
            "center": {"x": 6, "y": 4},
            "radiusX": 7,
            "radiusY": 3,
            "angleOfRotation": 50,
        }
        self.assertRaises(ValueError, overlap_object, object1, object2)

    def test_negative(self):
        object1 = {
            "type": "ellipse",
            "center": {"x": 4, "y": 4},
            "radiusX": -1,
            "radiusY": 3,
            "angleOfRotation": 0.0,
        }
        object2 = {
            "type": "ellipse",
            "center": {"x": 6, "y": 4},
            "radiusX": 7,
            "radiusY": 3,
            "angleOfRotation": 50,
        }

        self.assertRaises(ValueError, overlap_object, object1, object2)

    def test_bug_to_small_object(self):
        object1 = {
            "type": "polygon",
            "points": [
                {"x": 618, "y": 54},
                {"x": 625, "y": 61},
            ],
            "id": "56acfd7c-de50-4c45-906f-d97b4ea6467d",
            "parents": [],
            "children": [],
        }
        object2 = {
            "type": "polygon",
            "points": [
                {"x": 618, "y": 54},
                {"x": 618, "y": 61},
                {"x": 625, "y": 61},
                {"x": 625, "y": 54},
            ],
            "id": "56acfd7c-de50-4c45-906f-d97b4ea6467d",
            "parents": [],
            "children": [],
        }

        overlap = overlap_object(object1, object2)
        expOverlap = 0
        self.assertAlmostEqual(overlap, expOverlap, places=1)
