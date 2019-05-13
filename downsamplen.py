#!/usr/bin/env python3

import numpy as np


def downsamplen(iin, ds, flag_sum_instead_of_average=False):
    """
    This program downsample the input array. If it is a 3D array, it will be treated by a stack of 2D arrays.
    If the number of rows or columns is not multiples of ds, the extra row/column will be threw away.
    e.g. a 5*5 array downsample by 2, will give a 2*2 array

    args:
        iin: input array. 3D array is treated as stack of 2d arrays.
        ds: 2 for binning of 2 elements
        flag_sum_instead_of_average:

    returns:
        A downsampled array
    """
    
    dims = iin.shape
    nx = dims[0]
    ny = dims[1]
    
    if len(dims) > 2:
        nim = dims[2]
    else:
        nim = 1
        
    ds = max(1, round(ds))
    nx = nx - (nx % ds)
    ny = ny - (ny % ds)
    nxout = nx/ds
    nyout = ny/ds
    
    if nim != 1:
        out = np.zeros((int(nxout), int(nyout), nim))
    else:
        out = np.zeros((int(nxout), int(nyout)))

    for i in range(0, nim):
        for j in range(0, ds):
            for k in range(0, ds):
                if nim != 1:
                    out[:, :, i] += np.single(iin[j:nx:ds, k:ny:ds, i])
                else:
                    out[:, :] += np.single(iin[j:nx:ds, k:ny:ds])
                
    if flag_sum_instead_of_average is False:
        out /= (ds ** 2)
        
    return out


def downsample2(data):
    return downsamplen(data, 2)


if __name__ == '__main__':
    import scipy.io
    a = scipy.io.loadmat('data/image.mat')
    b = a['img']
    dm2 = downsample2(b)
    dm3 = downsamplen(b, 3)
    dm5 = downsamplen(b, 5)
    dm7 = downsamplen(b, 7)
    scipy.io.savemat('test_output/test_downsample.mat',
                     {'data': b, 'dm2': dm2, 'dm3': dm3, 'dm5': dm5, 'dm7': dm7})
