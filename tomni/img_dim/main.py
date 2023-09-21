import numpy as np


def img_dim(arr, showChannels=False):
    """
    Get the dimensions and optionally the number of color channels of a numpy array representing an image.

    Args:
        arr (numpy.ndarray): The image represented as a numpy array.
        showChannels (bool, optional): Whether to include the number of color channels in the output.
                                        True to show channels, False to hide them. Defaults to False.

    Returns:
        tuple: A tuple containing the dimensions of the image (width, height) or (width, height, channels)
                depending on the value of showChannels.

    Example::

        import numpy as np
        image = np.zeros((100, 200, 3), dtype=np.uint8)
        dimensions = img_dim(image)
        print(dimensions)  # Output: (200, 100)

        dimensions_with_channels = img_dim(image, showChannels=True)
        print(dimensions_with_channels)  # Output: (200, 100, 3)
    """
    s = np.shape(arr)

    if showChannels:
        if len(s) > 2:
            return s[1], s[0], s[2]
        else:
            return s[1], s[0], 1
    else:
        return s[1], s[0]
