#!/usr/bin/env python3

import numpy as np
from to_polar import to_polar


def radial_average(x, x0=None, y0=None):
    """
    This program calculate the radial average.
    The center of the average is at (x0,y0) in unit of pixel now.
    Default is (n/2+1,n/2+1)

    args:
        x: input 2D array
        x0, y0: center to carry out the radial average

    returns:
        s: radial average at (0,n/2-1)
        ps: the polar coordinates of the input data

    """
    x = np.squeeze(x)
    n, n1 = x.shape
    
    if x0 is not None and y0 is not None:
        ps = to_polar(x, n / 2, 4 * n, 1, x0, y0)
    else:
        ps = to_polar(x, n / 2, 4 * n, 1, n / 2 + 1, n / 2 + 1)
    # ps = np.transpose(ps)
    s = ps.sum(axis=1) / (4 * n)
    
    return s, ps


if __name__ == '__main__':
    import scipy.io
    
    x = np.random.rand(128,128)
    s, ps = radial_average(x)

    scipy.io.savemat('test_output/test_radial.mat', {'input': x, 's': s, 'ps': ps})
