import numpy as np
from scipy.sparse import csr_matrix, find
import numpy_indexed as npi


def labels2listsOfPoints(labels: np.ndarray) -> np.ndarray:
    """
    Convert labeled regions into lists of points.

    Args:
        labels (np.ndarray): An array where every pixel is labeled to indicate which object it belongs to.
            The labels should be non-negative integers.

    Returns:
        List[List[Tuple[int, int]]]: A list of lists, where each inner list contains the (x, y) coordinates
            of points belonging to the corresponding label. The list is organized such that
            `output[label]` contains the points for the label with value `label`. The label values must start
            from 0 and be contiguous integers.

    Raises:
        ValueError: If the number of labels exceeds the supported limit.

    Note:
        - The function automatically determines the appropriate data type for labels based on their maximum value.
        - It uses sparse matrix operations to efficiently extract points for each label.
    """

    if np.max(labels) < 256:
        dataType = np.uint8
    elif np.max(labels) < 65536:
        dataType = np.uint16
    elif np.max(labels) < 4294967296:
        dataType = np.uint32
    else:
        raise ValueError("There are to many labels")

    # Memory check number of labels
    c = csr_matrix(labels, dtype=dataType)
    x, y, v = find(c)
    g = npi.group_by(v)
    output = g.split_array_as_list(np.array([y, x]).transpose())
    return output
