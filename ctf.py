#!/usr/bin/env python3

import re
import numpy as np

class ctf():
    """
    class for read/write ctf file

    attributes:
        noiseType can have 3 different options: 'None', 'EMAN_noise' or 'Fred_noise'
        please use hasattr() to check whether a field exist, getattr() to retrive data
        and setattr() to modify or add data to ctf object

    methods:
        loadFromFile: read a ctf file given filename
        writeTofile: write data to a ctf file given filename

    1. key value pairs are seperated by a space
        for example: "key value"
        key must contain no space, and value must be either float or int
    2. special values are 'zp_noise' and 'zp_ctf', the number after them means
        the number of element in the array, the next line contains all elements
        seperated by spaces
        for example: "zp_ctf 3", the next line is "1 2 3"
     3. 'EMAN_noise' can have multiple values. It is represented as multiple key
        value pairs started with 'EMAN_noise'
     4. [ffax dvt_original dvtfitted dvtnoise dvtbeam] are printed in multiple
        lines as vectors
     5. start line comments with '#', it must be placed as the first character in
        the line to be interpreted as comment, comments are ignored by this program

    """
    def __init__(self, filename=None, simple_format=0):
        self._initAllFields()
        if filename is not None:
            self.loadFromFile(filename, simple_format)

    def _initAllFields(self):
        self.symbols = ('defocus', 'deltadef', 'theta', 'bfactor', 'lambda',
            'Cs', 'qfactor', 'power_spectrum_patch_size', 'flag_prewhiten',
            'Fred_noise', 'EMAN_noise', 'zp_noise', 'zp_ctf')

        # rawData for debugging purpose only
        self.rawData = {}

        #self.defocus = 0
        #self.bfactor = 0
        #self.lambda_ = 0
        #self.Cs = 0
        #self.qfactor = 0
        #self.zp_noise = 0
        #self.zp_ctf = 0
        #self.para_noise = []
        #self.flag_prewhiten = 0
        #self.deltadef = 0
        #self.theta = 0

        # numpy arrays
        self.ffax = None
        self.dvt_original = None
        self.dvtfitted = None
        self.dvtnoise = None
        self.dvtbeam = None

    def loadFromFile(self, filename, simple_format):
        with open(filename, 'r', encoding='utf-8') as f:
            ffax = []
            dvt_original = []
            dvtfitted = []
            dvtnoise = []
            dvtbeam = []
            line = f.readline().strip()
            flg = None
            while line:
                # Deal with comments
                if line[0] != '#':
                    tmp = re.split("[\t ]+", line)
                    # Deal with special input, in this case, zp_ctf and zp_noise
                    if flg is not None:
                        if len(tmp) != flg[1]:
                            print("Warning: \'{}\' suppose to read {} \
                                values, but only {} present".format(flg[0],
                                flg[1], len(tmp)))
                        setattr(self, flg[0], [float(x) for x in tmp])
                        flg = None
                    # Deal with key value pairs
                    #print("{}: {}".format(tmp[0], tmp[1]))
                    if len(tmp) >= 2 and str.isalpha(tmp[1]):
                        tmp_used = tmp[0:2]
                        tmp_used[0] = tmp[1]
                        tmp_used[1] = tmp[0]
                        del tmp
                        tmp = tmp_used
                        del tmp_used

                    if len(tmp) == 2 and tmp[0] in self.symbols:  # defocus 2.766341
                        # deal with special cases
                        if tmp[0] == 'Fred_noise':
                            self.para_noise = float(tmp[1])
                        elif tmp[0] == 'EMAN_noise':
                            if not hasattr(self, 'para_noise'):
                                self.para_noise = []
                            self.para_noise.append(float(tmp[1]))
                        elif tmp[0] ==  'zp_ctf' or tmp[0] ==  'zp_noise':
                            flg = (tmp[0], int(tmp[1]))
                        else:
                            setattr(self, tmp[0], float(tmp[1]))
                            # put key value pair inside self.rawData
                            self.rawData[tmp[0]] = tmp[1]
                    elif len(tmp) == 5 and not simple_format:
                        tmp = [float(x) for x in tmp]
                        ffax.append(tmp[0])
                        dvt_original.append(tmp[1])
                        dvtfitted.append(tmp[2])
                        dvtnoise.append(tmp[3])
                        dvtbeam.append(tmp[4])
                line = f.readline().strip()
        # organize data structures
        self.ffax = np.array(ffax)
        self.dvt_original = np.array(dvt_original)
        self.dvtfitted = np.array(dvtfitted)
        self.dvtnoise = np.array(dvtnoise)
        self.dvtbeam = np.array(dvtbeam)
        # convert data types
        if hasattr(self, 'flag_prewhiten'):
            self.flag_prewhiten = bool(self.flag_prewhiten)
        if hasattr(self, 'power_spectrum_patch_size'):
            self.power_spectrum_patch_size = int(self.power_spectrum_patch_size)
        if hasattr(self, 'zp_noise'):
            self.zp_noise = [int(x) for x in self.zp_noise]
        if hasattr(self, 'zp_noise'):
            self.zp_ctf = [int(x) for x in self.zp_ctf]
        if hasattr(self, 'para_noise'):
            self.para_noise = [float(x) for x in self.para_noise]

    def writeTofile(self, filename, noiseType=None):
        self._zp_noise_comment = "# index of minimum points in ffax for background noise fitting"
        self._zp_ctf_comment = "# index of minimum points in ffax for CTF fitting"
        with open(filename, 'w', encoding='utf-8') as f:
            # Write key value pairs
            for s in self.symbols:
                # Deal with special cases: noises
                if noiseType is not None and s == noiseType:
                    if hasattr(self, 'para_noise') and \
                        self.para_noise is not None:
                        if s == "EMAN_noise":
                            for x in self.para_noise:
                                f.write("{} {}\n".format(s, x))
                        else:
                            # s == "Fred_noise"
                            f.write("{} {}\n".format(s, self.para_noise))
                    else:
                        print("Error: \'para_noise\' is not set")

                if hasattr(self, s):
                    # Deal with special cases: zp_noise and zp_ctf
                    if s == 'zp_noise' or s == 'zp_ctf':
                        if s == 'zp_noise':
                            f.write(self._zp_noise_comment + "\n")
                        else:
                            f.write(self._zp_ctf_comment + "\n")
                        z = getattr(self, s)
                        f.write("{} {}\n".format(s, len(z)))
                        f.write(" ".join([str(x) for x in z]) + "\n")
                    elif s == 'flag_prewhiten':
                        f.write("{} {}\n".format(s, int(getattr(self, s))))
                    else:
                        # General case
                        f.write("{} {}\n".format(s, getattr(self, s)))

            # write the last part (multiple line of 5 values)
            # ffax dvt_original dvtfitted dvtnoise dvtbeam
            if hasattr(self, 'ffax') and hasattr(self, 'dvt_original') and \
                hasattr(self, 'dvtfitted') and hasattr(self, 'dvtnoise') and \
                hasattr(self, 'dvtbeam'):
                # check if they have same length
                l = len(self.ffax)
                if l == len(self.dvt_original) and l == len(self.dvtfitted) \
                and l == len(self.dvtnoise) and l == len(self.dvtbeam):
                    for i in range(l):
                        # keep 6 decimal places
                        f.write("{:.6f} {:.6f} {:.6f} {:.6f} {:.6f}\n".format(
                            self.ffax[i], self.dvt_original[i], self.dvtfitted[i],
                            self.dvtnoise[i], self.dvtbeam[i]))



# below are for debugging purpose
if __name__ == "__main__":
    #filename = "dm02f-cv_20140831_23321342_2x_SumCorr_block_n.ctf"
    #filename = "18jun07c_em6b_00002gr_00010sq_v01_00002hl_v01_00005en.framescor2x_DW_dmBIN01.mrc.ctf"
    #filename = "17nov12c_jh2_00016gr_00057sq_v02_00011hl_v01_00005es.frames_cvcor2x.mrc-1D.ctf"
    filename = '18jun07c_em6b_00002gr_00010sq_v01_00002hl_v01_00005en.framescor2x_DW_dmBIN01.mrc.ctf'
    test = ctf(filename)
    # get all attribute name
    attrs = [x for x in dir(test) if x[0] != '_']
    # print all attributes, this should print all values in ctf file
    for x in attrs:
        print("{}: {}".format(x, getattr(test, x)))

    test = ctf(filename, 1)
    # get all attribute name
    attrs = [x for x in dir(test) if x[0] != '_']
    # print all attributes, this should print all values in ctf file
    for x in attrs:
        print("{}: {}".format(x, getattr(test, x)))
    # write the data back
    #test.writeTofile("test.ctf", noiseType="EMAN_noise")
    test.writeTofile("test1d.ctf")
