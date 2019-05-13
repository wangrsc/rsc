#!/usr/bin/env python3

import numpy as np


def discm(nx, ny, cx, cy, r):
    """
    Construct a circular disc (ones inside the disc)

    args:
        nx: dimension
        ny: dimension
        cx: center of disc
        cy: center of disc
        r: radius of the disc

    returns:
        An nx*ny array with centered disc.
    """
    x, y = np.mgrid[-cx + 1: nx + 1 - cx, -cy + 1: ny + 1 - cy]
    r2 = x * x + y * y
    m = r2 < (r+.5) * (r+.5)
    return m


def disc(n, r, origin=None):
    if origin is None:
        origin = [(n + 1) / 2, (n + 1) / 2]

    return discm(n, n, origin[0], origin[1], r)


if __name__ == '__main__':
    m1 = disc(1024, 256)
    m2 = discm(1024, 1536, 500, 800, 300)
    import scipy.io
    scipy.io.savemat('test_output/test_disc.mat', {'from_python': m1, 'm2': m2})
