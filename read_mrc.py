#!/usr/bin/env python3

import numpy as np
import os
import warnings
import struct


def read_mrc(filename, start_slice=1, num_slices=None):
    """
    This program read mrc files with an option to start from a specific slice.

    Image data follows with the origin in the lower left corner, looking down on the volume.
    In python, the image is read with nz = 1:nz while nx = ny = 1 (row major, last index first).
    In matlab, it is different:       nx = 1:nx while ny = nz = 1 (column first, first index first).
    So for 2D image, the transpose of python data is the same as matlab data.
    For 3D image stack, we need to convert it slice by slice.

    s.err =
        1: file doen't exist
        2: file is too small (<1024 bytes)
        3: Big Endian
        4: Not implemented data type
        5: Number of slices to read is smaller than 1
    """

    start_slice = float(start_slice)
    hdr = []
    extra_header = []
    s = type('', (), {})()
    s.err = 0
    # mmap = []

    if (num_slices is not None) and (num_slices < 1):
        s.err = 5
        warnings.warn('Number of slices must be larger than 1')
        return

    # Check whether file exist
    if not os.path.exists(filename):
        warnings.warn('File could not be found.')
        s.err = 1
        return

    # Open the file as a binary file
    f = open(filename, 'rb')  # read in binary file

    # Check the file size. If it is smaller than 1024 byte, it is wrong file.
    nbytes = os.path.getsize(filename)
    if nbytes < 1024:
        warnings.warn('File is too short for mrc header')
        s.err = 2
        return

    # get first 10 entries
    a = []
    for i in range(0, 10):
        x, = np.uint32(struct.unpack('<i', f.read(4)))
        a.append(x)
    
    if abs(a[0]) > 1e5:  # it is not encoded as little Endian
        s.err = 3
        warnings.warn('File is not in little Endian')
        return
    
    s.mode = a[3]
    s.nx = int(a[0])
    s.ny = int(a[1])
    s.nz = int(a[2])
    s.mx = int(a[7])
    s.my = int(a[8])
    s.mz = int(a[9])
    s.org = list(map(float, a[4:7]))
    nx = s.nx
    ny = s.ny
    # nz = s.nz

    if s.mode == 0:
        string = 'int8'
        pixbytes = 1
    elif s.mode == 1:
        string = 'int16'
        pixbytes = 2
    elif s.mode == 2:
        string = 'float32'
        pixbytes = 4
    elif s.mode == 6:
        string = 'uint16'
        pixbytes = 2
    else:
        s.err = 4
        raise ValueError('Readmrc: unknown data mode: ' + str(s.mode))
        # return

    s.string = string
    # pixbyte = int(pixbytes)

    # get the next 12 entries
    b = []
    for i in range(10, 22):
        x, = np.float32(struct.unpack('<f', f.read(4)))
        b.append(x)

    s.mi = b[9]
    s.ma = b[10]
    s.av = b[11]
    s.rez = float(b[0])
    s.pixa = s.rez / s.mx

    # get the next 30
    c = []
    for i in range(0, 30):
        x, = np.int32(struct.unpack('<i', f.read(4)))
        c.append(x)

    d = []
    for i in range(0, 8):
        x, = np.uint8(struct.unpack('<b', f.read(1)))        
        d.append(x)
    
    s.chars = list(map(chr, d))  

    e = []
    for i in range(0, 2):
        x, = np.int32(struct.unpack('<i', f.read(4)))        
        e.append(x)
    
    # 10 strings
    ns = min(e[1], 10)
    sstr = list(map(chr, np.zeros((800, 1))))
    sstr = np.reshape(sstr, (10, 80))
    for i in range(0, 10):
        g = []
        for j in range(0, 80):
            x, = np.uint8(struct.unpack('<b', f.read(1)))        
            g.append(x)
        g = list(map(int, g))
        sstr[i, :] = list(map(chr, g))
    s.header = sstr[0: ns, :]

    # Make sure we are at end of header
    f.seek(1024)

    # Handle extra header
    if c[1] > 0:
        extra_header = []
        extra_header_num = int(c[1] / 2)
        for i in range(0, extra_header_num):
            x, = np.int16(struct.unpack('<h', f.read(2)))
            extra_header.append(x)

    if start_slice > 1:
        skipbytes = int((start_slice - 1) * s.nx * s.ny * pixbytes)
        f.seek(skipbytes, 1)  # move this many byte from current position
        
    # Calculate how many slices and data to read in
    if num_slices is None:
        nz = int(int(s.nz) - int(start_slice) + 1)
        if nz < 0:
            nz = 0
    else:
        if num_slices > s.nz:
            nz = s.nz

    ndata_to_read = int(s.nx * s.ny * nz)

    # Read the image data
    out = np.zeros((nx, ny, nz))  # out array
    if s.mode == 0:
        # string = 'int8'
        mmap = np.fromfile(f, dtype='int8', count=ndata_to_read)
        out = np.int8(out)
    elif s.mode == 1:
        # string = 'int16'
        mmap = np.fromfile(f, dtype='int16', count=ndata_to_read)
        out = np.int16(out)
    elif s.mode == 2:
        # string = 'float32'
        mmap = np.fromfile(f, dtype='float32', count=ndata_to_read)
        out = np.float32(out)
    elif s.mode == 6:
        # string = 'uint16'
        mmap = np.fromfile(f, dtype='uint16', count=ndata_to_read)
        out = np.uint16(out)
    else:
        raise ValueError('Readmrc: unknown data mode: ' + str(s.mode))
        # return

    f.close()

    # As the data saved in mrc file is column first, we need to unwrap it that way
    for ii in range(nz):
        temp_img = mmap[nx * ny * ii: nx * ny * (ii + 1)]
        temp_img2 = np.reshape(temp_img, (ny, nx))
        out[:, :, ii] = np.transpose(temp_img2)

    return np.squeeze(out), s, hdr, extra_header


if __name__ == '__main__':
    out, s, hdr, extra_header = read_mrc('data/3dstack.mrc', 3)
    import scipy.io
    scipy.io.savemat('test_output/test_readMRC.mat', {'out': out, 's': s, 'hdr': hdr, 'extra': extra_header})
