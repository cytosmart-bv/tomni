from re import S
from typing import Tuple, Union

import numpy as np

from tomni.annotation_manager.annotations.point import Point
from tomni.annotation_manager.annotations.annotation import Annotation


class BinaryMask(Annotation):
    def __init__(self, binary_mask: np.ndarray):
        # always on [0,1]? if not parse. or allow multiple annotations in mask?
        self._binary_mask = binary_mask
        pass

    @property
    def get_mask(self) -> np.ndarray:
        return self._binary_mask

    def get_shape(self) -> Union[Tuple[int, int], Tuple[int, int, int]]:
        """_summary_

        Returns:
            Tuple[int, int]: _description_
        """
        pass

    def get_feature_x(self) -> None:
        """
        not sure what mask features we commonly use but they could be here.
        """
        pass
