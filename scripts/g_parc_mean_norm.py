 # -*- coding: utf-8 -*-
"""
Created on Wed May 15 17:00:06 2019

@author:Tobias Wolff
This function takes some subjets and segmentations as input and computes the mean and the standart deviation of all the segementations.
Required arguments:
    - Subjects directory
    - Subjects
    - Segmentations

"""

from statistics import mean, stdev

def g_parc_mean_norm(subjects_dir, subjects, segmentations):
    region_vol = []
    Vol_elements= []
    aseg_stat= []
    Mean_volume = 0
    Std_volume = 0
    inter_cranial_volume = 0
    for subject in subjects:
        
        #Get the individual path to the aseg.stat file and open it 
        path_stats_file = str(subjects_dir) + str(subject) + "/stats/aseg.stats"
        try:
            with open(path_stats_file) as stats_file:
                aseg_stat = stats_file.read().splitlines()
        except FileNotFoundError:
            print("The path", path_stats_file, "does have not an appropriate file. I am in the g_parc mean norm function")
        
        
        for segmentation in segmentations:            
            for aseg_stat_line in aseg_stat:
                # If the name of the segmentation is present in the aseg.stat file, then grep its volume value.
                # In the next step, norm the value with the total intercranial volume. 
                if segmentation in aseg_stat_line:
                    region_vol.append([segmentation, (float(aseg_stat_line.split()[3])/float(inter_cranial_volume))*100])
                if 'EstimatedTotalIntraCranialVol' in aseg_stat_line:
                     inter_cranial_volume= aseg_stat_line.split(',')[3]
    
    # Get only the values of the normed volumes and do not care about their names                
    for i in range(len(region_vol)):
      Vol_elements.append(region_vol[i][1])
    
    # Calculate the mean and the standart deviation and return the value
    if len(Vol_elements)== 0:
        Mean_volume = "."
        Std_volume = "."
    elif len(Vol_elements) == 1:        
        Mean_volume = Vol_elements
        Std_volume = "."

    elif len(Vol_elements) > 1:
        Std_volume = stdev(Vol_elements)
        Mean_volume = mean(Vol_elements)
    else:
        Std_volume=0
        Mean_volume =0
    return  [Mean_volume , "+ / - ", Std_volume]
