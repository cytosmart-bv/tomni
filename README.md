Tomni
=====

Tomni is created by CytoSMART.
The package was developed in house to centralize helper function for computer vision problems.
But in 2021 we went open source with it, so that researchers and educators can use it for free.

Tomni contains a collection of helpers functions based on openCV and numpy.
It used the image coordinates (same as openCV).

The function range from simplifying code like img_dim, to compute optimization like labels2contours, to processing of image like illumination correction.

## The name

Tomni is named by Denissa Daroţi after she won a bet with her mentor, by getting a (well deserved) 9/10 for her internship.

She choice to name as a combination of creator (Tom) and the main product of CytoSMART he was working on, [the Omni](https://cytosmart.com/products/omni).

## License

Tomni is free for academic and education use.
For commercial use please contact [CytoSMART](https://cytosmart.com/contact).

## Features

* Bounding box fitting (bbox fitting)
  * Center bounding box fit
  * Custom location box fit
* Illumination correction 
  * Brightfield
  * Fluorescence
* Json operation
  * Add circularity property
  * Scale object
  * Translate object
* Make a mask
  * Ellipse
  * Polygon
* Shape fitting
  * Rect around ellipse
* Transformers of data format
  * Contours to json
  * Ellipse to json
  * Json 2 contours
  * Json 2 label
  * Labels 2 contours
  * Labels 2 lists of points

## Credits
Sorted alphabetically

- Coenraad Stijne
- Denisa Daroţi
- Hristo Atanasov
- Jelle van Kerkvoorde
- Kirsten Koopman
- Manon van Erp
- Marina Tzenkova
- Tom de Vries
- Tom Nijhof