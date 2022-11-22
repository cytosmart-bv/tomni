import warnings
from dataclasses import asdict
from typing import List, Tuple

import cv2
import numpy as np

from ..annotation import Annotation
from ..point import Point


class Polygon(Annotation):
    def __init__(self, points: List[Point], id, label, children, parents):
        """Initializes a Polygon object.

        Args:
            points (List[Point]): Collection of edges describing the polygon.
            id (str): UUID identifier.
            label (str): Class label of annotation.
            children (List[Annotation]): Tracking annotations. Refers to t+1.
            parents (List[Annotation]): Tracking annotations. Refers to t-1.
        """
        MIN_NR_POINTS = 3

        super().__init__(id, label, children, parents)
        self._points: List[Point] = points
        self._contour: List[Tuple[int, int]] = self._parse_points_to_contour(points)

        self._has_enough_points = len(points) >= MIN_NR_POINTS
        if not self._has_enough_points:
            warnings.warn(
                f"Polygon has less than {MIN_NR_POINTS} points. Some features may not be available."
            )

        # features
        self._area = None
        self._circularity = None
        self._convex_hull_area = None
        self._perimeter = None
        self._roundness = None

    @property
    def area(self) -> float:
        """Quantity that expresses the extent of a polygon determined by cv2 contour operations.
        Requires 5 or more points.

        Returns:
            float: Polygon's area.
        """
        if not self._area:
            self._calculate_area()

        return self._area

    @property
    def circularity(self) -> float:
        """Circularity: (4 * pi * Area) / perimeter ** 2)

        Returns:
            float: Circularity in [0, 1].
        """
        if not self._circularity:
            self._calculate_circularity()

        return self._circularity

    @property
    def convex_hull_area(self) -> float:
        """Convex Hull Area by cv2 contour operations. 

        Returns:
            float: Polygon's convex hull area.
        """
        if not self._convex_hull_area:
            self._calculate_convex_hull_area()

        return self._convex_hull_area

    @property
    def label(self):
        return super().label

    @label.setter
    def label(self, value) -> None:
        super().label = value

    @property
    def perimeter(self) -> float:
        """Total length of polygon's boundary determined by cv2 contour operations.

        Returns:
            float: Polygon's perimeter.
        """
        if not self._perimeter:
            self._calculate_perimeter()

        return self._perimeter

    @property
    def points(self) -> List[Point]:
        return self._points

    @property
    def roundness(self) -> float:
        """Roundness: Area / (radius_enclosing_circle**2 * pi).

        Returns:
            float: Polygon's roundness in [0, 1].
        """
        if not self._roundness:
            self._calculate_roundness()

        return self._roundness

    def to_dict(self) -> dict:
        polygon_dict = {
            "type": "polygon",
            "area": self.area,
            "circularity": self.circularity,
            "convex_hull_area": self.convex_hull_area,
            "perimeter": self.perimeter,
            "points": [asdict(point) for point in self._points],
            "roundness": self.roundness,
        }

        super_dict = super().to_dict()
        dict_return_value = {**super_dict, **polygon_dict}
        return dict_return_value

    def _calculate_area(self) -> None:
        if self._has_enough_points:
            self._area = cv2.contourArea(self._contour)

    def _calculate_circularity(self):
        if not self._has_enough_points:
            return

        if not self._area:
            self._calculate_area()

        if not self._perimeter:
            self._calculate_perimeter()

        self._circularity = (4 * np.pi * self._area) / (self._perimeter ** 2)

    def _calculate_convex_hull_area(self) -> None:
        if not self._has_enough_points:
            return

        convex_hull = cv2.convexHull(self._contour)
        self._convex_hull_area = cv2.contourArea(convex_hull)

    def _calculate_perimeter(self) -> None:
        self._perimeter = cv2.arcLength(self._contour, True)

    def _calculate_roundness(self) -> None:
        if not self._has_enough_points:
            return

        if not self._area:
            self._calculate_area()

        _, radius = cv2.minEnclosingCircle(self._contour)
        enclosing_circle_area = radius ** 2 * np.pi
        self._roundness = self._area / enclosing_circle_area

    def _parse_points_to_contour(self, points) -> List[Tuple[int, int]]:
        contour_points = [[[point.x, point.y]] for point in points]
        contour = np.array(contour_points, dtype=np.int32)
        return contour
