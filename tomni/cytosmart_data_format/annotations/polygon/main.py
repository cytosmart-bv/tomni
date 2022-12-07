from math import sqrt
import warnings
from dataclasses import asdict
from typing import List

import cv2
import numpy as np

from ...utils import parse_points_to_contour
from ..annotation import Annotation
from ..point import Point


class Polygon(Annotation):
    def __init__(
        self,
        points: List[Point],
        id: str,
        label: str = "",
        children: List[Annotation] = [],
        parents: List[Annotation] = [],
    ):
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
        self.points: List[Point] = points
        self._contour: List[np.ndarray] = parse_points_to_contour(points)

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

    @points.setter
    def points(self, value: List[Point]) -> None:
        """
        Simplify every list of points to only have points that add information
        """
        filtered_points = []

        # Remove point that do no add new information
        for i in range(len(value)):
            prev_p = value[i - 1]
            cur_p = value[i]
            next_p = value[i + 1] if (i + 1) < len(value) else value[0]

            """
            If ratio heigh width for prev-cur and cur-next is the same.
            The point is on a straight line
            Comparing is done with division for optimization
            """
            prev_cur_width = prev_p.x - cur_p.x
            prev_cur_height = prev_p.y - cur_p.y
            cur_next_width = cur_p.x - next_p.x
            cur_next_height = cur_p.y - next_p.y

            if prev_cur_width * cur_next_height == prev_cur_height * cur_next_width:
                continue

            filtered_points.append(cur_p)

        self._points = filtered_points

    @property
    def roundness(self) -> float:
        """Roundness: Area / (radius_enclosing_circle**2 * pi).

        Returns:
            float: Polygon's roundness in [0, 1].
        """
        if not self._roundness:
            self._calculate_roundness()

        return self._roundness

    def to_dict(self, decimals: int = 2) -> dict:
        polygon_dict = {
            "type": "polygon",
            "points": [asdict(point) for point in self.points],
        }

        if self._has_enough_points:
            # Feature property is None if polygon has not enough points which results the round() to fail on a NoneType.
            polygon_features = {
                "area": round(self.area, decimals),
                "circularity": round(self.circularity, decimals),
                "convex_hull_area": round(self.convex_hull_area, decimals),
                "perimeter": round(self.perimeter, decimals),
                "roundness": round(self.roundness, decimals),
            }
            polygon_dict = {**polygon_features, **polygon_dict}

        super_dict = super().to_dict(decimals=decimals)
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

        self._circularity = (4 * np.pi * self._area) / (self._perimeter**2)

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
        enclosing_circle_area = radius**2 * np.pi
        self._roundness = self._area / enclosing_circle_area

    @staticmethod
    def __compare_list_points(l1: List[Annotation], l2: List[Annotation]):
        if len(l1) != len(l2):
            return False

        start_l2 = 0
        for i in range(len(l1)):
            if l1[0] == l2[i]:
                start_l2 = i
                break

        sliced_l2 = l2[start_l2:] + l2[:start_l2]
        print(sliced_l2)

        for i in range(len(l1)):
            if l1[i] != sliced_l2[i]:
                return False

        return True

    def __eq__(self, other):
        if not isinstance(other, Polygon):
            # don't attempt to compare against unrelated types
            return False

        are_points_equal = self.__compare_list_points(self.points, other.points)
        reverse_points = other.points
        reverse_points.reverse()
        are_points_equal_mirrored = self.__compare_list_points(
            self.points, reverse_points
        )
        return are_points_equal | are_points_equal_mirrored
