from unittest import TestCase

from tomni.annotation_manager import Ellipse, Point


class TestEllipseCompare(TestCase):
    def test_ignore_decimals(self):
        ellip1 = Ellipse(
            radius_x=1, radius_y=3, center=Point(10, 40), rotation=0, id="ellipse1"
        )
        ellip2 = Ellipse(
            radius_x=1.0,
            radius_y=3.0,
            center=Point(10, 40),
            rotation=0.0,
            id="ellipse2",
        )

        self.assertTrue(ellip1 == ellip2)

    def test_different_radius_x(self):
        ellip1 = Ellipse(
            radius_x=1, radius_y=3, center=Point(10, 40), rotation=45, id="ellipse1"
        )
        ellip2 = Ellipse(
            radius_x=2, radius_y=3, center=Point(10, 40), rotation=45, id="ellipse2"
        )

        self.assertFalse(ellip1 == ellip2)

    def test_different_radius_y(self):
        ellip1 = Ellipse(
            radius_x=1, radius_y=3, center=Point(10, 40), rotation=100, id="ellipse1"
        )
        ellip2 = Ellipse(
            radius_x=1, radius_y=2, center=Point(10, 40), rotation=100, id="ellipse2"
        )

        self.assertFalse(ellip1 == ellip2)

    def test_different_center(self):
        ellip1 = Ellipse(
            radius_x=1, radius_y=3, center=Point(10, 40), rotation=-100, id="ellipse1"
        )
        ellip2 = Ellipse(
            radius_x=1, radius_y=3, center=Point(11, 40), rotation=-100, id="ellipse2"
        )

        self.assertFalse(ellip1 == ellip2)

    def test_different_rotation(self):
        ellip1 = Ellipse(
            radius_x=1, radius_y=3, center=Point(10, 40), rotation=0, id="ellipse1"
        )
        ellip2 = Ellipse(
            radius_x=1, radius_y=3, center=Point(10, 40), rotation=10, id="ellipse2"
        )

        self.assertFalse(ellip1 == ellip2)

    def test_rotation_90(self):
        ellip1 = Ellipse(
            radius_x=3, radius_y=1, center=Point(10, 40), rotation=90, id="ellipse1"
        )
        ellip2 = Ellipse(
            radius_x=1, radius_y=3, center=Point(10, 40), rotation=0, id="ellipse2"
        )

        self.assertTrue(ellip1 == ellip2)

    def test_rotation_180(self):
        ellip1 = Ellipse(
            radius_x=1, radius_y=3, center=Point(10, 40), rotation=200, id="ellipse1"
        )
        ellip2 = Ellipse(
            radius_x=1, radius_y=3, center=Point(10, 40), rotation=20, id="ellipse2"
        )

        self.assertTrue(ellip1 == ellip2)

    def test_negative_rotation(self):
        ellip1 = Ellipse(
            radius_x=1, radius_y=3, center=Point(10, 40), rotation=-10, id="ellipse1"
        )
        ellip2 = Ellipse(
            radius_x=3, radius_y=1, center=Point(10, 40), rotation=80, id="ellipse2"
        )

        self.assertTrue(ellip1 == ellip2)
