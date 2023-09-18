ellipse_mask
=================
.. function:: make_mask_ellipse(image_size, x1, y1, rx, ry)

   Generates a boolean image with an ellipse of True surrounded by False.

   :param image_size: The size of the image in the format (width, height).
   :type image_size: tuple
   :param int x1: The x-coordinate of the center of the ellipse.
   :param int y1: The y-coordinate of the center of the ellipse.
   :param int rx: The length of the radius on the x-axis of the ellipse.
   :param int ry: The length of the radius on the y-axis of the ellipse.

   :return: A numpy array with a boolean data type, where True represents the region enclosed by the ellipse, and False represents the background.
   :rtype: numpy.ndarray

   The function provides two implementations for generating the ellipse mask: a small ellipse function for more precision and a big ellipse function for better memory management.

   If the provided radii (rx and ry) are both less than 100, the small ellipse function is used, which is more precise.

   If either of the radii (rx or ry) is greater than or equal to 100, the big ellipse function is used, which is less precise but more memory-efficient.

   The small ellipse function calculates the ellipse mask using the equation of an ellipse. The points within the ellipse are set to True.

   The big ellipse function generates the mask using OpenCV's `cv2.getStructuringElement` function and then fits it within the specified image size using a bounding box.
