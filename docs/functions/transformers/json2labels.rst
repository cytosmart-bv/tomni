json2labels
=========================
.. automodule:: tomni
   :members: json2labels
   :show-inheritance:

This function takes a list of JSON objects representing objects and converts them into a segmentation map. Each object in the JSON list is assigned a unique number in the output segmentation map.

Example Usage::

   import numpy as np

   # Define the output image dimensions
   output_dim = (100, 100)

   # Create a list of JSON objects representing objects
   json_objects = [
       {
           'type': 'ellipse',
           'center': {'x': 30, 'y': 30},
           'radiusX': 20,
           'radiusY': 10,
           'angleOfRotation': 45,
       },
       {
           'type': 'polygon',
           'points': [{'x': 60, 'y': 40}, {'x': 80, 'y': 60}, {'x': 70, 'y': 80}],
       }
   ]

   # Generate a segmentation map from the objects
   segmentation_map = json2labels(json_objects, output_dim)

   # Process the generated segmentation map as needed

.. note::
   - The function processes JSON objects representing ellipses and polygons, converting them into a segmentation map.
   - Each object in the segmentation map is assigned a unique number corresponding to its index in the JSON list.

You can save this documentation in a `.rst` file, such as `json2labels.rst`, and use Sphinx to generate documentation from it. Make sure to replace the function usage example with your specific information and documentation needs.
