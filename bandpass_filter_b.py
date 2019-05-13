#!/usr/bin/env python3

import numpy as np
import debug


def bandpass_filter_b(option, order, nn, pixelsize, resl, particlesize, unitmode):
    """
    Constructs a centered square band-pass butterworth filter
    It can be used to generate LP, HP and BP filters

    args:
        OPTION: a character (h/H, l/L, b/B for highpass, lowpass and bandpass filters)
            If the option is not 'B', program will ignore corresponding number (resl or particlesize).
        order: 5 is commonly used.
        nn: the SQUARE filter size.
        pixelsize: in unit of angstroms
        resl: defines the high end frequency (Lowpass)
        particlesize: defines the low end frequency (Highpass)
        unitmode=0 ==> in unit of angstrom (default)
        unitmode=1 ==> in unit of sampling frequency    resl
        resl, particlesize: 0 means no filter.

    returns:
        A square filter centered at the center of the array

    raises:
        None

    """

    nnu = np.floor(nn/2)
    nnv = nn - nnu - 1
    yy, xx = np.meshgrid(np.arange(-nnu, nnv+1), np.arange(-nnu, nnv+1))
    rr = np.sqrt(xx**2 + yy**2)  # in unit of pixels

    if int(unitmode):   # in unit of sampling frequency
        klp = resl / 0.5 * nnu
        khp = particlesize / 0.5 * nnu
    else:   # In unit of angstroms
        kx = 1 / (nn * pixelsize)   # in FFT, each pixel is  (1/Angstrom)

        # High pass filter
        if particlesize > 0:
            khp = (1 / particlesize) / kx
        else:
            khp = 0

        # Low pass filter
        if resl > 0:
            klp = (1 / resl) / kx
        else:
            klp = 0

    lpf = np.ones((nn, nn))
    hpf = np.ones((nn, nn))
    if khp > 0:
        if option == 'h' or option == 'H' or option == 'b' or option == 'B':   # High pass filter
            ftemp = 1 / (1.0 + (rr / khp) ** (2*order))
            hpf = 1 - ftemp
            hpf = np.sqrt(hpf)

    if klp > 0:
        if option == 'l' or option == 'L' or option == 'b' or option == 'B':   # Low pass filter
            if np.abs(klp) > np.finfo(float).eps:
                lpf = 1 / (1.0 + (rr / klp)**(2 * order))
                lpf = np.sqrt(lpf)
    return lpf * hpf


if __name__ == "__main__":
    b = bandpass_filter_b('b', 5, 1024, 1.056, 5.28, 105.6, 0)
    bb = debug.load_mat_var("data/bandpassfilter_output2.mat", "fout")
    debug.save_mat_var('test_output/bpoutb.mat', 'pythonout_b', b)
    print(np.sum(b-bb))

    b = bandpass_filter_b('L', 5, 1024, 1.056, 5.28, 105.6, 0)
    debug.save_mat_var('test_output/bpoutl.mat', 'pythonout_L', b)

    b = bandpass_filter_b('h', 5, 1024, 1.056, 5.28, 105.6, 0)
    debug.save_mat_var('test_output/bpouth.mat', 'pythonout_h', b)
