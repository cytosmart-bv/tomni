import numpy as np
from scipy.sparse import csr_matrix, find
import numpy_indexed as npi

def labels2listsOfPoints(labels: np.ndarray) -> np.ndarray:
    '''
    Transforms each label into a list of points.
    These points are for every point in the label.

    labels: (numpy.array) An array where every pixel is labeled to which object it belongs
    '''
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
