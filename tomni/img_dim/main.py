import numpy as np

def img_dim(arr, showChannels=False):
    '''
    This function gives the image dimensions and optional channel of a numpy array.
    arr: (numpy.ndarray) the image represented as numpy array
    showChannels: (boolean) if you want to output the number of color channels e.q. 1 for greyscale, 3 for BGR, 4 for BGRA
    '''
    s = np.shape(arr)

    if showChannels:
        if len(s) > 2:
            return s[1], s[0], s[2]
        else:
            return s[1], s[0], 1
    else:
        return s[1], s[0]