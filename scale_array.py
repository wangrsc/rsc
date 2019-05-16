#!/usr/bin/env python3

import numpy as np


def scale_array(x, lower=0, upper=1):
    """
    This program scale the input to be from lower to upper or from 0 to 1 if not lower and upper are given.

    args:
        x: input array
        lower: lower limit of the scaled array, default is 0
        upper: upper limit of the scaled array, default is 1

    returns:
        out: scaled array

    """

    if type(x) is int:
        x = np.single(x)

    if lower > upper:
        temp = lower
        lower = upper
        upper = temp

    x = np.squeeze(x)
    mn = np.min(x)
    mx = np.max(x)

    mrange = mx - mn

    if mrange < 1e-8:
        print('There is almost no feature in the input array.')
        out = x / mx
    else:
        out = (x - mn) / mrange * (upper - lower) + lower

    return out


def scale_image(data):
    return scale_array(data, 0, 255)


if __name__ == "__main__":
    import scipy.io
    import numpy as np

    a = scipy.io.loadmat('data/image.mat')
    b = a['img']
    b1 = scale_array(b, 0, 255)
    scipy.io.savemat('test_output/test_scale.mat', {'img': b, 'b1': b1})
