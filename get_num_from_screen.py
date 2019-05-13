#!/usr/bin/env python3


def get_num_from_screen(display_message, default_value=0, val_min=None, val_max=None):
    """
    This program get numeric input from command line within the range if it is set.

    args:
        display_message is required.
        default_value: numeric
        val_min and val_max: range of selection [val_min val_max]

    returns:
        A number within range if val_min and val_max are set.

    """
    # Construct the prompt message
    if val_max is not None:
        display_message = display_message + ' (' + str(val_min) + '~' + str(val_max) + ')'

    display_message = display_message + ' [' + str(default_value) + ']: '
    
    # Loop to get valid input
    flag_get_input = True    
    while flag_get_input:
        choice = input(display_message)  # Get input

        if len(choice) == 0:  # No input is given, so default value is used and finish
            out = default_value
            flag_get_input = False

        if choice.isdigit():  # Input is numeric
            out = float(choice)
            flag_get_input = False

            # If range is set, check it. Otherwise finish
            if (val_max is not None) and (val_min is not None):  # Range is set for input
                if out < val_min or out > val_max:  # Input is out of range
                    flag_get_input = True

    return out


if __name__ == '__main__':
    a = get_num_from_screen('Input a number', 0, 0, 15)
    print(a)
