# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 15:49:05 2019

@author: Tobias Wolff 
This scripts extract the information about the topological fixing time of the left
and right hemisphere. Next it indicates the number of holes in the left and right hemisphere. 
Both information are extracted from the log file of the specfific subject

Required arguments:  
    - Subjects directory
    - Subject 
"""


def holes_topo_checker(subjects_dir, subject):
        
    lh_holes = 0
    rh_holes = 0
    lh_defects = 0
    rh_defects = 0 
    topo_time_lh = 0
    topo_time_rh = 0 
    topo = 0 
    path_log_file = str(subjects_dir) + str(subject) + "/scripts/recon-all.log"
    
    #Get the log file: 
    try:
        with open(path_log_file, 'r') as logfile:
         lines_log_file = logfile.read().splitlines()
    except FileNotFoundError:
            print("The path in the holes_topo_checker function", path_log_file, "does not have an appropriate file")
            exit()
    lh = 1       
    for line_log_file in lines_log_file:

        #Look for the number of holes in the left and right hemisphere
        if "orig.nofix lhholes" in line_log_file:
            lh_holes = line_log_file.split()[3]
            lh_holes=lh_holes[:-1]
            lh_holes = int(lh_holes)
            rh_holes = line_log_file.split()[6]
            print("The holes in the left hemisphere are:", lh_holes, "and the holes in the right hemisphere are", rh_holes)
       
       # Look for the number of defects         
        if "defects found" in line_log_file and lh == 1 :
            lh_defects = line_log_file.split()[0]
            lh_defects = int(lh_defects)
            lh = 0
            print("The number of defects in the left hemisphere are:", lh_defects)
        elif "defects found" in line_log_file and lh == 0 :
            rh_defects = line_log_file.split()[0]
            rh_defects = int(rh_defects)
            print("The number of defects in the right hemisphere are:", rh_defects)

        #Look for the topological fixing time in the log file 
        if "topology fixing took" in line_log_file and topo == 0:
            topo_time_lh = line_log_file.split()[3]
            print("The topological fixing time of the LH is", topo_time_lh, "minutes")            
            topo = 1
        elif "topology fixing took" in line_log_file and topo == 1:
            topo_time_rh = line_log_file.split()[3]
            print("The topological fixing time of the RH is", topo_time_rh, "minutes")            
            
    return lh_holes, rh_holes, lh_defects, rh_defects, topo_time_lh, topo_time_rh
    