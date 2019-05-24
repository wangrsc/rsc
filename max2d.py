#!/usr/bin/env python3

import numpy as np


def max2d(iin):
    """
    Finds the max value and it's respective indices in a 1D or 2D array

    args:
        iin:    1D or 2D array

    returns:
        1D array w 3 values: max, row, column (respectively)
    """

    val = np.amax(iin)
    result = np.where(iin == val)

    if len(result) == 2:
        i, j = result[0], result[1]
        i, j = i[0], j[0]
    elif len(result) == 1:
        i = result[0]
        i = i[0]
        j = 0
    else:
        print('It is neither a 1D nor a 2D array.')
        print('Noting is done')
        return None

    val_array = [val, i, j]
    return val_array


if __name__ == '__main__':
    a = np.random.randint(0, 500, size=(10, 5))
    val, i, j = max2d(a)
    print(f'val is {val}, and index are {i}, {j}')
    import scipy.io
    scipy.io.savemat('test_output/test_max2d.mat', {'input': a})
