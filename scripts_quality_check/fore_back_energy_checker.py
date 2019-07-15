# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 12:11:34 2019

@author: wolfft

Get the foreground to background energy ratio:
Calculate the variance based on the brainmask image and 
divide it to the variance deviation of all non brain area
Idea from: http://preprocessed-connectomes-project.org/quality-assessment-protocol/
Because the variance is not available, we took the mean value of the background and the mean value of the brainS


Future: Would be interesting to see, what happens if one took another voulume which only computes the energy ration with regard to the background 
"""
import nibabel as nib
import numpy as np
import os
#import matplotlib.pyplot as plt
import subprocess


def fore_back_energy_checker(subjects_dir, subject):
    
    # Get the paths to the images: 
    path_image = str(subjects_dir) +str(subject) + "/mri/T1.mgz"
    path_brainmask = str(subjects_dir) + str(subject) + "/mri/wm.seg.mgz"
    
    b_signal = [] # List of the brainmask intensity values        
    
    # Average background intensity: 
    output = subprocess.check_output(["mri_seghead", "--invol", path_image, "--thresh", "20"])
    mean_backg = float(output.splitlines()[15].decode("utf-8").split()[4])
    print ("The mean background intesnsity is:", mean_backg)
    #Load the image
    brainmask = nib.load(path_brainmask)

    #Get data
    brainmask = brainmask.get_fdata()
    b_signal.append(brainmask[np.where(brainmask != 0) ])

    #Compute the mean: 
    b_mean = np.mean(b_signal)
    b_std = np.std(b_signal)

    ratio = b_std/mean_backg
    
    print("The foreground/background energy ratio of subject", subject, " is:", ratio)    
    #Return this ratio
    return ratio


subjects_dir = "/home/wolfft/qatools/blurr+control/"

subjects = []     
    ####Only for developing     
for subject in os.listdir(subjects_dir):
    path_aseg_stat  = str(subjects_dir) + str(subject) + "/stats/aseg.stats"
    if not os.path.isfile(path_aseg_stat):
        continue
    else:
        subjects.extend([subject])
                
for subject in subjects:
    ratio = fore_back_energy_checker(subjects_dir, subject)
    #print("The energy ratio for the subject", subject, "is ", ratio)

    
    
    
    