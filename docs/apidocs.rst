API Documentation
=================

Within the tomni there are helpers for different use cases.

Bounding boxes
----------------

A bounding box is an rectangle defined by 4 number.

x1: lowest x value

x2: highest x value

y1: lowest y value

y2: highest y value

An bounding box is never rotated.
The bounding box can be outside the image or even bigger than the image.

.. automodule:: tomni
   :members: bbox_fitting, bbox_fitting_center
   :show-inheritance:

.. automodule:: tomni.bbox_operations
   :members: check_overlap_bbox
   :show-inheritance:

Contour operations
-------------------------------------

OpenCV has already nice `operations <https://docs.opencv.org/4.5.5/dd/d49/tutorial_py_contour_features.html>`_ to apply to your contours.
We have some additional ones

.. automodule:: tomni.contour_operations
   :members: approximate_circle_by_area, get_center, roundness, circularity
   :show-inheritance:
