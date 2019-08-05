# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 15:49:05 2019

@author: Tobias Wolff 

This scripts extract the information about the topological fixing time of the 
left and right hemisphere. Next it indicates the number of holes in the left 
and right hemisphere. 

Required arguments:  
    - Subjects directory
    - Subject 
"""

def holes_topo_checker(subjects_dir, subject):

    import os
    import sys

    path_log_file = os.path.join(subjects_dir,subject,"scripts","recon-all.log")
    
    # Get the log file: 
    try:
        with open(path_log_file, 'r') as logfile:
         lines_log_file = logfile.read().splitlines()
    except FileNotFoundError:
            print("ERROR: could not find "+path_log_file)
            sys.exit(1)

    foundDefectsLH = 0
    foundTopoLH = 0 

    for line_log_file in lines_log_file:

        # Look for the number of holes in the left and right hemisphere
        if "orig.nofix lhholes" in line_log_file:
            lh_holes = line_log_file.split()[3]
            lh_holes = lh_holes[:-1]
            lh_holes = int(lh_holes)
            rh_holes = line_log_file.split()[6]
            print("There are ", lh_holes, " holes in the left hemisphere and ", rh_holes, " in the right hemisphere are")
       
        # Look for the number of defects         
        if "defects found" in line_log_file and foundDefectsLH == 0 :
            lh_defects = line_log_file.split()[0]
            lh_defects = int(lh_defects)
            print("There are ", lh_defects, " defects in the left hemisphere.")
            foundDefectsLH = 1
        elif "defects found" in line_log_file and foundDefectsLH == 1 :
            rh_defects = line_log_file.split()[0]
            rh_defects = int(rh_defects)
            print("There are ", rh_defects, " defects in the right hemisphere.")

        # Look for the topological fixing time in the log file 
        if "topology fixing took" in line_log_file and foundTopoLH == 0:
            topo_time_lh = line_log_file.split()[3]
            print("The topological fixing time of the left hemisphere is", topo_time_lh, "minutes")            
            foundTopoLH = 1
        elif "topology fixing took" in line_log_file and foundTopoLH == 1:
            topo_time_rh = line_log_file.split()[3]
            print("The topological fixing time of the right hemisphere is", topo_time_rh, "minutes")            
            
    return lh_holes, rh_holes, lh_defects, rh_defects, topo_time_lh, topo_time_rh
    
