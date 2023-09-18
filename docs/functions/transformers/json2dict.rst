json2dict
=========================
.. automodule:: tomni
   :members: json2dict
   :show-inheritance:

This function takes a list of JSON objects in standard CytoSMART format and extracts specific keywords from those objects, creating a dictionary with lists of extracted values. You can specify which keywords you want to extract by providing a list of keywords as an argument.

Example Usage::

   # Create a list of JSON objects representing annotations
   json_objects = [
       {
           'type': 'ellipse',
           'area': 100,
           'center': {'x': 30, 'y': 30},
           'id': 1
       },
       {
           'type': 'polygon',
           'area': 50,
           'center': {'x': 60, 'y': 60},
           'id': 2
       }
   ]

   # Extract specified keywords into a dictionary
   extracted_data = json2dict(json_objects, keywords=["type", "area", "center"])

   # Process the extracted data dictionary as needed

.. note::
   - The function allows you to specify which keywords to extract from the JSON objects.
   - The resulting dictionary contains lists of values for each specified keyword.
   - If a keyword is not found in a JSON object, `None` is added to the corresponding list.

You can save this documentation in a `.rst` file, such as `json2dict.rst`, and use Sphinx to generate documentation from it. Make sure to replace the function usage example with your specific information and documentation needs.
