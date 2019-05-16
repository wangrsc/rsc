#!/usr/bin/env python3

import numpy as np
from disc import disc
from mask import mask
from scale_array import scale_array, scale_image
import matplotlib.pyplot as plt
from imcolor import imcolor


def add_circle(img, vx, vy, vr, color=257, line_width=2, flag_scale_image=1, flag_display_image=1):
    """
      This program add circles of different sizes to an image.

     args:
         img: a 2D array (an image)
         vx: a list of the X coordinates of vesicle centers
         vy: a list of the Y coordinates of vesicle centers
         vr: a list of radii of vesicles in unit of pixels
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
    if flag_scale_image:
        img = scale_array(img, 0, 250)

    if vr.size == 0:
        print('No circles to add!')
    else:
        vx = np.round(np.squeeze(vx))
        vy = np.round(np.squeeze(vy))
        vr = np.round(np.squeeze(vr))
        box_line_w = line_width

        nr = np.prod(vr.shape)
        nmp = np.prod(vx.shape)
        if nr != nmp:
            print('The array of r and vx are of different size. The smaller will be used.')
            n_disk = min(nr, nmp)
        else:
            n_disk = nr

        # loop over vesicles having a non-zero radius
        for i in range(0, int(n_disk)):
            if vr[i] > 0:
                boxr = int(vr[i])  # box radius
                boxn = 2 * (boxr + box_line_w) + 1
                disc_small = disc(boxn, boxr).astype(int)
                box_add0 = disc(boxn, boxr + box_line_w) - disc_small  # a circle (pixels in line are one)
                box_mul0 = 1 - box_add0  # inverse of a circle (pixels in line are zero)

                cpoint = np.array([vx[i], vy[i]])
                img = mask(img, cpoint, box_mul0, box_add0 * color)    
    
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

    c = add_circle(b1, x[0:-1], y[0:-1], wx[0:-1], 259, 10, flag_scale_image=0, flag_display_image=1)
    scipy.io.savemat('test_output/test_add_circle.mat', {'from_python': c, 'vx': x, 'vy': y, 'b1': b1, 'vr': wx})
