#!/usr/bin/env python3

import numpy as np
import debug


def apply_filter(data, q, mode=0):
    """
     This program applies filter q to raw image in.
     If the filter is centered, mode needs to be 1
     Default filter is not centered.

    args:
        data: a 2D array to be filltered
        q: the filter ot the same size as data
        mode: 1 means the filter is centered

    returns:
        a 2D array which is filtered

    raises:
        None

    """

    if mode:
        q = np.fft.fftshift(q)
    fq = q * np.fft.fftn(data)

    return np.real(np.fft.ifftn(fq))


if __name__ == "__main__":
    data1 = debug.load_mat_var("data/ApplyFilter_in_2.mat", "in")
    q1 = debug.load_mat_var("data/ApplyFilter_in_2.mat", "q")
    res = apply_filter(data1, q1, 1)
    out = debug.load_mat_var("data/ApplyFilter_out_2.mat", "out")
    debug.save_mat_var("test_output/ApplyFilter_out_2_0.mat", "res", res)
    print(np.max(res)-np.max(out))
    print(np.min(res)-np.min(out))
    print(np.mean(res)-np.mean(out))
    print(np.sum(res-out))
