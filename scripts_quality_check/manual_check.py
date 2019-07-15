# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 15:01:53 2019

@author: Tobias Wolff
This function is the final check so that the viewer can see what image he has 
to look at again: 
"""
import csv
import numpy as np

def manual_check(path_check_file, subjects, metrics):
   
    # Initialize the new check file: 
    with open(path_check_file, "w") as csvoutput: 
        writer = csv.writer(csvoutput)
        writer.writerow(["Subject", "Decisive paramenter for the manuel check", "Value of this parameter"])
       
    #Compute mean number of holes: 
    all_lh_holes = [float(i) for i in metrics.all_lh_holes]
    all_rh_holes = [float(i) for i in metrics.all_rh_holes]
    all_lh_holes = np.array(all_lh_holes)
    all_rh_holes = np.array(all_rh_holes)
    all_holes = np.array([all_lh_holes, all_rh_holes])
    all_holes = np.average(all_holes, axis=0)
    
    all_lh_defects = [float(i) for i in metrics.all_lh_defects]
    all_rh_defects = [float(i) for i in metrics.all_rh_defects]
    all_lh_defects = np.array(all_lh_defects)
    all_rh_defects = np.array(all_rh_defects)
    all_defects = np.array([all_lh_defects, all_rh_defects])
    all_defects = np.average(all_defects, axis=0)
    
    all_con_lh_snr = [float(i) for i in metrics.all_con_lh_snr]
    all_con_rh_snr = [float(i) for i in metrics.all_con_rh_snr]
    all_con_lh_snr = np.array(all_con_lh_snr)
    all_con_rh_snr = np.array(all_con_rh_snr )
    all_con_snr = np.array([all_con_lh_snr, all_con_rh_snr ])
    all_con_snr = np.average(all_con_snr, axis=0)
    
    all_wm_snr_norm = [float(i) for i in metrics.all_wm_snr_norm]
    
    subjects_bad = [] 
    for index, subject in enumerate(subjects):
        if all_defects[index] > 135:   ####Do not change
            subjects_bad.append(subject)
            print("The subject ", subject, "has", all_defects[index], "defects. This are too many defects. FAIL")
            with open(path_check_file, "a") as csvoutput: 
                writer = csv.writer(csvoutput)
                writer.writerow([subject,"Defects", all_defects[index]]) 
                
        elif all_holes[index] > 120 and subject not in subjects_bad: # Do not change this value anymore
            subjects_bad.append(subject)
            print("The subject ",  subject, "has", all_holes[index], "holes. This are too many holes.FAIL")
            with open(path_check_file, "a") as csvoutput: 
                writer = csv.writer(csvoutput)
                writer.writerow([subject, "Holes", all_holes[index]]) 
                
        elif all_defects[index] > 100 and all_con_snr[index] < 2.65 and subject not in subjects_bad: 
            subjects_bad.append(subject)
            print("The subject ", subject, "has",all_defects[index]," defects and a contrast to noise ratio of", all_con_snr[index], ".FAIL")
            with open(path_check_file, "a") as csvoutput: 
                writer = csv.writer(csvoutput)
                writer.writerow([subject, "Defects and Contrast", [all_defects[index], all_con_snr[index]]]) 
                
        elif all_defects[index] > 110 and all_wm_snr_norm[index] < 6 and subject not in subjects_bad: 
            subjects_bad.append(subject)
            print("The subject ", subject, "has",all_defects[index]," defects and a signal to noise ratio of the wm of", all_wm_snr_norm[index], ".FAIL")
            with open(path_check_file, "a") as csvoutput: 
                writer = csv.writer(csvoutput)
                writer.writerow([subject, all_defects[index], "Defects and WM SNR", [all_defects[index], all_wm_snr_norm[index]]])
    print("The total number of detected subjects is", len(subjects_bad))