import uuid
from typing import Dict, List

import numpy as np

from .annotations import Annotation, Ellipse, Point, Polygon
from .utils import parse_points_to_contour


class AnnotationManager(object):
    def __init__(self, annotations: List[Annotation]):
        """Initializes a AnnotationManager object.

        Args:
            annotations (List[Annotation]): Collection of annotations, e.g. polygon or ellipse.
        """
        self._annotations = annotations

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
        """Initializes a AnnotationManager object from cv2 contours.
        Contours' shape must be [N, 1, 2] with dtype of np.int32.

        Args:
            contours (List[np.ndarray]): Collection of cv2 contours.
        """
        annotations = []
        for contour in contours:
            # change shape from [N, 1, 2] to [N, 2]
            contour = np.vstack(contour)

            points: Point = []
            for i in range(contour.shape[0]):
                points.append(Point(x=int(contour[i][0]), y=int(contour[i][1])))

            annotations.append(
                Polygon(
                    label="",
                    id=str(uuid.uuid4()),
                    children=[],
                    parents=[],
                    points=points,
                )
            )

        return cls(annotations)

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
        """I doubt this setter should be allowed to exist."""

    def __len__(self) -> int:
        return len(self._annotations)

    def __eq__(self, other: object) -> bool:
        """To check equality of to CDF objects
        Thats bit of a tricky one because you must compare all annotations IMO.
        Ex: cdf1 = AnnotationManager.from_something()
        cdf2 = AnnotationManager.from_something()
        is cdf1 == cdf2 must be possible.
        """
        pass

    def __contains__(self, other: Annotation):
        """to check if self.annotations contains other."""
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
        return [
            annotation.to_dict(decimals=decimals) for annotation in self._annotations
        ]

    def to_contours(self) -> List[np.ndarray]:
        """Transform CDF object to a collection of cv2 contours.

        Raises:
            ValueError: Raises error when annotations are not of type `Polygon`.

        Returns:
            List[np.ndarray]: Collection of contours as [[[x_0, y_0],..., [x_n, y_n]], ... ,[[x_0, y_0],..., [x_m, y_m]]]
        """
        if not all(
            [isinstance(annotation, Polygon) for annotation in self._annotations]
        ):
            raise ValueError("`to_contours is only supported on polygon-annotations.`")

        contours = [
            parse_points_to_contour(annotation.points)
            for annotation in self._annotations
        ]

        return contours

    def to_darwin(self) -> List[Dict]:
        """
        TODO: Convert annotations to darwin format (v7).
        """

    def append(self, other: Annotation):
        assert isinstance(other, Annotation), f"other "

        self._annotations.append(other)

    def __add__(self, other):
        """Ability to add to CDF objects together
        cdf1 + cdf2.
        cdf + dict

        """
        assert type(self) == AnnotationManager

        if type(other) == AnnotationManager:
            new_annotations = self._annotations + other._annotations
            return AnnotationManager(new_annotations)

        elif isinstance(other, Annotation):
            new_annotations = self._annotations + [other]
            return AnnotationManager(new_annotations)

        elif type(other) == dict:
            other_cdf = AnnotationManager.from_dicts([other])
            new_annotations = self._annotations + other_cdf._annotations
            return AnnotationManager(new_annotations)

        elif type(other) == list:
            other_cdf = AnnotationManager.from_dicts(other)
            new_annotations = self._annotations + other_cdf._annotations
            return AnnotationManager(new_annotations)

        else:
            ValueError(f"{type(self)} , {type(other)}")

    def __radd__(self, other):
        """Reverse of __add__
        if you do:
        dict + cdf -> error
        radd should flip the two parts and call add.
        so, dict + cdf becomes cdf + dict.
        """
        return self.__add__(other)

    def delete_annotation(self, item: Annotation):
        """Remove an annotation from self.annotations.
        Find and delete.
        """
        pass

    def filter(
        self, feature: str, min_val: float, max_val: float, inplace: bool = False,
    ):
        """Filter annotations by feature.

        Args:
            feature (str): Feature name, i.e. `roundness` or `area`.
            min_val (float): Minimum value to threshold.
            max_val (float): Maximum value to threshold
            inplace (bool, optional): If True, filter in-place. Modifies the object internally. If False, return collection of annotations. Defaults to False.

        Returns:
            AnnotationManager or List[Annotation]: Collection of filtered annotions or if `inplace=True` object with filterd annotations.
        """
        filtered_annotations = []

        for annotation in self._annotations:
            feature_value = getattr(annotation, feature)
            if min_val <= feature_value <= max_val:
                filtered_annotations.append(annotation)

        if inplace:
            self._annotations = filtered_annotations
            return self

        return filtered_annotations

    @classmethod
    def get_circularity_summary(self):
        """loops the cdf items to get avg, std, min, max."""

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
