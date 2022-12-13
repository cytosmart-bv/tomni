import uuid
from typing import Dict, List

import numpy as np

from .annotations import Annotation, Ellipse, Point, Polygon
from .utils import compress_polygon_points, parse_points_to_contour


class CytoSmartDataFormat(object):
    def __init__(self, annotations: List[Annotation]):
        """Initializes a CytoSmartDataFormat object.

        Args:
            annotations (List[Annotation]): Collection of annotations, e.g. polygon or ellipse.
        """
        self._annotations = annotations

    @classmethod
    def from_dicts(cls, dicts: List[dict], compress: bool = False, **kwargs):
        """Initializes a CDF object from a collection of CDF dictionaries.

        Args:
            dicts (List[dict]): List of CytoSmartDataFormat dictionaries.
            compress (bool, optional): Whether to apply lossy compression. If compress, additional parameters are used (see keyword args). 
                This is only applicable to polygon annotations. Other annotation types are skipped. Defaults to False.
        
        Keyword Args:
            mode (str): Compression mode. `rdp` or `recursive`.
            epsilon: If mode `rdp`, epsilon in the Ramer-Douglas-Peucker algorithm (RDP). Defaults to 0.9.
            n_iter: If mode `recursive`, nr. of iterations to recursively half points. Defaults to 3.
            
        Raises:
            ValueError: An error is raised when the dictionary contains neither polygon or ellipse type annotations.

        Returns:
            CytoSmartDataFormat: A CytoSmartDataFormat object initialized from passed dictionaries.
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
                )
            elif d[TYPE_KEY] == "polygon":
                points = [Point(x=p["x"], y=p["y"]) for p in d["points"]]
                if compress:
                    points = compress_polygon_points(
                        points=points,
                        mode=kwargs.get("mode", None),
                        n_iter=kwargs.get("n_iter", 3),
                        epsilon=kwargs.get("epsilon", 0.9),
                    )

                annotation = Polygon(
                    label=d.get(LABEL_KEY, None),
                    id=d.get(ID_KEY, str(uuid.uuid4())),
                    children=d.get(CHILDREN_KEY, []),
                    parents=d.get(PARENTS_KEY, []),
                    points=points,
                )
            else:
                raise ValueError(
                    f"CDF cannot be created. Dict with id {d.get('id', None)} misses type-key with value ellipse or polygon."
                )
            annotations.append(annotation)

        return cls(annotations)

    @classmethod
    def from_contours(
        cls, contours: List[np.ndarray], compress: bool = False, **kwargs
    ):
        """Initializes a CytoSmartDataFormat object from cv2 contours.
        Contours' shape must be [N, 1, 2] with dtype of np.int32.

        Args:
            contours (List[np.ndarray]): Collection of cv2 contours.
            compress (bool, optional): Whether to apply lossy compression. If compress, additional parameters are used (see keyword args). Defaults to False.

        Keyword Args:
            mode (str): Compression mode. `rdp` or `recursive`.
            epsilon: If mode `rdp`, epsilon in the Ramer-Douglas-Peucker algorithm (RDP). Defaults to 0.9.
            n_iter: If mode `recursive`, nr. of iterations to recursively half points. Defaults to 3.
        """
        annotations = []
        for contour in contours:
            # change shape from [N, 1, 2] to [N, 2]
            contour = np.vstack(contour)

            points: Point = []
            for i in range(contour.shape[0]):
                points.append(Point(x=int(contour[i][0]), y=int(contour[i][1])))

            if compress:
                points = compress_polygon_points(
                    points=points,
                    mode=kwargs.get("mode", None),
                    n_iter=kwargs.get("n_iter", None),
                    epsilon=kwargs.get("epsilon", None),
                )

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
        self, feature: str, min_val: float, max_val: float, inplace: bool = False,
    ):
        """Filter annotations by feature.

        Args:
            feature (str): Feature name, i.e. `roundness` or `area`.
            min_val (float): Minimum value to threshold.
            max_val (float): Maximum value to threshold
            inplace (bool, optional): If True, filter in-place. Modifies the object internally. If False, return collection of annotations. Defaults to False.

        Returns:
            CytoSmartDataFormat or List[Annotation]: Collection of filtered annotions or if `inplace=True` object with filterd annotations.
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
