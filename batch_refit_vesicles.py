#!/usr/bin/env python3
# This is used to test the command line input

import getopt
from batch_refit_subtract_new_withPOPC_in_folder_parfor_2019 \
    import batch_refit_subtract_new_withPOPC_in_folder_parfor_2019


def main(argv):
    """
    This is the wrapper to run batch_refit_subtract_new_withPOPC_in_folder_parfor_2018Aug.
    The input parameters are : file_pattern, pixelsize, model_type,
            ves_filename_after_base, ctf_filename_after_base, scaling_of_mp_if_skip_refit_xy = 0,
            flag_mask_part_for_ves_fit = 0, flag_display_image = 0, star_filename_after_base = None
    """

    msg_usage = 'batch_refit_vesicles.py ' \
                '-f <file_pattern> ' \
                '-p <pixelsize>  ' \
                '-m <model_type>  ' \
                '-v <ves_filename_after_base>  ' \
                '-c <ctf_filename_after_base>  ' \
                '[-s <scaling_of_mp_if_skip_refit_xy>  ' \
                '-a <flag_mask_part_for_ves_fit 1/0>  ' \
                '-d <flag_display_image 1/0>  ' \
                '-r <star_filename_after_base>]'

    print('------------------------')
    print(f"Original command: {argv}")
    print('------------------------')

    # If no name is given, exit.
    if len(argv) < 6:
        print('Not enough parameters.')
        print(msg_usage)
        sys.exit(2)

    argv = argv[1:]

    try:
        opts, args = getopt.getopt(argv, "f:p:m:v:c:s:a:d:r:", [
            "file_pattern=",
            "pixelsize=",
            "model_type=",
            "ves_filename_after_base=",
            "ctf_filename_after_base=",
            "scaling_of_mp_if_skip_refit_xy=",
            "flag_mask_part_for_ves_fit=",
            "flag_display_image=",
            "star_filename_after_base="])
    except getopt.GetoptError:
        print('Wrong input parameters.')
        print(msg_usage)
        sys.exit(2)

    # print(f'opts: {opts}')
    # print(f"args: {args}")

    # Set default value of optional variables
    scaling_of_mp_if_skip_refit_xy = 0
    flag_mask_part_for_ves_fit = 0
    flag_display_image = 0
    star_filename_after_base = None

    # extract from opts
    for opt, arg in opts:
        if opt == '-h':
            print(msg_usage)
            sys.exit()
        elif opt in ("-f", "--file_pattern"):
            file_pattern = arg
        elif opt in ("-p", "--pixelsize"):
            pixelsize = float(arg)
        elif opt in ("-m", "--model_type"):
            model_type = int(arg)
        elif opt in ("-v", "--ves_filename_after_base"):
            ves_filename_after_base = arg
        elif opt in ("-c", "--ctf_filename_after_base"):
            ctf_filename_after_base = arg
        elif opt in ("-s", "--scaling_of_mp_if_skip_refit_xy"):
            scaling_of_mp_if_skip_refit_xy = float(arg)
        elif opt in ("-a", "--flag_mask_part_for_ves_fit"):
            flag_mask_part_for_ves_fit = int(arg)
        elif opt in ("-d", "--flag_display_image"):
            flag_display_image = int(arg)
        elif opt in ("-r", "--star_filename_after_base"):
            star_filename_after_base = arg

    # run the program
    batch_refit_subtract_new_withPOPC_in_folder_parfor_2019(
        file_pattern, pixelsize, model_type,
        ves_filename_after_base, ctf_filename_after_base,
        scaling_of_mp_if_skip_refit_xy,
        flag_mask_part_for_ves_fit, flag_display_image,
        star_filename_after_base)


if __name__ == "__main__":
    import sys
    try:
        if sys.stdin.isatty():  # In a terminal
            # print('This is running in a terminal.')
            # print(f'{repr(sys.argv)}')
            main(sys.argv)
        else:
            print('This is running in Pycharm.')
    except AttributeError:  # stdin is NoneType if not in terminal mode
        print('The program has some errors.')
        pass
