import uuid
from typing import Dict, List, Tuple, Union

import cv2
import numpy as np

from tomni.transformers import labels2listsOfPoints, positions2contour

from .annotations import Annotation, Ellipse, Point, Polygon
from .utils import parse_points_to_contour

MIN_NR_POINTS = 5


class AnnotationManager(object):
    def __init__(self, annotations: List[Annotation]):
        """Initializes a AnnotationManager object.

        Args:
            annotations (List[Annotation]): Collection of annotations, e.g. polygon or ellipse.
        """
        self._annotations = annotations

    @classmethod
    def from_dicts(
        cls,
        dicts: List[dict],
    ):
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
                    accuracy=d.get("accuracy", 1),
                )
            elif d[TYPE_KEY] == "polygon":
                if len(d["points"]) < MIN_NR_POINTS:
                    continue
                if "inner_points" in d:
                    inner_points = [
                        [Point(x=pi["x"], y=pi["y"]) for pi in inner_contour]
                        for inner_contour in d["inner_points"]
                    ]

                annotation = Polygon(
                    label=d.get(LABEL_KEY, None),
                    id=d.get(ID_KEY, str(uuid.uuid4())),
                    children=d.get(CHILDREN_KEY, []),
                    parents=d.get(PARENTS_KEY, []),
                    points=[Point(x=p["x"], y=p["y"]) for p in d["points"]],
                    inner_points=inner_points,
                    accuracy=d.get("accuracy", 1),
                )
            else:
                raise ValueError(
                    f"CDF cannot be created. Dict with id {d.get('id', None)} misses type-key with value ellipse or polygon."
                )
            annotations.append(annotation)

        return cls(annotations)

    @classmethod
    def from_contours(
        cls,
        contours: List[np.ndarray],
        hierarchy: Union[np.ndarray, None] = None,
    ):
        """Initializes a AnnotationManager object from cv2 contours.
        Contours' shape must be [N, 1, 2] with dtype of np.int32.

        Args:
            contours (List[np.ndarray]): Collection of cv2 contours.
            hierarchy (bool, optional): the hierarchy from cv2.findContours using the RETR_CCOMP mode.
                Defaults to None.
                Currently, only hierarchy returned by RETR_CCOMP is supported.
                If none, no hierarchy will be used.
        """

        annotations = []
        # Check whether inner contours are present
        if isinstance(hierarchy, np.ndarray):
            # Iterate over all contours and their hierarchies
            for idx, contour in enumerate(contours):
                current_hierarchy = hierarchy[0][idx]

                if current_hierarchy[-1] == -1:
                    # If the contour has no parent, it is an outer contour
                    if len(contour) < MIN_NR_POINTS:
                        continue

                    # change shape from [N, 1, 2] to [N, 2]
                    contour = np.vstack(contour)

                    outer_points = [Point(x=int(pt[0]), y=int(pt[1])) for pt in contour]

                    # Find the indices of the inner contours
                    inner_indices = [
                        i for i, h in enumerate(hierarchy[0]) if h[3] == idx
                    ]
                    # Add the corresponding inner contours
                    inner_contours = [
                        contours[inner_idx] for inner_idx in inner_indices
                    ]

                    list_of_inner_points = [
                        [
                            Point(x=int(pt[0]), y=int(pt[1]))
                            for pt in inner_contour.reshape(-1, 2)
                        ]
                        for inner_contour in inner_contours
                    ]

                    annotations.append(
                        Polygon(
                            label="",
                            id=str(uuid.uuid4()),
                            children=[],
                            parents=[],
                            points=outer_points,
                            inner_points=list_of_inner_points,
                        ),
                    )
        else:
            for contour in contours:
                if len(contour) < MIN_NR_POINTS:
                    continue
                contour = np.vstack(contour)
                points = [Point(x=int(pt[0]), y=int(pt[1])) for pt in contour]

                annotations.append(
                    Polygon(
                        label="",
                        id=str(uuid.uuid4()),
                        children=[],
                        parents=[],
                        points=points,
                        inner_points=[],
                    ),
                )
        return cls(annotations)

    @classmethod
    def from_binary_mask(
        cls,
        mask: np.ndarray,
        include_inner_contours: bool = False,
    ):
        """Initializes a AnnotationManager object from a binary mask.

        Args:
            mask (np.ndarray): Binary mask input.

        Returns:
            AnnotationManager: New annotation manager object from binary mask.
        """

        unique_values = np.unique(mask)
        assert np.array_equal(unique_values, np.array([0, 1])) or np.array_equal(
            unique_values, np.array([0, 255])
        ), "A binary mask must contain either 0 and 1 or 0 and 255 only."
        mask = mask.astype(np.uint8)

        mode = cv2.RETR_CCOMP if include_inner_contours else cv2.RETR_EXTERNAL
        contours, hierarchy = cv2.findContours(mask, mode, cv2.CHAIN_APPROX_SIMPLE)

        if include_inner_contours:
            return AnnotationManager.from_contours(contours, hierarchy=hierarchy)
        else:
            return AnnotationManager.from_contours(contours, None)

    @classmethod
    def from_labeled_mask(
        cls,
        mask: np.ndarray,
        include_inner_contours: bool = False,
    ):
        """Initializes a AnnotationManager object from a labeled mask.
        A labeled mask contains components indicated by the same pixel values (see example below).

        Example containing two components yielding a AnnotationManager object with two annotations:
        [[0,0,2,1,1],
        [0,0,2,0,0],
        [0,0,2,0,]]

        Args:
            mask (np.ndarray): A labeled mask with a max. nr. of components limited by max(np.uint32).
            include_inner_contours (bool, optional): Include annotations that are contained within another annotation. Defaults to False.

        Returns:
            AnnotationManager: A new AnnotationManager object.
        """
        # TODO: Seperate labeled objects and then findcontours seperately. (also add label parameter to from_contours)
        mask = mask.astype(np.uint8)
        _, mask = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)

        mode = cv2.RETR_CCOMP if include_inner_contours else cv2.RETR_EXTERNAL
        contours, hierarchy = cv2.findContours(mask, mode, cv2.CHAIN_APPROX_SIMPLE)

        if not include_inner_contours:
            return AnnotationManager.from_contours(contours, None)
        else:
            return AnnotationManager.from_contours(contours, hierarchy=hierarchy)

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

    def to_dict(
        self,
        decimals: int = 2,
        mask_json: Union[List[dict], None] = None,
        min_overlap: float = 0.9,
        features: Union[List[str], None] = None,
        metric_unit: str = "",
        feature_multiplier: int = 1,
        **kwargs,
    ) -> List[Dict]:
        """Transform AM object to a collection of our format.

        Args:
            decimals (int, optional): The number of decimals to use when rounding. Defaults to 2.
            mask_json (Union[dict, None], optional): The dict mask that indicates what area to include in the output dict.
                Defaults to None.
            min_overlap (float, optional): Minimum overlap required between the polygon and the mask, expressed as a value between 0 and 1
                Defaults to 0.9.
            features (Union[List[str], None], optional): The features that you want to calculate and add to the dict objects.
                Defaults to None, which returns all features.
            metric_unit (str, optional): The suffix you want to add to the dict keys' names in camelCasing. Defaults to "".
            feature_multiplier (int, optional): A multiplier used during feature calculation. For example 1/742. Defaults to 1.

        Returns:
            List[Dict]: Output is a list of dicts in cytosmart format.
        """

        if mask_json is not None:
            filtered_annotations = self._annotations.copy()
            filtered_annotations = [
                annotation
                for annotation in filtered_annotations
                if annotation.is_in_mask(mask_json, min_overlap)
            ]

            return [
                annotation.to_dict(
                    decimals=decimals,
                    features=features,
                    metric_unit=metric_unit,
                    feature_multiplier=feature_multiplier,
                    **kwargs,
                )
                for annotation in filtered_annotations
            ]

        return [
            annotation.to_dict(
                decimals=decimals,
                features=features,
                metric_unit=metric_unit,
                feature_multiplier=feature_multiplier,
                **kwargs,
            )
            for annotation in self._annotations
        ]

    def to_contours(self) -> List[np.ndarray]:
        """Transform AM object to a collection of cv2 contours.

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

    def to_binary_mask(self, shape: Tuple[int, int]) -> np.ndarray:
        """Transform an AM object to a binary mask.
        Annotations can only be polygon or ellipse.

        Args:
            shape (Tuple[int, int]): Shape of the new binary mask.

        Returns:
            np.ndarray: A binary mask in [0, 1].
        """
        mask = np.zeros(shape, dtype=np.uint8)
        for annotation in self.annotations:
            mask = cv2.bitwise_or(mask, annotation.to_binary_mask(shape))

        return mask

    def to_labeled_mask(self, shape: Tuple[int, int]) -> np.ndarray:
        """Transform an AM object to a labeled mask.
        Annotations can only be polygon or ellipse.

        shape (Tuple[int, int]): Shape of the new labeled mask.

        Returns:
            np.ndarray: A new labeled mask.
        """
        mask = np.zeros(shape, dtype=np.uint8)
        label_color = 1

        for annotation in self._annotations:
            if isinstance(annotation, Polygon):
                points = np.array(
                    [[point.x, point.y] for point in annotation.points], dtype=np.int32
                )
                cv2.fillPoly(mask, [points], color=label_color)
            elif isinstance(annotation, Ellipse):
                cv2.ellipse(
                    mask,
                    center=(annotation.center.x, annotation.center.y),
                    axes=(annotation.radius_x, annotation.radius_y),
                    angle=annotation.rotation,
                    startAngle=0,
                    endAngle=360,
                    color=label_color,
                    thickness=-1,
                )
            else:
                raise TypeError(
                    "Innapropiate annotation type for `to_labeled_mask`. Supported annotations are ellipse and polygon."
                )

            # increase color for every annotation.
            label_color += 1

        return mask

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

    def filter(
        self,
        feature: str,
        min_val: float,
        max_val: float,
        feature_multiplier: int = 1,
        inplace: bool = False,
    ):
        """Filter annotations by feature.

        Args:
            feature (str): Feature name, i.e. `roundness` or `area`.
            min_val (float): Minimum value to threshold.
            max_val (float): Maximum value to threshold
            feature_multiplier (int, optional): A multiplier used in the feature calculations. For example 1/742. Defaults to 1.
            inplace (bool, optional): If True, filter in-place. Modifies the object internally. If False, return collection of annotations. Defaults to False.

        Returns:
            AnnotationManager or List[Annotation]: Collection of filtered annotions or if `inplace=True` object with filterd annotations.
        """
        filtered_annotations = []

        for annotation in self._annotations:
            annotation._feature_multiplier = feature_multiplier
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
