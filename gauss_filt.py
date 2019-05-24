#!/usr/bin/env python3

import numpy as np


def gauss_filt(iin, fc, stack=0):
    """
    This program filters the nD array with a Gaussian filter at fc. It uses
    Fast Fourier Transforming to efficiently process array

    args:
        iin: 1D, 2D, 3D, 4D array
            If stack is 1, 2D, 3D and 4D arrays will be treated as a stack of 1D, 2D, 3D arrays.
        fc: cutoff frequency (0.5 is the Nyquist frequency)
        stack: 1 means to treat the 3D array as a stack of 2d arrays

    returns:
        np.float32(out.real): the filtered nD array with single point precision

    """

    iin = np.squeeze(iin)

    # Check the dimension of the array
    m = np.shape(iin)
    nd = len(m)
    if stack > 0:
        ns = m[nd - 1]
        m = np.delete(m, nd - 1)  # remove the last element
        nd = nd - 1
    else:
        ns = 1

    # Check whether the array/image has features
    if abs(fc) < 1e-9:
        print('There is no feature in the array! Nothing is done.')
        return iin

    k = -np.log(2) * np.ones_like(m) / (2 * np.square(fc) * np.square(m))  # representing -1/sigma

    if nd == 1:
        n = m[0]
        x = np.arange((-n / 2), (n / 2))
        q = np.exp(k * np.square(x))  # e ^ 1/sigma * x^2

    elif nd == 2:
        n = m[0]
        p = m[1]
        x, y = np.mgrid[(-n / 2): (n / 2), (-p / 2): (p / 2)]
        q = np.exp(k[0] * np.square(x) + k[1] * np.square(y))

    elif nd == 3:
        n = m[0]
        p = m[1]
        r = m[2]
        x, y, z = np.mgrid[(-n / 2): (n / 2), (-p / 2): (p / 2), (-r / 2): (r / 2)]
        q = np.exp(k[0] * np.square(x) + k[1] * np.square(y) + k[2] * np.square(z))

    else:
        print("gauss_filt: Input matrix has dimension > 3. Nothing is done.")
        return iin

    q = np.fft.fftshift(q)

    if ns == 1:
        fq = q * np.fft.fftn(iin)
        out = np.real(np.fft.ifftn(fq))

    else:
        out = np.zeros_like(iin)
        for ii in range(ns):
            if nd == 1:
                fq = q * np.fft.fft(iin[:, ii])
                out[:, ii] = np.real(np.fft.ifft(fq))

            elif nd == 2:
                fq = q * np.fft.fft2(iin[:, :, ii])
                out[:, :, ii] = np.real(np.fft.ifft2(fq))

            elif nd == 3:
                fq = q * np.fft.fftn(iin[:, :, :, ii])
                out[:, :, :, ii] = np.real(np.fft.ifftn(fq))

    return out


def gauss_filt_1d(iin, fc):
    return gauss_filt(iin, fc)


if __name__ == '__main__':
    import scipy.io

    a = np.random.rand(128, 128, 128, 10)
    b1d = gauss_filt_1d(a[:, 0, 0, 0], .15)

    scipy.io.savemat('test_output/test99.mat', {'a': a, 'b1d': b1d})

    # b1d = gauss_filt(a[:, 0, 0, 0], .2)
    # b2d = gauss_filt(a[:, :, 0, 0], .2)
    # b3d = gauss_filt(a[:, :, :, 0], .2)
    #
    # b1ds = gauss_filt(a[:, :, 0, 0], .2, 1)
    # b2ds = gauss_filt(a[:, :, :, 0], .2, 1)
    # b3ds = gauss_filt(a[:, :, :, :], .2, 1)
    #
    # scipy.io.savemat('test_output/test99.mat', {'a': a, 'b1d': b1d,  'b2d': b2d,  'b3d': b3d,
    #                                             'b1ds': b1ds,  'b2ds': b2ds,  'b3ds': b3ds})
