# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 10:40:28 2019

@author: wolfft
"""
import os 
import csv

def defects_checker(subjects_dir, subject):
    lh_defects = 0
    rh_defects = 0
    path_log_file = str(subjects_dir) + str(subject) + "/scripts/recon-all.log"
    try:
        with open(path_log_file, 'r') as logfile:
         lines_log_file = logfile.read().splitlines()
    except FileNotFoundError:
            print("The path in the holes_topo_checker function", path_log_file, "does not have an appropriate file")
            exit()
    lh = 1        
    for line_log_file in lines_log_file:

        #Look for the number of holes in the left and right hemisphere
        if "defects found" in line_log_file and lh == 1 :
            lh_defects = line_log_file.split()[0]
            lh_defects = int(lh_defects)
            lh = 0
        elif "defects found" in line_log_file and lh == 0 :
            rh_defects = line_log_file.split()[0]
            rh_defects = int(rh_defects)
    print("For subject", subject, "the holes in the left hemisphere are:", lh_defects, "and the holes in the right hemisphere are", rh_defects)
            
    return lh_defects, rh_defects
    
subjects_dir = "/groups/ag-reuter/datasets/adni/ADNI-3T-FS-5.3-Good/"
path_data_file = "/home/wolfft/qatools/adni-results/defects.csv"
with open(path_data_file,'w') as csvoutput:
    writer = csv.writer(csvoutput)
    writer.writerow(["Subject", "lh_defects", "rh_defects"])

subjects = []
for subject in os.listdir(subjects_dir):
    path_aseg_stat  = str(subjects_dir) + str(subject) + "/stats/aseg.stats"
    print("Checking paths for subject", subject)
    if not os.path.isfile(path_aseg_stat):
        continue
    else:
        subjects.extend([subject])
lh_defects = 0
list_lh_defects = []
list_rh_defects =[]
rh_defects = 0
for index, subject in enumerate(subjects): 
    lh_defects, rh_defects = defects_checker(subjects_dir, subject)
    with open(path_data_file,'a') as csvoutput:
        writer = csv.writer(csvoutput)
        writer.writerow([subject, lh_defects, rh_defects])
        