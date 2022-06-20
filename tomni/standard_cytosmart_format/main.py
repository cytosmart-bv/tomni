from __future__ import annotations

import logging

from typing import List
from ..json_operations import add_area


def is_scf(scf_json):
    """Checks if an json complies with scf"""
    for i, scf_object in enumerate(scf_json):
        if not type(scf_json) == dict and not "type" in scf_object:
            logging.error(
                f"the {i}th element does not have the Standard CytoSMART Format"
            )
            return False
    return True


class SCFJson:
    def __init__(self, scf_json: List[dict]) -> None:
        """
        STANDARD CYTOSMART FORMAT
        Standardized annotation format of cytoSMART that has the following uses:
        - Validate that two annotations are the same even when they are processed at different times.

        Args:
            scf_json (list[dict]): a list of scf_objects that comply with SCF. allowed types 'polygon' and 'ellipse'
                polygon example:
                    {
                        "type": "polygon",
                        "points": [
                            {"x": 0, "y": 10},
                            {"x": 10, "y": 10},
                            {"x": 10, "y": 0},
                            {"x": 0, "y": 0},
                        ],
                        "id": "UNIQUE_ID",
                    }

                ellipse example:
                    {
                        "type": "ellipse",
                        "center": {"x": 20, "y": 30},
                        "radiusX": 10,
                        "radiusY": 12,
                        "angleOfRotation": 0,
                        "id": "UNIQUE_ID",
                    }

        Raises:
            ValueError: object is not in the Standard CytoSMART Format
        """
        if not is_scf(scf_json):
            raise ValueError("object is not in the Standard CytoSMART Format")
        scf_json = self._remove_id(scf_json)
        self._add_area_parameters(scf_json)
        self.scf_json = sorted(scf_json, key=lambda scf_object: scf_object["area"])

    def __len__(self) -> int:
        return len(self.scf_json)

    def __add__(self, other: SCFJson) -> SCFJson:
        return SCFJson(self.scf_json + other.scf_json)

    def __eq__(self, other: SCFJson) -> bool:
        return self.scf_json == other.scf_json

    @staticmethod
    def _add_area_parameters(scf_json):
        """Adds the area to the scf_json"""
        for scf_object in scf_json:
            if not "area" in scf_object:
                add_area(scf_object)

    @staticmethod
    def _remove_id(scf_json):
        """Remove id from the scf_object so scf_json can be compared"""
        new_scf_json = []
        for scf_object in scf_json:
            new_scf_json.append(
                {k: v for k, v in scf_object.items() if k not in ["id"]}
            )
        return new_scf_json
