#!/usr/bin/env python3

import numpy as np
import debug as dbg


def norm_ref_e_mean(data):
    """
    This program makes the mean of images to zero and the sigma to 1

    args:
        data: a 2D array or a 3D array which is treated as a stack of 2d arrays

    returns:
        The zero-mean and normalized image.

    To dos:
     [in]=norm_ref_e_mean(in,maskin,flag_apply_mask_to_image)
     If mask is used, the normalization is done only within the mask
    % As flag_apply_mask_to_image has never been used and it is duplicate if
    % maskin is provided, so it is removed.
    """

    n = data.shape
    if len(n) == 3:
        n1 = n[0]
        n2 = n[1]
        ref_no = n[2]
    elif len(n) == 2:
        n1 = n[0]
        n2 = n[1]
        ref_no = 1
    else:
        print('Input is not a 2D or 3D array. Nothing is done.')
        return data

    factor = 1.0 / n1 / n2  # 1/the number of pixel per image

    data = np.reshape(data, (n1*n2, ref_no))

    mean_out1 = np.zeros(ref_no)
    factor_out = np.zeros(ref_no)

    for i in range(ref_no):

        data_mean = np.sum(data[:, i]) * factor
        data[:, i] -= data_mean
        mean_out1[i] = data_mean
        # If it has a large mean (e.g. 245.11), the mean is not still around 0.1-0.9. So do it twice.
        data_mean = np.sum(data[:, i]) * factor
        data[:, i] -= data_mean

        mean_out1[i] += data_mean

        energy = np.sum(data[:, i]**2) * factor
        data[:, i] = data[:, i] / np.sqrt(energy)
        factor_out[i] = 1.0 / np.sqrt(energy)

    return np.reshape(data, (n1, n2, ref_no))


if __name__ == "__main__":
    import scipy.io

    data = dbg.load_mat_var("data/norm_ref_e_mean.mat", "in")

    res = norm_ref_e_mean(data)
    scipy.io.savemat("test_output/test_norm_ref.mat", {"res": res, "data": data})
