from abc import ABC, abstractmethod
from typing import List


class Annotation(ABC):
    def __init__(self, id: str, label: str, children: List, parents: List) -> None:
        self._id: str = id
        self._label: str = label
        self._children: List[Annotation] = children
        self._parents: List[Annotation] = parents

    @abstractmethod
    def to_dict(self, decimals: int = 2) -> dict:
        """Creates a dictionary in CDF of annotation.
        Args:
            decimals (int, optional): The number of decimals to use when rounding. Defaults to 2.

        Returns:
            dict: CytoSmart Data Format dict.
        """        
        return {
            "id": self._id,
            "label": self._label,
            "children": self._children,
            "parents": self._parents,
        }

    @property
    @abstractmethod
    def label(self) -> str:
        return self._label

    @label.setter
    @abstractmethod
    def label(self, value) -> None:
        self._label = value
