# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 15:21:35 2019

@author: Tobias Wolff
This simple script writes the information that were assembled during the quality checker function to the a csv file. 
The function recon_all_aseg_outlier adds afterwards information to the csv file. 
Because the recon_all_aseg_outlier function needs all the subjects to run, it was easier to add the information in its function. 
Required arguments: 
    - path_data_file 
    - List of WM SNR values based on the norm image
    - List of GM SNR values based on the norm image
    - List of WM SNR values based on the orig image
    - List of GM SNR values based on the orig image
    - List of the relative Corpus Callosum size
    - List ot the number of holes for the left and right hemisphere
    - List of the topological fixing time for the Left and the right hemisphere
    - List of the contrast to noise ratio for all the subjects 
"""
import csv

def write_information_to_file(path_data_file, metrics):
    with open(path_data_file,'r') as csvinput:
        reader= csv.reader(csvinput)
        reader = list(reader)
        for index, row in enumerate(reader[1:]):
            row.append(metrics.all_wm_snr_norm[index])
            row.append(metrics.all_gm_snr_norm[index])
            row.append(metrics.all_wm_snr_orig[index])
            row.append(metrics.all_gm_snr_orig[index])
            row.append(metrics.cc_items[index])

            if metrics.cc_items[index] < 0.001:
                row.append("YES")
            else:
                row.append("NO")
            row.append(metrics.all_lh_holes[index])
            row.append(metrics.all_rh_holes[index])
            row.append(metrics.all_lh_defects[index])
            row.append(metrics.all_rh_defects[index])
            row.append(metrics.all_topo_lh[index])
            row.append(metrics.all_topo_rh[index])
            row.append(metrics.all_con_lh_snr[index])
            row.append(metrics.all_con_rh_snr[index])
    with open(path_data_file,'w') as csvoutput:
        writer = csv.writer(csvoutput)
        writer.writerows(reader)
        
