#!/usr/bin/env python3

import os


def get_files_having_pattern(filepattern):
    """
    This is used to get a list of filename having a certain pattern in current folder.

    If filepattern has *, no modification will be made.
    Otherwise, * will be added to both side.

    args:
        filepattern: a string

    returns:
        A list of filenames

    """

    # If argument is not a string, or only contains white space, or an empty string
    if (type(filepattern) is not str) or (str(filepattern).isspace()) or (len(filepattern) == 0):
        print('A string is required as the argument.')
        exit(1)

    # Display the input argument
    print(f'... filepattern is {filepattern}')

    # Get the list of files
    files = os.listdir('./')

    newlist = []
    indt = str(filepattern).find('*')
    if indt == -1 or (filepattern[0] == '*' and filepattern[-1] == '*'):  # search everywhere
        # Remove * from the filepattern
        if filepattern[0] == '*' and filepattern[-1] == '*':  # search everywhere
            filepattern = filepattern[1:-1]  # remove both the first and the last character

        for item in files:
            if str(item).find(filepattern) > -1:
                newlist.append(item)

    elif filepattern[-1] == '*':  # filename starts with the pattern
        filepattern = filepattern[0:-1]  # remove the last character
        for item in files:
            if str(item).find(filepattern) == 0:
                newlist.append(item)

    elif filepattern[0] == '*':  # filename ends with the pattern
        filepattern = filepattern[1:]  # remove the last character
        for item in files:
            if (str(item).find(filepattern) > -1) and (str(item).find(filepattern) == len(item)-len(filepattern)):
                newlist.append(item)
    newlist.sort()

    return newlist


if __name__ == '__main__':
    os.chdir('data')
    a = get_files_having_pattern('*dmBIN01.mrc')
    for item in a:
        print(item)
    print('-----------')
