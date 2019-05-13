#!/usr/bin/env python3

# process .mrc files

import struct
import os
import numpy as np

class mrc():

    def __init__(self, filename=None):
        self._initAllFields()
        if filename is not None:
            self._loadFromFile(filename)

    def _initAllFields(self):
        pass

    def _loadFromFile(self, filename):
        fsize = os.stat(filename).st_size
        #print(fsize)
        with open(filename, "rb") as f:
            rawHeader = f.read(1024)
            preCursor = 0

            # 1. read 10 integer (40 bytes)
            cursor = 40
            a = struct.unpack("<iiiiiiiiii", rawHeader[preCursor:cursor])
            [nx, ny, nz, mode, ncstart, nrstart, nsstart, mx, my, mz] = a
            preCursor = cursor
            # print(a)
            # should be 3840 3840 1 2 -1920 -1920 -1 3840 3840 1 for the test file

            # 2. read 12 float (48 bytes)
            cursor += 48
            b = struct.unpack("<ffffffffffff", rawHeader[preCursor:cursor])
            [xlength, ylength, zlength, alpha, beta, gamma, mapc, mapr, maps, amin, amax, amean] = b
            preCursor = cursor
            # print(b)
            # xlength ylength zlength alpha beta gamma mapc mapr maps amin amax amean
            # 4055.04003906250 4055.04003906250 1.05599999427795 90 90 90 1.40129846432482e-45 2.80259692864963e-45 4.20389539297445e-45 12.2504720687866 15.3350839614868 13.4940538406372

            # 3. read 30 integer (120 bytes)
            cursor += 120
            c = struct.unpack("<iiiiiiiiiiiiiiiiiiiiiiiiiiiiii", rawHeader[preCursor:cursor])
            extendedHeaderSize = c[1]
            preCursor = cursor
            #print(c)
            # should be all 0 in test file

            # 4. read 8 byte string (8 bytes)
            cursor += 8
            d = rawHeader[preCursor:cursor].decode("utf-8")
            preCursor = cursor
            # print(d)
            # should be "MAP DA" in test file

            # 5. read 2 integer (8 bytes)
            cursor += 8
            e = struct.unpack("<ii", rawHeader[preCursor:cursor])
            preCursor = cursor
            # print(e)
            # should be 1048992488 10 in test file

            # 6. read up to 10 strings, each with 80 bytes (800 bytes)
            _str = []
            for _ in range(10):
                cursor += 80
                _str.append(rawHeader[preCursor:cursor].decode("utf-8"))
                preCursor = cursor
            #print(_str)

            # 7. TODO: read extended header (skipped because test file had no extended header)

            # 8. read data
            pixelSize = 4
            nPixel = nx * ny * nz
            #print(nPixel)
            # data portion:
            # type "*float32"
            # number of value to read: 14745600

            self.img = np.reshape(np.fromfile(f, dtype=np.float32, count=nPixel), (nx, ny, nz))
            #np.savetxt("img.csv", img, delimiter=",")


# below are for debugging purpose
if __name__ == "__main__":
    filename = "18jun07c_em6b_00002gr_00010sq_v01_00002hl_v01_00005en.framescor2x_DW_dmBIN01.mrc"
    filename = "test3.mrc"
    test = mrc(filename)
    # get all attribute name
    attrs = [x for x in dir(test) if x[0] != '_']
    # print all attributes
    #for x in attrs:
    #    print("{}: {}".format(x, getattr(test, x)))
