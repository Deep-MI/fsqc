# -*- coding: utf-8 -*-
"""
qatools-python


description:

this is a set of quality assurance / quality control scripts for Freesurfer 6.0
processed structural MRI data.

it is a revision and translation to python of the original Freesurfer QA Tools
that are provided at https://surfer.nmr.mgh.harvard.edu/fswiki/QATools

it has been augmented by additional functions from the MRIQC toolbox, available 
at https://github.com/poldracklab/mriqc and https://osf.io/haf97, and with the
shapeDNA and brainPrint toolboxes, available at https://reuter.mit.edu

The current version is a development version that can be used for testing 
purposes. It will almost certainly be revised, corrected, and extended in the 
future.

The program will use an existing OUTPUT_DIR (or try to create it) and 
write a csv table into that location.

The csv table will contain the following variables/metrics:

- subject       ...  subject ID
- wm_snr_orig   ...  signal-to-noise for white matter in orig.mgz
- gm_snr_orig   ...  signal-to-noise for gray matter in orig.mgz
- wm_snr_norm   ...  signal-to-noise for white matter in norm.mgz
- gm_snr_norm   ...  signal-to-noise for gray matter in norm.mgz
- cc_size       ...  size of the corpus callosum
- lh_holes      ...  number of holes in the left hemisphere
- rh_holes      ...  number of holes in the right hemisphere
- lh_defects    ...  number of defects in the left hemisphere
- rh_defects    ...  number of defects in the right hemisphere
- topo_lh       ...  topological fixing time for the left hemisphere
- topo_rh       ...  topological fixing time for the right hemisphere
- con_lh_snr    ...  wm/gm contrast signal-to-noise ration in the left hemisphere
- con_rh_snr    ...  wm/gm contrast signal-to-noise ration in the right hemisphere

If the (optional) shape pipeline was run in addition to the core pipeline, the 
output directory will also contain results files of the brainPrint analysis, 
and the above csv table will contain several additional metrics: for a number 
of lateralized brain structures (e.g., ventricles, subcortical structures, gray 
and white matter), the lateral asymmetry will be computed, i.e. distances 
between numerical shape descriptors, where large values indicate large 
asymmetries and hence potential issues with the segmentation of these 
structures.


usage: 

    python3 quality_checker.py --subjects_dir <directory> --output_dir <directory>
                              [--subjects SubjectID [SubjectID ...]] [--shape]
                              [--norms <file>] [-h]

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
      --norms <file>
                            path to file with normative values

    getting help:
      -h, --help            display this help message and exit


authors: 

- qatools-python: Tobias Wolff, Kersten Diers, and Martin Reuter.
- Freesurfer QA Tools: David Koh, Stephanie Lee, Jenni Pacheco, Vasanth Pappu, 
  and Louis Vinke. 
- MRIQC toolbox: Oscar Esteban, Daniel Birman, Marie Schaer, Oluwasanmi Koyejo, 
  Russell Poldrack, and Krzysztof Gorgolewski.
- shapeDNA and brainPrint toolboxes: Martin Reuter.


citations:

Esteban O, Birman D, Schaer M, Koyejo OO, Poldrack RA, Gorgolewski KJ; MRIQC: 
Advancing the Automatic Prediction of Image Quality in MRI from Unseen Sites; 
PLOS ONE 12(9):e0184661; doi:10.1371/journal.pone.0184661.

Wachinger C, Golland P, Kremen W, Fischl B, Reuter M; 2015; BrainPrint: a 
Discriminative Characterization of Brain Morphology; Neuroimage: 109, 232-248; 
doi:10.1016/j.neuroimage.2015.01.032.

Reuter M, Wolter FE, Shenton M, Niethammer M; 2009; Laplace-Beltrami 
Eigenvalues and Topological Features of Eigenfunctions for Statistical Shape 
Analysis; Computer-Aided Design: 41, 739-755, doi:10.1016/j.cad.2009.02.007.


requirements:

At least one subject whose structural MR image was processed with Freesurfer 6.0.

A Python version >= 3.4 is required to run this script.

Required packages include the skimage and nibabel packages.

For (optional) shape analysis, a working version of Freesurfer, the shapeDNA 
scripts and the brainPrint scripts are required. See https://reuter.mit.edu for
download options.


license:

<todo>

"""

# ------------------------------------------------------------------------------
# imports

import os 
import sys
import errno
import argparse
import tempfile
import importlib
import csv

from datetime import datetime

from wm_gm_anat_snr_checker import wm_gm_anat_snr_checker
from recon_all_aseg_outlier_checker import recon_all_aseg_outlier_checker
from cc_size_checker import cc_size_checker
from holes_topo_checker import holes_topo_checker
from contrast_checker import contrast_checker 
from shape_checker import shape_checker
from create_graph import create_graph

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
    #optional.add_argument('--erode', dest='amount_erosion', help="Amount of erosion steps during the CNR computation", default=3, required=False)
    optional.add_argument('--erode', dest='amount_erosion', help=argparse.SUPPRESS, default=3, required=False) # #erode is currently a hidden option
    optional.add_argument('--norms', dest ="normative_values", help="path to file with normative values", default=None, metavar="<file>", required=False) 

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

    if sys.version_info <= (3, 4):
        print('\nERROR: Python version must be 3.4 or greater\n')
        sys.exit(1)

    if importlib.util.find_spec("skimage") is None:
        print('\nERROR: the \'skimage\' package is required for running this script, please install.\n')
        sys.exit(1)

    if importlib.util.find_spec("nibabel") is None:
        print('\nERROR: the \'nibabel\' package is required for running this script, please install.\n')
        sys.exit(1)


    # --------------------------------------------------------------------------
    # get and process inputs

    # parse arguments
    arguments = parse_arguments()

    # assign arguments
    subjects_dir = arguments.subjects_dir
    output_dir = arguments.output_dir
    subjects = arguments.subjects
    shape = arguments.shape
    normative_values = arguments.normative_values
    amount_erosion = arguments.amount_erosion

    # check arguments
    if os.path.isdir(subjects_dir):
        print("Found subjects directory", subjects_dir)
    else:
        print('ERROR: subjects directory '+subjects_dir+' is not an existing directory\n')
        sys.exit(1)

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

    if shape is True:
        if os.environ.get('FREESURFER_HOME') is None:
            print('\nERROR: need to set the FREESURFER_HOME environment variable for shape analysis\n')
            sys.exit(1)
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

    if normative_values is not None:
        if not os.path.isfile(normative_values):
            print('\nERROR: '+normative_values+' is not a regular file\n')
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
        for subject in subjects:
            path_aseg_stat = os.path.join(subjects_dir,subject,"stats","aseg.stats")
            if not os.path.isfile(path_aseg_stat):
                print("Could not find.aseg stats file for subject",subject)
                subjects.remove(subject)

    # determine default output files
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
        print("Starting quality check for subject", subject, "at", datetime.now())

        # get WM and GM SNR for orig.mgz
        wm_snr_orig, gm_snr_orig = wm_gm_anat_snr_checker(subjects_dir, subject, amount_erosion, ref_image="orig.mgz")

        # get WM and GM SNR for norm.mgz
        wm_snr_norm, gm_snr_norm = wm_gm_anat_snr_checker(subjects_dir, subject, amount_erosion, ref_image="norm.mgz")

        # check CC size
        cc_size = cc_size_checker(subjects_dir, subject)

        # check topology
        lh_holes, rh_holes, lh_defects, rh_defects, topo_lh, topo_rh = holes_topo_checker(subjects_dir, subject)

        # check contrast
        con_lh_snr, con_rh_snr = contrast_checker(subjects_dir, subject)

        # store data
        metricsDict.update( { subject : {
            'subject' : subject,
            'wm_snr_orig': wm_snr_orig, 'gm_snr_orig' : gm_snr_orig, 
            'wm_snr_norm' : wm_snr_norm, 'gm_snr_norm' : gm_snr_norm, 
            'cc_size' : cc_size, 
            'lh_holes' : lh_holes, 'rh_holes' : rh_holes, 'lh_defects' : lh_defects, 'rh_defects' : rh_defects, 'topo_lh' : topo_lh, 'topo_rh' : topo_rh,
            'con_lh_snr' : con_lh_snr, 'con_rh_snr' : con_rh_snr
            }})

        # shape analysis
        if shape == True:

            # compute brainprint
            brainprint = shape_checker(subjects_dir, subject, output_dir)

            # get a subset of the brainprint results
            dist = { subject : brainprint[os.path.abspath(os.path.join(output_dir,subject+"-brainprint.csv"))]['dist'] }
    
            # store data
            metricsDict[subject].update(dist[subject])

        # message
        print("Done with the quality check for subject", subject, "at", datetime.now())
        print("")

    # look for aseg outliers across subjects: <todo> should return some data; currently we don't do this, because if there are outliers one should not use the 2*SD criterion to detect them (because it's not robust).
    # recon_all_aseg_outlier_checker(subjects_dir, subjects, path_data_file, path_means_file, normative_values)

    # flag subjects that reqire further checking: <todo> should return some data; we currently don't do this steps because of the questionable classification
    # manual_check(path_check_file, subjects, metrics)    

    # --------------------------------------------------------------------------
    # generate output

    # we pre-specify the fieldnames because we want to have this particular order
    metricsFieldnames = ['subject','wm_snr_orig','gm_snr_orig','wm_snr_norm','gm_snr_norm','cc_size','lh_holes','rh_holes','lh_defects','rh_defects','topo_lh','topo_rh','con_lh_snr','con_rh_snr']
 
    if shape == True:
        metricsFieldnames.extend(dist[subject].keys())

    # write csv
    with open(path_data_file, 'w') as datafile:
        #csvwriter = csv.DictWriter(datafile, fieldnames=list(metricsDict[list(metricsDict.keys())[0]].keys()), delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL) # this requires less preceding code, but gives an unsorted list of fieldnames
        csvwriter = csv.DictWriter(datafile, fieldnames=metricsFieldnames, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writeheader()
        for subject in list(metricsDict.keys()):
            csvwriter.writerow(metricsDict[subject])

    # --------------------------------------------------------------------------         
    # Create interactive graph <todo>

    # if plotly_username != "": 
    #    create_graph(subjects, plotly_username, plotly_key, metrics)    

    # --------------------------------------------------------------------------
    # exit

    print("Done with the quality control at:", datetime.now())
