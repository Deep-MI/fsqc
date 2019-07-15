 # -*- coding: utf-8 -*-
"""
Created on Wed May 15 15:06:56 2019
@author:Tobias Wolff

This function looks out for the mean values of the segmentations in a passed file. 
This file must be located in the subjects directory. 
Required Arguments:
    - At least one segmentation
    - The path to the mean_file
Return Value:
    - The mean values extracted extracted either from the defaultAsegMeans.txt file,
    or from the user specified file in a list
"""

def read_parc_mean_from_table(segmentations, look_up_mean_file):
    #segmentation: List with the segmentation,
    means_from_file = []
    try:
        with open(look_up_mean_file) as f:
            lines_aseg_means_file = f.read().splitlines()
    except IOError:
        print('Impossible to open the Look up means file, please verify path or existence')
        exit()
        
    #Loop through all the segmentations, that were passed in the arguments
    for segmentation in segmentations:
        #Loop through the whole aseg.means file to see whether the requested segmentation is present or not     
        for line_aseg_means_file in lines_aseg_means_file:
            if segmentation in line_aseg_means_file:
                #Get the value of the Look_up_means file of the form: -- +/- ..
                means_from_file.append(line_aseg_means_file.split()[1:4])

    #When no match is found, then just return a ".". This is treated in the recon_all_aseg_outlier_checker as a case, that is not found. 
    if(len(means_from_file) == 0): 
        return ['.', '+/-', '.']           
        
    return [means_from_file[0][0], '+/-', means_from_file[0][2]] 
