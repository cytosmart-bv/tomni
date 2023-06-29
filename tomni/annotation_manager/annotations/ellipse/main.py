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
        """
        super().__init__(id, label, children, parents)
        self._center: Point = center
        self.radius_x: float = radius_x
        if radius_y:
            self.radius_y: float = radius_y
        else:
            self.radius_y: float = radius_x
        self.rotation: float = rotation

        self._circularity: Union[float, None] = None
        self._area: Union[float, None] = None
        self._perimeter: Union[float, None] = None
        self._aspect_ratio: Union[float, None] = None

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
    def circularity(self) -> float:
        """Circularity described by 4 * pi * Area / Perimeter**2.

        Returns:
            float: Ellipse's circularity.
        """
        if not self._circularity:
            self._calculate_circularity()

        return self._circularity

    @property
    def area(self) -> float:
        """Area described by pi * radius_x * radius_y.

        Returns:
            float: Ellipse's area.
        """
        if not self._area:
            self._calculate_area()

        return self._area

    @property
    def perimeter(self) -> float:
        """Perimeter described by 2*pi*sqrt((radius_x**2 + radius_y**2) / 2).

        Returns:
            float: Ellipse's perimeter.
        """
        if not self._perimeter:
            self._calculate_perimeter()

        return self._perimeter

    @property
    def aspect_ratio(self) -> float:
        """Ratio between minor and major axis in this case radius_x * 2 / radius_y * 2.

        Returns:
            float: Ellipse's aspect ratio.
        """
        if not self._aspect_ratio:
            self._calculate_aspect_ratio()

        return self._aspect_ratio

    def to_dict(self, decimals: int = 2, **kwargs) -> dict:
        dict_ellipse = {
            "type": "ellipse",
            "center": asdict(self.center),
            "radiusX": self.radius_x,
            "radiusY": self.radius_y,
            "angleOfRotation": self.rotation,
            "aspect_ratio": round(self.aspect_ratio, decimals),
            "area": round(self.area, decimals),
            "circularity": round(self.circularity, decimals),
            "perimeter": round(self.perimeter, decimals),
        }

        super_dict = super().to_dict(decimals=2)
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

    def is_in_mask(self, mask_json: dict, min_overlap: float = 0.9) -> bool:
        """Check if an ellipse is within a binary mask.

        Args:
            mask_json (dict): A dict mask in cytosmart dict format.
            min_overlap (float, optional): Minimum overlap required between the ellipse and the mask, expressed as a value between 0 and 1. Defaults to 0.9.

        Returns:
            bool: True if the ellipse is within the mask and meets the required overlap, False otherwise.
        """

        json_object = {
            "type": "ellipse",
            "center": {"x": self.center.x, "y": self.center.y},
            "radiusX": self.radius_x,
            "radiusY": self.radius_y,
            "angleOfRotation": self.rotation,
        }

        overlap_ratio = overlap_object(json_object, mask_json)

        # Check if the polygon is within the masked area with at least the specified overlap
        return overlap_ratio >= min_overlap

    def _calculate_circularity(self) -> None:
        self._circularity = 4 * np.pi * self.area / self.perimeter**2

    def _calculate_perimeter(self) -> None:
        self._perimeter = 2 * np.pi * np.sqrt((self._radius_x**2 + self._radius_y**2) / 2)

    def _calculate_area(self) -> None:
        self._area = np.pi * self._radius_x * self._radius_y

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
