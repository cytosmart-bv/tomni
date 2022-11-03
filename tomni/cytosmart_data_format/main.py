from typing import Dict, List, Union

from .annotations import Annotation


class CytoSmartDataFormat:
    def __init__(self, cdf_dicts: List[Dict]):
        self._cdf_data = self._parse_data_objects(cdf_dicts)

        # another thing imaginable should be cover a whole scan where...
        # to break down into timepoints and timepoints do have cdf_data.
        # cdf_data has data types like ellipses, polygons, masks, etc.
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

    @property.setter
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
