from typing import Dict, List, Union

import numpy as np

from .annotations import Annotation, Point, Polygon


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
        annotations = []

        for d in dicts:
            if d[TYPE_KEY] == "ellipse":
                print(1)
            elif d[TYPE_KEY] == "polygon":
                annotation = Polygon(
                    label=d.get(LABEL_KEY, None),
                    id=d[ID_KEY],
                    children=d[CHILDREN_KEY],
                    parents=d[PARENTS_KEY],
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

    def to_dict(self) -> List[Dict]:
        """To convert the cdf_data into a json dict.
        May require and encoder or a seperate function, e.g. to_json, rather than the built-in __dict__.
        # Filters, gating
        """
        pass

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

    def __del__(self, other):
        """Remove an annotation from self.annotations.
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
