fit_rect_around_ellipse
============================

.. function:: fit_rect_around_ellipse(x, y, r1, r2, alpha)

   This function calculates the bounding box around an ellipse.

   :param int x: x-coordinate of the center of the ellipse.
   :param int y: y-coordinate of the center of the ellipse.
   :param float r1: Longest radius of the ellipse.
   :param float r2: Shortest radius of the ellipse.
   :param float alpha: Angle in degrees between the longest radius and the x-axis.

   :return: A tuple containing the coordinates (x1, y1, x2, y2) of the bounding box.
   :rtype: tuple
