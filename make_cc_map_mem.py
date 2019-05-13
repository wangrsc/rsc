#!/usr/bin/env python3

import numpy as np
import numpy.fft as npfft
import debug
import time
from pad_pic import pad_pic


def make_cc_map_mem(dctf, vesicle_array):
    """
    Calculate the cross-correlation between the data and a stack of references.
    This program use less memory in two ways:
        (1) It dosen't store cc maps for each vesicle model;
        (2) It pad the vesicle models here instead of storing big vesicle models.

    r_array is not used now. So it will be used as a flag for display figure.

    args:
        dctf: 2d array
        vesicle_array: stack of N references. The reference size can be different from the data
        r_array: list of N vesicle radii

    returns:
        [ccm, cci]: a 2D array containing cross-correlation coefficient
                    and a 2D array containing the index of the ref which best fit the data

    Note: r_array was removed
    """

    n = np.shape(np.squeeze(dctf))
    ns1 = n[0]
    ns2 = n[1]
    if ns1 != ns2:
        print("the sample image is not square")

    n = vesicle_array.shape
    nr1 = n[0]
    nr2 = n[1]
    if len(n) == 3:
        nr3 = n[2]
    else:
        nr3 = 1

    if ns1 != nr1 or ns2 != nr2:
        print('Padding is needed: sample({:4d}x{:-4d}), ref({:4d}x{:-4d})'.format(ns1, ns2, nr1, nr2))

    # =========================

    nd = ns1
    nterms = nr3

    print("Computing cross correlations...")
    t = time.time()
    ftdat = npfft.fftn(dctf)
    for i in range(nterms):
        if ns1 != nr1 or ns2 != nr2:
            p = pad_pic(vesicle_array[:, :, i], ns1, ns2, 0)
        else:
            p = vesicle_array[:, :, i]
        pf = npfft.fftn(npfft.fftshift(p))
        cc_now = np.real(npfft.ifftn(ftdat * np.conj(pf)))

        if i == 0:
            cci = np.ones((nd, nd)) * 1
            ccm = cc_now
        else:
            flag = np.greater(cc_now, ccm)
            cci = cci * (1 - flag) + np.ones((nd, nd)) * (i + 1) * flag
            ccm = ccm * (1 - flag) + cc_now * flag
    elapsed = time.time() - t
    print("t = {}".format(elapsed))
    return [ccm, cci]


if __name__ == "__main__":
    dctf = debug.load_mat_var("data/make_cc_map_in1.mat", "Dctf")
    vesicle_array = debug.load_mat_var("data/make_cc_map_in1.mat", "vesicle_array")
    r_array = debug.load_mat_var("data/make_cc_map_in1.mat", "r_array")
    res_ccm, res_cci = make_cc_map_mem(dctf, vesicle_array)
    ccm = debug.load_mat_var("data/make_cc_map_out1.mat", "ccm")
    cci = debug.load_mat_var("data/make_cc_map_out1.mat", "cci")
    print(np.max(res_ccm)-np.max(ccm))
    print(np.min(res_ccm)-np.min(ccm))
    print(np.mean(res_ccm)-np.mean(ccm))
    print(np.sum(res_ccm-ccm))
    print(np.max(res_cci)-np.max(cci))
    print(np.min(res_cci)-np.min(cci))
    print(np.mean(res_cci)-np.mean(cci))
    print(np.sum(res_cci-cci))
    print()

    dctf = debug.load_mat_var("data/make_cc_map_in2.mat", "Dctf")
    vesicle_array = debug.load_mat_var("data/make_cc_map_in2.mat", "vesicle_array")
    res_ccm, res_cci = make_cc_map_mem(dctf, vesicle_array)
    ccm = debug.load_mat_var("data/make_cc_map_out2.mat", "ccm")
    cci = debug.load_mat_var("data/make_cc_map_out2.mat", "cci")
    print(np.max(res_ccm)-np.max(ccm))
    print(np.min(res_ccm)-np.min(ccm))
    print(np.mean(res_ccm)-np.mean(ccm))
    print(np.sum(res_ccm-ccm))
    print(np.max(res_cci)-np.max(cci))
    print(np.min(res_cci)-np.min(cci))
    print(np.mean(res_cci)-np.mean(cci))
    print(np.sum(res_cci-cci))
