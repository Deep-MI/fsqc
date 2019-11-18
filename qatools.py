# -*- coding: utf-8 -*-
"""
qatools-python


============
Description:
============

This is a set of quality assurance / quality control scripts for Freesurfer 6.0
processed structural MRI data.

It is a revision, extension, and translation to the Python language of the 
original Freesurfer QA Tools that are provided at 
https://surfer.nmr.mgh.harvard.edu/fswiki/QATools

It has been augmented by additional functions from the MRIQC toolbox, available 
at https://github.com/poldracklab/mriqc and https://osf.io/haf97, and with the
shapeDNA and brainPrint toolboxes, available at https://reuter.mit.edu

The current version is a development version that can be used for testing 
purposes. It will be revised, and extended in the future.

The core functionality of this toolbox is to compute the following features:

- wm_snr_orig   ...  signal-to-noise for white matter in orig.mgz
- gm_snr_orig   ...  signal-to-noise for gray matter in orig.mgz
- wm_snr_norm   ...  signal-to-noise for white matter in norm.mgz
- gm_snr_norm   ...  signal-to-noise for gray matter in norm.mgz
- cc_size       ...  relative size of the corpus callosum
- holes_lh      ...  number of holes in the left hemisphere
- holes_rh      ...  number of holes in the right hemisphere
- defects_lh    ...  number of defects in the left hemisphere
- defects_rh    ...  number of defects in the right hemisphere
- topo_lh       ...  topological fixing time for the left hemisphere
- topo_rh       ...  topological fixing time for the right hemisphere
- con_snr_lh    ...  wm/gm contrast signal-to-noise ratio in the left hemisphere
- con_snr_rh    ...  wm/gm contrast signal-to-noise ratio in the right hemisphere
- rot_tal_x     ...  rotation component of the Talairach transform around the x axis
- rot_tal_y     ...  rotation component of the Talairach transform around the y axis
- rot_tal_z     ...  rotation component of the Talairach transform around the z axis

The program will use an existing OUTPUT_DIR (or try to create it) and write a 
csv table into that location. The csv table will contain the above metrics plus
a subject identifier.

In addition to the core functionality of the toolbox there are several optional
modules that can be run according to need:

- screenshots module

This module allows for the automated generation of cross-sections of the brain 
that are overlaid with the anatomical segmentations (asegs) and the white and 
pial surfaces. These images will be saved to the 'screenshots' subdirectory 
that will be created within the output directory. These images can be used for 
quickly glimpsing through the processing results. Note that no display manager 
is required for this module, i.e. it can be run on a remote server, for example.

- shape features

The purpose of this optional module is the computation of shape features, i.e. 
a brainPrint anylsis. If this module is run, the output directory will also 
contain results files of the brainPrint analysis, and the above csv table will 
contain several additional metrics: for a number of lateralized brain 
structures (e.g., ventricles, subcortical structures, gray and white matter), 
the lateral asymmetry will be computed, i.e. distances between numerical shape 
descriptors, where large values indicate large asymmetries and hence potential 
issues with the segmentation of these structures.

- fornix module

This is a module to assess potential issues with the segementation of the 
corpus callosum, which may incorrectly include parts of the fornix. To assess 
segmentation quality, a screesnhot of the contours of the corpus callosum 
segmentation overlaid on the norm.mgz will be saved in the 'fornix' 
subdirectory of the output directory. Further, a shapeDNA / brainPrint analysis
will be conducted on a surface model of the corpus callosum. By comparing the
resulting shape descriptors, which will appear in the main csv table, deviant 
segmentations may be detected.


======
Usage: 
======

    python3 quatools.py --subjects_dir <directory> --output_dir <directory>
                              [--subjects SubjectID [SubjectID ...]] [--shape]
                              [--screenshots] [--fornix] [-h]

    required arguments:
      --subjects_dir <directory>
                            subjects directory with a set of Freesurfer 6.0 
                            processed individual datasets.
      --output_dir <directory>
                            output directory

    optional arguments:
      --subjects SubjectID [SubjectID ...]
                            list of subject IDs
      --shape               run shape analysis (requires additional scripts)
      --screenshots         create screenshots of individual brains
      --fornix              check fornix segmentation

    getting help:
      -h, --help            display this help message and exit


=============
Known Issues: 
=============

The program will analyze recon-all logfiles, and may fail or return erroneous
results if the logfile is append by multiple restarts of recon-all runs. 
Ideally, the logfile should therefore consist of just a single, successful 
recon-all run.


========
Authors: 
========

- qatools-python: Kersten Diers, Tobias Wolff, and Martin Reuter.
- Freesurfer QA Tools: David Koh, Stephanie Lee, Jenni Pacheco, Vasanth Pappu, 
  and Louis Vinke. 
- MRIQC toolbox: Oscar Esteban, Daniel Birman, Marie Schaer, Oluwasanmi Koyejo, 
  Russell Poldrack, and Krzysztof Gorgolewski.
- shapeDNA and brainPrint toolboxes: Martin Reuter.


===========
References:
===========

Esteban O, Birman D, Schaer M, Koyejo OO, Poldrack RA, Gorgolewski KJ; MRIQC: 
Advancing the Automatic Prediction of Image Quality in MRI from Unseen Sites; 
PLOS ONE 12(9):e0184661; doi:10.1371/journal.pone.0184661.

Wachinger C, Golland P, Kremen W, Fischl B, Reuter M; 2015; BrainPrint: a 
Discriminative Characterization of Brain Morphology; Neuroimage: 109, 232-248; 
doi:10.1016/j.neuroimage.2015.01.032.

Reuter M, Wolter FE, Shenton M, Niethammer M; 2009; Laplace-Beltrami 
Eigenvalues and Topological Features of Eigenfunctions for Statistical Shape 
Analysis; Computer-Aided Design: 41, 739-755, doi:10.1016/j.cad.2009.02.007.


=============
Requirements:
=============

A working installation of Freesurfer 6.0 or later must be sourced.

At least one subject whose structural MR image was processed with Freesurfer 
6.0 or later.

A Python version >= 3.4 is required to run this script.

Required packages include the nibabel and scikit-image package for the core
functionality, plus the the matplotlib, pandas, transforms3d, and future 
packages for some optional modules and functions.

For (optional) shape analysis, the shapeDNA scripts and the brainPrint scripts 
are required. See https://reuter.mit.edu for download options. # TODO


========
License:
========

<todo>

"""

# ------------------------------------------------------------------------------
# internal settings (might be turned into command-line arguments in the future)

FORNIX_SCREENSHOT = True
FORNIX_SHAPE = False
FORNIX_N_EIGEN = 15

# ------------------------------------------------------------------------------
# imports

import os 
import sys
import errno
import argparse
import tempfile
import importlib
import csv
import time

from checkSNR import checkSNR
from checkCCSize import checkCCSize
from checkTopology import checkTopology
from checkContrast import checkContrast 
from checkRotation import checkRotation
from runBrainPrint import runBrainPrint
from evaluateFornixSegmentation import evaluateFornixSegmentation
from createScreenshots import createScreenshots


# ------------------------------------------------------------------------------
# functions

def parse_arguments():

    parser = argparse.ArgumentParser(description='''
        This program takes existing Freesurfer 6.0 analysis results of one
        or more subjects and computes a set of quality metrics. These will be 
        reported in a summary csv table.

        For a description of these metrics, see the gitlab/github page or the 
        header section of this script.

        The (optional) analysis of shape features requires additional scripts 
        that can be obtained from https://reuter.mit.edu
        ''', 
        add_help=False, formatter_class=argparse.RawTextHelpFormatter)

    required = parser.add_argument_group('required arguments')
    required.add_argument('--subjects_dir', dest="subjects_dir", help="subjects directory with a set of Freesurfer 6.0 \nprocessed individual datasets.", metavar="<directory>", required=True)
    required.add_argument('--output_dir', dest="output_dir", help="output directory", metavar="<directory>", required=True)

    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('--subjects', dest="subjects", help="list of subject IDs. If omitted, all suitable sub-\ndirectories witin the subjects directory will be \nused.", default=[], nargs='+', metavar="SubjectID", required=False)
    optional.add_argument('--shape', dest='shape', help="run shape analysis (requires additional scripts)", default=False, action="store_true", required=False)
    optional.add_argument('--screenshots', dest='screenshots', help="create screenshots of individual brains", default=False, action="store_true", required=False)
    optional.add_argument('--fornix', dest='fornix', help="check fornix segmentation", default=False, action="store_true", required=False)
    #optional.add_argument('--erode', dest='amount_erosion', help="Amount of erosion steps during the CNR computation", default=3, required=False)
    optional.add_argument('--erode', dest='amount_erosion', help=argparse.SUPPRESS, default=3, required=False) # erode is currently a hidden option
    optional.add_argument('--output_suffix', dest='output_suffix', help=argparse.SUPPRESS, default=None, required=False) # output_suffix is currently a hidden option

    help = parser.add_argument_group('getting help')
    help.add_argument('-h', '--help', help="display this help message and exit", action='help')

    # check if there are any inputs; if not, print help and exit
    if len(sys.argv)==1:
        args = parser.parse_args(['--help'])
    else:
        args = parser.parse_args()

    return args

# ------------------------------------------------------------------------------
# main
    
if __name__ == "__main__":

    # --------------------------------------------------------------------------
    # say hello

    print("")
    print("-----------------------------")
    print("qatools-python")
    print("-----------------------------")
    print("")

    # --------------------------------------------------------------------------
    # check some basics

    if os.environ.get('FREESURFER_HOME') is None:
        print('\nERROR: need to set the FREESURFER_HOME environment variable\n')
        sys.exit(1)

    if sys.version_info <= (3, 4):
        print('\nERROR: Python version must be 3.4 or greater\n')
        sys.exit(1)

    if importlib.util.find_spec("skimage") is None:
        print('\nERROR: the \'skimage\' package is required for running this script, please install.\n')
        sys.exit(1)

    if importlib.util.find_spec("nibabel") is None:
        print('\nERROR: the \'nibabel\' package is required for running this script, please install.\n')
        sys.exit(1)

    if importlib.util.find_spec("transforms3d") is None:
        # this package is less important and less stanard, so we just return a
        # warning (and NaNs) if it is not found.
        print('\nWARNING: the \'transforms3d\' package is recommended, please install.\n')

    # --------------------------------------------------------------------------
    # get inputs

    # parse arguments
    arguments = parse_arguments()

    # assign arguments
    subjects_dir = arguments.subjects_dir
    output_dir = arguments.output_dir
    subjects = arguments.subjects
    shape = arguments.shape
    screenshots = arguments.screenshots
    fornix = arguments.fornix
    amount_erosion = arguments.amount_erosion
    output_suffix = arguments.output_suffix

    # --------------------------------------------------------------------------
    # check arguments

    # check if subject directory exists
    if os.path.isdir(subjects_dir):
        print("Found subjects directory", subjects_dir)
    else:
        print('ERROR: subjects directory '+subjects_dir+' is not an existing directory\n')
        sys.exit(1)

    # check if output directory exists or can be created and is writable
    if os.path.isdir(output_dir):
        print("Found output directory", output_dir)
    else:
        try:
            os.mkdir(output_dir)
        except:
            print('ERROR: cannot create output directory '+output_dir+'\n')
            sys.exit(1)

        try:
            testfile = tempfile.TemporaryFile(dir=output_dir)
            testfile.close()
        except OSError as e:
            if e.errno != errno.EACCES:  # 13
                e.filename = output_dir
                raise
            print('\nERROR: '+output_dir+' not writeable (check access)!\n')
            sys.exit(1)

    # check if screenshots subdirectory exists or can be created and is writable
    if screenshots is True:
        if os.path.isdir(os.path.join(output_dir,'screenshots')):
            print("Found screenshots directory", os.path.join(output_dir,'screenshots'))
        else:
            try:
                os.mkdir(os.path.join(output_dir,'screenshots'))
            except:
                print('ERROR: cannot create screenshots directory '+os.path.join(output_dir,'screenshots')+'\n')
                sys.exit(1)

            try:
                testfile = tempfile.TemporaryFile(dir=os.path.join(output_dir,'screenshots'))
                testfile.close()
            except OSError as e:
                if e.errno != errno.EACCES:  # 13
                    e.filename = os.path.join(output_dir,'screenshots')
                    raise
                print('\nERROR: '+os.path.join(output_dir,'screenshots')+' not writeable (check access)!\n')
                sys.exit(1)

    # check further screenshots dependencies
    if screenshots is True and importlib.util.find_spec("pandas") is None:
        print('\nERROR: the \'pandas\' package is required for running this script, please install.\n')
        sys.exit(1)

    if screenshots is True and importlib.util.find_spec("matplotlib") is None:
        print('\nERROR: the \'matplotlib\' package is required for running this script, please install.\n')
        sys.exit(1)

    # check if fornix subdirectory exists or can be created and is writable
    if fornix is True:
        if os.path.isdir(os.path.join(output_dir,'fornix')):
            print("Found fornix directory", os.path.join(output_dir,'fornix'))
        else:
            try:
                os.mkdir(os.path.join(output_dir,'fornix'))
            except:
                print('ERROR: cannot create fornix directory '+os.path.join(output_dir,'fornix')+'\n')
                sys.exit(1)

            try:
                testfile = tempfile.TemporaryFile(dir=os.path.join(output_dir,'fornix'))
                testfile.close()
            except OSError as e:
                if e.errno != errno.EACCES:  # 13
                    e.filename = os.path.join(output_dir,'fornix')
                    raise
                print('\nERROR: '+os.path.join(output_dir,'fornix')+' not writeable (check access)!\n')
                sys.exit(1)

    # check if shapeDNA / brainPrint dependencies # TODO: adjust to python version of shapeDNA
    if shape is True:
        if os.environ.get('SHAPEDNA_HOME') is None:
            print('\nERROR: need to set the SHAPEDNA_HOME environment variable for shape analysis\n')
            sys.exit(1)
        if not os.path.isfile(os.path.join(os.environ.get('SHAPEDNA_HOME'),"key.txt")):
            print("\nERROR: could not find file key.txt within "+os.environ.get('SHAPEDNA_HOME')) 
            sys.exit(1)
        if not os.path.isfile(os.path.join(os.environ.get('SHAPEDNA_HOME'),"shapeDNA-tria")):
            print("\nERROR: could not find file shapeDNA-tria within "+os.environ.get('SHAPEDNA_HOME')) 
            sys.exit(1)
        if  importlib.util.find_spec("fs_brainPrint") is None:
            print("\nERROR: could not import the fs_brainPrint scripts, are they on the PYTHONPATH?") 
            sys.exit(1)
        if importlib.util.find_spec("future") is None:
            print('\nERROR: the \'future\' package is required for running the shape analysis, please install.\n')
            sys.exit(1)

    # if subjects are not given, get contents of the subject directory and 
    # check if aseg.stats exists; otherwise, just check that aseg.stats exists
    if subjects == []:
        for subject in os.listdir(subjects_dir):
            path_aseg_stat = os.path.join(subjects_dir,subject,"stats","aseg.stats")
            if os.path.isfile(path_aseg_stat):
                print("Found aseg.stats file for subject",subject)
                subjects.extend([subject])
    else:
        subjects_to_remove = list()
        for subject in subjects:
            path_aseg_stat = os.path.join(subjects_dir,subject,"stats","aseg.stats")
            if not os.path.isfile(path_aseg_stat):
                print("Could not find.aseg stats file for subject",subject)
                subjects_to_remove.extend([subject])
        [ subjects.remove(x) for x in subjects_to_remove ]

    # check if we have any subjects after all
    if subjects == []:
        print("\nERROR: no subjects to process") 
        sys.exit(1)

    # determine default output files
    if output_suffix is not None:
        path_data_file = os.path.join(output_dir,'qatools-results-'+output_suffix+'.csv')
    else:
        path_data_file = os.path.join(output_dir,'qatools-results.csv')
    path_means_file = os.path.join(output_dir,'qatools-means.csv')
    path_check_file = os.path.join(output_dir,'qatools-check.csv')
    path_shape_file = os.path.join(output_dir,'qatools-shape.csv')

    # --------------------------------------------------------------------------
    # process

    # start the processing with a message
    print("")
    print("-----------------------------")

    # create dict for this subject
    metricsDict = dict()

    # loop through the specified subjects
    for subject in subjects:

        #
        print("Starting qatools-python for subject", subject, "at", time.strftime('%Y-%m-%d %H:%M %Z', time.localtime(time.time())))
        print("")

        # ----------------------------------------------------------------------
        # compute core metrics

        # get WM and GM SNR for orig.mgz
        wm_snr_orig, gm_snr_orig = checkSNR(subjects_dir, subject, amount_erosion, ref_image="orig.mgz")

        # get WM and GM SNR for norm.mgz
        wm_snr_norm, gm_snr_norm = checkSNR(subjects_dir, subject, amount_erosion, ref_image="norm.mgz")

        # check CC size
        cc_size = checkCCSize(subjects_dir, subject)

        # check topology
        holes_lh, holes_rh, defects_lh, defects_rh, topo_lh, topo_rh = checkTopology(subjects_dir, subject)

        # check contrast
        con_snr_lh, con_snr_rh = checkContrast(subjects_dir, subject)

        # check rotation
        rot_tal_x, rot_tal_y, rot_tal_z = checkRotation(subjects_dir, subject)

        # store data
        metricsDict.update( { subject : {
            'subject' : subject,
            'wm_snr_orig': wm_snr_orig, 'gm_snr_orig' : gm_snr_orig, 
            'wm_snr_norm' : wm_snr_norm, 'gm_snr_norm' : gm_snr_norm, 
            'cc_size' : cc_size, 
            'holes_lh' : holes_lh, 'holes_rh' : holes_rh, 'defects_lh' : defects_lh, 'defects_rh' : defects_rh, 'topo_lh' : topo_lh, 'topo_rh' : topo_rh,
            'con_snr_lh' : con_snr_lh, 'con_snr_rh' : con_snr_rh,
            'rot_tal_x' : rot_tal_x, 'rot_tal_y' : rot_tal_y , 'rot_tal_z' : rot_tal_z  
            }})

        # 
        print("")

        # ----------------------------------------------------------------------
        # run optional modules

        # shape analysis
        if shape is True:
    
            # message
            print("-----------------------------")
            print("Running brainPrint analysis ...")
            print("")

            # compute brainprint
            brainprint = runBrainPrint(subjects_dir, subject, output_dir)

            # get a subset of the brainprint results
            distDict = { subject : brainprint[os.path.abspath(os.path.join(output_dir,subject+"-brainprint.csv"))]['dist'] }
    
            # store data
            metricsDict[subject].update(distDict[subject])

        # screenshots
        if screenshots is True:

            # message
            print("-----------------------------")
            print("Creating screenshots ...")
            print("")

            # check / create outdir
            outdir = os.path.join(output_dir,'screenshots',subject)
            if not os.path.isdir(outdir):
                os.mkdir(outdir)
            outfile = os.path.join(outdir,subject+'.png')

            # process
            createScreenshots(SUBJECT=subject,SUBJECTS_DIR=subjects_dir,OUTFILE=outfile,INTERACTIVE=False)

        # fornix
        if fornix is True:

            # message
            print("-----------------------------")
            print("Checking fornix segmentation ...")
            print("")

            # check / create outdir
            outdir = os.path.join(output_dir,'fornix',subject)
            if not os.path.isdir(outdir):
                os.mkdir(outdir)

            # process
            fornixShapeOutput = evaluateFornixSegmentation(SUBJECT=subject,SUBJECTS_DIR=subjects_dir,OUTPUT_DIR=outdir,CREATE_SCREENSHOT=FORNIX_SCREENSHOT,RUN_SHAPEDNA=FORNIX_SHAPE,N_EIGEN=FORNIX_N_EIGEN)

            # create a dictionary from fornix shape ouput
            fornixShapeDict = { subject : dict(zip(map("fornixShapeEV{:0>3}".format,range(FORNIX_N_EIGEN)), fornixShapeOutput)) }
       
            # store data
            if FORNIX_SHAPE:
                metricsDict[subject].update(fornixShapeDict[subject])

        # message
        print("Finished subject", subject, "at", time.strftime('%Y-%m-%d %H:%M %Z', time.localtime(time.time())))
        print("")

    # --------------------------------------------------------------------------
    # generate output

    # we pre-specify the fieldnames because we want to have this particular order
    metricsFieldnames = ['subject','wm_snr_orig','gm_snr_orig','wm_snr_norm','gm_snr_norm','cc_size','holes_lh','holes_rh','defects_lh','defects_rh','topo_lh','topo_rh','con_snr_lh','con_snr_rh','rot_tal_x', 'rot_tal_y', 'rot_tal_z']

    if shape is True:
        metricsFieldnames.extend(distDict[subject].keys())

    if fornix is True and FORNIX_SHAPE is True:
        metricsFieldnames.extend(sorted(fornixShapeDict[subject].keys()))

    # write csv
    with open(path_data_file, 'w') as datafile:
        csvwriter = csv.DictWriter(datafile, fieldnames=metricsFieldnames, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writeheader()
        for subject in list(metricsDict.keys()):
            csvwriter.writerow(metricsDict[subject])

    # --------------------------------------------------------------------------
    # exit

    sys.exit(0)
