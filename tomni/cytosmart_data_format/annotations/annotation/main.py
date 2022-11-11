from abc import ABC, abstractmethod
from typing import List


class Annotation(ABC):
    def __init__(self, id: str, label: str, children: List, parents: List) -> None:
        self._id: str = id
        self._label: str = label
        self._children: List[Annotation] = children
        self._parents: List[Annotation] = parents

    @abstractmethod
    def to_dict(self) -> dict:
        """Creates a dictionary in CDF of annotation.

        Returns:
            dict: Dictionary of anntation.
        """
        return {
            "id": self.id,
            "label": self.label,
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

