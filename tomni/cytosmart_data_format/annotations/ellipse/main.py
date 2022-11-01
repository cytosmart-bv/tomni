import numpy as np
from cell_fea.morphology import circularity

from ..annotation import Annotation
from ..point import Point


class Ellipse(Annotation):
    def __init__(self, radius: Point, center: Point, rotation: float):
        self._radius: Point = radius
        self._center: Point = center
        self._rotation: float = rotation

        self._circularity = None
        self._roundness = None
        self._area = None
        self._perimeter = None
        # self._perimeter?

    @property.getter
    def radius(self) -> Point:
        """x and y
        """
        return self._radius

    @property.getter
    def center(self) -> Point:
        """x and y
        """
        return self._center

    @property.getter
    def rotation(self) -> float:
        """ rotation in degree.
        """
        pass
        return self._rotation

    @property.getter
    def get_circluratiy(self) -> str:
        if not self._circularity:
            # Circularity (C) = 4 * pi * Area / perimeter**2
            # Perimeter/circumference = 2*pi*sqrt((radX**2 + radY**2) / 2)
            # Ellipse Area = pi * radX * radY
            perimeter = (
                2 * np.pi * np.sqrt((self._radius.x ** 2 + self._radius.y ** 2) / 2)
            )
            circularity = (
                4 * np.pi * (np.pi * self._radius.x * self._radius.y) / perimeter ** 2
            )
            self._circularity = circularity
            return self._circularity
        else:
            return self._circularity

