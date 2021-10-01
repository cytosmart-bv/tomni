import unittest
from .main import check_overlap_bbox


class TestOverlap(unittest.TestCase):
    def test_overlap_x(self):
        bb1 = [0, 10, 0, 10]
        bb2 = [5, 15, 0, 10]
        output = check_overlap_bbox(bb1, bb2)
        self.assertEqual(output, True)

    def test_overlap_y(self):
        bb1 = [0, 10, 0, 10]
        bb2 = [0, 10, 5, 15]
        output = check_overlap_bbox(bb1, bb2)
        self.assertEqual(output, True)

    def test_overlap_xy(self):
        bb1 = [0, 10, 0, 10]
        bb2 = [5, 15, 5, 15]
        output = check_overlap_bbox(bb1, bb2)
        self.assertEqual(output, True)

    def test_touch_x(self):
        bb1 = [0, 10, 0, 10]
        bb2 = [10, 15, 0, 10]
        output = check_overlap_bbox(bb1, bb2)
        self.assertEqual(output, False)

    def test_touch_y(self):
        bb1 = [0, 10, 0, 10]
        bb2 = [0, 10, 10, 15]
        output = check_overlap_bbox(bb1, bb2)
        self.assertEqual(output, False)

    def test_touch_xy(self):
        bb1 = [0, 10, 0, 10]
        bb2 = [10, 15, 10, 15]
        output = check_overlap_bbox(bb1, bb2)
        self.assertEqual(output, False)

    def test_complete_miss(self):
        bb1 = [0, 10, 0, 10]
        bb2 = [20, 30, 20, 30]
        output = check_overlap_bbox(bb1, bb2)
        self.assertEqual(output, False)

    def test_wrong_length(self):
        bb1 = [0, 10, 0, 10, 2]
        bb2 = [10, 15, 10, 15, 2]
        with self.assertRaises(TypeError):
            check_overlap_bbox(bb1, bb2)

    def test_wrong_length_one(self):
        bb1 = [0, 10, 0, 10, 2]
        bb2 = [10, 15, 10, 15]
        with self.assertRaises(TypeError):
            check_overlap_bbox(bb1, bb2)
