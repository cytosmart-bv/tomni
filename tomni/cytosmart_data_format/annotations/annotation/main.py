from abc import ABC, abstractclassmethod, abstractproperty
from typing import Dict, List


class Annotation(ABC):
    # rename Shape
    def __init__(self, cdf_item: Dict) -> None:
        self._id: str
        self._label: str
        self._children: List[Annotation]  # guid of the child
        self._parents: List[Annotation]  # guid of
        if not self._parse_item(cdf_item):
            # additional require contour?
            raise ValueError

        # example feature.
        self._circularity = None
        pass

    @abstractclassmethod
    def __str__(self) -> str:
        """Potentially use this built-in to create a json or something else.
        """
        pass

    @abstractclassmethod
    def _parse_item(self, cdf_item: Dict) -> bool:
        pass

    @property.getter
    def get_label(self) -> str:
        pass

    @property.setter
    def set_label(self) -> str:
        # is a label mutuable?
        # its a maybe
        pass

    @property.getter
    @abstractproperty
    def get_circluratiy(self) -> str:
        """Circularity and other features. 
        """
        pass

