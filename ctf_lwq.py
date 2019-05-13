#!/usr/bin/env python3

import numpy as np


def ctf_lwq(n, res, _lambda, defocus, cs, bfactor, qfactor, include_chi=False):
    """
    Compute the contrast transfer function corresponding
    CTF is centered at the center of the square in this program.

    The EM image is fundamentally cylindrically symmetric. If the FT coefficients
    in the four corners are not set to zero, odd artifacts will be introduced due
    to the rectanglular symmetry.

    args:
        n:       pixel
        res:     angstrom/pixel
        cs:      mm
        Bfact:   anstrogm^2.
        Qfact:   decimal number (0-1.0)
        Defocus: microns.

    returns:
        an nxn matrix with h(n/2+1) corresponding to the zero-frequency amplitude.

    raises:
        None
    """

    nrs = n * res         # angstrom
    f2 = 1 / (nrs**2)  # Spatial frequency squared
    f4 = f2 ** 2
    df = defocus * 10000  # in angstrom
    cs = cs * 1.0e7       # in angstrom

    n2 = n / 2 
    mx, my = np.meshgrid(np.arange(-n2, n2), np.arange(-n2, n2))
    r2 = mx**2 + my**2
    r4 = r2**2
    kb = np.pi * (-_lambda * df * f2 * r2 + 0.5 * _lambda**3 * cs * f4 * r4) 
    chi = kb - np.arcsin(qfactor) 
    # The following is the same as the above formula. But the chi is readily
    # used to see the periods (e.g. within ctf 2 zeros means chi is smaller
    # than 2pi). The returned chi is in unit of pi.
    h = np.sin(chi) * np.exp(-bfactor * f2 * r2) 
    chi = chi / np.pi 
    mask = np.where(r2 < n2**2, 1, 0)
    h = h * mask
    if include_chi:
        return [h, chi]
    else:
        return h


if __name__ == '__main__':
    hh, hchi = ctf_lwq(1024, 1.387, 0.0251, 1.5, 2, 200, 0.07, include_chi=True)

    import scipy.io
    scipy.io.savemat('test_output/test_ctf_lwq.mat', {'hh': hh, 'chi': hchi})
