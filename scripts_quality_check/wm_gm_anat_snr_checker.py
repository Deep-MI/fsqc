# -*- coding: utf-8 -*-
"""
Created on Mon May 27 15:39:13 2019
@author: Tobias Wolff

WM GM ANAT checker

This function checks the SNR of the white and the gray matter. The white matter segmentation is taken 
out from the aparc+aseg image and the gray matter from the aseg image. The big white matter is eroded with 3
neighbours in order to ignore partial volumes. For the gray matter this is not possible, because the layer 
is aready very thin. An erosion would eliminate nearly the whole signal. 

Arguments(required):
    - Path to the subjects directory 
    - The subject that should be treated
Arguments(optional):
    - The number of erosions, default = 3
    When reducing the number of erosions the SNR should become worse, because more partial volume are taken 
    into account
    - One can change the reference image. The default image on which the SNR is computed is the norm.mgz image. 
    When passing a "2" for the option_base argument, the image will be the original one
    
"""

import numpy as np
import nibabel as nib
from skimage.morphology import binary_erosion

def wm_gm_anat_snr_checker(subjects_dir, subject, nb_erode = 3, option_base = 1):
    
    print("The number of erosions for the white matter SNR is: ", int(nb_erode) )
        
    #Get the path to the different files: 
    path_aparc_aseg  = str(subjects_dir) + str(subject) + "/mri/aparc+aseg.mgz"
    path_aseg = str(subjects_dir) + "/" + str(subject) + "/mri/aseg.mgz"
    
    #Choice on which image base the SNR should be computed
    if(option_base == 1):
        path_reference_image = str(subjects_dir) + str(subject) + "/mri/norm.mgz"
        print("The SNR is computed on the base of the norm.mgz image")

    elif(option_base == 2):
        path_reference_image = str(subjects_dir) + str(subject) + "/mri/orig.mgz"
        print("The SNR is computed on the base of the orig.mgz image")
            
    #Reading the aparc+aseg image to locate gray and white matter    
    inseg = nib.load(path_aparc_aseg)
    data_aparc_aseg = inseg.get_fdata()    

    #Reading the image to identify the itensities of the white and gray matter at the different locations. 
    #If the option_base is set to two, the variable norm will be the original image. 
    norm = nib.load(path_reference_image)
    norm_data = norm.get_fdata()    

    #Create 3D binary data where the white matter locations are encoded with 1, all the others with zero
    b_wm_data = np.zeros((256,256,256))
    
    #The following keys represent the white matter labels in the aparc+aseg image
    wm_labels = [2, 41, 7, 46, 251, 252, 253, 254, 255, 77, 78, 79]
    
    #Find the wm labels in the aparc+aseg image and set the locations in the binary image to one 
    for i in wm_labels:
        x, y, z = np.where(data_aparc_aseg == i)      
        b_wm_data[x,y,z] = 1 
        
    nb_erode = int(nb_erode) + 4
    b_wm_data = binary_erosion(b_wm_data,np.ones((nb_erode, nb_erode,nb_erode)))
    signal = []
    
    #Computation of the SNR
    x, y, z = np.where(b_wm_data == 1)
    signal.append(norm_data[x,y,z])
    signal_mean = np.mean(signal)
    signal_std = np.std(signal)
    wm_snr = signal_mean/signal_std
    print("The signal to noise ratio of the white matter is", wm_snr) 


    #Computation of the SNR of the gray matter:
    #No erosion for the gray matter possible, beacause the signal is low.
    aseg = nib.load(path_aseg)
    data_aseg = aseg.get_fdata()
    
    #Create binary data where the gray matter locations are encoded with 1, all the others with zero
    b_gm_data = np.zeros((256,256,256))
    
    #The following keys represent the gray matter labels in the aseg image    
    gm_labels = [ 3, 42 ]
    
    for i in gm_labels:
        x, y, z = np.where(data_aseg == i)
        b_gm_data[x, y, z] = 1
    
    # Computation of the SNR 
    signal_gm =[]
    x, y, z = np.where(b_gm_data == 1)
    signal_gm.extend(norm_data[x,y,z])
    signal_gm_mean = np.mean(signal_gm)
    signal_gm_std = np.std(signal_gm)
    gm_snr =signal_gm_mean/signal_gm_std
    print ("The signal to noise ratio of the gray matter is:", gm_snr)        
    return wm_snr, gm_snr






































'''    
    n=256
    bdata=[[[0 for k in range(n)] for j in range(n)] for l in range(n)]
    histogram = [0]*2300
    histogramb = [0]*2300
    for i in range(256):
        print("I am in the outer loop for the first calculation, nb loob:", i)
        for j in range(256):
            for l in range(256):
                histogram[int(data[i,j,l])] += 1
                if int(data[i, j, l]) == 2:
                    bdata[i][j][l] = 1
                elif int(data[i, j, l]) == 41:
                    bdata[i][j][l] = 1
                elif int(data[i, j, l]) == 7:
                    bdata[i][j][l] = 1
                elif int(data[i, j, l]) == 46:
                    bdata[i][j][l] = 1
                elif int(data[i, j, l]) == 251:
                    bdata[i][j][l] = 1
                elif int(data[i, j, l]) == 252:
                    bdata[i][j][l] = 1
                elif int(data[i, j, l]) == 253:
                    bdata[i][j][l] = 1
                elif int(data[i, j, l]) == 254:
                    bdata[i][j][l] = 1
                elif int(data[i, j, l]) == 255:
                    bdata[i][j][l] = 1
                elif int(data[i, j, l]) == 77:
                    bdata[i][j][l] = 1
                elif int(data[i, j, l]) == 78:
                    bdata[i][j][l] = 1
                elif int(data[i, j, l]) == 79:
                    bdata[i][j][l] = 1
    for i in range(256):
        for j in range(256):
            for l in range(256):
                histogramb[int(bdata[i][j][l])] += 1

'''            


'''
def parse_arguments():
    
    parser= argparse.ArgumentParser(description = 'Parsing the arguments to the WM GM ANAT SNR checker')
    parser.add_argument('--s', dest = 'subject')
    parser.add_argument('--o', dest = 'datfile')
    parser.add_argument('--nerode', dest = 'nb_erode', default = 3)
    parser.add_argument('--tmp', 'tmpdir', dest = tmp_dir)
    parser.add_argument('--no-cleanup', dest = no_clean_up)
    parser.add_argument('--clean_up', dest = clean_up)
    parser.add_argument('--force', dest = force)
    args = parser.parse_args()
    print(args.accumulate(args.integers))    
    
    
    
if __name__== "__main__":
    arguments = parse_arguments()'''
    