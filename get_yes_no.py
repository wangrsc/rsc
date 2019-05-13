#!/usr/bin/env python3


def get_yes_no(display_message, default_value=0):
    """
    This is used to get input from the command line.

    args:
        display_message: a string for prompt
        Default value: an integer: 0: no, non-zero: y

    returns:
        Output: True or False
    """

    switcher = {'Y': True, 'y': True, '1': True, 'N': False, 'n': False, '0': False}

    # Construct the prompt message
    if default_value == 0:
        default_value = False
        display_message = display_message + ' (Y/y/1/N/n/0)' + ' [' + 'N' + ']: '
    else:
        default_value = True
        display_message = display_message + ' (Y/y/1/N/n/0)' + ' [' + 'Y' + ']: '

    # Loop to get valid input
    flag_get_input = True
    while flag_get_input:
        choice = input(display_message)   # Get input (only the first character

        if len(choice) == 0:   # No input is given, so default value is used and finish
            out = default_value
            flag_get_input = False
        else:
            if switcher.get(choice[0]) is None:
                flag_get_input = True
            else:
                out = switcher.get((choice[0]))
                flag_get_input = False

    return out


if __name__ == '__main__':
    a = get_yes_no('Choose selection', 0)
    print(a)
