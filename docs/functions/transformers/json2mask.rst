json2mask
=========================
.. py:function:: json2mask(json_objects: list, img_shape: tuple, minimum_size_contours: int = 3) -> numpy.ndarray

   Convert annotations in standard CytoSMART format to a binary mask.

   :param list json_objects: A list of JSON objects representing annotations in standard CytoSMART format.
   :param tuple img_shape: The dimensions of the mask (height, width).
   :param int minimum_size_contours: The minimum number of points a contour should have to be included (default is 3).
   :return: A binary mask representing the annotations in the image.
   :rtype: numpy.ndarray

This function takes a list of JSON objects in standard CytoSMART format, representing annotations, and converts them into a binary mask. The binary mask has the same dimensions as the specified image shape and contains the annotated regions.

Example Usage::

   import numpy as np

   # Define the image shape
   img_shape = (10, 10)

   # Create a list of JSON objects representing annotations
   json_objects = [
       {
           'type': 'polygon',
           'points': [{'x': 2, 'y': 2}, {'x': 3, 'y': 4}, {'x': 4, 'y': 2}],
       },
       {
           'type': 'ellipse',
           'center': {'x': 6, 'y': 6},
           'radiusX': 3,
           'radiusY': 2,
       }
   ]

   # Generate a binary mask from the annotations
   mask = json2mask(json_objects, img_shape)

   # Process the generated binary mask as needed

.. note::
   - The function processes JSON objects representing polygons and ellipses, converting them into a binary mask.
   - The `minimum_size_contours` parameter allows you to filter out small contours from the mask.
   - The resulting binary mask has the same dimensions as the specified `img_shape`.

You can save this documentation in a `.rst` file, such as `json2mask.rst`, and use Sphinx to generate documentation from it. Make sure to replace the function usage example with your specific information and documentation needs.
