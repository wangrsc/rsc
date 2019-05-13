#!/usr/bin/env python3

import numpy as np


def divide_conquer(rawd1, size_x, size_y, edge_x, edge_y, cut_factor, include_ref=False):
    """
    Python utility to divide/combine large data array
    It will divided data if the input array is 2D, it will combine when it is 4D (combine 4D to 2D)
    It will fill the image with the mean value if the resulted image after division is not a multiple of specified size
    However, it will NOT try to remove the margin when combine the data, that means if you divided the data then combine
    it, you will likely to get a larger data set with mean-value margins

    If rawd is just one image (2-D array), it will be divided.
    If rawd is an array of images (3-D or 4-D array), it will be combined.

    args:
        data: a 2D array to be filltered
        q: the filter ot the same size as data
        mode: 1 means the fitler is centered

    returns:
        a 2D array which is filtered

    raises:
        None

    (1) Divide:
        This program will cut the original picture into small pieces (size_x*size_y)
        with overlap of edge_x and edge_y.
        If the last one is less than cut_factor of the size,
        then we recenter the whole cutting.
        Otherwise, we just pad the original picture with mean of the image.
    e.g. divide_conquer(rawd,size_x) == divide_conquer(rawd,size_x,size_x,0,0,0.5)
         divide_conquer(rawd,size_x,edge_x) == divide_conquer(rawd,size_x,size_x,edge_x,edge_y,0.5)
         divide_conquer(rawd,size_x,edge_x,cutfactor) == divide_conquer(rawd,size_x,size_x,edge_x,edge_y,cutfactor)
         divide_conquer(rawd,size_x,size_y,edge_x,edge_y) == divide_conquer(rawd,size_x,size_y,edge_x,edge_y,0.5)
    (2) Combine:
    e.g. same as above and plus the following:
         divide_conquer(rawd): edge_x=edge_y=0, size_x*size_y=size(image);
        Combine a set of images to form a big one.
    """

    # Must copy the array because it will be resized
    rawd = np.copy(rawd1)
    n = np.shape(rawd)

    mx = size_x - 2 * edge_x  # The actual size of area of interst
    my = size_y - 2 * edge_y
    # ---Handle input errors and display error message!
    if size_x <= 0 or size_y <= 0:
        print("The window size shold be bigger than zero!")
    if mx <= 0 or my <= 0:
        print("The size of area of interest is {}x{}. Please increase window "
              "size of decrease edge width".format(mx, my))

    # divide
    if len(n) == 2:
        nx = n[0]
        ny = n[1]
        num_x = np.floor((nx-2 * edge_x) / mx)
        left_x = nx - 2 * edge_x - num_x * mx
        num_y = np.floor((ny-2 * edge_y) / my)
        left_y = ny - 2 * edge_y - num_y * my

        x0 = 0  # the starting index for cutting.
        y0 = 0

        mean_rawd = np.mean(rawd)
        if left_x < mx * cut_factor:
            x0 = np.max(x0, np.floor(left_x / 2))
        else:
            inc_x = mx - left_x
            rawd = np.r_[rawd, np.zeros((int(inc_x), rawd.shape[1]))]
            rawd[nx:int(nx+inc_x), :] = mean_rawd
            num_x += 1
        if left_y < my * cut_factor:
            y0 = np.max(y0, np.floor(left_y / 2))
        else:
            inc_y = mx - left_y
            rawd = np.c_[rawd, np.zeros((rawd.shape[0], int(inc_y)))]
            rawd[:, ny:int(ny+inc_y)] = mean_rawd
            num_y += 1

        # Now there are num_x*num_y pieces starting at (x0,y0)
        out = np.zeros((int(size_x), int(size_y), int(num_x), int(num_y)))  # 4 dimension array
        ref_x = np.zeros((int(num_x), int(num_y)))
        ref_y = np.zeros((int(num_x), int(num_y)))
        for i in range(int(num_x)):
            for j in range(int(num_y)):
                xs = x0 + (size_x - 2 * edge_x) * i
                ys = y0 + (size_y - 2 * edge_y) * j
                ref_x[i, j] = xs
                ref_y[i, j] = ys
                out[:, :, i, j] = rawd[xs:xs+size_x, ys:ys+size_y]
        if include_ref:
            return [out, ref_x, ref_y]
        else:
            return out
    # --- End of dividing of input image-----------------------------

    # combine
    else:
        # nx = n[0]
        # ny = n[1]
        nr = n[2]
        nc = n[3]
        big_size_x = edge_x * 2 + nr * (size_x - 2 * edge_x)
        big_size_y = edge_y * 2 + nc * (size_y - 2 * edge_y)
        out = np.zeros((big_size_x, big_size_y))
        for i in range(nr):
            for j in range(nc):
                xs = mx * i + edge_x
                ys = my * j + edge_y
                xn = xs + size_x - edge_x
                yn = ys + size_y - edge_y
                xd = edge_x
                yd = edge_y
                if i == 0:
                    xs -= edge_x
                    xd -= edge_x
                if j == 0:
                    ys -= edge_y
                    yd -= edge_y
                out[xs:xn, ys:yn] = rawd[xd:size_x, yd:size_y, i, j]
        return out


if __name__ == '__main__':
    data = np.zeros((100, 100))
    for x in range(100):
        for y in range(100):
            data[x, y] = x * 100 + y
    print("data dimension before divide: {}".format(np.shape(data)))
    res, ref_x, ref_y = divide_conquer(data, 50, 50, 10, 10, 0.01, include_ref=True)
    print("data dimension after divide: {}".format(np.shape(res)))
    new_data = divide_conquer(res, 50, 50, 10, 10, 0.1)
    print(np.equal(data, new_data[:data.shape[0], :data.shape[1]]))

    import scipy.io
    scipy.io.savemat('test_output/test_divide_conque.mat',
                     {'data': data, 'res': res, 'ref_x': ref_x, 'ref_y': ref_y, 'new_data': new_data})
