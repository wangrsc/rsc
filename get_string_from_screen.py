#!/usr/bin/env python3


def get_string_from_screen(display_message, default_value=None):
    """
    This is used to get a string from the command line.

    args:
        display_message: a string for prompt
        default_value: a string

    returns:
        A string
    """
    # Construct the prompt message
    if default_value is not None:
        display_message = display_message + ' [' + default_value + ']: '
    else:
        default_value = True
        display_message = display_message + ': '

    # Loop to get valid input
    flag_get_input = True
    while flag_get_input:
        choice = input(display_message)  # Get input (only the first character

        if len(choice) == 0:  # No input is given, so default value is used and finish
            if default_value is not None:
                out = default_value
                flag_get_input = False
        else:
            out = choice
            flag_get_input = False

    return out


if __name__ == '__main__':
    a = get_string_from_screen('Imput a string')
    print(a)
    a = get_string_from_screen('Imput a string', 'Default')
    print(a)
