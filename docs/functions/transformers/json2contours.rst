json2contours
=========================
.. automodule:: tomni
   :members: json2contours
   :show-inheritance:


This function takes a JSON object as input and converts it into a contour represented as a numpy array. The JSON object should have the following format:

Example Usage::

   import numpy as np

   # Define a JSON object representing a polygon
   json_object = {
       'type': 'polygon',
       'points': [{'x': 2, 'y': 2}, {'x': 3, 'y': 4}, {'x': 4, 'y': 2}],
   }

   # Convert the JSON object to a contour
   contour = json2contours(json_object)

   # Process the contour as needed

.. note::
   - The function requires the JSON object to have the `'type'` set to `'polygon'`.
   - The `'points'` field should contain a list of dictionaries representing the coordinates of the polygon's points.

You can save this documentation in a `.rst` file, such as `json2contours.rst`, and use Sphinx to generate documentation from it. Make sure to replace the function usage example with your specific information and documentation needs.
