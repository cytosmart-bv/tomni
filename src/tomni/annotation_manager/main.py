import uuid
from typing import Dict, List, Tuple, Union

import cv2
import numpy as np

from tomni.annotation_manager.utils.contours2polygons import contours2polygons
from .annotations import Annotation, Ellipse, Point, Polygon
from .utils import parse_points_to_contour

MIN_NR_POINTS_POLYGON = 5


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
        """
        Initializes the class with a list of dictionaries containing annotations.

        Args:
            cls ('AnnotationManager'): The class itself.
            dicts (List[dict]): A list of dicts containing annotations.

        Raises:
            ValueError: Raised if the input dictionaries are not properly formatted.

        Note:
            Only Polygon and Ellipse annotations are supported.

        Returns:
            AnnotationManager: An instance of the AnnotationManager class containing the parsed annotations.
        """
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
                if len(d["points"]) < MIN_NR_POINTS_POLYGON:
                    continue
                if "inner_points" in d:
                    inner_points = [
                        [Point(x=pi["x"], y=pi["y"]) for pi in inner_contour]
                        for inner_contour in d["inner_points"]
                    ]
                else:
                    inner_points = []

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
    def from_binary_mask(
        cls, mask: np.ndarray, include_inner_contours: bool = False, label: str = ""
    ):
        """
        Initializes an AnnotationManager object from a binary mask.

        Args:
            cls ('AnnotationManager'): The class itself.
            mask (np.ndarray): Binary mask input.
            include_inner_contours (bool, optional): Include annotations that are contained within another annotation.
                Defaults to False.
            label (str, optional): A label to assign to the annotations. Defaults to "".

        Returns:
            AnnotationManager: A new AnnotationManager object created from the binary mask.
        """

        mask = mask.astype(np.uint8)
        mode = cv2.RETR_CCOMP if include_inner_contours else cv2.RETR_EXTERNAL
        contours, hierarchy = cv2.findContours(mask, mode, cv2.CHAIN_APPROX_SIMPLE)

        annotations = contours2polygons(
            contours=contours,
            hierarchy=hierarchy,
            include_inner_contours=include_inner_contours,
            label=label,
        )

        return cls(annotations)

    @classmethod
    def from_labeled_mask(
        cls,
        mask: np.ndarray,
        labels: Union[List[str], str] = "",
        include_inner_contours: bool = False,
    ):
        """
        Initializes an AnnotationManager object from a labeled mask.
        A labeled mask contains components indicated by the same pixel values.

        Args:
            cls ('AnnotationManager'): The class itself.
            mask (np.ndarray): A labeled mask with a maximum number of components limited by max(np.uint32).
            labels (Union[List[str], str], optional): A list of class names to add to Polygon labels. Defaults to "".
                Should have the same number of unique pixel values as classes.
                Class names in order of low pixel value to high pixel value.
            include_inner_contours (bool, optional): Include annotations that are contained within another annotation.
                Defaults to False.

        Example input with multiple pixel values::

            [
                [0, 0, 2, 1, 1],
                [0, 0, 2, 0, 0],
                [0, 0, 2, 0, 0]
            ]

        Returns:
            AnnotationManager: A new AnnotationManager object.
        """
        mode = cv2.RETR_CCOMP if include_inner_contours else cv2.RETR_EXTERNAL

        annotations = []
        if isinstance(labels, str):
            mask = mask.astype(np.uint8)
            _, mask = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(mask, mode, cv2.CHAIN_APPROX_SIMPLE)

            annotations = contours2polygons(
                contours=contours,
                include_inner_contours=include_inner_contours,
                hierarchy=hierarchy,
                label=labels,
            )

        elif isinstance(labels, List):
            unique_values = np.unique(mask)
            unique_values = unique_values[unique_values != 0]

            if len(labels) < len(unique_values):
                raise ValueError(
                    f"Not enough labels for unique pixel values. {len(labels)} labels for {len(unique_values)} unique pixel values."
                )

            # Generate seperate mask for each class and find contours.
            for pixel_value in unique_values:
                class_mask = np.uint8(mask == pixel_value)
                contours, hierarchy = cv2.findContours(
                    class_mask, mode, cv2.CHAIN_APPROX_SIMPLE
                )
                annotations.extend(
                    contours2polygons(
                        contours=contours,
                        hierarchy=hierarchy,
                        include_inner_contours=include_inner_contours,
                        label=labels[pixel_value - 1],
                    )
                )
        else:
            raise ValueError("Labels must be either a string or a list of strings.")

        return cls(annotations)

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
        feature_multiplier: float = 1,
        **kwargs,
    ) -> List[Dict]:
        """
        Transform the AnnotationManager object into a collection of data in AxionBio format.

        Args:
            decimals (int, optional): The number of decimals to use when rounding. Defaults to 2.
            mask_json (Union[dict, None], optional): The dictionary mask that indicates the area to include in the output dictionary.
                Defaults to None.
            min_overlap (float, optional): Minimum overlap required between the polygon and the mask, expressed as a value between 0 and 1.
                Defaults to 0.9.
            features (Union[List[str], None], optional): The features you want to calculate and add to the dictionary objects.
                Defaults to None, which returns all features.
            metric_unit (str, optional): The suffix to add to the dictionary keys' names in camelCasing. Defaults to "".
            feature_multiplier (float, optional): A multiplier used during feature calculation, e.g., 1/742. Defaults to 1.

        Note:
            - If a `mask_json` is provided, the method filters annotations based on their overlap with the mask.
            - Only annotations meeting the specified `min_overlap` criteria are included in the output.
            - If no `mask_json` is provided, all annotations are included in the output.

        Returns:
            List[Dict]: Output is a list of dictionaries in AxionBio format.
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
        """
        Transform an AnnotationManager object to a collection of OpenCV-style contours.

        This method generates a collection of contours from the annotations stored in the AnnotationManager object.
        Supported annotation type for conversion is 'Polygon'. Each contour is represented as a NumPy array of shape
        (N, 1, 2), where N is the number of points in the contour, and each point has (x, y) coordinates.

        Raises:
            ValueError: If any annotation in the AnnotationManager is not of type 'Polygon'.

        Returns:
            List[np.ndarray]: A collection of contours, where each contour is represented as a NumPy array.

        Note:
            - This method supports only annotations of type 'Polygon' for conversion to contours.
            - Each contour is represented as a NumPy array of shape (N, 1, 2), where N is the number of points in
              the contour, and each point has (x, y) coordinates.
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
        """
        Transform an AnnotationManager object to a binary mask.

        This method generates a binary mask from the annotations stored in the AnnotationManager object.
        Supported annotation types for conversion are polygon and ellipse.

        Args:
            shape (Tuple[int, int]): The shape (width, height) of the new binary mask.

        Returns:
            np.ndarray: A binary mask where annotated regions are represented by 1 (True) and
            non-annotated regions are represented by 0 (False).

        Note:
            - This method supports annotations of type Polygon and Ellipse for conversion to a binary mask.
            - The binary mask represents annotated regions with 1 and non-annotated regions with 0.
        """

        mask = np.zeros(shape, dtype=np.uint8)
        for annotation in self.annotations:
            mask = cv2.bitwise_or(mask, annotation.to_binary_mask(shape))

        return mask

    def to_labeled_mask(self, shape: Tuple[int, int]) -> np.ndarray:
        """
        Transform an Annotation Manager object to a labeled mask. This method generates a labeled mask from the annotations stored in the AnnotationManager object. Supported
        annotation types for conversion are polygon and ellipse.

        Args:
            shape (Tuple[int, int]): The shape (width, height) of the new labeled mask.

        Returns:
            np.ndarray: A new labeled mask where each labeled region corresponds to an annotation.

        Raises:
            TypeError: If the AnnotationManager contains annotations of unsupported types.

        Note:
            - This method supports annotations of type Polygon and Ellipse for conversion to a labeled mask.
            - Each labeled region in the generated mask corresponds to an annotation, and the regions are labeled with unique integer values starting from 1.
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
        feature_multiplier: float = 1.0,
        inplace: bool = False,
    ):
        """
        Filter annotations based on a specified feature.

        This method filters annotations in the AnnotationManager based on a given feature within a specified value range.
        Annotations that meet the filtering criteria are included in the result.

        Args:
            feature (str): The name of the feature to use for filtering, e.g., 'roundness' or 'area'.
            min_val (float): The minimum threshold value for the feature.
            max_val (float): The maximum threshold value for the feature.
            feature_multiplier (float, optional): A multiplier used in feature calculations. Defaults to 1.
            inplace (bool, optional): If True, filter annotations in-place, modifying the object internally.
                If False, return a collection of filtered annotations without modifying the original object. Defaults to False.

        Returns:
            Union[AnnotationManager, List[Annotation]]: If `inplace=True`, returns the AnnotationManager object
            with the filtered annotations. If `inplace=False`, returns a list of filtered annotations.

        Note:
            - This method filters annotations based on a specified feature within the provided value range.
            - The `feature_multiplier` parameter allows scaling of the feature calculation if needed.
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
