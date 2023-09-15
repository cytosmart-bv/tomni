.. py:function:: json2vgg(json_list: List[dict], image_name: str, extension: str = ".jpg", add_accuracy: bool = True) -> dict

   Transform a list of JSON objects into a JSON format suitable for 'VGG Image Annotator'.

   :param List[dict] json_list: A list of JSON objects in the standard CytoSMART format.
   :param str image_name: The name of the image where the annotations will be overlaid within 'VGG Image Annotator'.
   :param str extension: The file extension of the image (default is ".jpg").
   :param bool add_accuracy: Whether to add accuracy information to the generated JSON (default is True).
   :return: A JSON object formatted for 'VGG Image Annotator'.
   :rtype: dict

This function takes a list of JSON objects in the standard CytoSMART format and transforms them into a JSON format suitable for use in 'VGG Image Annotator'. It includes information about the image filename, regions (annotations), and optional accuracy attributes.

Example Usage::

   json_objects = [
       {
           'type': 'ellipse',
           'center': {'x': 100, 'y': 100},
           'radiusX': 50,
           'radiusY': 30,
           'angleOfRotation': 45,
           'accuracy': 0.95
       },
       {
           'type': 'polygon',
           'points': [{'x': 200, 'y': 200}, {'x': 250, 'y': 250}, {'x': 300, 'y': 200}],
           'accuracy': 0.90
       }
   ]

   vgg_annotation = json2vgg(json_objects, "image1")

   # Process the generated VGG annotation as needed

.. note::
   - The function transforms JSON objects representing ellipses and polygons into the format expected by 'VGG Image Annotator'.
   - You can customize the `add_accuracy` parameter to include or exclude accuracy information in the generated JSON.
   - The generated JSON is structured for use with the 'VGG Image Annotator'.

You can save this documentation in a `.rst` file, such as `json2vgg.rst`, and use Sphinx to generate documentation from it. Make sure to replace the function usage example with your specific information and documentation needs.
