#!/usr/bin/env python3

import numpy as np
import scipy.io
import debug

from get_ctf_for_vesicle_subtraction import get_ctf_for_vesicle_subtraction
from generate_3d_map_radial_2018 import generate_3d_map_radial_2018
from apply_filter import apply_filter

from gauss_filt import gauss_filt

import matplotlib.pyplot as plt
from imgray import imgray
from imcolor import imcolor
from add_circle import add_circle


def subtract_ves_2019(data_in, fx, fy, mx, my, mr, mp, pixelsize, info_ctf, displaymode=0):
    """
    This is used to subtract a set of vesicles from input micrograph.
    Just subtraction, no fitting.

    args:
        data_in: a 2D array
        mx,my: positions of vesicles in unit of pixels
        mr: radius of vesicles in unit of angstrom
        mp: amplitude of the model vesicles
        pixelsize: in unit of angstrom per pixel
        info_ctf: ctf information
        displaymode:

    returns:
        rtn: vesicle-subtract image
        An mrc file and a text file of vesicle fitting information are generated.

    """
    num_ves = mx.size
    n = data_in.shape
    ndx = n[0]
    ndy = n[1]
    # padx = int(ndx/2)
    # pady = int(ndy/2)
    # small_now = np.zeros((ndx*2, ndy*2))
    # small_now[padx:padx+ndx, pady:pady+ndy] += data
    small_now = np.copy(data_in)

    # check whether th vesicle is completely outside the image
    flag_out = np.less(mx + mr, 1)
    flag_out += np.less(my + mr, 1)
    flag_out += np.greater(mx - mr, ndx)
    flag_out += np.greater(my - mr, ndy)

    nd = min(ndx, ndy)
    for i in range(num_ves):

        if (mp[i] > 0) and (not flag_out[i]):
            x0 = int(np.round(mx[i] - 1))
            y0 = int(np.round(my[i] - 1))
            r0 = mr[i]
            cutw = int(min(np.round(r0 / pixelsize * 2) * 2, nd))

            cutx0 = int(max(np.round(x0 - cutw / 2), 0))
            cutx1 = int(min(np.round(x0 + cutw / 2), ndx))
            cuty0 = int(max(np.round(y0 - cutw / 2), 0))
            cuty1 = int(min(np.round(y0 + cutw / 2), ndy))
            cutw_half = int(cutw / 2)

            data = np.zeros((cutw, cutw))
            # print(i)

            data[cutw_half - (x0 - cutx0): cutw_half + (cutx1 - x0), cutw_half - (y0 - cuty0): cutw_half + (
                    cuty1 - y0)] = small_now[cutx0: cutx1, cuty0: cuty1]

            n_here = cutw
            ctf_here = get_ctf_for_vesicle_subtraction(info_ctf, pixelsize, n_here)

            vesicle_model = generate_3d_map_radial_2018(fx, fy, mr[i] / pixelsize, n_here / 2, 4)

            model = apply_filter(vesicle_model, ctf_here, 0)

            data_after_sub = data - (model * mp[i])
            xt0 = cutw_half - (x0 - cutx0)
            xt1 = cutw_half + (cutx1 - x0)
            yt0 = cutw_half - (y0 - cuty0)
            yt1 = cutw_half + (cuty1 - y0)
            small_now[cutx0: cutx1, cuty0: cuty1] = data_after_sub[xt0: xt1, yt0: yt1]

    if displaymode:
        print('... prepare images to display...')
        plt.subplot(1, 2, 1)
        imf = gauss_filt(data_in, 0.2)
        imd = add_circle(imf, mx, my, np.maximum(mr / pixelsize - 20, 20), flag_display_image=0, flag_scale_image=1)
        imcolor(imd)
        plt.title('Original')
        plt.subplot(1, 2, 2)
        imgray(gauss_filt(small_now, 0.2))
        plt.title('After subtraction')
        plt.show()

    return small_now


if __name__ == "__main__":
    # import time
    fx = debug.load_mat_var("data/subtract_ves_2019_in.mat", "fx")
    fx.shape = (fx.shape[1],)
    fy = debug.load_mat_var("data/subtract_ves_2019_in.mat", "fy")
    fy.shape = (fy.shape[1],)

    pixelsize = debug.load_mat_var("data/subtract_ves_2019_in.mat", "pixelsize")
    info_ctf = {"defocus": 1.4398, "bfactor": 48, "lambda": 0.0197, "Cs": 2.7, "qfactor": 0.07, "flag_prewhiten": 0,
                "deltadef": 0.0073, "theta": 0.3649}

    import scipy.io
    from read_box_e_m import read_box_e_m

    mx, my, mr, mp, __ = read_box_e_m(
        'data/18jun07c_em6b_00002gr_00010sq_v01_00002hl_v01_00005en.framescor2x_DW_dmBIN01.mrc_resub44_screen.txt')

    a = scipy.io.loadmat('data/image.mat')
    data = a['img']

    nn = np.size(mx)

    # t1 = time.time()
    res_out = subtract_ves_2019(data, fx, fy, mx[0:nn], my[0:nn], mr[0:nn], mp[0:nn],
                                pixelsize, info_ctf, displaymode=1)
    # t2 = time.time() - t1
    # print(t2)
    scipy.io.savemat('test_output/test_subtract_ves.mat', {'from_python': res_out, 'info_ctf': info_ctf,
                                                           'fx': fx, 'fy': fy, 'mx': mx, 'my': my, 'mr': mr, 'mp': mp,
                                                           'pixelsize': pixelsize, 'in': data})
