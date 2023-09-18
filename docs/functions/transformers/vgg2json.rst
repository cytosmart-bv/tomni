vgg2json
=========================
.. automodule:: tomni
   :members: vgg2json
   :show-inheritance:
   
This function takes a dictionary `vgg_data`, which should contain annotations for multiple images, and transforms these annotations into a list of JSON objects. Each JSON object represents an annotation for a given image.

For each annotation in the `vgg_data`, the function checks the type of shape (polygon, circle, or ellipse) and converts it into the appropriate JSON format. The resulting JSON objects are collected in a list.

Example Usage::

   import json
   vgg_annotations = {
       'image1.jpg': {
           'regions': [
               {
                   'shape_attributes': {
                       'name': 'polygon',
                       'all_points_x': [x1, x2, x3],
                       'all_points_y': [y1, y2, y3],
                   }
               },
               {
                   'shape_attributes': {
                       'name': 'circle',
                       'cx': cx,
                       'cy': cy,
                       'r': r,
                   }
               }
           ]
       },
       'image2.jpg': {
           'regions': [
               {
                   'shape_attributes': {
                       'name': 'ellipse',
                       'cx': cx,
                       'cy': cy,
                       'rx': rx,
                       'ry': ry,
                       'theta': alpha,
                   }
               }
           ]
       }
   }

   json_annotations = vgg2json(vgg_annotations)

   # Process the JSON annotations as needed

.. note::
   - This function is designed to work with annotations created using the 'VGG Image Annotator'.
   - It converts different shape types (polygon, circle, ellipse) into JSON representations.
