.. py:function:: contour2bbox(contour: np.ndarray) -> tuple

   Convert OpenCV contours into a bounding box in the format (xmin, ymin, xmax, ymax).

   :param contour: An array with coordinates defining the contour of an object.
   :type contour: np.ndarray
   :return: A tuple containing the bounding box coordinates (xmin, ymin, xmax, ymax).
   :rtype: tuple

This function takes an OpenCV contour as input, which is an array of coordinates defining the contour of an object. It then computes the bounding box around this contour and returns the bounding box coordinates as a tuple in the format (xmin, ymin, xmax, ymax).

Example Usage::

   import cv2
   import numpy as np
   from contour2bbox import contour2bbox

   # Create an example contour
   contour = np.array([[[3, 3]], [[3, 5]], [[5, 5]], [[5, 3]]], dtype=np.int32)

   # Compute the bounding box
   bbox = contour2bbox(contour)

   # bbox will contain the coordinates (xmin, ymin, xmax, ymax) of the bounding box

.. note::
   - The function uses the `cv2.boundingRect` function from OpenCV to compute the bounding box.
   - The input `contour` should be a NumPy array with shape `[N, 1, 2]`, where `N` is the number of points in the contour.
   - The function returns a tuple with four integer values representing the bounding box coordinates.

You can save this documentation in a `.rst` file, such as `contour2bbox.rst`, and use Sphinx to generate documentation from it. Make sure to replace the function usage example with your specific information and documentation needs.
