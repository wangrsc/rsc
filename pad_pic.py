#!/usr/bin/env python3

import numpy as np


def pad_pic(data, nx, ny, padvalue=0.0):
    """
    This program pad the input data with pad value

    args:
        data: 2D array of an image
        nx*ny: the size of the new array
        padvalue: values used to fill the padded regions

    returns:
        out: padded array
    """

    n = data.shape
    if len(n) >= 2 and n[0] <= nx and n[1] <= ny:
        ndx = n[0]
        ndy = n[1]

        ref_ptx = int(np.floor(nx/2) - np.floor(ndx/2))
        ref_pty = int(np.floor(ny/2) - np.floor(ndy/2))

        if len(n) == 3:
            ndz = n[2]
            out = np.ones((nx, ny, ndz)) * padvalue
            for i in range(ndz):
                out[ref_ptx:ref_ptx+ndx, ref_pty:ref_pty+ndy, i] = data[:, :, i]
        else:
            out = np.ones((nx, ny)) * padvalue
            out[ref_ptx:ref_ptx+ndx, ref_pty:ref_pty+ndy] = data

        return out
    else:
        print("The input image is bigger than the new window. Please resize the windowsize")
        return data


if __name__ == "__main__":
    import scipy.io
    a = np.linspace(1, 100, 100)
    b = np.r_[[a], [a], [a], [a], [a], [a]]
    c = pad_pic(b, 7, 102)
    d = pad_pic(b, 8, 105, 11.2)
    scipy.io.savemat('test_output/test_pad.mat', {'data': b, 'pad1': c, 'pad2': d})
