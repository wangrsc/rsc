#!/usr/bin/env python3


def num2strn(num, n):
    """
    It produce a string of a number with desired digits including leading zeros

    args:
        num: a scalar
        n:  an integer for number of digits

    returns:
        a string of length n
    """
    return str(num).zfill(n)


if __name__ == '__main__':
    a = 99
    print(num2strn(a, 3))
    a = 333
    print(num2strn(a, 2))
