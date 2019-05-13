#!/usr/bin/env python3

import math
import numpy as np

from mask import mask
from scale_array import scale_array, scale_image
import matplotlib.pyplot as plt
from imcolor import imcolor


def add_cross(img, vx, vy, cross_length=20, color=257, line_width=2, flag_scale_image=1, flag_display_image=1):
    """
      This program add crosses of the same size to an image.

     args:
         img: a 2D array (an image)
         vx: a list of the X coordinates
         vy: a list of the Y coordinates
         cross_length: a number for the cross size
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
         a 2D array of the image with crosses
    """
    
    if flag_scale_image:
        img = scale_array(img, 0, 250)

    cross_length = np.int32(cross_length)
    nmp = np.prod(vx.shape)

    thk = line_width
    marker = np.zeros([2 * cross_length + 1, 2 * cross_length + 1])
    marker[:, cross_length + math.floor(1 - thk) - 1:cross_length + math.ceil(1 + thk)] = color
    marker[cross_length + math.floor(1 - thk) - 1:cross_length + math.ceil(1 + thk), :] = color
    mul = (marker == 0)

    for i in range(0, int(nmp)):
        img = mask(img, np.array((round(vx[i]), round(vy[i]))), mul, marker)

    if flag_display_image:
        imcolor(img)
        plt.show()

    return img


if __name__ == '__main__':
    import scipy.io
    from read_box_e_m import read_box_e_m

    x, y, wx, wy, __ = read_box_e_m(
        'data/18jun07c_em6b_00002gr_00010sq_v01_00002hl_v01_00005en.framescor2x_DW_dmBIN01.mrc_resub44_screen.txt')

    a = scipy.io.loadmat('data/image.mat')
    b = a['img']
    b1 = scale_image(b)

    c = add_cross(b1, x, y, 50, 257, 5, flag_scale_image=0, flag_display_image=1)

    scipy.io.savemat('test_output/test_add_cross.mat', {'from_python': c, 'vx': x, 'vy': y, 'b1': b, 'vr': wx})
