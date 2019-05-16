#!/usr/bin/env python3

import numpy as np
import scipy.linalg


def least_square(data, model):
    """
    Least square fit of a 2D array

    args:
        data: nxn array
        model: nxn array

    returns:
        [LP0 LP1]:  LP0 + LP1 * model
        None: if input is not correct

    """

    """
    if len(data.shape) != 2 or data.shape != model.shape or data.shape[0] != data.shape[1]:
        print("The matrix cannot be used for fitting!")
        return None
    """
    # Make sure the input are arrays without single dimension
    data = np.squeeze(np.array(data))
    model = np.squeeze(np.array(model))

    n = data.size

    aa = np.array([[n, np.sum(model)], [np.sum(model), np.sum(model**2)]])
    b = np.array([np.sum(data), np.sum(data*model)])

    x = scipy.linalg.inv(aa)@b

    return x

def least_square_1d(data, model):
    return least_square(data, model)


if __name__ == "__main__":
    import scipy.io
    tt = scipy.io.loadmat('data/least_square_in.mat')
    data = tt['data']
    model = tt['model']
    paras = least_square(data, model)  # MATLAB output: [0.8361, 0.0449]
    print(paras)
    print('-----------')
    data1 = np.copy(data)
    model1 = np.copy(model)
    data1 = data1.reshape(data1.size)
    model1 = model1.reshape(model1.size)
    paras = least_square_1d(data1, model1)  # MATLAB output: [0.8361, 0.0449]
    print(paras)
