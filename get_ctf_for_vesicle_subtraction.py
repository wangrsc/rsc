#!/usr/bin/env python3

import numpy.fft as npfft
from contrast_transfer_astig import contrast_transfer_astig
from ctf_lwq import ctf_lwq


def get_ctf_for_vesicle_subtraction(info_ctf, pixelsize, n_here):
    """
    Calculate the ctf for vesicle subtraction, which is not centered and ready to use

    args:
        info_ctf: an object including all ctf parameters
        pixelsize: in unit of angstrom per pixel
        n_here: image size

        Note: if there is field of deltadef, it is a 2D ctf parameters (astigmatism exists)

    returns:
        ctf: a 2D array representing the centered ctf
    """

    if isinstance(info_ctf, dict):
        if 'deltadef' in info_ctf:  # 2D ctf parameters
            spar = {'n': n_here, 'pixelsize': pixelsize}
            ctf = npfft.fftshift(contrast_transfer_astig(spar, info_ctf))

        else:  # % 1D ctf files
            lambda_ = info_ctf['lambda']
            defocus = info_ctf['defocus']
            cs = info_ctf['Cs']

            if hasattr(info_ctf, 'B'):
                bfactor = info_ctf['B']
            elif hasattr(info_ctf, 'bfactor'):
                bfactor = info_ctf['bfactor']

            if hasattr(info_ctf, 'alpha'):
                qfactor = info_ctf['alpha']
            elif hasattr(info_ctf, 'qfactor'):
                qfactor = info_ctf['qfactor']

            ctf = npfft.fftshift(ctf_lwq(n_here, pixelsize, lambda_, defocus, cs, bfactor, qfactor))
            # ctf is not centered, but is ready to be convoluted with image.

    return ctf


if __name__ == '__main__':
    import scipy.io

    info_ctf = {"defocus": 1.4398, "bfactor": 48, "lambda": 0.0197, "Cs": 2.7, "qfactor": 0.07, "flag_prewhiten": 0,
                "deltadef": 0.0073, "theta": 0.3649}
    n_here = 450
    pixelsize = 1.056
    res = get_ctf_for_vesicle_subtraction(info_ctf, pixelsize, n_here)
    scipy.io.savemat('test_output/test_get_ctf.mat', {'info_ctf': info_ctf, 'from_python': res})
