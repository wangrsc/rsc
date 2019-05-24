#!/usr/bin/env python3

import math
import numpy as np
import scipy
from numpy_array_index_function import sub2ind


def to_polar(ww, nr=None, ntheta=None, rscale=1, x0=None, y0=None):
    """
    Convert the image W(x,y) to polar coords P(r,theta).
    In the P array, P(1,theta) corresponds to r=0, and
    theta=0 corresponds to points (x,y0) with x>x0.
    In typical use, if W is nxn, we set ntheta=2n and nr=n/2, and rscale=1.
    Default values are nr=floor(nx/2), ntheta=nx*2, rscale=1, x0=nr+1, y0=nr+1.

    args:
        ww:
        nr: 
        ntheta: 
        rscale: 
        x0, y0: 
    
    returns:
        
    """
    
    nx, ny = ww.shape
    if nr is None:
        nr = math.floor(nx / 2)
    if ntheta is None:
        ntheta = 2 * nx
    if x0 is None:
        x0 = nr + 1
    if y0 is None:
        y0 = nr + 1

    nr = int(nr)
    ntheta = int(ntheta)

    eps = 0.0001
    theta = np.array([np.arange(0, ntheta) * 2 * math.pi / ntheta])
    ct = scipy.cos(theta)
    st = scipy.sin(theta)
    r = np.array([np.arange(0, nr) * rscale])    
    
    xx = np.matmul(np.transpose(r), ct) + x0
    yy = np.matmul(np.transpose(r), st) + y0
    
    xx = np.transpose(xx).reshape(nr * ntheta)
    yy = np.transpose(yy).reshape(nr * ntheta)

    xx = np.maximum(xx, eps)
    xx = np.minimum(xx, nx - eps)
    
    yy = np.maximum(yy, eps)
    yy = np.minimum(yy, ny - eps)

    xx = np.asarray(xx)
    yy = np.asarray(yy)

    x0 = np.floor(xx)
    xi = xx - x0
    x0 -= 1
    x1 = x0 + 1

    y0 = np.floor(yy)
    yi = yy - y0
    y0 -= 1
    y1 = y0 + 1

    tx0y0 = np.squeeze(sub2ind([nx, ny], x0, y0))
    tx0y1 = np.squeeze(sub2ind([nx, ny], x0, y1))
    tx1y0 = np.squeeze(sub2ind([nx, ny], x1, y0))
    tx1y1 = np.squeeze(sub2ind([nx, ny], x1, y1))

    tx0y0 = tx0y0.astype(int)
    tx0y1 = tx0y1.astype(int)
    tx1y0 = tx1y0.astype(int)
    tx1y1 = tx1y1.astype(int)
   
    ww1d = ww.reshape(ww.size)

    pp = (1 - yi) * (ww1d[tx0y0] * (1 - xi) + ww1d[tx1y0] * xi) + yi * (ww1d[tx0y1] * (1 - xi) + ww1d[tx1y1] * xi)
    pp = pp.reshape(nr, ntheta, order='F')
    
    return pp


if __name__ == '__main__':
    import scipy.io
    
    ww = np.arange(64).reshape(8, 8)
    x = to_polar(ww, 4, 32, 1)

    import scipy.io
    scipy.io.savemat('test_output/test_to_polar.mat', {'ww': ww, 'x': x})
