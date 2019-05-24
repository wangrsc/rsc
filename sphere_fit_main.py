#!/usr/bin/env python3

import numpy as np
import numpy.fft as npfft
import scipy.optimize
import debug
from least_square import least_square, least_square_1d
from generate_3d_map_radial_2018 import generate_3d_map_radial_2018
from ves_density_circular import ves_density_circular
from get_membrane_profile import get_membrane_profile
from shift_array import shift_array


def sphere_fit_main(p, mode, n, pixelsize, data, ctf, a, d, t, cp, wth, x=None, y=None, scale=None):
    """
    This is called by vesicle subtraction to fit the vesicle size and position
    using either fake membrane profile or rale membrane profile

    args:
        p: initial guess of parameters [radius x0 y0]
        mode:
            1: perfect sphere fit for radius and position
            44: real membrane profile, vesicle type
        pixelsize:
        data: nxn or nxn x2 array. If it is a nxnx2 array, it has a mask
        ctf:    nxn array representing the CTF
        a:  parameters for fake membrane profile
        d:  parameters for fake membrane profile
        t:  parameters for fake membrane profile
        cp: parameters for fake membrane profile
        wth:parameters for fake membrane profile
        x:  parameters for fake membrane profile
        y:  parameters for fake membrane profile
        scale:parameters for fake membrane profile

    return:
        [radius x_fit y_fit]

    """    
    if (len(data.shape) > 2) and data.shape[2] == 2:  # If data is nxnx2, it includes a mask
        nzt = data.shape[2]
        data_mask = data[:, :, 1]
        data = data[:, :, 0]
    else:
        nzt = 1

    # nxt = data.shape[0]
    # nyt = data.shape[1]

    if mode == 1:
        a, x, y = p
        dd = ves_density_circular(n, pixelsize, a, d, t, cp, wth, x, y)
    elif mode > 1:
        a, x_fit, y_fit = p
        n_here = n

        fxt, fyt, pixelsize_membrane = get_membrane_profile(mode)
        fxt = fxt * pixelsize_membrane / pixelsize   # membrane profile is in the same pixelsize as in the image now.
        dd = generate_3d_map_radial_2018(fxt, fyt, a / pixelsize, n_here / 2, 1)

        shiftx = np.round(x_fit) - (np.round(n_here / 2) + 1) + 1  # Calculate shift for shift_array
        shifty = np.round(y_fit) - (np.round(n_here / 2) + 1) + 1
        shiftx += ((shiftx < 1) * n_here)
        shifty += ((shifty < 1) * n_here)
        dd = shift_array(dd, shiftx, shifty)
    else:
        print('The mode is not chosen correctly!')
        return None

    model = np.real(npfft.ifftn(npfft.fftn(dd) * ctf))

    if nzt > 1:
        ind = np.where(data_mask > 0)
        lp = least_square_1d(data[ind], model[ind])
    else:
        lp = least_square(data, model)

    if nzt > 1:
        e = np.sum((lp[0] + model*lp[1] - data)**2 * data_mask)
    else:
        e = np.sum((lp[0] + model*lp[1] - data)**2)

    return e


if __name__ == "__main__":
    par0 = debug.load_mat_var("data/sphere_fit_main_in.mat", "par0")[0, 0]
    par1 = debug.load_mat_var("data/sphere_fit_main_in.mat", "par1")[0, 0]
    par2 = debug.load_mat_var("data/sphere_fit_main_in.mat", "par2")[0, 0]

    mode = debug.load_mat_var("data/sphere_fit_main_in.mat", "mode")[0, 0]
    n_here = debug.load_mat_var("data/sphere_fit_main_in.mat", "n_here")[0, 0]
    pixelsize = debug.load_mat_var("data/sphere_fit_main_in.mat", "pixelsize")[0, 0]
    data_for_opt = debug.load_mat_var("data/sphere_fit_main_in.mat", "data_for_opt")
    Ctf = debug.load_mat_var("data/sphere_fit_main_in.mat", "Ctf")
    r0 = debug.load_mat_var("data/sphere_fit_main_in.mat", "r0")[0, 0]
    d = debug.load_mat_var("data/sphere_fit_main_in.mat", "d")[0, 0]
    t = debug.load_mat_var("data/sphere_fit_main_in.mat", "t")[0, 0]
    cp = debug.load_mat_var("data/sphere_fit_main_in.mat", "cp")[0, 0]
    wth = debug.load_mat_var("data/sphere_fit_main_in.mat", "wth")[0, 0]

    res = scipy.optimize.fmin(sphere_fit_main, np.array([par0, par1, par2]),
                              (mode, n_here, pixelsize, data_for_opt, Ctf, r0, d, t, cp, wth),
                              xtol=1e0, ftol=1e2, maxiter=2000, maxfun=2000)
    print(res)   # 153.66102702 206.74914238  55.61474384
    # MATLAB result: par = [153.6610  206.7491   55.6147]
