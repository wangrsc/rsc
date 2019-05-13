#!/usr/bin/env python3

import numpy as np


def polar_to_2d_uniform(n, pixel_size, fx, fy):
    """
    This is used to generate a 2D map from the given 1D-profile
    pixelsize should be in the same unit as of fx.

    args:
        n:          size of the output 2D array
        pixelsize:  in unit of that for fx
        fx:         1D profile. It must be uniformly distributed points (intervals between points are the same)
        fy:         function value of fx

    returns:
        a n*n array

    """

    # get fx interval which will be used for lookup
    # If the interval between fx[1] and fx[0] and the average interval differs less than a small number,
    # it is the right type of input.
    if np.abs((fx[1]-fx[0]) - ((fx[-1]-fx[0]) / (len(fx) - 1))) < np.abs(((fx[1]+fx[0])/2/10000)):  # a regular grid
        fx_interval_inv = 1 / (fx[1]-fx[0])
    else:
        print("The membrane profile is not on a regular grid.")
        return None

    x, y = np.mgrid[-n/2: n/2, -n/2: n/2]
    r_look = np.sqrt(x ** 2 + y ** 2) * pixel_size

    # Outside
    flag_outside = np.greater_equal(r_look, fx[-1])
    m0 = np.zeros(r_look.shape) + flag_outside * fy[-1]

    # Inside
    flag_inside = np.less_equal(r_look, fx[0])
    m0 += flag_inside * fy[0]

    # the mask for in-range
    flag = (1 - flag_outside) * (1 - flag_inside)

    # generate the lookup table for each pixel
    left = (np.floor((r_look-fx[0]) * fx_interval_inv)).astype(int)
    right = left + 1

    # set the outside pixels to fx(end-1) and the inside to fx(0)
    left = np.where(flag > 0, left, 0)
    right = np.where(flag > 0, right, len(fx)-1)
    m0 = np.where(flag > 0, (fy[left] + (fy[right]-fy[left]) * (r_look-fx[left]) / (fx[right]-fx[left])), m0)

    return m0


if __name__ == '__main__':
    import scipy.io

    fx = np.arange(12)
    fy = np.sin(fx)

    c = polar_to_2d_uniform(128, 0.6, fx, fy)

    scipy.io.savemat('test_output/test_polar.mat', {'fx': fx, 'fy': fy,  'c': c})
