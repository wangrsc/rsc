#!/usr/bin/env python3

import numpy as np
from import_rsc_functions import *
import matplotlib.pyplot as plt


def add_box(img, vx, vy, box_size, color=257, line_width=2, flag_scale_image=1, flag_display_image=1):
    """
      This program add boxes of the same size to an image.

     args:
         img: a 2D array (an image)
         vx: a list of the X coordinates of vesicle centers
         vy: a list of the Y coordinates of vesicle centers
         box_size: a number for the box size in unit of pixels
         color: an integer higher than 250.
                # 251: blue
                # 252: green
                # 253: yellow
                # 254: orange
                # 255: red
         line_width: in unit of pixel
         flag_scale_image: scale the image to be in the ranges of 0-250
         flag_display_image: show image in a pop-up window

     returns:
         a 2D array of the image with circles

     raises:
         None

     """

    img = np.double(img)
    if flag_scale_image:
        img = scale_array(img, 0, 250)
        
    vx = np.round(vx)
    vy = np.round(vy)
    r = np.round(box_size / 2)

    boxr = r
    box_line_w = line_width
    boxn = 2 * (boxr + box_line_w) + 1
    boxn = int(boxn)
    box_line_w = int(box_line_w)
    
    box = np.zeros((boxn, boxn))
    box[0:box_line_w, :] = 1
    box[boxn - box_line_w: boxn, :] = 1
    box[:, 0:box_line_w] = 1
    box[:, boxn-box_line_w:boxn] = 1
    box_add_0 = box  # pixels in line are one
    box_mul_0 = 1 - box_add_0  # inverse of the box

    nmp = np.prod(vx.shape)

    for i in range(0, int(nmp)):
        img = mask(img, np.array([vx[i], vy[i]]), box_mul_0, box_add_0 * color)

    if flag_display_image:
        imcolor(img)
        plt.show()

    return img


if __name__ == '__main__':
    import scipy.io

    x, y, wx, wy, __ = read_box_e_m(
        'data/18jun07c_em6b_00002gr_00010sq_v01_00002hl_v01_00005en.framescor2x_DW_dmBIN01.mrc_resub44_screen.txt')

    a = scipy.io.loadmat('data/image.mat')
    b = a['img']
    b1 = scale_image(b)
    c = add_box(b1, x, y, 50, 259, 10, flag_scale_image=1, flag_display_image=1)

    scipy.io.savemat('test_output/test_add_box.mat', {'from_python': c, 'vx': x, 'vy': y, 'b1': b1})
