import gc
from dataclasses import asdict
from typing import List, Tuple, Union

import cv2
import numpy as np

from tomni.annotation_manager.annotations.annotation import Annotation
from tomni.annotation_manager.annotations.point import Point
from tomni.annotation_manager.utils import overlap_object


class Ellipse(Annotation):
    def __init__(
        self,
        radius_x: float,
        center: Point,
        rotation: float,
        id: str,
        label: str = "",
        children: List[Annotation] = [],
        parents: List[Annotation] = [],
        radius_y: Union[float, None] = None,
        accuracy: float = 1,
    ):
        """Initializes a Ellipse object.

        Args:
            radius_x (float): Radius of ellipse in X direction.
            radius_y (float): Radius of ellipse in Y direction.
                Defaults to None. If None, radius_y will inherit the value of radius_x.
            center (Point): Coordinate of the center (x, y).
            rotation (float): Angle of rotation in degrees.
                Rotations will be set between 0 and 90
                If a rotation is the high or low multiplies of 180 will be added or subtracted
                If a rotation is between 90 and 180 the radii will be flipped and 90 will be subtracted
            id (str): UUID identifier.
            label (str): Class label of annotation.
            children (List[Annotation]): Tracking annotations. Refers to t+1.
            parents (List[Annotation]): Tracking annotations. Refers to t-1.
            accuracy (float, optional): The confidence of the model's prediction. Defaults to 1.
        """
        super().__init__(id, label, children, parents, accuracy)
        self._center: Point = center
        self.radius_x: float = radius_x
        if radius_y:
            self.radius_y: float = radius_y
        else:
            self.radius_y: float = radius_x
        self.rotation: float = rotation

        self._feature_multiplier: float = 1
        self._area: Union[float, None] = None
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
    def accuracy(self):
        """Accuracy of ellipse."""
        return self._accuracy

    @accuracy.setter
    def points(self, *arg, **kwargs) -> None:
        raise SyntaxError("Accuracy is Immutable")

    @property
    def label(self):
        return super().label

    @label.setter
    def label(self, value) -> None:
        super().label = value

    @property
    def radius_x(self) -> float:
        """Radius of ellipse in X direction."""
        return self._radius_x

    @radius_x.setter
    def radius_x(self, new_radius_x):
        self._radius_x = new_radius_x

    @property
    def radius_y(self) -> float:
        """Radius of ellipse in X direction."""
        return self._radius_y

    @radius_y.setter
    def radius_y(self, new_radius_y):
        self._radius_y = new_radius_y

    @property
    def center(self) -> Point:
        """Center of ellipse."""
        return self._center

    @property
    def rotation(self) -> float:
        """Rotation in degrees."""
        return self._rotation

    @rotation.setter
    def rotation(self, new_rotation) -> float:
        # Everything above 180 is a repetition of below
        new_rotation = new_rotation % 180
        if new_rotation >= 90:
            self.radius_x, self.radius_y = self.radius_y, self.radius_x
            self._rotation = new_rotation % 90
        else:
            self._rotation = new_rotation

    @property
    def area(self) -> float:
        """Area described by pi * radius_x * radius_y.

        Returns:
            float: Ellipse's area.
        """
        if self._area is None:
            self._calculate_area()
        return self._area * self._feature_multiplier**2

    @property
    def circularity(self) -> float:
        """Circularity described by 4 * pi * Area / Perimeter**2.

        Returns:
            float: Ellipse's circularity.
        """
        if self._circularity is None:
            self._calculate_circularity()
        return self._circularity

    @property
    def convex_hull_area(self) -> Union[float, None]:
        """Calculate the convex hull area of an ellipse.

        This property computes the area of the convex hull of the ellipse using the formula:
        Area = π * radius_x * radius_y.

        Returns:
            Union[float, None]: The convex hull area of the ellipse, or None if it cannot be calculated.
        """
        if self._convex_hull_area is None:
            self._calculate_convex_hull_area()
        return self._convex_hull_area * self._feature_multiplier**2

    @property
    def average_diameter(self) -> float:
        """Returns the average diameter of an ellipse.

        Returns:
            float: Average diameter.
        """
        if self._average_diameter is None:
            self._calculate_average_diameter()
        return self._average_diameter * self._feature_multiplier

    @property
    def minor_axis(self) -> float:
        """Returns the minor axis of an ellipse.

        Returns:
            float: Minor axis length.
        """
        if self._minor_axis is None:
            self._calculate_minor_axis()
        return self._minor_axis * self._feature_multiplier

    @property
    def major_axis(self) -> float:
        """Return the major axis of the polygon.

        Returns:
            float: major axis length.
        """
        if self._major_axis is None:
            self._calculate_major_axis()
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
    def perimeter(self) -> float:
        """Perimeter described by 2*pi*sqrt((radius_x**2 + radius_y**2) / 2).

        Returns:
            float: Ellipse's perimeter.
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

        dict_ellipse = {
            "type": "ellipse",
            "center": asdict(self.center),
            "radiusX": self.radius_x,
            "radiusY": self.radius_y,
            "angleOfRotation": self.rotation,
        }

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

            dict_ellipse[feature_name] = round(getattr(self, feature), decimals)

        super_dict = super().to_dict(decimals=decimals)
        dict_return_value = {**super_dict, **dict_ellipse}
        return dict_return_value

    def to_binary_mask(self, shape: Tuple[int, int]) -> np.ndarray:
        """Transform an ellipse to a binary mask.

        Args:
            shape (Tuple[int, int]): Shape of the new ellipse's binary mask.

        Returns:
            np.ndarray: A binary mask in [0, 1].
        """
        mask = np.zeros(shape, dtype=np.uint8)
        return cv2.ellipse(
            mask,
            center=(self.center.x, self.center.y),
            axes=(self.radius_x, self.radius_y),
            angle=self.rotation,
            startAngle=0,
            endAngle=360,
            color=1,
            thickness=-1,
        )

    def is_in_mask(self, mask_json: List[dict], min_overlap: float = 0.9) -> bool:
        """Check if an ellipse is within a binary mask.

        Args:
            mask_json (List[dict]): A list of dict masks in AxionBio dict format.
            min_overlap (float, optional): Minimum overlap required between the ellipse and the mask, expressed as a value between 0 and 1. Defaults to 0.9.

        Returns:
            bool: True if the ellipse is within a mask and meets the required overlap, False otherwise.
        """

        json_object = {
            "type": "ellipse",
            "center": {"x": self.center.x, "y": self.center.y},
            "radiusX": self.radius_x,
            "radiusY": self.radius_y,
            "angleOfRotation": self.rotation,
        }

        for mask in mask_json:
            overlap_ratio = overlap_object(json_object, mask)
            if overlap_ratio >= min_overlap:
                return True

        return False

    def _calculate_circularity(self) -> None:
        if not self._area:
            self._calculate_area()

        if not self._perimeter:
            self._calculate_perimeter()

        self._circularity = 4 * np.pi * self._area / self._perimeter**2

    def _calculate_perimeter(self) -> None:
        self._perimeter = (
            2 * np.pi * np.sqrt((self._radius_x**2 + self._radius_y**2) / 2)
        )

    def _calculate_roundness(self) -> None:
        if not self._area:
            self._calculate_area()

        if not self._major_axis:
            self._calculate_major_axis()

        if self.major_axis == 0:
            self._roundness = 0
        else:
            enclosing_circle_area = (self._major_axis / 2) ** 2 * np.pi
            self._roundness = self._area / enclosing_circle_area

    def _calculate_area(self) -> None:
        self._area = np.pi * self._radius_x * self._radius_y

    def _calculate_convex_hull_area(self) -> None:
        if not self._area:
            self._calculate_area()
        self._convex_hull_area = self._area

    def _calculate_minor_axis(self) -> None:
        self._minor_axis = min(self._radius_x, self._radius_y) * 2

    def _calculate_major_axis(self) -> None:
        self._major_axis = max(self._radius_x, self._radius_y) * 2

    def _calculate_average_diameter(self) -> None:
        self._average_diameter = (self._radius_x * 2 + self._radius_y * 2) / 2

    def _calculate_aspect_ratio(self) -> None:
        if self._radius_x == self._radius_y:
            self._aspect_ratio = 1.0
        elif self._radius_x > self._radius_y:
            self._aspect_ratio = self._radius_y / self._radius_x
        else:
            self._aspect_ratio = self._radius_x / self._radius_y

    def __eq__(self, other):
        if self.radius_x != other.radius_x:
            return False

        if self.radius_y != other.radius_y:
            return False

        if self.rotation != other.rotation:
            return False

        if self.center != other.center:
            return False

        return True
