#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from scale_array import *


def imcolor(data):
    """
    This display an image in gray scale with some colors

    args:
        data: 2d array to be displayed in gray scale plus some colors

    returns:
        None

    """
    t1 = np.linspace(0, 1, 256).reshape(256, 1)
    new_color = np.tile(t1, (1, 3))
    # 251: blue
    # 252: green
    # 253: yellow
    # 254: orange
    # 255: red
    new_color[251, :] = [0.2, 0.2, 1]
    new_color[252, :] = [0.1, 0.8, 0.1]
    new_color[253, :] = [0.9, 0.9, 0]
    new_color[254, :] = [1, 0.5, 0.1]
    new_color[255, :] = [1, 0.1, 0.1]

    new_cmap = ListedColormap(new_color)

    h1 = plt.gcf()
    h2 = h1.gca()
    h2.imshow(data, cmap=new_cmap)


if __name__ == '__main__':
    data = np.random.randn(30, 30)
    data = scale_array(data, 0, 250)
    data[:, 0] = 251
    data[:, 1] = 252
    data[:, 2] = 253
    data[:, 3] = 254
    data[:, 4] = 255

    plt.figure(99)
    imcolor(data)
    plt.show()
