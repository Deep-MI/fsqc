# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 12:56:45 2019

@author: wolfft


Histogram CC oasis subject
"""

import os
import numpy as np
import matplotlib.pyplot as plt


absolute_cc_values = []
icv_values = [] 
cc_elements = ['CC_Posterior', 'CC_Mid_Posterior', 'CC_Central', 'CC_Mid_Anterior', 'CC_Anterior']


def get_cc_size(subjects_dir):
    relative_cc =[]
    absolute_cc = []
    relative_cc_index = []
    
    for index, subject in enumerate(os.listdir(subjects_dir)):
        path_aseg_stat  = str(subjects_dir) + str(subject) + "/stats/aseg.stats"   
        if not os.path.isfile(path_aseg_stat):
            continue
        with open(path_aseg_stat) as stats_file:
            aseg_stats = stats_file.read().splitlines()

        sum_cc = 0;   
        for cc_segmentation in cc_elements:
            for aseg_stat_line in aseg_stats:
                if cc_segmentation in aseg_stat_line:
                    sum_cc += float(aseg_stat_line.split()[3])
                elif 'EstimatedTotalIntraCranialVol' in aseg_stat_line:
                    inter_cranial_volume= float(aseg_stat_line.split(',')[3])    
        relative_cc.extend([sum_cc/inter_cranial_volume])
        print("The index", index, "corresponds to subject", subject, "with a relative CC size of:", sum_cc/inter_cranial_volume)
        absolute_cc.extend([sum_cc])
        relative_cc_index.extend([index])
    return absolute_cc, relative_cc, relative_cc_index             

subjects_dir = "/groups/ag-reuter/datasets/oasis1/fs60/"

[absolute_cc_values, relative_cc_values, indices ]= get_cc_size(subjects_dir)
relative_cc_values = np.array(relative_cc_values)
absolute_cc_values = np.array(absolute_cc_values)

potential_outliers_abs = np.where(absolute_cc_values > 5000)
print("The indices of the potential outliers  in the absolute volumes are:", potential_outliers_abs)
plt.hist(absolute_cc_values, bins='auto')
plt.title("Absolute CC Histogram")
plt.show()


potential_outliers_rel = np.where(relative_cc_values > 0.0025)
print("The indices of the potential outliers  in the relative volumes are:", potential_outliers_rel)
plt.hist(relative_cc_values, bins='auto')
plt.title("Relative CC Histogram")
plt.show()

