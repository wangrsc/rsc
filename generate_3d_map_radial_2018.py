#!/usr/bin/env python3

import numpy as np
import debug
# import time


def generate_3d_map_radial_2018(fx, fy, r_here, half_size, flag_accuracy=4):
    """
    This program generate a 3d volume of a vesicle using the membrane profile (fx, fy).

    args:
        (fx,fy) is the function which defines the radial density of the membrane.
                fx: in unit of pixels
                fx,fy should include the whole membrane (e.g. -30A to 30A)
        r_here: radius in unit of pixels
        half_size: half of the image size
        r, fx and half_size are of the same unit.

    returns:
        pm1: the projection of a 3D vesicle

    """

    # get fx interval which will be used for lookup
    if np.abs((fx[1]-fx[0]) - (fx[-1]-fx[-2])) < np.abs(((fx[1]-fx[0])/len(fx)/10000)):  # a regular grid
        # fx_interval_inv = 1 / (fx[1]-fx[0])
        fx_interval_inv = (np.size(fx) - 1) / (fx[-1] - fx[0])
        # nx = fx.size
    else:
        print("The membrane profile is not on a regular grid.")
        return None

    # Setup grids
    nt = int(half_size)
    da = 1.0 / flag_accuracy

    # a slice along the z direction (x-z plane)
    z2d, x2d = np.meshgrid(np.arange(0, da+nt, da), np.arange(0, da+nt, da))
    r3d = np.sqrt(x2d**2 + z2d**2)
    r_looks = (r3d - r_here)

    # Outside the liposome
    flag_outside = np.greater_equal(r_looks, (fx[-1]))
    m0 = np.zeros(r_looks.shape) + flag_outside * fy[-1]

    # Inside the liposome
    flag_inside = np.less_equal(r_looks, (fx[0]))
    m0 += flag_inside * fy[0]

    # the mask for membrane
    flag = (1 - flag_outside) * (1 - flag_inside)

    # ===================
    # Generate a quarter of a slice of a 3d map along the x-z plane with flag_accuracy.
    # (only in the first quardrant)

    # generate the lookup table for each pixel
    left = (np.floor((r_looks-fx[0]) * fx_interval_inv)).astype(int)
    right = left + 1

    # set the outside pixels to fx(end-1) and the inside to fx(0)
    left = np.where(flag > 0, left, 0)
    right = np.where(flag > 0, right, len(fx)-1)
    m0 = np.where(flag > 0, (fy[left] + (fy[right]-fy[left]) * (r_looks-fx[left]) / (fx[right]-fx[left])), m0)

    # ===================
    # generate the radial profile for the projection of the slice.
    # fx and fy here are the projection of a x-z slice
    fx = x2d[:, 0]
    fy = np.sum(m0, axis=1) * da
    fy -= np.sum(m0[:, 0: int(np.round(1/da))], axis=1) * 0.5 * da
    # Actually, the slice near the equator should be only counted as 50% since we will do a
    # multiplication by 2 later to get the whole sphere.

    # ===================
    # Generate the lower left quarter of the projected liposome.
    y2d, x2d = np.meshgrid(np.arange(-1*nt, 1), np.arange(-1*nt, 1))
    r2d = np.sqrt(x2d**2 + y2d**2)

    flag = np.less(r2d, fx[-1])
    m0 = np.zeros(r2d.shape) + (1 - flag) * fy[-1]  # Outside the radius, set the fy(end);

    left = (np.floor((r2d-fx[0]) * flag_accuracy)).astype(int)
    right = left + 1

    # set the outside pixels to fx(end-1) and the inside to fx(0)
    left = np.where(flag > 0, left, 0)
    right = np.where(flag > 0, right, len(fx)-1)
    m0 = np.where(flag > 0, (fy[left] + (fy[right]-fy[left]) * (r2d-fx[left]) / (fx[right]-fx[left])), m0)

    # ===================
    # patch the other quandrants
    pm1 = np.zeros((nt*2, nt*2))
    pm1[:m0.shape[0], :m0.shape[1]] = m0

    pm1[nt:nt*2, 0:nt+1] = pm1[nt:0:-1, 0:nt+1]
    pm1[0:nt*2, nt:nt*2] = pm1[0:nt*2, nt:0:-1]

    pm1 = pm1 * 2.0

    return pm1


if __name__ == "__main__":
    fx = debug.load_mat_var("data/generate_3D_map_radial_2018_in.mat", "fx")
    fx.shape = (fx.shape[1])
    fy = debug.load_mat_var("data/generate_3D_map_radial_2018_in.mat", "fy")
    fy.shape = (fy.shape[1])
    rr = debug.load_mat_var("data/generate_3D_map_radial_2018_in.mat", "r_here")
    half_size = debug.load_mat_var("data/generate_3D_map_radial_2018_in.mat", "half_size")
    half_size = half_size[0][0]

    pm1 = generate_3d_map_radial_2018(fx, fy, rr, half_size)

    import scipy.io
    scipy.io.savemat('test_output/test15.mat', {'fx': fx, 'fy': fy, 'r': rr, 'half_size': half_size, 'pm1': pm1})
