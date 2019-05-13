#!/usr/bin/env python3

import numpy as np
import scipy.io
import inspect

# the global variable to check whether it is in debug mode
DEBUG = True

# decorator
def debugFunction(func):
    def wrapper(*args, **kwargs):
        if DEBUG:
            return func(*args, **kwargs)
    return wrapper

@debugFunction
def debug_print(*args, **kwargs):
    # get current function info
    info = inspect.stack()[2]
    print("{}({}:{}): ".format(info[3], info[1], info[2]), end="")
    #print(inspect.stack()[1][3], inspect.stack()[1][1], inspect.stack()[1][2])
    print(*args, **kwargs)

@debugFunction
def load_mat_var(matfile, var):
    f = scipy.io.loadmat(matfile)
    # print(f.keys())
    # print(var in f.keys())
    # print(f["in"])
    #print(f[var])
    if var in f.keys():
        return f[var]
    else:
        return None

@debugFunction
def save_mat_var(matfile, varname, var):
    scipy.io.savemat(matfile, {varname: var})

def testFunction():
    a = 1
    a += 1
    debug_print("What is value of a? {}".format(a))

if __name__ == "__main__":
    testFunction()
    DEBUG = False
    testFunction()
