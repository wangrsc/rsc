#!/usr/bin/env python3

import numpy as np
# from pathlib import Path
import os


def read_box_e_m(filename=''):
    """
    This program read a text file which contains 4 or 5 columns of numeric values.
    It can read both the particle file from EMAN, matlab or the vesicle file from matlab

    args:
        filename: filename which has either 4 or 5 column of data

    returns:
        x, y: coordinates
        wx: box size in X-axis for particle files
            vesicle radii for vesicle files
        wy: box size in Y-axis for particle files
            vesicle scaling factor  for vesicle files
        type: particle types for particle files
            zeros for vesicle files
    Note: empty lists will be returned if file doesn't exist.

    """
    # ask the user to input a filename
    while filename == '':
        filename = input('Please specify filename of saved coordinates: ')

    # Check whether file exist
    if os.path.exists(filename):
        data_file = open(filename, 'r')
    else:
        print(filename + ' does not exist!')
        x = np.array([])
        y = np.array([])
        wx = np.array([])
        wy = np.array([])
        wtype = np.array([])
        return x, y, wx, wy, wtype

    # Read data line by line
    data_saved = []
    lines = data_file.readlines()
    for line in lines:
        line = line.strip()  # All leading and trailing whitespaces are removed
        line = line.split()  # Splits a string into a list.
        line = list(map(float, line))  # Convert to float
        data_saved.append(line)
    data_file.close()

    # Data file contains either 4 or 5 columns
    data = np.array(data_saved)
    shape = data.shape
    column_max = shape[-1]
    
    if data.size > 1:
        x = data[:, 0]
        y = data[:, 1]
        wx = data[:, 2]
        wy = data[:, 3]
        if column_max > 4:
            wtype = data[:, 4]
        else:
            wtype = data[:, 3] * 0
                
    else:
        print('*** No particles saved in {}. ***'.format(filename))
        x = np.array([])
        y = np.array([])
        wx = np.array([])
        wy = np.array([])
        wtype = np.array([])
    
    return x, y, wx, wy, wtype


if __name__ == '__main__':
    x, y, wx, wy, __ = read_box_e_m(
        'data/18jun07c_em6b_00002gr_00010sq_v01_00002hl_v01_00005en.framescor2x_DW_dmBIN01.mrc_resub44_screen.txt')
    print(x)
    print(y)
    print(wx)
    print(wy)
