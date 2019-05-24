#!/usr/bin/env python3

import scipy.optimize
import debug
import numpy as np
from subtract_ves_2019 import subtract_ves_2019
from get_membrane_profile import get_membrane_profile
from get_ctf_for_vesicle_subtraction import get_ctf_for_vesicle_subtraction
from sphere_fit_main import sphere_fit_main
from generate_3d_map_radial_2018 import generate_3d_map_radial_2018
from shift_array import shift_array
from apply_filter import apply_filter
from least_square import least_square_1d, least_square


def subtract_vesicles_popc_ect_2019(im, mx, my, mr, mp, pixelsize, info_ctf, model_type,
                                    im_mask=None, bad_vesicle_amplitude_threshold=None):
    """
    This is used to refit or resubtract vesicles.

    args:
        im: input image
        mx, my: vesicle center in unit of pixels
        mr: vesicle radii in unit of angstrom
        mp: scaling factor for each vesicle
        pixelsize: in unit of angstrom
        info_ctf: a dictionary for CTF parameters
        model_type: an integer for vesicle model
            44: OHSU Krios 300eV data
        im_mask: mask for the image including the padding edges
        bad_vesicle_amplitude_threshold: bad_vesicle_amplitude_threshold

    return:
        out:    vesicle subtracte image
        mxout, myout:   vesicle center positions
        mrout:          vesicle radii
        mpout:          vesicle scaling factors
        nt_bad_ves:     number of bad vesicles
        bad_vesicle_amplitude_threshold: bad_vesicle_amplitude_threshold

    note:
        Vesicle box is padded with image mean when it is too close to the edge of a micrograph
        im_mask: set the area occupied by a particle to zeros. So no fitting in that region.
        im0: updated image after subtraction of already-fitted vesicles
        im0_used: im0 after subtraction of not-fitted vesicles (ii+1:end) to
        reduce effect of non-fitted vesicles on current fitting
        data_for_fitting: cropped from im0_used
        data_crop_original: for updating im0
    """

    # initial value
    if bad_vesicle_amplitude_threshold is None:
        bad_vesicle_amplitude_threshold = 0.1

    flag_refit = 1
    # flag_display_fit = 0

    if im_mask is not None:
        flag_mask = 1
    else:
        flag_mask = 0

    # Set up membrane profile fxt, fyt, pixelsize_membrane
    fxt, fyt, pixelsize_membrane = get_membrane_profile(model_type)
    fxt *= (pixelsize_membrane / pixelsize)  # membrane profile is in the same pixelsize as in the image now.

    # Check image
    img_size_x, img_size_y = im.shape
    n_ves = mr.size
    if (mx.size != n_ves) or (my.size != n_ves):
        print('**** subtract_vesicles_POPC_etc: input array is not right!')
        return im
    im0 = im
    img_mean = np.mean(im0[:])
    nt_bad_ves = 0

    mxout = mx * 0
    myout = my * 0
    mrout = mr * 0
    mpout = mr * 0

    # TODO:
    # star_file are not implemented yet
    # To use local ctf for each vesicle based on refined particle ctf from starfile
    """
    if(isfield(info_ctf, 'star_file') && exist(info_ctf.star_file, 'file'))
        star1 = read_relion_starfile_2dclass_info(info_ctf.star_file)
        info_ctf_saved = info_ctf
        flag_use_local_ctf_from_particle_star_file = 1

        Find index of particle for each vesicle
        nves = numel(mx)
        index_of_particle_for_vesicle = mx * 0
        Loop over vesicles.
        for ii = 1 : nves
            x0 = mx(ii)
            y0 = my(ii)
            d2=(star1.CoordinateX-x0).^2+(star1.CoordinateY-y0).^2
            [~, val_ind] = min(d2)
            index_of_particle_for_vesicle(ii) = val_ind
        end
        mean_defocusU = mean(star1.DefocusU + star1.DefocusV)/2
        if(abs(mean_defocusU/1e4-info_ctf.defocus)>0.1) defocus differs >0.1um, trust global
            flag_use_local_ctf_from_particle_star_file = 0
        end
    else
        flag_use_local_ctf_from_particle_star_file = 0
    end
    """
    pixelsize_factor = (pixelsize_membrane / pixelsize) ** 3

    for i in range(n_ves):  # loop over vesicles
        # Crop out image for vesicle fitting/subtraction
        print('*** vesicle {} out of {}'.format(i + 1, n_ves))

        x0 = int(np.round(mx[i] - 1))
        y0 = int(np.round(my[i] - 1))
        r0 = mr[i] / pixelsize  # in unit of pixels
        cutw = int(np.round(r0 * 2) * 2)

        # In the past, the vesicle box is shifted if the vesicle is too close to the edge.
        # Now, the vesicle box is padded with image mean So the vesicle position is OK.
        cutx0 = int(max(np.round(x0 - cutw / 2), 0))
        cutx1 = int(min(np.round(x0 + cutw / 2), img_size_x))
        cuty0 = int(max(np.round(y0 - cutw / 2), 0))
        cuty1 = int(min(np.round(y0 + cutw / 2), img_size_y))
        cutw_half = int(cutw / 2)

        if (cutx1 - cutx0) < cutw or (cuty1 - cuty0) < cutw:
            flag_near_edge = 1
        else:
            flag_near_edge = 0

        data_for_fitting = np.zeros((cutw, cutw)) + img_mean
        # Don't forget actually copying data
        data_crop_original = data_for_fitting.copy()

        # TODO: local ctf using Relion information
        # To deal with local ctf: only defocus and angle are used. Others are
        # from the global ones.
        """
        if(flag_use_local_ctf_from_particle_star_file)
            info_ctf.defocus = (star1.DefocusU(index_of_particle_for_vesicle(ii)) 
            + star1.DefocusV(index_of_particle_for_vesicle(ii)))/2/1e4
            info_ctf.deltadef = (star1.DefocusU(index_of_particle_for_vesicle(ii)) 
            - star1.DefocusV(index_of_particle_for_vesicle(ii)))/1e4
            info_ctf.theta = star1.DefocusAngle(index_of_particle_for_vesicle(ii))/180*pi
        end
        """

        # im0 is the image after subtraction of already-fitted vesicles (1:ii-1)
        # im0_used subtract all unsubtracted vesicles (ii+1:end) except the one to be
        # fitted here from im0
        if flag_refit and (i < n_ves - 1):
            im0_used = subtract_ves_2019(im0, fxt, fyt, mx[i + 1:], my[i + 1:], mr[i + 1:], mp[i + 1:], pixelsize,
                                         info_ctf, 0)
        else:
            im0_used = im0

        data_for_fitting[cutw_half - (x0 - cutx0):cutw_half + (cutx1 - x0), cutw_half - (y0 - cuty0):cutw_half + (
                cuty1 - y0)] = im0_used[cutx0: cutx1, cuty0: cuty1]

        data_crop_original[cutw_half - (x0 - cutx0): cutw_half + (cutx1 - x0), cutw_half - (y0 - cuty0):cutw_half + (
                cuty1 - y0)] = im0[cutx0:cutx1, cuty0:cuty1]
        data = data_for_fitting - img_mean

        if flag_near_edge:
            data_mask_edge = np.zeros((cutw, cutw))
            data_mask_edge[cutw_half - (x0 - cutx0): cutw_half + (cutx1 - x0), cutw_half - (y0 - cuty0): cutw_half + (
                    cuty1 - y0)] = 1
            tmp = data
            data = np.zeros((*data.shape, 2))
            data[:, :, 0] = tmp
            data[:, :, 1] = data_mask_edge  # 4/25/2017 The mask will be used when refit vesicle in sphere_fit_main.m

        if flag_mask:
            if flag_near_edge:
                data_mask = np.zeros((cutw, cutw))
                data_mask[cutw_half - (x0 - cutx0): cutw_half + (cutx1 - x0), cutw_half - (y0 - cuty0): cutw_half + (
                        cuty1 - y0)] = im_mask[cutx0: cutx1, cuty0: cuty1]

                data_mask *= data_mask_edge
            else:
                data_mask = im_mask[cutx0 - 1:cutx0 + cutw - 1, cuty0 - 1:cuty0 + cutw - 1]

            if np.sum(data_mask[:] > 0) < data.size:
                # We have blocked region either near edge or due to blocked particle
                if len(data.shape) <= 2 or data.shape[2] != 2:
                    tmp = data
                    data = np.zeros((*data.shape, 2))
                    data[:, :, 0] = tmp
                data[:, :, 1] = data_mask

        n_here = cutw

        # ctf need to be calculated for each vesicle due to different sizes
        ctf2d = get_ctf_for_vesicle_subtraction(info_ctf, pixelsize, n_here)

        # Refit the vesicles
        if flag_refit:
            d = 50
            t = 0.2
            cp = 0.05
            wth = 4.2
            # opt= optimset('TolFun',1e2, 'TolX',1e0,'MaxIter',2000,'MaxFunEvals',2000)
            par = np.array([r0 * pixelsize, n_here / 2 + 1, n_here / 2 + 1])
            mode = 1

            data_for_opt = np.copy(data)
            par = scipy.optimize.fmin(sphere_fit_main, par,
                                      (mode, n_here, pixelsize, data_for_opt, ctf2d, r0, d, t, cp, wth),
                                      xtol=1e0, ftol=1e2, maxiter=2000, maxfun=2000, disp=False)
            a_fit = par[0]
            x_fit = par[1]
            y_fit = par[2]

            # Check the result
            if (a_fit / pixelsize > n_here / 2) or (np.abs(x_fit - (n_here / 2 + 1)) > (n_here / 4)) \
                    or (np.abs(y_fit - (n_here / 2 + 1)) > (n_here / 4)):
                # Bigger than the cropped area or Moved more than 1/4 of the cropped size
                a_fit = r0 * pixelsize
                x_fit = n_here / 2 + 1
                y_fit = n_here / 2 + 1

        else:
            x_fit = mx[i] - ((x0 - cutw / 2) - 1)  # cutw/2+1+round_off
            y_fit = my[i] - ((y0 - cutw / 2) - 1)
            a_fit = mr[i]

        # r0 = a_fit/pixelsize

        # Generate vesicle image
        dd = generate_3d_map_radial_2018(fxt, fyt, a_fit / pixelsize, n_here / 2, 4)
        shiftx = np.round(x_fit) - (np.round(n_here / 2) + 1) + 1  # Calculate shift for shift_array
        shifty = np.round(y_fit) - (np.round(n_here / 2) + 1) + 1  #
        shiftx += ((shiftx < 1) * n_here)
        shifty += ((shifty < 1) * n_here)
        dd = shift_array(dd, int(shiftx), int(shifty))

        # Apply CTF
        if model_type < 5 or model_type > 6:  # model 5, 6 are radial average from the data. So no CTF is needed.
            model = apply_filter(dd, ctf2d, 0)
        else:
            model = dd  # We don't apply CTF here.

        # least square fit to determine vesicle amplitude.
        if flag_refit:
            if len(data.shape) > 2 and data.shape[2] > 1:
                # either the vesicle is near edge or area occupied by a particle is set to zeros
                datat = data[:, :, 0]
                lp = least_square_1d(datat[data[:, :, 1] > 0], model[data[:, :, 1] > 0])
            else:
                lp = least_square(data, model)

        else:
            lp = np.array([0, mp[i]])

        if len(data.shape) > 2 and data.shape[2] > 1:
            data_after_sub = data_crop_original - lp[1] * model * data[:, :, 1]
        else:
            data_after_sub = data_crop_original - lp[1] * model

        im0[cutx0:cutx1, cuty0:cuty1] = \
            data_after_sub[cutw_half - (x0 - cutx0): cutw_half + (cutx1 - x0),
            cutw_half - (y0 - cuty0): cutw_half + (cuty1 - y0)]

        # check vesicle amplitude
        if flag_refit:
            # Adjust vesicle amplitude as the scaling is not right after dose compensation.
            # As vesicles are picked automatically. The first vesicle should have
            # the strongest amplitude. If bad_vesicle_amplitude_threshold> 1st
            # vesicle, use that.
            if i == 0:
                bad_vesicle_amplitude_threshold = bad_vesicle_amplitude_threshold / pixelsize_factor
                if lp[1] < bad_vesicle_amplitude_threshold:
                    print('*** vesicle amplitude is changed from {} to {} ***'.format(bad_vesicle_amplitude_threshold,
                                                                                      lp[1] * 0.5))
                    bad_vesicle_amplitude_threshold = lp[1] * 0.5

            if lp[1] < bad_vesicle_amplitude_threshold:
                print('****** Vesicle {} is not fitted right! ******'.format(i + 1))

                nt_bad_ves += 1

        mxout[i] = x_fit + (x0 - cutw / 2) - 1
        myout[i] = y_fit + (y0 - cutw / 2) - 1
        mrout[i] = a_fit
        mpout[i] = lp[1]

    out = im0
    return [out, mxout, myout, mrout, mpout, nt_bad_ves, bad_vesicle_amplitude_threshold]


if __name__ == "__main__":
    info_ctf = {"defocus": 1.4398, "bfactor": 48, "lambda": 0.0197, "Cs": 2.7, "qfactor": 0.07, "flag_prewhiten": 0,
                "deltadef": 0.0073, "theta": 0.3649}
    data = debug.load_mat_var("data/subtract_vesicles_POPC_ect_2019_in.mat", "im")
    mx = debug.load_mat_var("data/subtract_vesicles_POPC_ect_2019_in.mat", "mx")[0]
    # print(mx.shape)
    my = debug.load_mat_var("data/subtract_vesicles_POPC_ect_2019_in.mat", "my")[0]
    mr = debug.load_mat_var("data/subtract_vesicles_POPC_ect_2019_in.mat", "mr")[0]
    mp = debug.load_mat_var("data/subtract_vesicles_POPC_ect_2019_in.mat", "mp")[0]
    im_mask = debug.load_mat_var("data/subtract_vesicles_POPC_ect_2019_in.mat", "im_mask")
    pixelsize = 1.056
    model_type = 44
    res_out = subtract_vesicles_popc_ect_2019(data, mx, my, mr, mp, pixelsize, info_ctf, model_type, im_mask)
    print(res_out)
