from dataclasses import asdict
from typing import List, Tuple, Union, Dict
import cv2
import numpy as np

from tomni.annotation_manager.annotations.annotation import Annotation
from tomni.annotation_manager.annotations.point import Point
from tomni.annotation_manager.utils import (
    are_lines_equal,
    parse_points_to_contour,
    overlap_object,
    parse_points_to_inner_contour,
)

MIN_NR_POINTS_POLYGON = 5

from ...utils import compress_polygon_points, parse_points_to_contour


class Polygon(Annotation):
    def __init__(
        self,
        points: List[Point],
        id: str,
        inner_points: Union[List[List[Point]], List] = [],
        label: str = "",
        children: List[Annotation] = [],
        parents: List[Annotation] = [],
        feature_multiplier: int = 1,
        accuracy: float = 1,
    ):
        """Initializes a Polygon object.

        Args:
            points (List[Point]): Collection of edges describing the polygon.
            id (str): UUID identifier.
            inner_points (Union[List[List[Point]], List]): Collection of edges describing the inner contours or an empty list when there are no inner contours.
            label (str): Class label of annotation.
            children (List[Annotation]): Tracking annotations. Refers to t+1.
            parents (List[Annotation]): Tracking annotations. Refers to t-1.
            accuracy (float, optional): The confidence of the model's prediction. Defaults to 1.
            features (Union[List[str],None]): list of features that the user wants returned.
                Defaults to None
            metric_unit (str, optional): A suffix added to the name of the feature in the dict. Defaults to "".
            feature_multiplier (int, optional): Pixel density of the image. Defaults to 1.
        """
        super().__init__(id, label, children, parents, accuracy)
        self._points = points
        self._inner_points = inner_points
        if len(self._points) < 5:
            raise ValueError("Polygon must have atleast 5 points.")
        self._contour: np.ndarray = parse_points_to_contour(points)
        self._inner_contours: List[np.ndarray] = parse_points_to_inner_contour(
            inner_points
        )
        self._feature_multiplier = feature_multiplier

        self._area: Union[float, None] = None
        self._outer_area: Union[float, None] = None
        self._aspect_ratio: Union[float, None] = None
        self._average_diameter: Union[float, None] = None
        self._circularity: Union[float, None] = None
        self._convex_hull_area: Union[float, None] = None
        self._major_axis: Union[float, None] = None
        self._minor_axis: Union[float, None] = None
        self._perimeter: Union[float, None] = None
        self._roundness: Union[float, None] = None

        self._all_features = {
            "area": {"is_ratio": False},
            "aspect_ratio": {"is_ratio": True},
            "average_diameter": {"is_ratio": False},
            "circularity": {"is_ratio": True},
            "convex_hull_area": {"is_ratio": False},
            "major_axis": {"is_ratio": False},
            "minor_axis": {"is_ratio": False},
            "perimeter": {"is_ratio": False},
            "roundness": {"is_ratio": True},
        }

    @property
    def accuracy(self) -> float:
        """Accuracy of ellipse."""
        return self._accuracy

    @accuracy.setter
    def accuracy(self, *arg, **kwargs) -> None:
        raise SyntaxError("Accuracy is Immutable")

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
    def inner_points(self) -> List[List[Point]]:
        return self._inner_points

    @inner_points.setter
    def inner_points(self, *arg, **kwargs) -> None:
        raise SyntaxError("Inner Points are Immutable")

    @property
    def area(self) -> Union[float, None]:
        """Quantity that expresses the extent of a polygon determined by cv2 contour operations.
        Requires 5 or more points.

        Returns:
            Union[float, None]: Polygon's area or None.
        """
        if self._area is None:
            self._calculate_area()
        return self._area * self._feature_multiplier**2

    @property
    def circularity(self) -> Union[float, None]:
        """Circularity: (4 * pi * Area) / perimeter ** 2)

        Returns:
            Union[float, None]: Circularity in [0, 1] or None.
        """

        if self._circularity is None:
            self._calculate_circularity()
        return self._circularity

    @property
    def convex_hull_area(self) -> Union[float, None]:
        """Convex Hull Area by cv2 contour operations.

        Returns:
            Union[float, None]: Polygon's convex hull area or None.
        """

        if self._convex_hull_area is None:
            self._calculate_convex_hull_area()
        return self._convex_hull_area * self._feature_multiplier**2

    @property
    def average_diameter(self) -> float:
        """Returns the average diameter of a polygon.

        Returns:
            float: Average diameter.
        """
        if self._average_diameter is None:
            self._calculate_average_diameter()
        return self._average_diameter * self._feature_multiplier

    @property
    def minor_axis(self) -> float:
        """Return the minor axis of the polygon.

        Returns:
            float: Minor axis length.
        """
        if self._minor_axis is None:
            self._calculate_axes()
        return self._minor_axis * self._feature_multiplier

    @property
    def major_axis(self) -> float:
        """Return the major axis of the polygon.

        Returns:
            float: major axis length.
        """
        if self._major_axis is None:
            self._calculate_axes()
        return self._major_axis * self._feature_multiplier

    @property
    def aspect_ratio(self) -> float:
        """Ratio between minor and major axis.

        Returns:
            float: Ellipse's aspect ratio.
        """
        if self._aspect_ratio is None:
            self._calculate_aspect_ratio()
        return self._aspect_ratio

    @property
    def perimeter(self) -> Union[float, None]:
        """Total length of polygon's boundary determined by cv2 contour operations.

        Returns:
            Union[float, None]: Polygon's perimeter or None.
        """

        if self._perimeter is None:
            self._calculate_perimeter()
        return self._perimeter * self._feature_multiplier

    @property
    def roundness(self) -> Union[float, None]:
        """Roundness: Area / (radius_enclosing_circle**2 * pi).

        Returns:
            Union[float, None]: Polygon's roundness in [0, 1] or None.
        """

        if self._roundness is None:
            self._calculate_roundness()
        return self._roundness

    def to_dict(
        self,
        decimals: int = 2,
        features: Union[List[str], None] = None,
        metric_unit="",
        feature_multiplier: int = 1,
        **kwargs,
    ) -> dict:
        """Returns a dictionary of the annotation in AxionBio format.

        Args:
            decimals (int, optional): The number of decimals to use when rounding. Defaults to 2.
            features (Union[List[str], None], optional): The features that are calculated and returned in the dict.
                Defaults to None, which means all features are calculated and returned.
            metric_unit (str, optional): The suffic added to the dict key names in camelCasing. Defaults to "".
                For example: "area" with suffix "um" becomes "areaUm"
            feature_multiplier (int, optional): A multiplier used during feature calculations. For example; 1/742. Defaults to 1.

        Raises:
            ValueError: It raises and error if any of the features are not compatible with the Annotation Manager.

        Returns:
            dict: a dictionary of the annotation in AxionBio format with the calculated features.
        """
        self._feature_multiplier = feature_multiplier

        # Check if features list is provided; otherwise, return all features
        if features is None:
            features = list(self._all_features.keys())
        else:
            missing_features = set(features).difference(set(self._all_features.keys()))
            if missing_features:
                raise ValueError(
                    f"The following features are not compatible with the Annotation Manager: {', '.join(missing_features)}"
                )

        points = self._points.copy()
        inner_points = self._inner_points.copy()
        if kwargs.get("do_compress", False):
            points = compress_polygon_points(
                points,
                kwargs.get("epsilon", 3),
                min_number_of_points=MIN_NR_POINTS_POLYGON,
            )
            inner_points = [
                compress_polygon_points(
                    inner_polygon,
                    kwargs.get("epsilon", 3),
                    min_number_of_points=MIN_NR_POINTS_POLYGON,
                )
                for inner_polygon in inner_points
            ]

        inner_polygons = []
        for inner_polygon in inner_points:
            inner_polygons.append(
                [asdict(inner_point) for inner_point in inner_polygon]
            )

        polygon_dict = {
            "type": "polygon",
            "points": [asdict(point) for point in points],
            "inner_points": inner_polygons,
        }

        polygon_features = {}
        for feature in features:
            feature_name = (
                feature
                if self._all_features[feature]["is_ratio"]
                else feature + "_" + metric_unit
            )

            # Convert snake_casing to camelCasing
            first_word, *remaining_words = feature_name.split("_")
            feature_name = "".join(
                [first_word.lower(), *map(str.title, remaining_words)]
            )

            polygon_features[feature_name] = round(getattr(self, feature), decimals)
        polygon_dict = {**polygon_features, **polygon_dict}

        super_dict = super().to_dict(decimals=decimals)
        dict_return_value = {**super_dict, **polygon_dict}
        return dict_return_value

    def is_in_mask(self, mask_json: List[dict], min_overlap: float = 0.9):
        """Check if a polygon is within a binary mask.

        Args:
            mask_json (List[dict]): A list of dict masks in AxionBio dict format.
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
            points = np.array(
                [[point.x, point.y] for point in self._points], dtype=np.int32
            )
            cv2.fillPoly(mask, [points], color=1)

        if self._inner_points:
            mask_inner = np.zeros(shape, dtype=np.uint8)
            for inner_polygon in self._inner_points:
                points = np.array(
                    [[point.x, point.y] for point in inner_polygon], dtype=np.int32
                )
                cv2.fillPoly(mask_inner, [points], color=1)
            mask = mask - mask_inner

        return mask

    def _calculate_area(self) -> None:
        # outer area for calculating circularity f.e.
        self._outer_area = cv2.contourArea(self._contour)
        self._area = self._outer_area
        for inner_contour in self._inner_contours:
            area_inner = cv2.contourArea(inner_contour)
            self._area -= area_inner

    def _calculate_circularity(self):
        if not self._outer_area:
            self._calculate_area()

        if not self._perimeter:
            self._calculate_perimeter()

        self._circularity = (4 * np.pi * self._outer_area) / (self._perimeter**2)

    def _calculate_convex_hull_area(self) -> None:
        convex_hull = cv2.convexHull(self._contour)
        self._convex_hull_area = cv2.contourArea(convex_hull)

    def _calculate_perimeter(self) -> None:
        self._perimeter = cv2.arcLength(self._contour, True)

    def _calculate_roundness(self) -> None:
        if not self._outer_area:
            self._calculate_area()

        _, radius = cv2.minEnclosingCircle(self._contour)
        enclosing_circle_area = radius**2 * np.pi
        self._roundness = self._outer_area / enclosing_circle_area

    def _calculate_axes(self) -> None:
        _, (diameter_1, diameter_2), _ = cv2.fitEllipse(self._contour)
        self._minor_axis = min(diameter_1, diameter_2)
        self._major_axis = max(diameter_1, diameter_2)

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
        are_points_equal_mirrored = are_lines_equal(
            self.points, reverse_points, is_enclosed=True
        )
        return are_points_equal | are_points_equal_mirrored
