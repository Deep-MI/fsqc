# -*- coding: utf-8 -*-
"""
Created on Wed May 29 16:09:26 2019

@author: Tobias Wolff
This is the main script for the quality control. This script calls several function that compute: \n
    - The WM and GM SNR based on the norm.mgz image 
    - The WM and GM SNR based on the orig.mgz image 
    - The size of the Corpus Callosum 
    - The number of holes in the LH and RH occured during the toplogy fixing 
    - The number of defects in the LH and RH occured during the topology fixing
    - The topological fixing time of the LH and the RH 
    - The Contrast to Noise ratio of the LH and the RH 
    - The outliers in relation to the segmentation volumes  
    
    optional: 
    - The Shape distances for several regions 

Note: 
    - If you do not specify some subjects, the scripts will execute the QC over the whole directory. 
    - You need to define the subjects dir with a slash at the end. 
    - Test call to the function:
        python3 quality_checker.py -sdir /path/to/your/subjects/dir/ \
    -recs /path/to/your/quality_checker/scripts/ -rcsv /path/to/your/metrics_result_file.csv/ \
    -mch /path/to/your/manual_check_file.csv \
    -fsh /path/to/your/freesurfer/home/directory/ -sk /path/to/your/shape/key.txt \
    -sh /path/to/your/shapeDNA/scripts/ -scsv /path/to/your/shape_results_file.csv \
    -pname plotly_username -pkey plotly_key

Required Arguments: 
    - Subjects directory, 
    - Recon checker scripts 
    - path_data_file: CSV file in which the results will be saved
    - pat_manual_check_file
    
Optional Arguments: 
    - Subjects: If specified, not the whole directory will be processed 
    -fsh, -sk, -sh, -scsv: Freesurfer Home Directory, Shape Key, Shape scripts home directory, results of the shape analysis 
        When specifying a shape_home directory, the script will compute the segmentation distances
        and save them into a csv file
    -pname -pkey: Plotly username, Plotly Key: You can sign up to plotly and then have a
    nice boyplot diagram of your results. This boyplot is semi-interactive as you can 
    see the subject ID when sliding across the points
    - Stats: If one wants to have a file with the information treated in the outlier part. 
        This file will be created in the subjects directory with the name mean_file 
    - lumeans: If one has already computed the means of the directory, there is an option to look 
        up these means instead of computing them. 
    - nerode: If one wants to shorten the WM when computing the CNR, one can erode more than 
        the default value of three pixel. 
    
    
TO DO: 
    Include Fore/Background energy ratio, probably by using mri_seghead
    Include Line_detector by using th Hough transform 
"""

import argparse
import os 
import csv
from datetime import datetime
from wm_gm_anat_snr_checker import wm_gm_anat_snr_checker
from recon_all_aseg_outlier_checker import recon_all_aseg_outlier_checker
from cc_size_checker import cc_size_checker
from write_information_to_file import write_information_to_file
from holes_topo_checker import holes_topo_checker
from contrast_control import contrast_control 
from shape_checker import shape_checker
from create_graph import create_graph
from manual_check import manual_check
from shape_distances import write_shape_to_file


def parse_arguments():
    parser= argparse.ArgumentParser(description = '''This is the main script for the quality control. This script calls several function that compute: \n
    - The WM and GM SNR based on the norm.mgz image 
    - The WM and GM SNR based on the orig.mgz image 
    - The size of the Corpus Callosum 
    - The number of holes in the LH and RH occured during the toplogy fixing 
    - The number of defects in the LH and RH occured during the topology fixing
    - The topological fixing time of the LH and the RH 
    - The Contrast to Noise ratio of the LH and the RH 
    - The outliers in relation to the segmentation volumes  
    
    optional: 
    - The Shape distances for several segmentations 

Note: 
    - If you do not specify some subjects, the scripts will execute the QC over the whole directory. 
    - You need to define the subjects dir with a slash at the end. 
    - Test call to the function:
        python3 quality_checker.py -sdir /path/to/your/subjects/dir/ \
    -recs /path/to/your/quality_checker/scripts/ -rcsv /path/to/your/metrics_result_file.csv/ \
    -mch /path/to/your/manual_check_file.csv \
    -fsh /path/to/your/freesurfer/home/directory/ -sk /path/to/your/shape/key.txt \
    -sh /path/to/your/shapeDNA/scripts/ -scsv /path/to/your/shape_results_file.csv \
    -pname plotly_username -pkey plotly_key

Required Arguments: 
    - Subjects directory, 
    - Recon checker scripts 
    - path_data_file: CSV file in which the results will be saved
    - pat_manual_check_file
    
Optional Arguments: 
    - Subjects: If specified, not the whole directory will be processed 
    -fsh, -sk, -sh, -scsv: Freesurfer Home Directory, Shape Key, Shape scripts home directory, results of the shape analysis 
        When specifying a shape_home directory, the script will compute the segmentation distances
        and save them into a csv file
    -pname -pkey: Plotly username, Plotly Key: You can sign up to plotly and then have a
    nice boyplot diagram of your results. This boyplot is semi-interactive as you can 
    see the subject ID when sliding across the points
    - Stats: If one wants to have a file with the information treated in the outlier part. 
        This file will be created in the subjects directory with the name mean_file 
    - lumeans: If one has already computed the means of the directory, there is an option to look 
        up these means instead of computing them. 
    - nerode: If one wants to shorten the WM when computing the SNR, one can erode more than 
        the default value of three pixel. 
''', formatter_class = argparse.RawTextHelpFormatter)

    parser.add_argument('--subjets_dir', '-sdir', dest = "subjects_dir")
    parser.add_argument('--subjects', '-s', nargs = '+',  dest = "subjects", default = [])
    parser.add_argument('--recon_checker_scripts', '-recs', dest = "re_che_scr")
    parser.add_argument('--result_csv', '-rcsv', dest = "path_data_file")
    parser.add_argument('--manuel_check', '-mch', dest = "path_manuel_check_file")
    
    parser.add_argument('--freesurfer_home', '-fsh', dest = "freesurfer_home", default ="")
    parser.add_argument('--shape_key', '-sk', dest = "shape_key", default ="" )    
    parser.add_argument('--shape_home', '-sh', dest = "shape_home", default = "")
    parser.add_argument('--shape_file', '-scsv', dest = "path_shape_file", default = "")

    parser.add_argument('--plotly_uname', '-pname', dest = "plotly_username", default = "")
    parser.add_argument('--plotly_key', '-pkey', dest = "pkey", default = "" )
    
    parser.add_argument('--nerode', dest = 'nb_erode', default = 3)
    parser.add_argument('--stats', dest = "print_means_to_file", default = 0)
    parser.add_argument('--lumeans', dest ="look_up_means_from_file", default = 0)

    
    args = parser.parse_args()
    return args
    
if __name__ == "__main__":
    arguments = parse_arguments()
    subjects_dir = arguments.subjects_dir
    subjects = arguments.subjects
    qc_checker_scripts = arguments.re_che_scr 
    path_data_file = arguments.path_data_file
    path_check_file = arguments.path_manuel_check_file
    
    freesurfer_home = arguments.freesurfer_home
    shape_key = arguments.shape_key
    shape_home = arguments.shape_home    
    path_shape_file = arguments.path_shape_file    

    plotly_username = arguments.plotly_username
    plotly_key = arguments.pkey
    
    print_means_file = arguments.print_means_to_file
    look_up_means = arguments.look_up_means_from_file
    nb_erode = arguments.nb_erode

    lh_holes = 0
    rh_holes = 0
    lh_defects = 0
    rh_defects = 0
    topo_lh = 0
    topo_rh = 0
    con_lh_snr = 0
    con_rh_snr = 0
    wm_snr_norm = 0
    gm_snr_norm = 0
    wm_snr_orig = 0
    gm_snr_orig = 0
    
    class metrics:
        all_wm_snr_norm = []
        all_gm_snr_norm = []
        all_gm_snr_orig = []
        all_wm_snr_orig = []
        all_topo_lh =[]
        all_topo_rh = []
        all_lh_holes=[]
        all_rh_holes =[]
        all_lh_defects =[]
        all_rh_defects = []
        cc_items = []
        subject_list = []
        all_con_lh_snr = []
        all_con_rh_snr = []    
    
    print("Startingt the quality control at", datetime.now())
    print("The subjects directory is:", subjects_dir)
    
    #str(subjects_dir) + "QA/quality_checker.csv"
    with open(path_data_file, 'w') as datafile:
        writer = csv.writer(datafile)
        writer.writerow (["Subject", "SNR_white_matter_norm", "SNR_gray_matter_norm", "SNR_white_matter_orig","SNR_gray_matter_orig","Relative_Corpus_Callosum_size","Probable_Misssegmentation_Corpus_Callosum", "Holes_LH", "Holes_RH","Defects_LH", "Defects_RH", "Topo_fixing_time_LH", "Topo_fixing_time_RH", "Contrast_WM_GM_LH_rawavg_mgz", "Contrast_WM_GM_RH_rawavg_mgz", "Number_of_outliers", "Segmentations"])
    
    #First possibility: Get the subjects of the directory
    if subjects == []:
        for subject in os.listdir(subjects_dir):
            path_aseg_stat  = str(subjects_dir) + str(subject) + "/stats/aseg.stats"
            if not os.path.isfile(path_aseg_stat):
                continue
            else:
                subjects.extend([subject])
            
    #Loop through the whole directory or through the specified subjects
    for subject in subjects:
        path_aseg_stat  = str(subjects_dir) + str(subject) + "/stats/aseg.stats"    
        with open(path_data_file, 'a')as datafile:
            writer = csv.writer(datafile)
            row = [str(subject)]
            writer.writerow(row)        
        if not os.path.isfile(path_aseg_stat):
            continue
        else:
            print("Starting the quality check for subject", subject, "at", datetime.now())
            if nb_erode != 3: 
                wm_snr_norm, gm_snr_norm = wm_gm_anat_snr_checker(subjects_dir, subject,nb_erode)
                wm_snr_orig, gm_snr_orig = wm_gm_anat_snr_checker(subjects_dir, subject,nb_erode ,option_base = 2)
            else:
                wm_snr_norm, gm_snr_norm = wm_gm_anat_snr_checker(subjects_dir, subject)
                wm_snr_orig, gm_snr_orig = wm_gm_anat_snr_checker(subjects_dir, subject, option_base = 2)
            metrics.cc_items.append(cc_size_checker(subjects_dir, subject))
            lh_holes, rh_holes, lh_defects, rh_defects, topo_lh, topo_rh = holes_topo_checker(subjects_dir, subject)
            con_lh_snr, con_rh_snr = contrast_control(subjects_dir, subject)
            if shape_home != "":
                shape_checker(subjects_dir, subject, shape_home, shape_key, freesurfer_home, qc_checker_scripts)
            print("Done with the quality check for subject", subject, "at", datetime.now(), " \n \n ")            
            
            metrics.all_wm_snr_norm.append(wm_snr_norm)
            metrics.all_gm_snr_norm.append(gm_snr_norm)
            metrics.all_wm_snr_orig.append(wm_snr_orig)
            metrics.all_gm_snr_orig.append(gm_snr_orig)
            metrics.all_lh_holes.append(lh_holes)
            metrics.all_rh_holes.append(rh_holes) 
            metrics.all_lh_defects.append(lh_defects)
            metrics.all_rh_defects.append(rh_defects)
            metrics.all_topo_lh.append(topo_lh)
            metrics.all_topo_rh.append(topo_rh)       
            metrics.all_con_lh_snr.append(con_lh_snr)
            metrics.all_con_rh_snr.append(con_rh_snr)
            
            
    # Write the usual metrics into the CSV file
    write_information_to_file(path_data_file, metrics)
    
    #Write shape information into seperate CSV file, if the shape scripts are sourced. 
    if shape_home != "":
        write_shape_to_file(subjects_dir, subjects, path_shape_file)
       
    #Look for Aseg outliers 
    if int(look_up_means) == 1 or int(print_means_file) == 1: 
        recon_all_aseg_outlier_checker(subjects_dir, subjects, qc_checker_scripts, path_data_file, print_means_file, look_up_means)
    else: 
        recon_all_aseg_outlier_checker(subjects_dir, subjects, qc_checker_scripts, path_data_file)  
        
    #Subjects that have to be checked again
    manual_check(path_check_file, subjects, metrics)    
         
    #Create interactive graph
    if plotly_username != "": 
        create_graph(subjects, plotly_username, plotly_key, metrics)    
     
    print("Done with the quality control at:", datetime.now())
