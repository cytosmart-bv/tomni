from cell_fea.morphology import circularity

from ..annotation import Annotation
from ..point import Point


class Ellipse(Annotation):
    def __init__(self, radius: Point, center: Point, rotation: float):
        self._radius: Point = radius
        self._center: Point = center
        self._rotation: float = rotation

        self._circularity = None
        pass

    @property.getter
    def radius(self) -> Point:
        """x and y
        """
        pass

    @property.getter
    def center(self) -> Point:
        """x and y
        """
        pass

    @property.getter
    def rotation(self) -> float:
        """ rotation in degree.
        """
        pass

    @property.getter
    def get_circluratiy(self) -> str:
        if not self._circularity:
            # FIXME: Probably some helper function to get contours or simply tomni.
            self._circularity = circularity([[0]])
            return self._circularity
        else:
            return self._circularity

