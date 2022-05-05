Roundness VS Circularity
=========================

Roundness and circularity both give a number between 0 and 1.
Both are only 1 for a perfect circle.
And both go to zero when you give it an infinitely long line.

Circularity
-----------

Circularity is the difference between area and perimeter.
If the object is a circle the area to perimeter is maximum (1)

This is done using both the Area and Perimeter to calculate the squared radius.
Then dividing the 2 be each other.

Via Area

.. math::

   r_a^2 = \frac{ A  }{\pi}

Via Perimeter

.. math::

   r_p^2 = (\frac{ P  }{2*\pi})^2

Resulting in

.. math::

 circularity = \frac{r_a^2}{r_p^2} = \frac{ \frac{ A  }{\pi}  }{(\frac{ P  }{2*\pi})^2} = \frac{ 4 \pi A  }{P^2}

Roundness
-----------

Roundness is based on the relation between the enclosing circle and the object.
It calculates the area of both and divided them.

This means roundness is more focused if the contours covers a perfect area and less if the perimeter is bumpy or not.

Difference with an Oval
------------------------

Lets take an oval with one radius twice the lenght of the other.
So :math:`r_1 = 2 r_2`

**Roundness**
Enclosing circle has radius of the biggest radius :math:`2 r_2`.
Meaning the area would be :math:`(2 r_2)^2 \pi`.
The area of the oval would be :math:`r_1 r_2 \pi = (2 r_2) r_2 \pi`

The roundness would be

.. math::

   \frac{ (2 r_2) r_2 \pi }{(2 r_2)^2 \pi} = \frac{ 1 }{2}

**Circularity**
The area stays the same.
The perimeter

.. math::

   P = 2 \pi \sqrt{\frac{r_1^2 + r_2^2}{2}} = 2 \pi \sqrt{\frac{5}{2}} r_2

Make circularity

.. math::

   circularity = \frac{ 4 \pi (2 r_2) r_2 \pi  }{(2 \pi \sqrt{\frac{5}{2}} r_2)^2} = \frac{ 8 \pi^2 r_2^2  }{4 \pi^2 \frac{5}{2} r_2^2} =  \frac{4}{5}

Difference with an dented circle
--------------------------------

Lets take a perfect circle and remove a pizza slice of 1 degree (you know what you do at fun math parties).

The area will be :math:`\frac{359}{360} r^2 \pi`

The enclosing circle will be :math:`r^2 \pi`

The roundness would now be :math:`\frac{359}{360}`

The perimeter will now be :math:`\frac{359}{360} 2 r \pi + 2 r`

So the circularity will be

.. math::

   \frac{ 4 \pi A  }{P^2} = \frac{ 4 \pi \frac{359}{360} r^2 \pi }{(\frac{359}{360} 2 r \pi + 2 r)^2} = \frac{ 4 \pi^2 \frac{359}{360} r^2 }{r^2 (\frac{359}{360}^2 4 \pi^2 + 8 \pi \frac{359}{360} + 4)} = 0.5762209483925725

Conclusion
------------

Circularity is great for quantifying how smooth a surface is.
Where roundness is great for quantifying how much it overlaps with a circle

Sources
--------

- `Engineering the geometrical shape of mesenchymal stromal cells through defined cyclic stretch regimens <https://rdcu.be/cLN85>`_
- `Microenvironment complexity and matrix stiffness regulate breast cancer cell activity in a 3D in vitro model <https://rdcu.be/cLN9S>`_
