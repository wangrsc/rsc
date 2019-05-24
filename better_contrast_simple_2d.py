import numpy as np

def better_contrast_simple_2d(im, left=None, right=None, flag_stack=0):
    """
    This function changes the contrast of the image by moving the left and
    right point as in photo software.

    args:
        im: 1d, 2d, 3d or 4d array
        left, right: in unit of standard deviation of the images.
        flag_stack: 1 means the input is a stack or n-1 D array
                4d will be treated as a stack of 3d
                3d will be treated as a stack of 2d
                2d will be treated as a stack of 1d

    returns:
        Contrast enhanced array
    """

    if (left is None and right is None):
        left = 5
        right = 5
    elif (right is None):
        right = left
        
    im = np.single(np.array(im))
    imo = np.copy(im)

    if (flag_stack):
        nxyz = np.shape(im)

        if len(nxyz) == 4:
            for ii in range(0, nxyz[-1]):
                imo[:, :, :, ii] = better_contrast_simple_2d(im[:, :, :, ii], left, right, 0)
        elif len(nxyz) == 3:
            for ii in range(0, nxyz[-1]):
                imo[:, :, ii] = better_contrast_simple_2d(im[:, :, ii], left, right, 0)
        elif len(nxyz) == 2:
            for ii in range(0, nxyz[-1]):
                imo[:, ii] = better_contrast_simple_2d(im[:, ii], left, right, 0)
        else:
            print('The input array is not 2d, 3d, or 4d and can not be a stack.')
            print('Nothing is done.')

        return imo
    else:
        avg = np.mean(im)

        im = im - avg
        st = np.std(im, ddof=1)

        left = -left * st
        right = right * st
        highm = (im > right)
        lowm = (im < left)
        midm = 1- highm - lowm
        imo = im * midm + lowm * left + highm * right

        return imo


if __name__ == '__main__':
    im = np.random.rand(128, 64, 12)
    x = better_contrast_simple_2d(im, 2, 2, 1)

    import scipy.io
    scipy.io.savemat('test_output/test_contrast.mat', {'input': im, 'from_python': x})
