from typing import List

from ..annotation import Annotation
from ..point import Point


class Polygon(Annotation):
    def __init__(self):
        self._points: List[Point]
        pass

    @property
    def points(self) -> List[Point]:
        """Points to be returned.
        """
        pass

    @property
    def get_feature_x(self) -> float:
        """Idea is to calculate feature once and store inside the annotation.
        """

