#!/usr/bin/env python3

import numpy as np
from radius import radius
# from collections import *


def contrast_transfer_astig(s, info_ctf):
    """

    To calcualte 2D CTF for both isotropic and non-isotropic(astimatism).

    args:
        s: 2d freqs (in A^-1) or s.n and s.pixelsize
        info_ctf: a structure including ctf parameters
            lambda
            defocus
            Cs
            B
            alpha
            deltadef
            theta
    returns:
        a 2D array representing off-centered CTF ready to convolute with image.

    """

    flag_astig = False
    if isinstance(s, dict):
        n = s['n']
        pixelsize = s['pixelsize']
        s = radius(n) / (n*pixelsize)
    if isinstance(info_ctf, dict):
        pp = info_ctf
        lambda_ = pp['lambda']
        defocus = pp['defocus']
        cs = pp['Cs']
        if 'B' in pp:   # hasattr(P, 'B'):
            b = pp['B']
        if 'bfactor' in pp:   # hasattr(P, 'bfactor'):
            b = pp['bfactor']

        if 'alpha' in pp:   # hasattr(P, 'bfactor'):
            alpha = pp['alpha']
        if 'qfactor' in pp:   # hasattr(P, 'bfactor'):
            alpha = pp['qfactor']

        if 'deltadef' in pp:  # we are handling astigmatism
            deltadef = pp['deltadef']
            theta = pp['theta']
            flag_astig = True
        else:
            deltadef = 0
            flag_astig = 0

    if flag_astig:
        yy, xx = np.meshgrid(np.arange(-n/2, n/2), np.arange(-n/2, n/2))
        r2 = (xx**2 + yy**2)
        theta0 = np.arctan2(yy, xx)
        f0 = 1 / (n*pixelsize)

        chi4 = np.pi / 2 * cs * lambda_**3 * 1e7 * f0**4 * r2**2  # f^4 term of chi

        df = defocus + deltadef * np.cos(2*(theta-theta0))
        chi = (-np.pi * 1e4 * lambda_ * df * f0**2 * r2 + chi4 - alpha) / np.pi
        c = np.sin(np.pi * chi) * np.exp(-r2 * f0**2 * b)
    else:
        s2 = s**2
        chi = -1e4 * lambda_ * defocus * s2 + cs * lambda_**3 * 5e6 * s2**2 - alpha / np.pi
        c = np.sin(np.pi * chi) * np.exp(-b * s2)
    return c


if __name__ == '__main__':
    s1 = {"n": 450, "pixelsize": 1.056}
    info_ctf1 = {"defocus": 1.4398, "bfactor": 48, "lambda": 0.0197, 
                 "Cs": 2.7, "qfactor": 0.07, "flag_prewhiten": 0, "deltadef": 0.0073, "theta": 0.3649}
    res = contrast_transfer_astig(s1, info_ctf1)
    import scipy.io
    scipy.io.savemat('test_output/test_ctf.mat', {'s': s1, 'info_ctf': info_ctf1, 'ctf': res})
