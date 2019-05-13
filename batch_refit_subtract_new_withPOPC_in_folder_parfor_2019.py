#!/usr/bin/env python3

import numpy as np
import os
from import_rsc_functions import *
import matplotlib.pyplot as plt

# import time


class Struct(object):  # Used to create an empty structure/class
    pass


def batch_refit_subtract_new_withPOPC_in_folder_parfor_2019(
        file_pattern, pixelsize, model_type,
        ves_filename_after_base, ctf_filename_after_base, scaling_of_mp_if_skip_refit_xy=0,
        flag_mask_part_for_ves_fit=0, flag_display_image=0, star_filename_after_base=None):
    """
    This is used to resubtract vesicles using different models.
    CTF file must be image.mrc.ctf
    Vesicle file is  image.mrc.vestxt
    All files in the same folder!!

    This is 30% slower than the fitting using dumb membrane profile.
    When calling this function, all parameters need to be given. The default
    
    % scaling_of_mp_if_skip_refit_xy: if given, no refit of xy here. Just use
    % saved mp. The scaling can be less than 1 to leave some bilayer residue.
    % <=0: means refit!

    args:
        file_pattern: a string used to identify the image files 
        pixelsize: in unit of angstrom per pixel 
        model_type: an integer 
        ves_filename_after_base: a string used to construct vesicle info filename 
        ctf_filename_after_base: a string used to construct ctf filename 
        scaling_of_mp_if_skip_refit_xy: a scalar 
        flag_mask_part_for_ves_fit: don't subtract particle region. This is not implemented yet. 
        flag_printlay_image: a boolean  
        star_filename_after_base: used to read ctf from Relion files
         
    returns:
        a vesicle subtracted file is generated.
        a vesicle information file is generated.
    
    To dos:
        Use different ctf from Relion star file for different vesicles. 
    """

    # print('Current folder is ' + os.getcwd())

    # Check whether use Relion star files for local CTF
    if star_filename_after_base is None:
        flag_use_local_ctf_from_particle_star_file = 0
    else:
        flag_use_local_ctf_from_particle_star_file = 1

    # Check whether skip fitting but scale the saved amplitudes
    if scaling_of_mp_if_skip_refit_xy > 0:
        flag_skip_refit_xy = 1
    else:
        flag_skip_refit_xy = 0

    # get a list of image file names in current folder
    files = get_files_having_pattern(file_pattern)
    print('CTF file pattern is: ' + ctf_filename_after_base)
    print('CTF file pattern is: ' + ves_filename_after_base)

    # get_base_filename needs to be implemented
    print('... get file basename...')
    n_to_delete_from_end_tobasename = get_base_filename(files[0], 11)

    # To generate the mask for blank strips due to padding of images.
    flag_mask_edge = get_yes_no('Are there blank edges in the image (e.g. K2 image)?', 1)
    if flag_mask_edge:
        im, __, __, __ = read_mrc(files[0])
        nx, ny = np.shape(im)
        print(f'Current image size is {nx} x {ny}.')
        print("If there are two strips from the padding of images, we can correct it here.")
        nx0 = get_num_from_screen("What is the image size in X before padding?", 3710)
        ny0 = get_num_from_screen("What is the image size in Y before padding?", 3838)

        # The blank strips will be set to zero while image region is set to 1.
        mask_k2_edge_setto_0 = pad_pic(np.ones([nx0, ny0]), nx, ny, 0)

    # Loop over each image
    for i in range(len(files)):
        print('----------------------------------------')
        print(f'........ ii= {i} ............')

        # ===================================================
        # Read image, ctf, and vesicle information
        infilename = files[i]
        ves_file = infilename[0: -n_to_delete_from_end_tobasename] + ves_filename_after_base
        ctf_file = infilename[0: -n_to_delete_from_end_tobasename] + ctf_filename_after_base
        
        print(f'CTF file is {ctf_file}')
        print(f'vesicle file is {ves_file}')
        
        # check ctf and vesicle files
        if not os.path.isfile(ctf_file):
            print(f'*** ctf file does not exist: {ctf_file}')
            continue
        if not os.path.isfile(ves_file):
            print(f'*** ctf file does not exist: {ves_file}')
            continue

        print('*** Reading image file ', infilename)
        im, __, __, __ = read_mrc(infilename)
        im0 = np.copy(im)
            
        print(f'*** Reading CTF file {ctf_file}')
        info_ctf = ctf(ctf_file, simple_format=1)

        ## To dos
        # use gCTF fitted local CTF for each particle in Relion star file format
        if flag_use_local_ctf_from_particle_star_file:
            print('Not implemented yet!')
            # star_file=[infilename(1:end-n_to_delete_from_end_tobasename) star_filename_after_base]
            # It includes the CTF parameters
            # info_ctf.flag_use_local_ctf_from_particle_star_file = 1
            # info_ctf.star_file = star_file

        print(f'*** Reading vesicle info: {ves_file}')
        mx1d, my1d, mr1d, mp1d, __ =  read_box_e_m(ves_file)

        # ===================================================
        # The following was used to delete fake vesicles at the end of each file.
        # flag_ves is boolean
        flag_ves = mr1d < 20
        flag_mp = mp1d < 1e-8
        flag_ves = (flag_ves + flag_mp) > 0
        for ih in range(len(mx1d)):
            if flag_ves[ih]:
                print(f'... Deleting vesicle at ({mx1d[ih]},{my1d[ih]}) with a radius of {mr1d[ih]}')

        # To remove vesicles having inf or nan information
        flag_ves_inf_nan = np.isnan(mx1d) + np.isinf(mx1d) \
                           + np. isnan(my1d) + np.isinf(my1d) \
                           + np.isnan(mr1d) + np.isinf(mr1d) \
                           + np. isnan(mp1d) + np.isinf(mp1d)
        flag_ves = (flag_ves + flag_ves_inf_nan) > 0

        # Remove bad vesicles
        mx1d = remove_array_elements(mx1d, flag_ves)
        my1d = remove_array_elements(my1d, flag_ves)
        mr1d = remove_array_elements(mr1d, flag_ves)
        mp1d = remove_array_elements(mp1d, flag_ves)

        # To dos
        """
        # Generate a mask for the image based on picked particles, so the bias on
        # the amplitude of the to-be-subtracted vesicle model is eliminated.
        # Method 1: put a circular mask around each particles
        if(flag_mask_part_for_ves_fit)
            [img_size_x, img_size_y]=size(im)
            part_file=[infilename,'.matbox'
            f_part=fopen(part_file)
            if(~(f_part>0))
                print(' Particle file ',part_file,' does NOT exist. No mask is used.')
                im_mask=ones(img_size_x,img_size_y)
            else
                im_mask=zeros(img_size_x,img_size_y)
                %                 [px py pwx pwy]=read_box_E_M(part_file)
                [px, py]=read_box_E_M(part_file)
                n_part=numel(px)
                for jj=1:n_part
                    ax=px(jj)
                    ay=py(jj)
                    ar=round(80/pixelsize) % Assume particles are within a circle of 160A in diameter.
                    im_mask=im_mask+disc(img_size_x,ar,[ax,ay])
                end
                im_mask=im_mask<1% masked aera is 0 and outside is 1 to keep
            end
            if(flag_mask_edge)
                im_mask=im_mask .* mask_k2_edge_setto_0
            end
        """

        if flag_mask_edge:
            im_mask= np.copy(mask_k2_edge_setto_0)

        # =========================================
        # If skip fitting, mr1d contains mp1d and mr1d
        mr1d_in = Struct
        if flag_skip_refit_xy: # use saved mp
            mr1d_in.mr1d = mr1d
            mr1d_in.mp1d = mp1d * scaling_of_mp_if_skip_refit_xy
            del mr1d
            mr1d = mr1d_in
            del mr1d_in

        # to dos
        """
        if flag_mask_part_for_ves_fit:
            [im, mxnew, mynew, mrnew, mpnew]=subtract_vesicles_POPC_ect_2019(im,mx1d,my1d,mr1d,mp1d,pixelsize,info_ctf,model_type,im_mask)
        else:
            [im, mxnew, mynew, mrnew, mpnew]=subtract_vesicles_POPC_ect_2019(im,mx1d,my1d,mr1d,mp1d,pixelsize,info_ctf,model_type)
        """
        # This should be deleted as it is for testing the program
        im = np.copy(im0)
        mxnew = mx1d
        mynew = my1d
        mrnew = mr1d
        mpnew = mp1d

        file_out = infilename[0: -4] + '_ves' + num2strn(model_type,2) + '.mrc'

        write_mrc(im, pixelsize, file_out, 2)
        print(f'Subtracted image was saved to {file_out}')

        if not flag_skip_refit_xy:  # vesicle informaiton is fitted
            pickname = infilename[0: -4] + '_resub' + num2strn(model_type,2) + '.txt'
            write_ves_file(pickname, mxnew, mynew, mrnew, mpnew)
            print(f'Vesicle info are saved to {pickname}')


        if flag_display_image:
            plt.subplot(1,2,1)

            radius_decrease = np.round(nx/100)
            im0 = gauss_filt(im0, 0.15)
            tt1 = add_circle(scale_image(im0), mxnew, mynew, mrnew/pixelsize-radius_decrease, 259, 10, 0, 0)
            imcolor(tt1)
            plt.title('Original')
            plt.axis('image')

            plt.subplot(1,2,2)
            im = gauss_filt(im, 0.15)
            tt1 = add_circle(scale_image(im), mxnew, mynew, mrnew/pixelsize-radius_decrease, 259, 10, 0, 0)
            imcolor(tt1)
            plt.title('Vesicle subtracted')
            plt.axis('image')

            plt.savefig(infilename[0: -4] + ".ps")
            plt.show()
            # plt.close()

if __name__ == "__main__":
    import os
    os.chdir('data')
    f1 = '*dmBIN01.mrc'
    batch_refit_subtract_new_withPOPC_in_folder_parfor_2019(
        f1, 1.056, 44, 'dmBIN01.mrc_resub44_screen.txt', 'dmBIN01.mrc.ctf', 0, 0, 1 )
