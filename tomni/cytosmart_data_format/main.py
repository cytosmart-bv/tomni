import uuid
from typing import Dict, List

import numpy as np

from .annotations import Annotation, Ellipse, Point, Polygon


class CytoSmartDataFormat(object):
    def __init__(self, annotations: List[Annotation]):
        self._annotations = annotations

        # another thing imaginable should be cover a whole scan where...
        # to break down into timepoints and timepoints do have cdf_data.
        # cdf_data has data types like ellipses, polygons, masks, etc.
        pass

    @classmethod
    def from_dicts(cls, dicts: List[dict]):
        TYPE_KEY = "type"
        LABEL_KEY = "label"
        CHILDREN_KEY = "children"
        PARENTS_KEY = "parents"
        ID_KEY = "id"
        CENTER_KEY = "center"
        annotations = []

        for d in dicts:
            if d[TYPE_KEY] == "ellipse":
                annotation = Ellipse(
                    label=d.get(LABEL_KEY, None),
                    id=d.get(ID_KEY, str(uuid.uuid4())),
                    children=d.get(CHILDREN_KEY, []),
                    parents=d.get(PARENTS_KEY, []),
                    radius_x=d["radiusX"],
                    radius_y=d.get("radiusY", None),
                    center=Point(x=d[CENTER_KEY]["x"], y=d[CENTER_KEY]["y"]),
                    rotation=d["angleOfRotation"],
                )
            elif d[TYPE_KEY] == "polygon":
                annotation = Polygon(
                    label=d.get(LABEL_KEY, None),
                    id=d.get(ID_KEY, str(uuid.uuid4())),
                    children=d.get(CHILDREN_KEY, []),
                    parents=d.get(PARENTS_KEY, []),
                    points=[Point(x=p["x"], y=p["y"]) for p in d["points"]],
                )
            else:
                raise ValueError(
                    f"CDF cannot be created. Dict with id {d.get('id', None)} misses type-key with value ellipse or polygon."
                )
            annotations.append(annotation)

        return cls(annotations)

    @classmethod
    def from_contours(cls, contours: List[np.ndarray]):
        """could be an option"""
        pass

    @classmethod
    def from_masks(cls, masks: List[np.ndarray]):
        """could be an option"""
        pass

    @classmethod
    def from_darwin(cls, dicts: List[dict]):
        """must be an option"""
        pass

    @property
    def annotations(self) -> List[Annotation]:
        return self._annotations

    @annotations.setter
    def annotations(self, other_annotations: List[Annotation]):
        """I doubt this setter should be allowed to exist.
        """

    def __len__(self) -> int:
        return len(self._annotations)

    def __eq__(self, other: object) -> bool:
        """To check equality of to CDF objects
        Thats bit of a tricky one because you must compare all annotations IMO.
        Ex: cdf1 = CytoDataFormat.from_something()
        cdf2 = CytoDataFormat.from_something()
        is cdf1 == cdf2 must be possible.
        """
        pass

    def __contains__(self, other: Annotation):
        """to check if self.annotations contains other.
        """
        pass

    def __iter__(self):
        self.idx = 0
        return self

    def __next__(self):
        if self.idx < self.__len__():
            annotation = self.annotations[self.idx]
            self.idx += 1
            return annotation
        else:
            raise StopIteration

    def to_dict(self, decimals: int = 2) -> List[Dict]:
        """Transform CDF object to a collection of our format.

        Args:
            decimals (int, optional): The number of decimals to use when rounding. Defaults to 2.

        Returns:
            List[Dict]: Collection of CDF dicts.
        """        
        return [annotation.to_dict(decimals=decimals) for annotation in self._annotations]

    def to_darwin(self) -> List[Dict]:
        """
        TODO: Convert annotations to darwin format (v7).
        """

    def __add__(self, other):
        """Ability to add to CDF objects together
        cdf1 + cdf2.

        or possiby
        - cdf + dict
        - cdf + darwin
        - ...
        """
        pass

    def __radd__(self, other):
        """Reverse of __add__
        if you do:
        dict + cdf -> error
        radd should flip the two parts and call add.
        so, dict + cdf becomes cdf + dict.
        """
        pass

    def delete_annotation(self, item: Annotation):
        """Remove an annotation from self.annotations.
        Find and delete.
        """
        pass

    @classmethod
    def get_circularity_summary(self):
        """loops the cdf items to get avg, std, min, max.
        """

    def get_feature_summaries(self, features: List[str]) -> Dict:
        """Pass a list of features to calculated.

        This is not ideal and i am for suggestion. I want to avoid having to calculate over and over.
        """
        circularity = []
        for cdf_item in self._cdf_data:
            circularity.append(cdf_item.circularity)

        return {
            "circularity": {"avg": 1, "std": 1, "min": 1, "max": 1},
            "...": "...",
            "feature_n": {"avg_n": 1, "std_n": 1, "min_n": 1, "max_n": 1},
        }
