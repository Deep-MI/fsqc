# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 10:02:16 2019

@author: Tobias Wolff

This function evaluates the relative size of the Corpus Callosum in order to 
detect possible outliers. It computes the sum of the volumes of the Corpus 
Callosum as precised in the aseg.stats file. 

Required Arguments: 
    - subjects_dir
    - subject
"""

def cc_size_checker(subjects_dir, subject):

    import os

    path_stats_file = os.path.join(subjects_dir,subject,"stats","aseg.stats")

    with open(path_stats_file) as stats_file:
        aseg_stats = stats_file.read().splitlines()

    cc_elements = ['CC_Posterior', 'CC_Mid_Posterior', 'CC_Central', 'CC_Mid_Anterior', 'CC_Anterior']
    
    sum_cc = 0
    
    # Loop through the cc elements
    for cc_segmentation in cc_elements:
        # Look for the element in the aseg.stats line
        for aseg_stat_line in aseg_stats:
            # If the segmentation is found, compute the sum and return it. 
            if cc_segmentation in aseg_stat_line:
                sum_cc += float(aseg_stat_line.split()[3])
            elif 'EstimatedTotalIntraCranialVol' in aseg_stat_line:
                inter_cranial_volume= float(aseg_stat_line.split(',')[3])    

    relative_cc = sum_cc/inter_cranial_volume

    return relative_cc
