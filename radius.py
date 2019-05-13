#!/usr/bin/env python3

import numpy as np


def radius(n, org=None, square=0):
    """
    Create an n(1) x n(2) array where the value at (x,y) is the distance from the
    origin, the default origin being ceil((n+1)/2).  If n is a scalar,
    then the output array is n x n.
    If a second output argument is given,
    the angle (in radians) is also supplied.
    The org argument is optional, in which case the FFT center is used.
    If the square argument is given and is =1, r will be returned as the
    radius squared.

    args:
        n: a scalar or a 2*1 array which specifies the output 2D array size
        org: a 2*1 array which specifies the center
        square: 1 means r^2 instead of r is returned

    returns:
        a 2D array
        or None if the origin is of the wrong format.
    """
    n = np.array([n, n])

    if org is None:
        org = np.ceil((n+1)/2)
    else:
        if len(org) != 2:
            print('Origine must be a 2*1 array')
            return None

    x = org[0]
    y = org[1]
    xx, yy = np.mgrid[1-x: n[0]-x+1, 1-y: n[1]-y+1]  # Make zero at x,y

    if square > 0:
        r = (xx**2 + yy**2)
    else:
        r = np.sqrt(xx**2 + yy**2)

    # to do:
    # if nargout>1
    #     theta = atan2(Y,X)

    return r


if __name__ == '__main__':
    import scipy.io
    a = radius(128)
    scipy.io.savemat('test_output/test_radius.mat', {'from_python': a})
