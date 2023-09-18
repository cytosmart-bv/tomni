binary2contours
=========================

.. automodule:: tomni
   :members: binary2contours
   :show-inheritance:


This function transforms a binary image into a list of contours, where each contour represents an object in the image. It can also optionally return inner contours (contours within other contours) if specified.

The `binary_img` parameter should be a NumPy array representing a binary image, where objects of interest are typically in white (255) and the background is in black (0).

If `return_inner_contours` is set to True (default), the function will return both outer and inner contours. Outer contours are the top-level contours, while inner contours are nested within outer contours. When `return_inner_contours` is False, only outer contours are returned.

This function uses OpenCV's `cv2.findContours` method internally to extract contours from the binary image.

Example Usage::

   import cv2
   import numpy as np
   from typing import List

   # Load a binary image
   binary_image = cv2.imread('binary_image.png', cv2.IMREAD_GRAYSCALE)

   # Get both outer and inner contours
   contours = binary2contours(binary_image)

   # Get only outer contours
   outer_contours = binary2contours(binary_image, return_inner_contours=False)

   # Process the contours as needed

.. note::
   - This function is designed for binary images where objects of interest are white, and the background is black.
   - Inner contours are provided in the same list as their corresponding outer contours when `return_inner_contours` is True.

.. seealso::
   - OpenCV documentation for `cv2.findContours`: https://docs.opencv.org/4.x/opencv2/opencv-python-tutorials.html#opencv-python-tutorials-content
