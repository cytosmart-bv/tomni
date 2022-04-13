API Documentation
=================

Within the tomni there are helpers for different use cases.

Bounding boxes
----------------

A bounding box is an rectangle defined by 4 number.
:x1: lowest x value
:x2: highest x value
:y1: lowest y value
:y2: highest y value

An bounding box is never rotated.
The bounding box can be outside the image or even bigger as the image.

.. automodule:: tomni
   :members: bbox_fitting, bbox_fitting_center, bbox_operations
   :show-inheritance:

.. automodule:: tomni.bbox_operations
   :members: check_overlap_bbox
   :show-inheritance:
