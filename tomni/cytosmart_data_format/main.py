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

    @classmethod
    def from_contours(cls, contours: List[np.ndarray]):
        """could be an option"""
        pass

    def __len__(self) -> int:
        return len(self._cdf_data)

    def __eq__(self, __o: object) -> bool:
        # if {}== {}:
        """To check equality of to cdf items"""
        pass

    def compare_two_json_list(self):
        """aka two cdf object
        """
        pass

    def __iter__(self):
        # Something like that.
        # Potentially look into combination of __next__ and __iter__
        while True:
            yield self._cdf_data

    def __dict__(self) -> List[Dict]:  # Alternative: to_json.
        """To convert the cdf_data into a json dict.
        May require and encoder or a seperate function, e.g. to_json, rather than the built-in __dict__.
        # Filters, gating
        """
        pass

    def _parse_data_objects(cdf_dicts: List[Dict]):
        """To parse cdf dicts to proper data types
        """
        pass

    @property
    def cdf_data(self) -> List[Annotation]:
        return self._cdf_data

    @cdf_data.setter
    def cdf_data(self, cdf_dicts: List[Dict]):
        self._cdf_data = self._parse_data_objects(cdf_dicts)

    @classmethod
    def add_cdf_data(self, cdf_dicts: Union[List[Dict], Dict]):
        """Parse and add to cdf data if not already exists
        """
        pass

    @classmethod
    def remove_cdf_data(self, cdf_dicts: Union[List[Dict], Dict]):
        """Parse and add to cdf data if not already exists
        """
        pass

    @classmethod
    def cdf_data_contains_item(self, cdf_item: Dict) -> bool:
        """Check for `cdf_item` in self._cdf_data.items
        First parse cdf_item.
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
