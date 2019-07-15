# -*- coding: utf-8 -*-
"""
Created on Thu May 16 12:30:12 2019

@author: Tobias Wolff
This function returns the relativ value of the volume of one subject of one segmentation. 
The function could return more values, but it is called within a loop, that treats all subjects and all segmentations. 

Required arguments:
    - Subjects directory
    - The subject
    - Segmentation
"""
def g_parc_val_norm(subjects_dir, subjects, segmentations):
    #Subjects: subjects ID
    #Statsfilepath aseg.stats Volumetric group analysis
    #segmentation: Subcortical Segmentation: Segsfile2 List of all possible  segmentations
    segmentation_vol = []
    Vol_norm = []
    inter_cranial_volume = 0
    
    for subject in subjects:
        path_stats_file = str(subjects_dir) + str(subject) + "/stats/aseg.stats"
        
        #Open the specific aseg.stats file of one subject. This is implemented for the usual directory convention of freesurfer. Very important, that this is kept. 
        try:
            with open(path_stats_file) as stats_file:
                aseg_stat = stats_file.read().splitlines()
        except FileNotFoundError:
            print("The path in the g_parc_val_norm function ", path_stats_file, "does not have an appropriate file")
            exit()
        
        # Then, get the volume values of the required segmentations and norm them. 
        # Highly important that the aseg.stat file first gives the information about the inter_cranial volume and then the information about the 
        for segmentation in segmentations:
            for aseg_stat_line in aseg_stat:
                if segmentation in aseg_stat_line:
                    segmentation_vol.append([segmentation, (float(aseg_stat_line.split()[3])/float(inter_cranial_volume))*100])
                if 'EstimatedTotalIntraCranialVol' in aseg_stat_line:
                     inter_cranial_volume = aseg_stat_line.split(',')[3]

    # Get only the volumes, and do not care anymore of their name. 
    for each_vol in range(len(segmentation_vol)):
         Vol_norm.append([segmentation_vol[each_vol][0], segmentation_vol[each_vol][1]])

    return [i[1] for i in Vol_norm]
