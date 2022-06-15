from __future__ import annotations

from ..json_operations import add_area

class SCFJson:
    def __init__(self, scf_json : list) -> None:
        #TODO validate if correct format
        scf_json = self._remove_id(scf_json)
        self._add_morphology_parameters(scf_json)
        self.scf_json = sorted(scf_json, key=lambda scf_object: scf_object['area']) 

    def __len__(self) -> int:
        return len(self.scf_json)

    def __add__(self, other : SCFJson) -> SCFJson:
        return SCFJson(self.scf_json, other.scf_json)
    
    def __eq__(self, other : SCFJson) -> bool:
        return self.scf_json == other.scf_json
    
    @staticmethod
    def _add_morphology_parameters(scf_json):
        for scf_object in scf_json:
            if not 'area' in scf_object:
                add_area(scf_object)

    @staticmethod
    def _remove_id(scf_json):
        new_scf_json = []
        for scf_object in scf_json:
            new_scf_json.append({k:v for k,v in scf_object.items() if k not in ['id']})
        return new_scf_json