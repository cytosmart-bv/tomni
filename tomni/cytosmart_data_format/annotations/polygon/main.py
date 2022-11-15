import warnings
from dataclasses import asdict
from typing import List, Tuple

import cv2
import numpy as np

from ..annotation import Annotation
from ..point import Point


class Polygon(Annotation):
    def __init__(self, points: List[Point], id, label, children, parents):
        super().__init__(id, label, children, parents)
        self._points: List[Point] = points
        self._contour: List[Tuple[int, int]] = self._parse_points_to_contour(points)

        self._has_enough_points = len(points) >= 5
        if not self._has_enough_points:
            warnings.warn(
                "Polygon has less than 5 points. Some features may not be available."
            )

        # features
        self._area = None  # done
        self._aspect_ratio = None  # done
        self._average_diameter = None
        self._circularity = None  # done
        self._convex_hull_area = None  # done
        self._minor_axis = None
        self._major_axis = None
        self._perimeter = None  # done
        self._roundness = None  # done

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
    def aspect_ratio(self) -> float:
        """Aspect Ratio (AR): axis_minor / axis_major
        Requires 5 or more points.

        Returns:
            float: Aspect ratio in [0, 1].
        """
        if not self._aspect_ratio:
            self._calculate_aspect_ratio()

        return self._aspect_ratio

    @property
    def average_diameter(self) -> float:
        """Average Diameter (AD): (minor_axis + major_axis) / 2. 
        Requires 5 or more points.

        Returns:
            float: Average diameter.
        """
        if not self._average_diameter:
            self._calculate_average_diameter()

        return self._average_diameter

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
    def major_axis(self) -> float:
        """Fits an ellipse to polygon and detemermines major axis.

        Returns:
            float: Polygon's major axis.
        """
        if not self._major_axis:
            self._calculate_major_axis()

        return self._major_axis

    @property
    def minor_axis(self) -> float:
        """Fits an ellipse to polygon and detemermines minor axis.

        Returns:
            float: Polygon's minor axis.
        """
        if not self._minor_axis:
            self._calculate_minor_axis()

        return self._minor_axis

    @property
    def perimeter(self) -> float:
        """Total length of polygon's boundary determined by cv2 contour operations.

        Returns:
            float: Polygon's perimeter
        """
        if not self._perimeter:
            self._calculate_perimeter()

        return self._perimeter

    @property
    def points(self) -> List[Point]:
        return self._points

    @property
    def roundness(self) -> float:
        """Roundness: Area / (radius_enclosing_circle**2 * pi) in [0, 1].

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
            "aspect_ratio": self.aspect_ratio,
            "circularity": self.circularity,
            "convex_hull_area": self.convex_hull_area,
            "diameter": self.average_diameter,
            "minor_axis": self.minor_axis,
            "major_axis": self.major_axis,
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

    def _calculate_aspect_ratio(self) -> None:
        if not self._has_enough_points:
            return

        if not self._minor_axis:
            self._calculate_minor_axis()

        if not self._major_axis:
            self._calculate_major_axis()

        self._aspect_ratio = self._minor_axis / self._major_axis

    def _calculate_average_diameter(self) -> None:
        if not self._has_enough_points:
            return

        if not self._major_axis:
            self._calculate_major_axis()

        if not self._minor_axis:
            self._calculate_minor_axis()

        self._average_diameter = (self._minor_axis + self._major_axis) / 2

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

    def _calculate_major_axis(self) -> None:
        if not self._has_enough_points:
            return

        _, (r1, r2), _ = cv2.fitEllipse(self._contour)
        self._major_axis = max(r1, r2)

    def _calculate_minor_axis(self) -> None:
        if not self._has_enough_points:
            return

        _, (r1, r2), _ = cv2.fitEllipse(self._contour)
        self._minor_axis = min(r1, r2)

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
