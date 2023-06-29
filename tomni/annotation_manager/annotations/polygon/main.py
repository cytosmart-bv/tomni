import gc
import warnings
from dataclasses import asdict
from typing import List, Tuple, Union

import cv2
import numpy as np

from tomni.annotation_manager.annotations.annotation import Annotation
from tomni.annotation_manager.annotations.point import Point
from tomni.annotation_manager.utils import are_lines_equal, parse_points_to_contour, simplify_line, overlap_object

from ...utils import compress_polygon_points, parse_points_to_contour


class Polygon(Annotation):
    def __init__(self, points: List[Point], id: str, label: str = "", children: List[Annotation] = [], parents: List[Annotation] = []):
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
        self._points: List[Point] = simplify_line(points)
        self._contour: np.ndarray = parse_points_to_contour(points)

        self._has_enough_points = len(points) >= MIN_NR_POINTS
        if not self._has_enough_points:
            warnings.warn(f"Polygon has less than {MIN_NR_POINTS} points. Some features may not be available.")

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
    def points(self, *arg, **kwargs) -> None:
        raise SyntaxError("Points are Immutable")

    @property
    def roundness(self) -> float:
        """Roundness: Area / (radius_enclosing_circle**2 * pi).

        Returns:
            float: Polygon's roundness in [0, 1].
        """
        if not self._roundness:
            self._calculate_roundness()

        return self._roundness

    def to_dict(self, decimals: int = 2, **kwargs) -> dict:
        points = self._points.copy()
        if kwargs.get("do_compress", False):
            points = compress_polygon_points(points, kwargs.get("epsilon", 3))

        polygon_dict = {"type": "polygon", "points": [asdict(point) for point in points]}

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

    def is_in_mask(self, mask_json: dict, min_overlap: float = 0.9):
        """Check if a polygon is within a binary mask.

        Args:
            mask_json (dict): A dict mask in cytosmart dict format.
            min_overlap (float, optional): Minimum overlap required between the polygon and the mask, expressed as a value between 0 and 1.
            Defaults to 0.9.

        Returns:
            bool: True if the polygon is within the mask and meets the required overlap, False otherwise.
        """
        if len(self.points) < 1:
            return False

        json_points = [{"x": point.x, "y": point.y} for point in self.points]
        json_object = {"type": "polygon", "points": json_points}

        overlap_ratio = overlap_object(json_object, mask_json)

        # Check if the polygon is within the masked area with at least the specified overlap
        return overlap_ratio >= min_overlap

    def to_binary_mask(self, shape: Tuple[int, int]) -> np.ndarray:
        """Transform a polygon to a binary mask.

        Args:
            shape (Tuple[int, int]): Shape of the new polygon's binary mask.

        Returns:
            np.ndarray: A binary mask in [0, 1].
        """
        mask = np.zeros(shape, dtype=np.uint8)
        if len(self._points) > 0:
            points = np.array([[point.x, point.y] for point in self._points], dtype=np.int32)
            cv2.fillPoly(mask, [points], color=1)

        return mask

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

    def __eq__(self, other):
        if not isinstance(other, Polygon):
            # don't attempt to compare against unrelated types
            return False

        are_points_equal = are_lines_equal(self.points, other.points, is_enclosed=True)
        reverse_points = other.points
        reverse_points.reverse()
        are_points_equal_mirrored = are_lines_equal(self.points, reverse_points, is_enclosed=True)
        return are_points_equal | are_points_equal_mirrored
