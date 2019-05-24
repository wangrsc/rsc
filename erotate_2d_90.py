#!/usr/bin/env python3

import numpy as np

def erotate_2d_90(iin, flag_shift_center=0):
    """
    Rotate object counter_clockwise by 90;

    args:
        iin:    2D array
        flag_shift_center:

    returns:
        Rotated 2D array
    """

    if not flag_shift_center:
        print("If center is at n/2+1, after rotation, the center needs to be shifted")
        print("So please set flag_shift_center to 1.")

    m = np.shape(iin)
    if len(m) != 2:
        print('Input array is not 2D.')
        print('Nothing is done')
        return iin

    nx = m[0]
    ny = m[1]
    out = np.zeros_like(iin)
    for i in range(nx):
        for j in range(ny):
            out[i, j] = iin[j, nx - i - 1]

    if flag_shift_center > 0:
        out0 = np.copy(out)
        out[1: nx, :] = out0[0: nx-1, :]
        out[0, :] = out0[-1, :]

    return out


if __name__ == '__main__':
    import scipy.io

    a = np.arange(64).reshape(8,8)

    c = erotate_2d_90(a, 1)
    scipy.io.savemat('test_output/test11.mat', {'from_python': c, 'input': a})
