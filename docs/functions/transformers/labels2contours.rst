labels2contours
=========================
.. automodule:: tomni
   :members: labels2contours
   :show-inheritance:

This function takes an array of labels where each pixel indicates which object it belongs to and transforms it into a list of OpenCV contours. Each contour represents an object in the labeled image.

Example Usage::

   import numpy as np

   # Create an array of labels
   labels = np.array([[0, 0, 1], [1, 1, 1], [0, 0, 0]], dtype=np.uint8)

   # Get OpenCV contours from the labeled image
   contours = labels2contours(labels)

   # Process the contours as needed

.. warning::
   - The `simplify_error` parameter is deprecated and no longer supported. Setting it to a non-zero value will have no effect.
   - This function relies on `labels2listsOfPoints` and `positions2contour` functions to convert labels to contours.
   - The input labels should be a 2D numpy array where each pixel is labeled with an object ID.

You can save this documentation in a `.rst` file, such as `labels2contours.rst`, and use Sphinx to generate documentation from it. Make sure to replace the function usage example with your specific information and documentation needs.
