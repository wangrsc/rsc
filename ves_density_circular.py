#!/usr/bin/env python3

import numpy as np
import scipy.io

def ves_density_circular(n, pixelsize, a, d=50, t=0.2, cp=0.05, wth=4.2,
                         x=None, y=None, scale=None, ion=0.0, full_return=False):
    """
    Density of a circular vesicle.
    Using ndgrid instead of meshgrid since ndgrid will generate i,j in matrix
    format, which is the one we are using now.
    Using integration method to calculate the density accurately.
    A density profile along the r direction is calculated first with a
    resolution scale times higher, then it is used as a look up table.
    The result is same as ves_density_circular4 (at least the 1-d profile)
    This one is a little bit faster and has more parameters

    args:
        a: radius in angstrom (~500 A)
        d: thickness in angstrom (50 A)
        t: heightf of the extra head-group density (0.2)
        cp: depth of central dip (0.05)
        wth: the half width of the head-group peaks and the central dip (4.2 A)

    returns:
        W: a 2D array containing a vesicle
    """

    if x is None:
        x = np.floor(n / 2 + 1)
    if y is None:
        y = np.floor(n / 2 + 1)
    if scale is None:
        if a / pixelsize > 50 * 2:
            scale = 1
        elif a / pixelsize > 25 * 2:
            scale = 2
        elif a / pixelsize > 12 * 2:
            scale = 4
        else:
            scale = 8

    pixelsize = pixelsize / scale
    a /= pixelsize
    d /= pixelsize
    wth /= pixelsize

    #   a0, t_in (a0-2wth), cp_in (a-wth), cp_out (a+wth), t_out (a1-2wth), a1;
    a1 = (a + d / 2)  # make the boundary of the membrane
    a0 = (a - d / 2)
    t_in = (a0 + 2 * wth)
    t_out = (a1 - 2 * wth)
    cp_in = (a - wth)
    cp_out = (a + wth)

    # Make zero at x,y (center of the nxn image)
    yy, xx = np.meshgrid(np.arange(1-y, n-y+1), np.arange(1-x, n-x+1))
    # index into the radial function
    rr = scale * np.sqrt(xx**2 + yy**2) + 1
    nr = np.floor(np.max(rr)) + 1

    dd = np.zeros((int(nr) + 1))

    xp = np.arange(0.5, nr + 0.5)
    xm = np.arange(-0.5, nr - 0.5)

    # array must be complex type in order to for arcsin later to work
    xp = xp.astype('complex', copy=False)
    xm = xm.astype('complex', copy=False)

    w1 = np.real(xp * np.sqrt(a1**2 - xp**2) + a1 ** 2 * np.arcsin(xp / a1) - xm * np.sqrt(a1**2 - xm**2)
                 - a1**2 * np.arcsin(xm / a1))
    w0 = np.real(xp * np.sqrt(a0**2 - xp**2) + a0 ** 2 * np.arcsin(xp / a0) - xm * np.sqrt(a0**2 - xm**2)
                 - a0**2 * np.arcsin(xm / a0))
    # w1-W0 is the total area in this slice
    t_in = np.real(xp * np.sqrt(t_in**2 - xp**2) + t_in**2 * np.arcsin(xp / t_in)
                   - xm * np.sqrt(t_in**2 - xm**2) - t_in**2 * np.arcsin(xm / t_in))
    t_out = np.real(xp * np.sqrt(t_out**2 - xp**2) + t_out**2 * np.arcsin(xp / t_out)
                    - xm * np.sqrt(t_out**2 - xm**2) - t_out**2 * np.arcsin(xm / t_out))
    cp_in = np.real(xp * np.sqrt(cp_in**2 - xp**2) + cp_in**2 * np.arcsin(xp / cp_in)
                    - xm * np.sqrt(cp_in**2 - xm**2) - cp_in**2 * np.arcsin(xm / cp_in))
    cp_out = np.real(xp * np.sqrt(cp_out**2 - xp**2) + cp_out**2 * np.arcsin(xp / cp_out)
                     - xm * np.sqrt(cp_out**2 - xm**2) - cp_out**2 * np.arcsin(xm / cp_out))
    #

    dd[0:int(nr)] = (w1 - w0) * 1.0 + (t_in - w0) * t + (w1 - t_out) * t - (cp_out - cp_in) * cp + w0 * ion
    scipy.io.savemat('test_output/test2.mat', {'w0': w0, 'ion': ion})
    r0 = np.floor(rr)
    rf = rr - r0
    r0 = r0.astype('int', copy=False)

    # Use D as a look-up table with linear interpolation.
    ww = (1 - rf) * dd[r0 - 1] + rf * dd[r0]
    ww = ww / (d + wth * 2 * 2 * t - wth * 2 * cp)
    if full_return:
        return [ww, dd, scale]
    else:
        return ww


if __name__ == "__main__":
    import scipy.io

    # ww, dd, scale = ves_density_circular(426, 1.056, 49.632, 50, 0.1, full_return=True)
    # scipy.io.savemat('test_output/test_ves_density.mat', {'w': ww, 'd': dd, 'scale': scale})

    mw, md, mscale = ves_density_circular(426, 1.056, 49.632, 50, 0.1, 0.05, 4.2, 214, 214, 4, 0.2, full_return=True)
    scipy.io.savemat('test_output/test_ves_density2.mat', {'mw': mw, 'md': md, 'mscale': mscale})
