#!/usr/bin/env python3

from import_rsc_functions import *


def get_base_filename(emfilename, n_to_delete_from_end_tobasename=4):
    """
    This is used to get to get base filename
    The way to do it is to determine how many characters to be deleted from the end.
    emfilename(1:end-n_to_delete_from_end_tobasename) will give the base filename.

    args:
        emfilename: a string of a filename
        n_to_delete_from_end_tobasename: a number of characters deleted from the end

    returns:
        n_to_delete_from_end_tobasename
    """

    flag_basename_done = 0
    print(f'-- Current filename is {emfilename}')
    print(f'-- Current basename is {emfilename[0: - n_to_delete_from_end_tobasename]}')
    while not flag_basename_done:
        n_to_delete_from_end_tobasename = get_num_from_screen(
            'Change number of characters to delete from the end:', n_to_delete_from_end_tobasename)
        print(f'-- Current filename is {emfilename}')
        print(f'-- Current basename is {emfilename[0: - int(n_to_delete_from_end_tobasename)]}')
        flag_basename_done = get_yes_no('Finished?', flag_basename_done)

    return int(n_to_delete_from_end_tobasename)


if __name__ == '__main__':
    file1 = '18jun07c_em6b_00002gr_00010sq_v01_00002hl_v01_00005en.framescor2x_DW_dmBIN01.mrc'
    n = get_base_filename(file1)
    print(f'Original file name is {file1}')
    print(f'The base filename is {file1[0:-n]}')
