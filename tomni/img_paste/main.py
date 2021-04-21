import numpy as np 

def img_paste(big_img, small_img, x, y):
    '''
    This function adds a small image to a bigger image by translating it to position x, y (img coordinates).
    :big_img: (numpy.ndarray) the big image that gets altered
    :small_img: (numpy.ndarray) the smaller image that gets added to the big_img
    :x: (int) image coordinate x
    :y: (int) image coordinate y
    
    return: None (big_img gets altered)
    '''
    size_bimg = (big_img.shape[1], big_img.shape[0])
    size_simg = (small_img.shape[1], small_img.shape[0])

    # calculate position in big image
    # START
    if x < 0:
        start_x = 0
        crop_x_start = -x
    elif x > size_bimg[0] - 1:
        return
    else:
        start_x = x
        crop_x_start = 0

    if y < 0:
        start_y = 0
        crop_y_start = -y
    elif y > size_bimg[1] - 1:
        return
    else:
        start_y = y
        crop_y_start = 0
    
    #STOP
    if x + size_simg[0] > size_bimg[0]:
        stop_x = size_bimg[0]
        if x >= 0:
            crop_x_stop = size_bimg[0] - x
        else:
            crop_x_stop = size_bimg[0] + crop_x_start
        
    elif x + size_simg[0] < 0:
        return
    else:
        stop_x = x + size_simg[0]
        crop_x_stop = size_simg[0]
    
    if y + size_simg[1] > size_bimg[1]:
        stop_y = size_bimg[1]
        if y >= 0:
            crop_y_stop = size_bimg[1] - y
        else:
            crop_y_stop = size_bimg[1] + crop_y_start
    elif y + size_simg[1] < 0:
        return
    else:
        stop_y = y + size_simg[1]
        crop_y_stop = size_simg[1]
    
    # Crop smaller image to fit
    overlay_img = small_img[crop_y_start:crop_y_stop, crop_x_start:crop_x_stop]
    big_img[start_y:stop_y, start_x:stop_x] = overlay_img