#!/usr/bin/env python3


import matplotlib.pyplot as plt


def imgray(data):
    """
    This display an image in gray scale

    args:
        data: 2d array to be displayed

    returns:
        None

    """
    h1 = plt.gcf()
    h2 = h1.gca()
    plt.set_cmap('gray')
    h2.imshow(data)


if __name__ == '__main__':
    import numpy as np
    data = np.random.randn(30, 30)
    data[:3, :3] = np.max(data)
    plt.figure(99)
    imgray(data)
    plt.show()
