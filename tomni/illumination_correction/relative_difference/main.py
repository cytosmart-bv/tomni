
import numpy as np
import cv2

def relative_difference(img: np.array, gauss_size: int = 301, smooth_size=None, do_normalize: bool= False, resize_ratio= None) -> np.array:
    """
    Remove big blurry artifact from the image.
    It will do this by taking the ratio difference between the blurred and raw image.
    
    # Usage
    This can be used for human vision.
    This is good as algorithm input for algorithm that rely on relative pixel difference.

    # NOT fractal
    This algorithm is NOT fractal. 
    Meaning the illumination correction followed by cropping will given a different result than first cropping.

    img (np.array): input image
    gauss_size (int): needs to be an odd number. 
        This is corralated to the size of the big artifact to remove.
    smooth_size (int): need to be an odd number.
        Is the size of the kernal of the gaussian filter that is used on the image before division.
    resize_ratio (float): the img is resized according to this ration before using a GaussianBlur.
        This is done to increase the speed of the function.
    do_normalize (bool): if true, the output img is normalized between the minimum and maximum
        value of the smoothed img. 
    """
    img = np.float32(img)
    
    if gauss_size % 2 == 0:
        gauss_size += 1

    if smooth_size:
        img = cv2.GaussianBlur(img, (smooth_size,smooth_size), 0)
    
    max_img = np.max(img)
    min_img = np.min(img)

    if resize_ratio:
        gb = cv2.resize(img, (0, 0), fx=resize_ratio, fy=resize_ratio, interpolation=cv2.INTER_LINEAR)
        gb = cv2.GaussianBlur(gb, (gauss_size, gauss_size), 0, borderType=cv2.BORDER_REPLICATE)
        gb = cv2.resize(gb, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_LINEAR)
    else:
        gb = cv2.GaussianBlur(img, (gauss_size, gauss_size), 0)
        gb = np.float32(gb)

    img = np.divide(img, gb + 1e-15, dtype=np.float32)
    
    
    if do_normalize:
        img = cv2.normalize(img, img, max_img, min_img, cv2.NORM_MINMAX)
    else:
        img = np.divide(img, np.max(img) + 1e-15, dtype=np.float32) * 255
    
    return img.astype(np.uint8)