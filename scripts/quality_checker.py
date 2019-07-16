# -*- coding: utf-8 -*-
"""
qatools-python

description:

this is a set of quality assurance / quality control scripts for Freesurfer 6.0
processed structural MRI data.

it is a revision and translation to python of the original Freesurfer QA Tools
that are provided at https://surfer.nmr.mgh.harvard.edu/fswiki/QATools

it has been augmented by additional functions from the MRIQC toolbox, available 
at https://github.com/poldracklab/mriqc and https://osf.io/haf97

authors: 

- qatools-python: Tobias Wolff, Kersten Diers, and Martin Reuter.
- Freesurfer QA Tools: David Koh, Stephanie Lee, Jenni Pacheco, Vasanth Pappu, 
  and Louis Vinke. 
- MRIQC toolbox: Oscar Esteban, Daniel Birman, Marie Schaer, Oluwasanmi Koyejo, 
  Russell Poldrack, and Krzysztof Gorgolewski.

citations:

Esteban O, Birman D, Schaer M, Koyejo OO, Poldrack RA, Gorgolewski KJ; MRIQC: 
Advancing the Automatic Prediction of Image Quality in MRI from Unseen Sites; 
PLOS ONE 12(9):e0184661; doi:10.1371/journal.pone.0184661.

requirements:

<todo: optionale brainprint-skripte>

license:

<todo>


"""

# ------------------------------------------------------------------------------
# list of todos:

# check all <todo> tags
# maybe remove short options, they are too confusing
# maybe re-format help and usage info
# add help="..." to add_argument
# probably discard the plotly username/key stuff
# the mriqc osf repository seems to have manual image ratings --> possibly use these for evaluation   
# get rid of the recs option
# get rid of the submodule in shape_checker.py


# ------------------------------------------------------------------------------
# imports

import argparse
import os 
import sys
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
from write_shape_to_file import write_shape_to_file

# ------------------------------------------------------------------------------
# functions

def parse_arguments():

    parser= argparse.ArgumentParser(description='''
        <todo>
        ''', formatter_class=argparse.RawTextHelpFormatter)

    requiredNamed = parser.add_argument_group('required named arguments')

    requiredNamed.add_argument('--subjects_dir', '-sdir', dest="subjects_dir", required=True)
    requiredNamed.add_argument('--recon_checker_scripts', '-recs', dest="re_che_scr", required=True)
    requiredNamed.add_argument('--result_csv', '-rcsv', dest="path_data_file", required=True)
    requiredNamed.add_argument('--manual_check', '-mch', dest="path_manual_check_file", required=True)

    parser.add_argument('--subjects', '-s', dest="subjects", default=[], nargs='+')
    
    parser.add_argument('--freesurfer_home', '-fsh', dest="freesurfer_home", default ="")
    parser.add_argument('--shape_key', '-sk', dest="shape_key", default ="" )    
    parser.add_argument('--shape_home', '-sh', dest="shape_home", default="")
    parser.add_argument('--shape_file', '-scsv', dest="path_shape_file", default="")

    parser.add_argument('--plotly_uname', '-pname', dest="plotly_username", default="")
    parser.add_argument('--plotly_key', '-pkey', dest="pkey", default="" )
    
    parser.add_argument('--nerode', dest='nb_erode', default=3)
    parser.add_argument('--stats', dest="print_means_to_file", default=0)
    parser.add_argument('--lumeans', dest ="look_up_means_from_file", default=0)

    # setting the default option -h will print out usage info if called without 
    # arguments
    #args = parser.parse_args(['-h'])
    args = parser.parse_args()

    return args

# ------------------------------------------------------------------------------
# main
    
if __name__ == "__main__":

    # parse arguments
    arguments = parse_arguments()

    # assign values 
    subjects_dir = arguments.subjects_dir
    subjects = arguments.subjects
    qc_checker_scripts = arguments.re_che_scr 
    path_data_file = arguments.path_data_file
    path_check_file = arguments.path_manual_check_file
    
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
    
    print("Starting the quality control at", datetime.now())
    print("The subjects directory is:", subjects_dir)
    
    # create output file
    with open(path_data_file, 'w') as datafile:
        writer = csv.writer(datafile)
        writer.writerow (["Subject", "SNR_white_matter_norm", "SNR_gray_matter_norm", "SNR_white_matter_orig","SNR_gray_matter_orig","Relative_Corpus_Callosum_size","Probable_Misssegmentation_Corpus_Callosum", "Holes_LH", "Holes_RH","Defects_LH", "Defects_RH", "Topo_fixing_time_LH", "Topo_fixing_time_RH", "Contrast_WM_GM_LH_rawavg_mgz", "Contrast_WM_GM_RH_rawavg_mgz", "Number_of_outliers", "Segmentations"])
    
    # first possibility: Get the subjects of the directory
    if subjects == []:
        for subject in os.listdir(subjects_dir):
            path_aseg_stat  = str(subjects_dir) + str(subject) + "/stats/aseg.stats"
            if not os.path.isfile(path_aseg_stat):
                continue
            else:
                subjects.extend([subject])
            
    # loop through the whole directory or through the specified subjects
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
    
    # Write shape information into seperate CSV file, if the shape scripts are sourced. 
    if shape_home != "":
        write_shape_to_file(subjects_dir, subjects, path_shape_file)
       
    # Look for Aseg outliers 
    if int(look_up_means) == 1 or int(print_means_file) == 1: 
        recon_all_aseg_outlier_checker(subjects_dir, subjects, qc_checker_scripts, path_data_file, print_means_file, look_up_means)
    else: 
        recon_all_aseg_outlier_checker(subjects_dir, subjects, qc_checker_scripts, path_data_file)  
        
    # Subjects that have to be checked again
    manual_check(path_check_file, subjects, metrics)    
         
    # Create interactive graph
    if plotly_username != "": 
        create_graph(subjects, plotly_username, plotly_key, metrics)    

    # Exit
    print("Done with the quality control at:", datetime.now())
