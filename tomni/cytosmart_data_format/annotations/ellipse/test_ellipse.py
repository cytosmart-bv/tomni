from unittest import TestCase

from tomni.cytosmart_data_format import Ellipse, Point


class TestEllipse(TestCase):
    def test_area(self):
        ellipse = Ellipse(radius=Point(0, 0), center=Point(0, 0), rotation=0)
        expected = 0.0
        actual = ellipse.area

        self.assertEqual(expected, actual)

    def test_circularity(self):
        pass

    def test_perimeter(self):
        pass

    def test_aspect_ratio(self):
        pass
