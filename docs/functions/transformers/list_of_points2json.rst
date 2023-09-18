list_of_points2json
=========================
.. automodule:: tomni
   :members: list_of_points2json 
   :show-inheritance:

This function takes a list or NumPy array of points that describe a polygon and converts it into a JSON object.

Example Usage::

   import numpy as np

   # Create a list of points
   points = [[0, 0], [1, 0], [1, 1], [0, 1]]

   # Get the JSON representation of the polygon
   polygon_json = list_of_points2json(points)

   # Process the JSON representation as needed

.. note::
   - The function reshapes the input into a format suitable for `contours2json` function, which is expected to receive contours in the format required for OpenCV.
   - This function assumes that the input points represent a closed polygon.

You can save this documentation in a `.rst` file, such as `list_of_points2json.rst`, and use Sphinx to generate documentation from it. Make sure to replace the function usage example with your specific information and documentation needs.
