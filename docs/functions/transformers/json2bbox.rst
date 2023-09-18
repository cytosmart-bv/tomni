json2bbox
=========================
.. automodule:: tomni
   :members: json2bbox
   :show-inheritance:

This function takes a dictionary representing a single standard CytoSMART format annotation and converts it into bounding box coordinates. The supported annotation types are 'polygon', 'ellipse', or 'circle'. Depending on the type, the function calculates the bounding box coordinates accordingly.

Example Usage::

   # Define a JSON object representing an ellipse
   scf_object = {
       'type': 'ellipse',
       'center': {'x': 20, 'y': 30},
       'radiusX': 15,
       'radiusY': 10,
       'angleOfRotation': 45
   }

   # Convert the JSON object to bounding box coordinates
   bbox = json2bbox(scf_object)  # (10, 20, 30, 40)

   # Process the bounding box coordinates as needed

.. note::
   - The function supports three types of annotations: 'polygon', 'ellipse', and 'circle'.
   - The bounding box coordinates are calculated based on the provided annotation type and parameters.
   - All bounding box values are rounded using Python's internal 'round' function (Banker's Rounding).

You can save this documentation in a `.rst` file, such as `json2bbox.rst`, and use Sphinx to generate documentation from it. Make sure to replace the function usage example with your specific information and documentation needs.
