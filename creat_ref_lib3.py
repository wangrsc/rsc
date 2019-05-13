#!/usr/bin/env python3

# import scipy.io
import numpy.fft as npfft
from ctf_lwq import *
from ves_density_circular import *


def creat_ref_lib3(n, a_per_pixel, r_in_a_min, r_in_a_max, r_step_in_a, defocus, cs, bfact, qfact, _lambda):
    """
    This program creat set of vesicles.
    [r_count,r_array,vesicle_array] = creat_ref_lib3(
        n,a_per_pixel,r_in_a_min,r_in_a_max,r_step_in_a,defocus,cs,bfact,qfact,lambda)
    If no CTF parameters are set, no CTF applied');

    args:
        r_step_in_a: interval of vesicle size
        n: image size
        a_per_pixel: pixel size in unit of angstrom

    returns:
        [r_count, r_array, vesicle_array]: number of radii, list of radii, n*n*r_count array

    raises:
        None

    """

    flag_ctf = 1  # as long as there is more than 5 args
    d_in_a = 50
    r_count = 0
    # r_end = np.floor((r_in_a_max - r_in_a_min) / r_step_in_a) + 1
    # i = np.floor(np.sqrt(r_end)) + 1

    # res = a_per_pixel
    if flag_ctf:
        hh = ctf_lwq(n, a_per_pixel, _lambda, defocus, cs, bfact, qfact)

    rval = np.arange(r_in_a_min, r_in_a_max, r_step_in_a)
    vesicle_array = np.zeros((n, n, len(rval)))
    r_array = np.zeros(rval.shape)
    for r in rval:
        r_array[r_count] = r
        t1 = ves_density_circular(n, a_per_pixel, r, d_in_a)
        if flag_ctf:
            t1 = np.real(npfft.ifftn(npfft.fftn(t1) * npfft.fftshift(hh)))

        # TODO: plot image
        # if usejava('jvm')
        #     subplot(i,i,r_count);
        #     imacs(real(t1));
        #     title(strcat('r=',num2str(r),char(197)));
        #     SetGrayscale; axis image;
        # end

        vesicle_array[:, :, r_count] = t1[:, :]
        print("{:.6f}".format(r))
        r_count += 1

    return [r_count, r_array, vesicle_array]


if __name__ == "__main__":
    r_count2, r_array2, vesicle_array2 = creat_ref_lib3(426, 1.056, 49.632,
                                                        159.456, 9.504, 1.4398, 2.7, 48, 0.07, 0.197)
    print(r_count2)
    print(r_array2)
    print(vesicle_array2.shape)
    scipy.io.savemat("test_output/test_ref_lib.mat",
                     {"r_count2_": r_count2, "r_array2_": r_array2, "vesicle_array2_": vesicle_array2})
