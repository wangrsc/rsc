#!/usr/bin/env python3

import numpy as np
import struct


def write_mrc(vol, pixel_size, filename, mode=2, flag_relion_center=0):
    """
    This program write MRC files with an option to use the center defined by Relion

    args:
        vol: a 2D or 3D array
        pixel_size: pixel size in unit of angstrom/pixel
        filename: a string
        mode: an integer
        flag_reglion_center: write the center of the volume using Relion convention

    returns:
        None, but a new mrc file will be generate

    """

    # Detect the mode to write the binary file
    if mode == 0:
        format_string = 'b'  # ''int8'
    elif mode == 1:
        format_string = 'h'  # 'int16'
    elif mode == 2:
        format_string = 'f'  # 'float32'
    elif mode == 6:
        format_string = 'H'  # 'uint16'
    else:
        print('ReadMRC: unknown data mode')
        print('Nothing is done.')
        return

    # add .mrc if not provided in the filename
    tt1 = filename.find('mrc')
    if tt1 == -1:
        filename = [filename, '.mrc']

    # open the file in a binary mode
    fd = open(filename, 'wb')  # binary mode

    # The first ten integers
    shape = vol.shape
    nx = shape[0]
    ny = shape[1]
    if len(shape) > 2:
        nz = shape[2]
    else:
        nz = 1

    if flag_relion_center:
        a = [nx, ny, nz, mode, 0, 0, 0, nx, ny, nz]
    else:
        a = [nx, ny, nz, mode, -nx / 2, -ny / 2, -nz / 2, nx, ny, nz]
    a = np.int32(a)

    fd.write(struct.pack('<iiiiiiiiii', *a))

    # The next 12 float32 parameters
    amin = np.amin(vol)
    amax = np.amax(vol)
    amean = np.mean(vol)

    # the pixelsize might be a list where the scale in different dimensions is different
    if type(pixel_size) == np.ndarray:
        if pixel_size.size == 3:
            b = np.array([nx * pixel_size[0], ny * pixel_size[1], nz * pixel_size[2], 90, 90, 90,
                          1, 2, 3, amin, amax, amean])
        elif pixel_size.size == 3:
            b = np.array([nx * pixel_size[0], ny * pixel_size[0], nz * pixel_size[1], 90, 90, 90,
                          1, 2, 3, amin, amax, amean])
    else:
        b = np.array([nx * pixel_size, ny * pixel_size, nz * pixel_size, 90, 90, 90,
                      1, 2, 3, amin, amax, amean])

    b = np.float32(b)
    fd.write(struct.pack('<ffffffffffff', *b))

    # The next 30 entries (23-52)
    # c = []
    for i in range(0, 30):
        fd.write(struct.pack('<i', 0))

    # The next two entries (53,54)

    q = np.array([1], dtype='int32')
    q.dtype = np.uint8
    machine_le = (q[0] == 1)
    # stamp = []
    if machine_le:
        temp = 'MAP '
        temp2 = [68, 65, 0, 0]

    else:
        temp = ' PAM'
        temp2 = [0, 0, 65, 68]

    temp2 = np.uint8(temp2)
    fd.write(temp.encode('ascii'))  # string in python 3.x
    fd.write(struct.pack('<BBBB', *temp2))

    # Two more entries (55,56)
    try:
        astd = np.std(np.single(vol[:]), ddof=1)
    except MemoryError:
        print('*** Standard deviation can not be calculated due to large map.')
        print('*** So set it to the first one slice')
        tt = np.single(vol[0, :, :])
        astd = np.std(tt[:])

    astd = np.float32(astd)
    fd.write(struct.pack('<f', astd))
    fd.write(struct.pack('<i', 10))  # number of labels

    # Ten more labels
    for i in range(0, 10):
        label = '#' + '.'*78 + '#'
        fd.write(label.encode('ascii'))  # string in python 3.x

    # Now write the data

    out = []  # out array
    for kk in range(nz):
        for jj in range(ny):
            if nz > 1:
                out.append(vol[:, jj, kk])
            else:
                out.append(vol[:, jj])

    out2 = np.reshape(out, (np.size(out),))
    fd.write(struct.pack('<'+format_string*out2.size, *out2))

    fd.close()


if __name__ == '__main__':
    from read_mrc import read_mrc
    img, s, hdr, extra_header = read_mrc('data/3dstack.mrc', 3)

    write_mrc(img, s.pixa, 'test_output/stack0_n.mrc', 2)
