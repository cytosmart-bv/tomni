mask2json
=========================
.. py:function:: get_edges(mask: numpy.ndarray) -> numpy.ndarray

   Get the edges of a binary mask.

   :param numpy.ndarray mask: Binary mask representing an object.
   :return: Edges of the mask.
   :rtype: numpy.ndarray

This function takes a binary mask as input and returns the edges of the mask using the Canny edge detection algorithm.

.. seealso::
   - OpenCV documentation for `cv2.Canny`: https://docs.opencv.org/4.x/opencv2/opencv-python-tutorials.html#opencv-python-tutorials-content

.. py:function:: mask2json(mask: numpy.ndarray, minimum_size_contours: int = 3, is_diagonal_connected: bool = True, return_inner_contours: bool = False) -> list

   Converts a binary mask into standard cytosmart format.

   :param numpy.ndarray mask: Binary mask.
   :param int minimum_size_contours: Minimum number of points a contour should have to be included (default is 3).
   :param bool is_diagonal_connected: If True, diagonal pixels are considered connected (default is True).
   :param bool return_inner_contours: Return internal contours (default is False). These are contours around holes within the main contour.
   :return: List of JSON objects representing the mask.
   :rtype: list

This function converts a binary mask into the standard cytosmart format, which includes polygons and their inner objects. It performs the following steps:

1. Detects edges using the Canny edge detection algorithm.
2. Labels connected components in the edges.
3. Converts the labeled edges into contours.
4. Optionally, includes inner contours if `return_inner_contours` is True.
5. Filters out contours with fewer points than `minimum_size_contours`.

The resulting JSON objects represent the contours and their inner objects in the mask.

Example Usage::

   import numpy as np

   # Create a binary mask
   mask = np.array([[0, 0, 1], [1, 1, 1], [0, 0, 0]], dtype=np.uint8)

   # Get JSON representation of the mask
   mask_json = mask2json(mask)

   # Process the JSON representation as needed

.. note::
   - This function uses OpenCV for edge detection and contour extraction.
