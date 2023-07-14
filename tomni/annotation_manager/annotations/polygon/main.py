from dataclasses import asdict
from typing import List, Tuple, Union, Dict
import quantiphy
import cv2
import numpy as np

from tomni.annotation_manager.annotations.annotation import Annotation
from tomni.annotation_manager.annotations.point import Point
from tomni.annotation_manager.utils import (
    are_lines_equal,
    parse_points_to_contour,
    simplify_line,
    overlap_object,
)

from ...utils import compress_polygon_points, parse_points_to_contour


class Polygon(Annotation):
    def __init__(
        self,
        points: List[Point],
        id: str,
        label: str = "",
        children: List[Annotation] = [],
        parents: List[Annotation] = [],
        pixel_density: int = 1,
        features: Union[List[str], None] = None,
        accuracy: float = 1,
        metric_unit: str = "",
    ):
        """Initializes a Polygon object.

        Args:
            points (List[Point]): Collection of edges describing the polygon.
            id (str): UUID identifier.
            label (str): Class label of annotation.
            children (List[Annotation]): Tracking annotations. Refers to t+1.
            parents (List[Annotation]): Tracking annotations. Refers to t-1.
            accuracy (float, optional): The confidence of the model's prediction. Defaults to 1.
            features (Union[List[str],None]): list of features that the user wants returned.
                Defaults to None
            metric_unit (str, optional): A suffix added to the name of the feature in the dict. Defaults to "".

        """
        super().__init__(id, label, children, parents, accuracy)
        self._points: List[Point] = simplify_line(points)
        self._contour: np.ndarray = parse_points_to_contour(points)
        self._metric_unit = metric_unit
        self._pixel_density = pixel_density

        self._area: Union[float, None] = None
        self._aspect_ratio: Union[float, None] = None
        self._average_diameter: Union[float, None] = None
        self._circularity: Union[float, None] = None
        self._convex_hull_area: Union[float, None] = None
        self._major_axis: Union[float, None] = None
        self._minor_axis: Union[float, None] = None
        self._perimeter: Union[float, None] = None

        self._all_features = {
            "area": {"is_ratio": False},
            "aspect_ratio": {"is_ratio": True},
            "average_diameter": {"is_ratio": False},
            "circularity": {"is_ratio": True},
            "convex_hull_area": {"is_ratio": False},
            "major_axis": {"is_ratio": False},
            "minor_axis": {"is_ratio": False},
            "perimeter": {"is_ratio": False},
        }

        if features is None:
            self._features = [feature for feature in self._all_features]
        else:
            missing_features = set(features).difference(set(self._all_features.keys()))
            if missing_features:
                raise ValueError(
                    f"The following features are not compatible with the Annotation Manager: {', '.join(missing_features)}"
                )

            self._features = features

    @property
    def accuracy(self) -> float:
        """Accuracy of ellipse."""
        return self._accuracy

    @accuracy.setter
    def points(self, *arg, **kwargs) -> None:
        raise SyntaxError("Points are Immutable")

    @property
    def label(self):
        return super().label

    @label.setter
    def label(self, value) -> None:
        super().label = value

    @property
    def points(self) -> List[Point]:
        return self._points

    @points.setter
    def points(self, *arg, **kwargs) -> None:
        raise SyntaxError("Points are Immutable")

    @property
    def area(self) -> Union[float, None]:
        """Quantity that expresses the extent of a polygon determined by cv2 contour operations.
        Requires 5 or more points.

        Returns:
            Union[float, None]: Polygon's area or None.
        """

        if "area" in self._features:
            self._calculate_area()
            return self._area * self._pixel_density**2
        return

    @property
    def circularity(self) -> Union[float, None]:
        """Circularity: (4 * pi * Area) / perimeter ** 2)

        Returns:
            Union[float, None]: Circularity in [0, 1] or None.
        """

        if "circularity" in self._features:
            self._calculate_circularity()
            return self._circularity
        return
        # return self._circularity

    @property
    def convex_hull_area(self) -> Union[float, None]:
        """Convex Hull Area by cv2 contour operations.

        Returns:
            Union[float, None]: Polygon's convex hull area or None.
        """

        if "convex_hull_area" in self._features:
            self._calculate_convex_hull_area()
            return self._convex_hull_area * self._pixel_density**2
        return

    @property
    def average_diameter(self) -> float:
        """Returns the average diameter of a polygon.

        Returns:
            float: Average diameter.
        """
        if "average_diameter" in self._features:
            self._calculate_average_diameter()
            return self._average_diameter * self._pixel_density
        return

    @property
    def minor_axis(self) -> float:
        """Return the minor axis of the polygon.

        Returns:
            float: Minor axis length.
        """
        if "minor_axis" in self._features:
            self._calculate_axes()
            return self._minor_axis * self._pixel_density
        return

    @property
    def major_axis(self) -> float:
        """Return the major axis of the polygon.

        Returns:
            float: major axis length.
        """
        if "major_axis" in self._features:
            self._calculate_axes()
            return self._major_axis * self._pixel_density
        return

    @property
    def aspect_ratio(self) -> float:
        """Ratio between minor and major axis.

        Returns:
            float: Ellipse's aspect ratio.
        """
        if "aspect_ratio" in self._features:
            self._calculate_aspect_ratio()
            return self._aspect_ratio
        return

    @property
    def perimeter(self) -> Union[float, None]:
        """Total length of polygon's boundary determined by cv2 contour operations.

        Returns:
            Union[float, None]: Polygon's perimeter or None.
        """

        if "perimeter" in self._features:
            self._calculate_perimeter()
            return self._perimeter * self._pixel_density
        return

    @property
    def roundness(self) -> Union[float, None]:
        """Roundness: Area / (radius_enclosing_circle**2 * pi).

        Returns:
            Union[float, None]: Polygon's roundness in [0, 1] or None.
        """

        if "roundness" in self._features:
            self._calculate_roundness()
            return self._roundness
        return

    def to_dict(self, decimals: int = 2, **kwargs) -> dict:
        points = self._points.copy()
        if kwargs.get("do_compress", False):
            points = compress_polygon_points(points, kwargs.get("epsilon", 3))

        polygon_dict = {
            "type": "polygon",
            "points": [asdict(point) for point in points],
        }

        # if the user wants any features returned
        if self._features:
            polygon_features = {}
            for feature in self._features:
                feature_name = (
                    feature
                    if self._all_features[feature]["is_ratio"]
                    else feature + "_" + self._metric_unit
                )
            
                # Convert snake_casing to camelCasing
                first_word, *remaining_words  = feature_name.split('_')
                feature_name = ''.join([first_word.lower(), *map(str.title, remaining_words)])
                
                polygon_features[feature_name] = round(getattr(self, feature), decimals)
            polygon_dict = {**polygon_features, **polygon_dict}

        super_dict = super().to_dict(decimals=decimals)
        dict_return_value = {**super_dict, **polygon_dict}
        return dict_return_value

    def is_in_mask(self, mask_json: List[dict], min_overlap: float = 0.9):
        """Check if a polygon is within a binary mask.

        Args:
            mask_json (List[dict]): A list of dict masks in cytosmart dict format.
            min_overlap (float, optional): Minimum overlap required between the polygon a mask, expressed as a value between 0 and 1.
            Defaults to 0.9.

        Returns:
            bool: True if the polygon is within a mask and meets the required overlap, False otherwise.
        """
        if len(self.points) < 1:
            return False

        json_points = [{"x": point.x, "y": point.y} for point in self.points]
        json_object = {"type": "polygon", "points": json_points}

        for mask in mask_json:
            overlap_ratio = overlap_object(json_object, mask)
            if overlap_ratio >= min_overlap:
                return True

        return False

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
        self._area = cv2.contourArea(self._contour)

    def _calculate_circularity(self):
        if not self._area:
            self._calculate_area()

        if not self._perimeter:
            self._calculate_perimeter()

        self._circularity = (4 * np.pi * self._area) / (self._perimeter**2)

    def _calculate_convex_hull_area(self) -> None:
        convex_hull = cv2.convexHull(self._contour)
        self._convex_hull_area = cv2.contourArea(convex_hull)

    def _calculate_perimeter(self) -> None:
        self._perimeter = cv2.arcLength(self._contour, True)

    def _calculate_roundness(self) -> None:
        if not self._area:
            self._calculate_area()

        _, radius = cv2.minEnclosingCircle(self._contour)
        enclosing_circle_area = radius**2 * np.pi
        self._roundness = self._area / enclosing_circle_area

    def _calculate_axes(self) -> None:
        _, (r1, r2), _ = cv2.fitEllipse(self._contour)
        self._minor_axis = min(r1, r2)
        self._major_axis = max(r1, r2)

    def _calculate_average_diameter(self) -> None:
        if self._minor_axis is None or self._major_axis is None:
            self._calculate_axes()

        self._average_diameter = (self._major_axis + self._minor_axis) / 2

    def _calculate_aspect_ratio(self) -> None:
        if self._minor_axis is None or self._major_axis is None:
            self._calculate_axes()

        self._aspect_ratio = self._minor_axis / self._major_axis

    def __eq__(self, other):
        if not isinstance(other, Polygon):
            # don't attempt to compare against unrelated types
            return False

        are_points_equal = are_lines_equal(self.points, other.points, is_enclosed=True)
        reverse_points = other.points
        reverse_points.reverse()
        are_points_equal_mirrored = are_lines_equal(self.points, reverse_points, is_enclosed=True)
        return are_points_equal | are_points_equal_mirrored
