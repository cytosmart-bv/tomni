from abc import ABC, abstractclassmethod, abstractproperty
from typing import Dict, List

import numpy as np


class Annotation(ABC):
    def __init__(self, cdf_item: Dict) -> None:
        self._id: str
        self._label: str
        self._children: List[Annotation]  # guid of the child
        self._parents: List[Annotation]  # guid of
        if not self._parse_item(cdf_item):
            # additional require contour?
            raise ValueError

    @abstractclassmethod
    def __str__(self) -> str:
        """Potentially use this built-in to create a json or something else.
        """
        pass

    @abstractclassmethod
    def _parse_item(self, cdf_item: Dict) -> bool:
        pass

    @property
    @abstractclassmethod
    def label(self) -> str:
        return self._label

    @label.setter
    @abstractclassmethod
    def label(self, value) -> str:
        # is a label mutuable?
        # its a maybe
        self._label = value

