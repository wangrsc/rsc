#!/usr/bin/env python3

import scipy.io as sio
import numpy as np
from gauss_filt import gauss_filt_1d


def get_membrane_profile(model_type):
    """
    This program is to output membrane profile for vesicle fitting
    POPC membrane profile; As long as the fx and fy are of the same unit.
    fyt(end) is set to zero, while max(fyt) is set to 1.
    No matter what the fy is, fy(end) is set to zero here to make no
    contributions to the outside liposome region.

    args:
        model_type: an integer
        44: OHSU GIF30eV Krios 300keV. Good for UW Krios too.

    returns:
        fx: in unit of current pixelsize
        fy: membrane profile
        pixelsize: current pixelsize
    """
    # 08/25/2018
    # fyt(end) is set to zero, while max(fyt) is set to 1.
    #   No matter what the fy is, fy(end) is set to zero here to make no
    #   contributions to the outside liposome region.
    #
    # This program is to output membrane profile for vesicle fitting
    # POPC membrane profile; As long as the fx and fy are of the same unit.
    #
    # 1 step function with regular parameters, d=50;t=0.2;cp=0.05;wth=4.2;
    # 2 step function with better parameters used to subtract for micrographs,d=61.64;t=-0.36;cp=0.18;wth=4.64;ion=-0.1;
    # 3 fx,fy model with zeros outside 60Angstrom
    # 4 fx,fy model with outside rings
    #
    # 5 Radial average from the data
    # 6 Smoothed radial average from the data
    #
    # 7 Asymmetric profile
    # 8 Similar to 7 but with fxt=fxsize2;
    # 9 Similar to 7
    #
    # 10: model-popc-blockn-simple.mat, r0d5_2x_2sig
    # 11: similar to 10, but r0d5_2x_3sig
    # 12: similar to 10, but r0d4_2x_2sig
    # 13: similar to 10, but r0d4_2x_3sig
    #
    # 20: From merged images, popc_merge_blockn_r0d5_2x_2sig.mat, _r0d5_2x_2sig
    # 21: popc_merge_blockn_r0d5_2x_2sig_dipout.mat
    # 22: popc_merge_blockn_r0d5_2x_2sig_dipout_width45.mat, wider wrt to case 21.
    # 23: popc_merge_blockn_r0d5_2x_2sig_dipout_width45_sym.mat,  outer half of case 22, symmetrized.
    # 24: popc_merge_blockn_r0d5_2x_2sig_bigves_99.mat, Big vesicles (r> 50pixels D>277A), well separated from others
    # 25: popc_merge_blockn_r0d5_2x_2sig_bigves_short.mat, Big vesicles but cut it to -75-75Angstrom
    #
    # 30: model-popc-3d_2015.mat
    # 34: 195 vesicles dm2 images
    #
    # 44: OHSU GIF30eV Krios 300keV
    # 45: symmetrized of 44
    #
    # 54: UWJune GIF30eV Krios 300keV
    #
    # scale_factor is used to manipulate membrane profile of model 54.

    if model_type == 44:
        # OHSU GIF30eV Krios 300keV, how_to_fit_back_hankel_to_get_membrane_profile_2016_jan.m
        # inverse ctf filter at ctf=0.05, no further modification,
        # qfactor=0.07, 854 vesicles, asymmetric
        # profile was raised up by mean(fynn(42:end))
        fxnn = np.arange(-25, 26)
        fynnall = [0.0226057019909365, 0.0252021990537559, 0.00485938558557869, 0.0256541100536305,
                   0.000981550525522873, -0.0497238811929170, 0.0440611267774491, 0.00488015547836201,
                   -0.00169744859071094, 0.0378464802756880, 0.0240096571753982, 0.0701905042504966, 0.112803145158847,
                   0.220858833655673, 0.325610180697430, 0.470355832691475, 0.585072998126252, 0.652651493194249,
                   0.656930757637444, 0.659836776122480, 0.638555542838540, 0.622161865703875, 0.590627989459644,
                   0.555197812566001, 0.452965746494022, 0.426309369525603, 0.470218987523958, 0.540928357498853,
                   0.559852365388236, 0.581389132430551, 0.606032801830115, 0.613400245596709, 0.635424310958883,
                   0.645131542098614, 0.621306836732483, 0.574827517925640, 0.457392485410873, 0.287206470195894,
                   0.160438292081854, 0.0604879337148811, 0.0364709272295661, 0.000868729643717925,
                   -0.000591637120631788, -0.0174713174128332, -0.0151496150820872, 0.0138930377783886,
                   -0.00274894092210304, 0.000264283341471494, 0.00722820749218572, 0.00406397815218479,
                   0.00964327412970650]

        # Set background to zeros arournd around +/- 32.76 A.
        fynnt = np.copy(np.asarray(fynnall))
        fynnt[0:12] = 0
        fynnt[40-1: np.size(fynnt)] = 0

        fxt = fxnn
        pixelsize_membrane = 2.112

        # smooth out the peaks
        fyt1 = gauss_filt_1d(fynnt, 0.15)

        fyt1 = fyt1 * (fyt1 > 0)
        fyt1 = fyt1 * 1.38
        
        fyt = fyt1
        fyt = fyt - fyt[-1]  # Set min to zeros
        fyt = fyt / np.max(fyt)  # to scale it to 0-1 range.

        # return [f['fxt'][0].astype('float64'), f['fyt'][0].astype('float64'), f['pixelsize_membrane'][0, 0]]
        return [fxt.astype('float64'), fyt.astype('float64'), pixelsize_membrane]
    else:
        print("Unsupported model type")
        return None


if __name__ == "__main__":
    a, b, c = get_membrane_profile(44)
    print(a)
    print(b)
    print(c)
