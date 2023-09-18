labels2listsOfPoints
=========================
.. automodule:: tomni
   :members: labels2listsOfPoints
   :show-inheritance:

This function takes an array of labels where each pixel is labeled to indicate which object it belongs to, and transforms it into an array of lists of points. Each list contains the (x, y) coordinates of pixels that belong to the same label.

Example Usage::

   import numpy as np

   # Create an array of labels
   labels = np.array([[0, 0, 1], [1, 1, 1], [0, 0, 0]], dtype=np.uint8)

   # Get lists of points for each label
   lists_of_points = labels2listsOfPoints(labels)

   # Process the lists of points as needed

.. note::
   - The function uses `numpy_indexed` for efficient grouping and splitting of the labels into lists of points.
   - The input labels should be a 2D numpy array where each pixel is labeled with an object ID.

You can save this documentation in a `.rst` file, such as `labels2listsOfPoints.rst`, and use Sphinx to generate documentation from it. Make sure to replace the function usage example with your specific information and documentation needs.
