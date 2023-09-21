# Tomni

[![Build Status](https://cytosmart.visualstudio.com/CytoSmartImageAnalysis/_apis/build/status/cytosmart-bv.tomni?branchName=main)](https://cytosmart.visualstudio.com/CytoSmartImageAnalysis/_build/latest?definitionId=384&branchName=main)
[![Downloads](https://pepy.tech/badge/tomni)](https://pepy.tech/project/tomni)

Tomni is a python package that contains a collection of helper functions based on OpenCV and NumPy. It can be used for any python based computer vision or image analysis problem. The package simplifies the code and takes care of edge cages, everything from simplifying code like img_dim to compute optimization like labels2contours or illumination correction image processing. Tomni uses the image coordinates (same as OpenCV).

Tomni is created by [CytoSMART](https://cytosmart.com).

The package was developed in-house to centralize the helper function for computer vision problems. In 2021, CytoSMART engineers turned it to open source, enabling researchers and educators to use it for free.

## Getting Tomni

```cmd
pip install tomni
```

## License

Tomni is free for academic and educational use.

For commercial use please contact [CytoSMART](https://cytosmart.com/contact).

## The name

The name Tomni is a combination of creator (Tom) and other CytoSMART product he was working on, [the Omni](https://cytosmart.com/products/omni). Tomni name was proposed by Denissa Daroţi, a former CytoSMART intern, who won a bet with her mentor by getting a (well deserved) 9/10 for her internship.

## Features

- Bounding box fitting (bbox fitting)
  - Center bounding box fit
  - Custom location box fit
- Image helpers
  - Get image dimensions
  - Convert color of an image
- Illumination correction
  - Brightfield
  - Fluorescence
- Contour operations
  - Get center
  - Approximate circle by area
  - Get roundness
  - Get circularity
- CytoSMART data format
  - Tba
- Json operation
  - Add circularity property
  - Scale object
  - Translate object
- Make a mask
  - Ellipse
  - Polygon
- Polygon downsampling
  - iterative downsampling
- Shape fitting
  - Rect around ellipse
- Transformers of data format
  - Contours to json
  - Ellipse to json
  - Json 2 contours
  - Json 2 label
  - Json 2 bbox
  - Labels 2 contours
  - Labels 2 lists of points
  - Binary 2 contours


## Examples

### Diameter vs radius
Most geometric operation use functions from OpenCV

Some of these function return diameter and some radius of the circle. This is not consistent.

For example, the function `cv2.minEnclosingCircle` returns the center and radius of the circle. The function `cv2.fitEllipse` returns the center and the major and minor axes of the ellipse.

#### Min enclosing circle example
```python
import cv2
import math
import numpy as np

points = np.array([[0, 0], [100, 0], [100, 100], [0, 100], [0, 0]], dtype=np.float32)

center, radius = cv2.minEnclosingCircle(points)
diameter = math.sqrt(50**2 + 50**2) 

print("Center:", center)
print("Major and Minor Axes:", radius)
print("Diameter calculated with Pythagoras formula", diameter)

```

this results in the following output:
```cmd
Center: (50.0, 50.0)
Major and Minor Axes: 70.71077728271484
Diameter calculated with Pythagoras formula 70.71067811865476
```
#### Fit ellipse example
```python
import cv2
import math
import numpy as np

# Generate some example points
points = np.array([[0, 0], [100, 0], [100, 100], [0, 100], [0, 0]], dtype=np.float32)

# Fit an ellipse to the points
ellipse = cv2.fitEllipse(points)

# Extract ellipse parameters
center, axes, angle = ellipse

diameter = math.sqrt(50**2 + 50**2) * 2

print("Center:", center)
print("Major and Minor Axes:", axes)
print("Diameter calculated with Pythagoras formula", diameter)
```

this results in the following output:

```cmd
Center: (50.0, 49.95212173461914)
Major and Minor Axes: (141.43260192871094, 141.5462188720703)
Diameter: 141.4213562373095
```
Example is related to the following functions in the package


## Credits

Sorted alphabetically

- Bram van der Velden
- Coenraad Stijne
- Denisa Daroţi
- Hristo Atanasov
- Jan-Niklas Schneider
- Jelle van Kerkvoorde
- Kirsten Koopman
- Lisa Koolen
- Manon van Erp
- Marina Tzenkova
- Tom de Vries
- Tom Nijhof
