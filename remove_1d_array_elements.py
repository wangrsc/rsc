#!/usr/bin/env python3

import numpy as np


def remove_array_elements(mxin, flag):

    """
    This program removes elements from a list according to the flag array.
    When the flag is one, the corresponding element will be removed.
    This works for data and class.

    args:
        mxin: a list
        flag: a list indicating whether corresponding element should be removed.

    returns:
        mxin: a shorter list

    """

    if isinstance(mxin, list) & isinstance(flag, list) & (len(mxin) == len(flag)):
        n = len(mxin)
        for i in range(n-1, -1, -1):  # delete from the end
            if flag[i] == 1:
                del mxin[i]
    elif len(np.shape(np.squeeze(mxin))) == 1:
        mxin = mxin.tolist()
        flag = flag.tolist()
        n = len(mxin)
        for i in range(n - 1, -1, -1):  # delete from the end
            if flag[i] == 1:
                del mxin[i]
        mxin = np.asanyarray(mxin)
    else:
        print('Input is not a list.')
        print('Nothing is done.')
        
    return mxin


if __name__ == '__main__':
    a = [1, 2, 3, 4, 5,  6, 7]
    flag = [1, 0, 1, 0, 1, 0, 1]
    b = remove_array_elements(a, flag)
    print(b)
