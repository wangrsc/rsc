#!/usr/bin/env python3

import numpy as np


def mask(data_in, cpoint, mul, add=0):
    """
    Mask out the region in data_in using mul and centering mul at cpoint.
    As Mask*data_in is used, zero pixels in mul will be set to zero or the add.

    args:
        data_in: a 2d array
        cpoint: a 2*n array for the x, y coordinates
        mul: mask
        add: elevate the whole region

    returns:
        out: the masked array
    """

    # cpoint can contain only 1 point
    try:
        nx, ny = np.shape(cpoint)
    except ValueError:  # only one point
        nx = np.shape(cpoint)
        ny = 1

    if nx != 2 and ny == 2:  # we need to reshape it to 2*n
        cpoint = cpoint.transpose()
        npoints = nx
    else:
        npoints = ny
    cpoint_saved = cpoint
    out = data_in.copy()

    for ii in range(npoints):
        if ny == 1:
            cpoint = cpoint_saved
        else:
            cpoint = cpoint_saved[:, ii]

        szm = np.array(mul.shape)
        lower = np.floor(szm / 2)
        upper = szm - lower - 1

        inl = np.maximum([1, 1], cpoint - lower)
        inu = np.minimum(data_in.shape, cpoint + upper)
        rgl = inl - cpoint + lower + 1
        rgu = inu - cpoint - upper + szm
        region = np.zeros(szm)
        region[int(rgl[0]) - 1:int(rgu[0]), int(rgl[1]) - 1:int(rgu[1])] = \
            data_in[int(inl[0]) - 1:int(inu[0]), int(inl[1]) - 1: int(inu[1])]
        region = region * mul + add

        out[int(inl[0]) - 1:int(inu[0]), int(inl[1]) - 1: int(inu[1])] = \
            region[int(rgl[0]) - 1:int(rgu[0]), int(rgl[1]) - 1:int(rgu[1])]

    return out


if __name__ == '__main__':
    from disc import disc
    import scipy.io
    data = np.random.rand(512, 768)
    mul = disc(128, 34)
    cp = np.array([200, 300])
    out = mask(data, cp, mul)
    scipy.io.savemat('test_output/test_mask.mat', {'data': data, 'mul': mul, 'out': out, "cp": cp})
