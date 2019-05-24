#!/usr/bin/env python3

import numpy as np


def sub2ind(array_shape, rows, cols):
    """
    Return linear index for a 2D indexies

    args:
        array_shape:
        rows:   1D array
        cols:   1D array

    returns:
        1D array
    """
    return np.array(rows) * array_shape[1] + np.array(cols)


def ind2sub(array_shape, ind):
    """
    Convert linear index to 2D index

    args:
        array_shape:
        ind:

    returns:

    """
    rows = (ind.astype('int') / array_shape[1])
    cols = (ind.astype('int') % array_shape[1]) # or numpy.mod(ind.astype('int'), array_shape[1])
    return (rows, cols)



