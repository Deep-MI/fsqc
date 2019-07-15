# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 10:54:59 2019

@author: Tobias Wolff 
Function that should be run if one wants to have an shape analysis of their subjects. 

# Set three environment variables: 
SHAPEDNA_HOME
SHAPEDNA_KEY
Freesurfer HOME
"""
import os
import subprocess 
from fs_brainPrint import compute_shapeDNAs
from fs_brainPrint import write_evs


def shape_checker(subjects_dir, subject, shape_home, shape_key, freesurfer_home, qc_checker_scripts): 
    #Options, that the compute_shapeDNAs need
    class options: 
        sid = subject 
        sdir = subjects_dir
        num = 50
        outdir = str(subjects_dir) + str(subject) + "/brainprint/"
        brainprint = str(outdir) + str(subject) +".brainprint_" + str(50) +".csv"
        keeptmp = False
        tsmooth = 3
        gsmooth = 0
        do3d = False
        skipcortex = False
        evec = False
    
    try:
    # Create target Directory
        os.mkdir(options.outdir)
        print("Directory " , options.outdir ,  " Created ") 
    except FileExistsError:
        print("Directory " , options.outdir ,  " already exists")

    os.environ['SHAPEDNA_KEY'] = str(shape_key)
    os.environ['SHAPEDNA_HOME'] = str(shape_home) 
    os.environ['FREESURFER_HOME'] = str(freesurfer_home)  
    (structures , evmat) = compute_shapeDNAs(options)
    write_evs(options.brainprint,structures,evmat)
    
    path_postproc = str(qc_checker_scripts) + "fs_brainPrintPostproc.py"
    subprocess.run(["python3", path_postproc, "--file",options.brainprint, "--vol=1", "--lin", "--asy=euc"])   
