#!/usr/bin/env python3

import numpy as np


def write_ves_file(filename, mx1d, my1d, mr1d, mp1d):
    """
    This program write out four columns in a text file

    args:
        filename:
        mx1d: a list of vesicle y-coordinates
        my1d: a list of vesicle x-coordinates
        mr1d: a list of vesicle radii
        mp1d: a list of vesicle scaling factors

    returns:
        None
        A text file with the name as filename will be generated.

    """
    
    f = open(filename, 'wt')
    n1 = np.size(mx1d)
    for i in range(0, n1):
        f.write(str(mx1d[i]) + ' ' + str(my1d[i]) + ' ' + str(mr1d[i]) + ' ' + str(mp1d[i]) + '\n')
    f.close()


if __name__ == '__main__':
    from read_box_e_m import read_box_e_m

    x, y, wx, wy, __ = read_box_e_m(
        'data/18jun07c_em6b_00002gr_00010sq_v01_00002hl_v01_00005en.framescor2x_DW_dmBIN01.mrc_resub44_screen.txt')

    write_ves_file('test_output/testves.txt', x, y, wx, wy)
