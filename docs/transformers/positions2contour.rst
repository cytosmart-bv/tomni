positions2contour
=========================
.. py:function:: positions2contour(positions: numpy.ndarray, simplify_error: float = 0, return_inner_contours: bool = False) -> numpy.ndarray

   Transform a list of positions into an OpenCV contour.

   :param numpy.ndarray positions: A 2-dimensional array with shape [N, 2], where N represents the number of points. Each row contains (x, y) positions.
   :param float simplify_error: Deprecated. Simplification is no longer supported (default is 0).
   :param bool return_inner_contours: A boolean indicating whether to return internal contours (default is False). Internal contours are contours around holes within the main contour.
   :return: An OpenCV contour representing the shape defined by the input positions.
   :rtype: numpy.ndarray

This function takes a 2-dimensional NumPy array `positions` containing (x, y) positions of points and transforms it into an OpenCV contour.

If `return_inner_contours` is set to True, the function will return both the external contour and internal contours (if present). The external contour represents the outer shape, and internal contours represent holes within the main contour.

.. warning::
   - The `simplify_error` parameter is deprecated and no longer supported. Setting it to a non-zero value will raise a DeprecationWarning.

Example Usage::

   import numpy as np

   # Create a list of (x, y) positions
   positions = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])

   # Get the external contour
   contour = positions2contour(positions)

   # Get the external and internal contours
   external_contour, internal_contours = positions2contour(positions, return_inner_contours=True)

   # Process the contours as needed

.. note::
   - The function uses OpenCV's `cv2.findContours` to extract contours from the input positions.
