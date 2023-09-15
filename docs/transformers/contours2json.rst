.. py:function:: ellipse2json(x: int, y: int, radius: int, secondRadius: Union[None, int] = None, alpha: float = 0) -> dict

   Create a JSON representation of an ellipse or circle.

   :param int x: Center x position.
   :param int y: Center y position.
   :param int radius: Radius of the ellipse or circle.
   :param int|None secondRadius: (Optional) Smallest radius for an ellipse. Defaults to `None`, indicating a circle.
   :param float alpha: (Optional) Angle of rotation for an ellipse. Defaults to 0.
   :return: A dictionary representing the ellipse or circle in a JSON-like format.
   :rtype: dict

This function creates a JSON-like representation of an ellipse or circle based on the provided parameters. You can specify the center position (`x` and `y`), the primary radius (`radius`), and optionally, the secondary radius (`secondRadius`) and the angle of rotation (`alpha`) for an ellipse.

Example Usage::

   # Create a JSON representation of a circle
   circle_json = ellipse2json(50, 50, 30)

   # Create a JSON representation of an ellipse
   ellipse_json = ellipse2json(70, 60, 40, 20, 45)

   # Use the resulting JSON representations as needed

.. note::
   - The function supports both circles and ellipses.
   - If `secondRadius` is not provided, it defaults to `radius`, creating a circle.
   - The `alpha` parameter is used to specify the angle of rotation for ellipses. It defaults to 0 for circles.
   - The function generates a unique identifier (`id`) for each ellipse or circle using the `uuid` module.

You can save this documentation in a `.rst` file, such as `ellipse2json.rst`, and use Sphinx to generate documentation from it. Make sure to replace the function usage example with your specific information and documentation needs.
