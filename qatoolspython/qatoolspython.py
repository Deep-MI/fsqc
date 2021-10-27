"""
This module provides the main functionality of the qatoolspython package.

"""

# ==============================================================================
# FUNCTIONS

# ------------------------------------------------------------------------------
# get_help()

def get_help(print_help=True, return_help=False):
    """
    a function to return a help message

    """

    HELPTEXT="""

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
    at https://github.com/poldracklab/mriqc and https://osf.io/haf97, and with code
    derived from the shapeDNA and brainPrint toolboxes, available at
    https://reuter.mit.edu.

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

    The program will use an existing output directory (or try to create it) and
    write a csv table into that location. The csv table will contain the above
    metrics plus a subject identifier.

    In addition to the core functionality of the toolbox there are several optional
    modules that can be run according to need:

    - screenshots module

    This module allows for the automated generation of cross-sections of the brain
    that are overlaid with the anatomical segmentations (asegs) and the white and
    pial surfaces. These images will be saved to the 'screenshots' subdirectory
    that will be created within the output directory. These images can be used for
    quickly glimpsing through the processing results. Note that no display manager
    is required for this module, i.e. it can be run on a remote server, for example.

    - fornix module

    This is a module to assess potential issues with the segmentation of the
    corpus callosum, which may incorrectly include parts of the fornix. To assess
    segmentation quality, a screesnhot of the contours of the corpus callosum
    segmentation overlaid on the norm.mgz will be saved in the 'fornix'
    subdirectory of the output directory.

    - shape module

    The shape module will run a shapeDNA / brainprint analysis to compute distances
    of shape descriptors between lateralized brain structures. This can be used
    to identify discrepancies and irregularities between pairs of corresponding
    structures. The results will be included in the main csv table, and the output
    directory will also contain a "brainprint" subdirectory.

    - outlier module

    This is a module to detect extreme values among the subcortical ('aseg')
    segmentations. The outlier detection is based on comparisons with the
    distributions of the sample as well as normative values taken from the
    literature (see References).

    For comparisons with the sample distributions, extreme values are defined in
    two ways: nonparametrically, i.e. values that are 1.5 times the interquartile
    range below or above the 25th or 75th percentile of the sample, respectively,
    and parametrically, i.e. values that are more than 2 standard deviations above
    or below the sample mean. Note that a minimum of 5 supplied subjects is
    required for running these analyses, otherwise `NaNs` will be returned.

    For comparisons with the normative values, lower and upper bounds are computed
    from the 95% prediction intervals of the regression models given in Potvin et
    al., 1996, and values exceeding these bounds will be flagged. As an
    alternative, users may specify their own normative values by using the
    '--outlier-table' argument. This requires a custom csv table with headers
    `label`, `upper`, and `lower`, where `label` indicates a column of anatomical
    names. It can be a subset and the order is arbitrary, but naming must exactly
    match the nomenclature of the 'aseg.stats' file. `upper` and `lower` are user-
    specified upper and lower bounds.

    The main csv table will be appended with the following summary variables, and
    more detailed output about will be saved as csv tables in the 'outliers'
    subdirectory of the main output directory.

    n_outliers_sample_nonpar ... number of structures that are 1.5 times the IQR
                                 above/below the 75th/25th percentile
    n_outliers_sample_param  ... number of structures that are 2 SD above/below
                                 the mean
    n_outliers_norms         ... number of structures exceeding the upper and
                                 lower bounds of the normative values


    ======
    Usage:
    ======

        python3 qatools.py --subjects_dir <directory> --output_dir <directory>
                                  [--subjects SubjectID [SubjectID ...]]
                                  [--screenshots] [--screenshots-html] 
                                  [--fornix] [--fornix-html] [--shape] 
                                  [--outlier] [--fastsurfer] [-h]

        required arguments:
          --subjects_dir <directory>
                                subjects directory with a set of Freesurfer 6.0
                                processed individual datasets.
          --output_dir <directory>
                                output directory

        optional arguments:
          --subjects SubjectID [SubjectID ...]
                                list of subject IDs
          --subjects-file <file>
                                filename of a file with subject IDs (one per line)
          --screenshots         create screenshots of individual brains
          --screenshots-html    create html summary page of screenshots (requires
                                --screenshots)
          --fornix              check fornix segmentation
          --fornix-html          create html summary page of fornix evaluation (requires 
                                 --fornix)          
          --shape               run shape analysis
          --outlier             run outlier detection
          --outlier-table       specify normative values (only in conjunction with
                                --outlier)
          --fastsurfer          use FastSurfer instead of FreeSurfer output

        getting help:
          -h, --help            display this help message and exit

        expert options:
          --screenshots_base <image>
                                path to an image that should be used instead of
                                norm.mgz as the base image for the screenshots
          --screenshots_overlay <image>
                                path to an image that should be used instead of
                                aseg.mgz as the overlay image for the screenshots;
                                can also be none
          --screenshots_surf <surf> [<surf> ...]
                                one or more path to surface files that should be
                                used instead of [lr].white and [lr].pial; can
                                also be none
          --screenshots_views <view> [<view> ...]
                                one or more views to use for the screenshots in
                                the form of x=<numeric> y=<numeric> and/or
                                z=<numeric>. order does not matter. default views
                                are x=-10 x=10 y=0 z=0.
          --screenshots_layout <rows> <columns>
                                layout matrix for screenshot images


    ========================
    Use as a python package:
    ========================

    As an alternative to their command-line usage, the qc scripts can also be run
    within a pure python environment, i.e. installed and imported as a python
    package.

    Use `import qatoolspython` (or sth. equivalent) to import the package within a
    python environment.

    Use the `run_qatools` function from the `qatoolspython` module to run an analysis:

    `from qatoolspython import qatoolspython`

    `qatoolspython.run_qatools(subjects_dir='/my/subjects/dir', output_dir='/my/output/dir')`

    See `help(qatoolspython)` for further usage info and options.


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
    - shapeDNA and brainPrint toolboxes: Martin Reuter


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

    Potvin O, Mouiha A, Dieumegarde L, Duchesne S, & Alzheimer's Disease Neuroimaging
    Initiative; 2016; Normative data for subcortical regional volumes over the lifetime
    of the adult human brain; Neuroimage: 137, 9-20;
    doi.org/10.1016/j.neuroimage.2016.05.016

    =============
    Requirements:
    =============

    A working installation of Freesurfer 6.0 or later must be sourced.

    At least one subject whose structural MR image was processed with Freesurfer
    6.0 or later.

    A Python version >= 3.5 is required to run this script.

    Required packages include (among others) the nibabel and skimage package for
    the core functionality, plus the the matplotlib, pandas, and transform3d
    packages for some optional functions and modules. See the `requirements.txt`
    file for a complete list. Use `pip3 install -r requirements.txt` to install
    these packages.

    For the shape analysis module, the brainprint and lapy packages from
    https://github.com/Deep-MI are required (both version 0.2 or newer).

    This software has been tested on Ubuntu 16.04, CentOS7, and MacOS 10.14.


    ========
    License:
    ========

    This software is licensed under the MIT License, see associated LICENSE file
    for details.

    Copyright (c) 2019 Image Analysis Group, DZNE e.V.

    """

    if print_help:
        print(HELPTEXT)

    if return_help:
        return HELPTEXT


# ------------------------------------------------------------------------------
# parse_arguments

def _parse_arguments():
    """
    an internal function to parse input arguments

    """

    # imports
    import sys
    import argparse

    # parse
    parser = argparse.ArgumentParser(description='''
        This program takes existing Freesurfer 6.0 analysis results of one
        or more subjects and computes a set of quality metrics. These will be
        reported in a summary csv table.

        For a description of these metrics, see the gitlab/github page or the
        header section of this script.
        ''',
        add_help=False, formatter_class=argparse.RawTextHelpFormatter)

    required = parser.add_argument_group('required arguments')
    required.add_argument('--subjects_dir', dest="subjects_dir", help="subjects directory with a set of Freesurfer 6.0 \nprocessed individual datasets.", metavar="<directory>", required=True)
    required.add_argument('--output_dir', dest="output_dir", help="output directory", metavar="<directory>", required=True)

    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('--subjects', dest="subjects", help="list of subject IDs. If omitted, all suitable sub-\ndirectories witin the subjects directory will be \nused.", default=None, nargs='+', metavar="SubjectID", required=False)
    optional.add_argument('--subjects-file', dest="subjects_file", help="filename with list of subject IDs (one per line). \nIf omitted, all suitable sub-directories witin \nthe subjects directory will be used.", default=None, metavar="<filename>", required=False)
    optional.add_argument('--shape', dest='shape', help="run shape analysis", default=False, action="store_true", required=False)
    optional.add_argument('--screenshots', dest='screenshots', help="create screenshots of individual brains", default=False, action="store_true", required=False)
    optional.add_argument('--screenshots-html', dest='screenshots_html', help="create html summary page for screenshots", default=False, action="store_true", required=False)
    optional.add_argument('--screenshots_base', dest='screenshots_base', help=argparse.SUPPRESS, default="default", metavar="<base image for screenshots>", required=False) # this is currently a hidden "expert" option
    optional.add_argument('--screenshots_overlay', dest='screenshots_overlay', help=argparse.SUPPRESS, default="default", metavar="<overlay image for screenshots>", required=False) # this is currently a hidden "expert" option
    optional.add_argument('--screenshots_surf', dest='screenshots_surf', help=argparse.SUPPRESS, default="default", nargs="+", metavar="<surface(s) for screenshots>", required=False) # this is currently a hidden "expert" option
    optional.add_argument('--screenshots_views', dest='screenshots_views', help=argparse.SUPPRESS, default="default", nargs="+", metavar="<dimension=coordinate [dimension=coordinate]>", required=False) # this is currently a hidden "expert" option
    optional.add_argument('--screenshots_layout', dest='screenshots_layout', help=argparse.SUPPRESS, default=None, nargs=2, metavar="<rows> <columns>", required=False) # this is currently a hidden "expert" option
    optional.add_argument('--fornix', dest='fornix', help="check fornix segmentation", default=False, action="store_true", required=False)
    optional.add_argument('--fornix-html', dest='fornix_html', help="create html summary page for fornix evaluation", default=False, action="store_true", required=False)    
    optional.add_argument('--outlier', dest='outlier', help="run outlier detection", default=False, action="store_true", required=False)
    optional.add_argument('--outlier-table', dest="outlier_table", help="specify normative values", default=None, metavar="<filename>", required=False)
    optional.add_argument('--fastsurfer', dest='fastsurfer', help="use FastSurfer output", default=False, action="store_true", required=False)

    help = parser.add_argument_group('getting help')
    help.add_argument('-h', '--help', help="display this help message and exit", action='help')

    # check if there are any inputs; if not, print help and exit
    if len(sys.argv)==1:
        args = parser.parse_args(['--help'])
    else:
        args = parser.parse_args()

    return args.subjects_dir, args.output_dir, args.subjects, \
        args.subjects_file, args.shape, args.screenshots, \
        args.screenshots_html, args.screenshots_base, \
        args.screenshots_overlay, args.screenshots_surf, \
        args.screenshots_views, args.screenshots_layout, args.fornix, \
        args.fornix_html, args.outlier, args.outlier_table, args.fastsurfer

# ------------------------------------------------------------------------------
# check arguments

def _check_arguments(subjects_dir, output_dir, subjects, subjects_file, shape, screenshots, screenshots_html, screenshots_base, screenshots_overlay, screenshots_surf, screenshots_views, screenshots_layout, fornix, fornix_html, outlier, outlier_table, fastsurfer):
    """
    an internal function to check input arguments

    """

    # --------------------------------------------------------------------------
    # imports

    import os
    import sys
    import errno

    import tempfile
    import importlib.util

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

    # check if both subjects and subjects-file were specified
    if subjects is not None and subjects_file is not None:
        print("ERROR: Use either --subjects or --subjects-file (but not both).")
        sys.exit(1)

    # check if subjects-file exists and get data
    if subjects_file is not None:
        if os.path.isfile(subjects_file):
            # read file
            with open(subjects_file) as subjects_file_f:
                subjects = subjects_file_f.read().splitlines()
        else:
            print("ERROR: Could not find subjects file", subjects_file)
            sys.exit(1)

    # if neither subjects nor subjects_file are given, get contents of the subject 
    # directory and check if aseg.stats (as a proxy) exists
    if subjects is None and subjects_file is None:
        subjects = []
        for subject in os.listdir(subjects_dir):
            path_aseg_stat = os.path.join(subjects_dir, subject, "stats", "aseg.stats")
            if os.path.isfile(path_aseg_stat):
                print("Found subject", subject)
                subjects.extend([subject])

    # check if screenshots subdirectory exists or can be created and is writable
    if screenshots is True:
        if os.path.isdir(os.path.join(output_dir, 'screenshots')):
            print("Found screenshots directory", os.path.join(output_dir, 'screenshots'))
        else:
            try:
                os.mkdir(os.path.join(output_dir, 'screenshots'))
            except:
                print('ERROR: cannot create screenshots directory '+os.path.join(output_dir, 'screenshots')+'\n')
                sys.exit(1)

            try:
                testfile = tempfile.TemporaryFile(dir=os.path.join(output_dir, 'screenshots'))
                testfile.close()
            except OSError as e:
                if e.errno != errno.EACCES:  # 13
                    e.filename = os.path.join(output_dir, 'screenshots')
                    raise
                print('\nERROR: '+os.path.join(output_dir, 'screenshots')+' not writeable (check access)!\n')
                sys.exit(1)

    # check further screenshots dependencies
    if screenshots is True and importlib.util.find_spec("pandas") is None:
        print('\nERROR: the \'pandas\' package is required for running this script, please install.\n')
        sys.exit(1)

    if screenshots is True and importlib.util.find_spec("matplotlib") is None:
        print('\nERROR: the \'matplotlib\' package is required for running this script, please install.\n')
        sys.exit(1)

    if screenshots is True:
        if os.environ.get('FREESURFER_HOME') is None:
            print('\nERROR: need to set the FREESURFER_HOME environment variable\n')
            sys.exit(1)
        else:
            path_check = os.path.join(os.environ['FREESURFER_HOME'], 'FreeSurferColorLUT.txt')
            if not os.path.isfile(path_check):
                print('\nERROR: the \'FreeSurferColorLUT.txt\' file needs to be present in the FREESURFER_HOME directory.\n')
                sys.exit(1)

    # check screenshots_base
    if screenshots_base == 'default':
        screenshots_base = [screenshots_base]
    else:
        if len(subjects)!=1:
            print('\nERROR: can only use the --screenshots_base argument for a single subject, which must be specified using --subject\n')
            sys.exit(1)
        if not os.path.isfile(screenshots_base):
            print('\nERROR: cannot find the screenshots base file '+screenshots_base+'\n')
            sys.exit(1)
        else:
            print("Using "+screenshots_base+" as screenshot base image")
            screenshots_base = [screenshots_base]

    # check screenshots_overlay
    if screenshots_overlay == 'default':
        screenshots_overlay = [screenshots_overlay]
    elif screenshots_overlay.lower() == 'none':
        screenshots_overlay = None
        print("Found screenshot overlays set to None")
    else:
        if len(subjects)!=1:
            print('\nERROR: can only use the --screenshots_overlay argument for a single subject, which must be specified using --subject\n')
            sys.exit(1)
        if not os.path.isfile(screenshots_overlay):
            print('\nERROR: cannot find the screenshots overlay file '+screenshots_overlay+'\n')
            sys.exit(1)
        else:
            print("Using "+screenshots_overlay+" as screenshot overlay image")
            screenshots_overlay = [screenshots_overlay]

    # check screenshots_surf (this is either 'default' or a list)
    if screenshots_surf == 'default':
        screenshots_surf = [screenshots_surf]
    elif screenshots_surf[0].lower() == 'none':
        screenshots_surf = None
        print("Found screenshot surfaces set to None")
    else:
        if len(subjects)!=1:
            print('\nERROR: can only use the --screenshots_surf argument for a single subject, which must be specified using --subject\n')
            sys.exit(1)
        for screenshots_surf_i in screenshots_surf:
            if not os.path.isfile(screenshots_surf_i):
                print('\nERROR: cannot find the screenshots surface file '+screenshots_surf_i+'\n')
                sys.exit(1)
            else:
                print("Using "+screenshots_surf_i+" as screenshot surface")

    # check if screenshots_views argument can be evaluated
    if screenshots_views == 'default':
        screenshots_views = [screenshots_views]
    else:
        for x in screenshots_views:
            isXYZ = x.split("=")[0] == "x" or x.split("=")[0] == "y" or x.split("=")[0] == "z"
            try:
                int(x.split("=")[1])
                isConvertible = True
            except:
                isConvertible = False
            if not isXYZ or not isConvertible:
                print()
                print('ERROR: could not understand '+x)
                print()
                print('       the --screenshots_views argument can only contain one or more x=<numeric> y=<numeric> z=<numeric> expressions.')
                print()
                print('       for example: --screenshots_views x=0')
                print('                    --screenshots_views x=-10 x=10 y=0')
                print('                    --screenshots_views x=0 z=0')
                print()
                sys.exit(1)

        print("Found screenshot coordinates ", screenshots_views)
        screenshots_views = [ (y[0], int(y[1])) for y in [ x.split("=") for x in screenshots_views ] ]

    # check screenshots_layout
    if screenshots_layout is not None:
        if all([ x.isdigit() for x in screenshots_layout ]):
            screenshots_layout = [ int(x) for x in screenshots_layout ]
        else:
            print('ERROR: screenshots_layout argument can only contain integer numbers\n')
            sys.exit(1)

    # check if fornix subdirectory exists or can be created and is writable
    if fornix is True:
        if os.path.isdir(os.path.join(output_dir, 'fornix')):
            print("Found fornix directory", os.path.join(output_dir, 'fornix'))
        else:
            try:
                os.mkdir(os.path.join(output_dir, 'fornix'))
            except:
                print('ERROR: cannot create fornix directory '+os.path.join(output_dir, 'fornix')+'\n')
                sys.exit(1)

            try:
                testfile = tempfile.TemporaryFile(dir=os.path.join(output_dir, 'fornix'))
                testfile.close()
            except OSError as e:
                if e.errno != errno.EACCES:  # 13
                    e.filename = os.path.join(output_dir, 'fornix')
                    raise
                print('\nERROR: '+os.path.join(output_dir, 'fornix')+' not writeable (check access)!\n')
                sys.exit(1)

    # check if shape subdirectory exists or can be created and is writable
    if shape is True:
        if os.path.isdir(os.path.join(output_dir, 'brainprint')):
            print("Found brainprint directory", os.path.join(output_dir, 'brainprint'))
        else:
            try:
                os.makedirs(os.path.join(output_dir, 'brainprint'))
            except:
                print('\nERROR: cannot create brainprint directory '+os.path.join(output_dir, 'brainprint')+'\n')
                sys.exit(1)

            try:
                testfile = tempfile.TemporaryFile(dir=os.path.join(output_dir, 'brainprint'))
                testfile.close()
            except OSError as e:
                if e.errno != errno.EACCES:  # 13
                    e.filename = os.path.join(output_dir, 'brainprint')
                    raise
                print('\nERROR: '+os.path.join(output_dir, 'brainprint')+' not writeable (check access)!\n')
                sys.exit(1)

    # check if shapeDNA / brainPrint dependencies
    if shape is True:
        # check if brainprintpython can be imported
        if  importlib.util.find_spec("brainprint") is None:
            print("\nERROR: could not import the brainprint package, is it installed?")
            sys.exit(1)

        if  importlib.util.find_spec("lapy") is None:
            print("\nERROR: could not import the lapy package, is it installed?")
            sys.exit(1)

    # check if outlier subdirectory exists or can be created and is writable
    if outlier is True:
        if os.path.isdir(os.path.join(output_dir, 'outliers')):
            print("Found outliers directory", os.path.join(output_dir, 'outliers'))
        else:
            try:
                os.makedirs(os.path.join(output_dir, 'outliers'))
            except:
                print('\nERROR: cannot create outliers directory '+os.path.join(output_dir, 'outliers')+'\n')
                sys.exit(1)

            try:
                testfile = tempfile.TemporaryFile(dir=os.path.join(output_dir, 'outliers'))
                testfile.close()
            except OSError as e:
                if e.errno != errno.EACCES:  # 13
                    e.filename = os.path.join(output_dir, 'outliers')
                    raise
                print('\nERROR: '+os.path.join(output_dir, 'outliers')+' not writeable (check access)!\n')
                sys.exit(1)

    # check if outlier-table exists if it was given, otherwise exit
    if outlier_table is not None:
        if os.path.isfile(outlier_table):
            print("Found table with normative values ", outlier_table)
        else:
            print("ERROR: Could not find table with normative values ", outlier_table)
            sys.exit(1)

    # check for required files
    subjects_to_remove = list()
    for subject in subjects:

        # -files: stats/aseg.stats
        path_check = os.path.join(subjects_dir, subject, "stats", "aseg.stats")
        if not os.path.isfile(path_check):
            print("Could not find", path_check, "for subject", subject)
            subjects_to_remove.extend([subject])

        # -files: surf/[lr]h.w-g.pct.mgh, label/[lr]h.cortex.label
        path_check = os.path.join(subjects_dir, subject, "surf", "lh.w-g.pct.mgh")
        if not os.path.isfile(path_check):
            print("Could not find", path_check, "for subject", subject)
            subjects_to_remove.extend([subject])

        path_check = os.path.join(subjects_dir, subject, "surf", "rh.w-g.pct.mgh")
        if not os.path.isfile(path_check):
            print("Could not find", path_check, "for subject", subject)
            subjects_to_remove.extend([subject])

        path_check = os.path.join(subjects_dir, subject, "label", "lh.cortex.label")
        if not os.path.isfile(path_check):
            print("Could not find", path_check, "for subject", subject)
            subjects_to_remove.extend([subject])

        path_check = os.path.join(subjects_dir, subject, "label", "rh.cortex.label")
        if not os.path.isfile(path_check):
            print("Could not find", path_check, "for subject", subject)
            subjects_to_remove.extend([subject])

        # -files: mri/transforms/talairach.lta
        path_check = os.path.join(subjects_dir, subject, "mri", "transforms", "talairach.lta")
        if not os.path.isfile(path_check):
            print("Could not find", path_check, "for subject", subject)
            subjects_to_remove.extend([subject])

        # -files: mri/norm.mgz, mri/aseg.mgz, mri/aparc+aseg.mgz for FreeSurfer
        # -files: mri/norm.mgz, mri/aseg.mgz, mri/aparc+aseg.orig.mgz for FastSurfer
        path_check = os.path.join(subjects_dir, subject, "mri", "norm.mgz")
        if not os.path.isfile(path_check):
            print("Could not find", path_check, "for subject", subject)
            subjects_to_remove.extend([subject])

        path_check = os.path.join(subjects_dir, subject, "mri", "aseg.mgz")
        if not os.path.isfile(path_check):
            print("Could not find", path_check, "for subject", subject)
            subjects_to_remove.extend([subject])

        if fastsurfer is True:
            path_check = os.path.join(subjects_dir, subject, "mri", "aparc+aseg.orig.mgz")
        else:
            path_check = os.path.join(subjects_dir, subject, "mri", "aparc+aseg.mgz")
        if not os.path.isfile(path_check):
            print("Could not find", path_check, "for subject", subject)
            subjects_to_remove.extend([subject])

        # -files: scripts/recon-all.log
        path_check = os.path.join(subjects_dir, subject, "scripts", "recon-all.log")
        if not os.path.isfile(path_check):
            print("Could not find", path_check, "for subject", subject)
            subjects_to_remove.extend([subject])

        # check screenshots
        if screenshots is True and screenshots_surf=="default":

            # -files: surf/[lr]h.white (optional), surf/[lr]h.pial (optional)
            path_check = os.path.join(subjects_dir, subject, "surf", "lh.white")
            if not os.path.isfile(path_check):
                print("Could not find", path_check, "for subject", subject)
                subjects_to_remove.extend([subject])

            path_check = os.path.join(subjects_dir, subject, "surf", "rh.white")
            if not os.path.isfile(path_check):
                print("Could not find", path_check, "for subject", subject)
                subjects_to_remove.extend([subject])

            path_check = os.path.join(subjects_dir, subject, "surf", "lh.pial")
            if not os.path.isfile(path_check):
                print("Could not find", path_check, "for subject", subject)
                subjects_to_remove.extend([subject])

            path_check = os.path.join(subjects_dir, subject, "surf", "rh.pial")
            if not os.path.isfile(path_check):
                print("Could not find", path_check, "for subject", subject)
                subjects_to_remove.extend([subject])

        # check fornix
        if fornix is True:

            # -files: mri/transforms/cc_up.lta
            path_check = os.path.join(subjects_dir, subject, "mri", "transforms", "cc_up.lta")
            if not os.path.isfile(path_check):
                print("Could not find", path_check, "for subject", subject)
                subjects_to_remove.extend([subject])

    # remove subjects with missing files after creating unique list
    [ subjects.remove(x) for x in list(set(subjects_to_remove)) ]

    # check if we have any subjects after all
    if not subjects:
        print("\nERROR: no subjects to process")
        sys.exit(1)

    # now return
    return subjects_dir, output_dir, subjects, subjects_file, shape, screenshots, screenshots_html, screenshots_base, screenshots_overlay, screenshots_surf, screenshots_views, screenshots_layout, fornix, fornix_html, outlier, outlier_table, fastsurfer


# ------------------------------------------------------------------------------
# check packages

def _check_packages():
    """
    an internal function to check required / recommended packages

    """

    import os
    import sys
    import importlib.util

    if os.environ.get('FREESURFER_HOME') is None:
        print('\nERROR: need to set the FREESURFER_HOME environment variable\n')
        sys.exit(1)

    if sys.version_info <= (3, 5):
        print('\nERROR: Python version must be 3.5 or greater\n')
        sys.exit(1)

    if importlib.util.find_spec("skimage") is None:
        print('\nERROR: the \'skimage\' package is required for running this script, please install.\n')
        sys.exit(1)

    if importlib.util.find_spec("nibabel") is None:
        print('\nERROR: the \'nibabel\' package is required for running this script, please install.\n')
        sys.exit(1)

    if importlib.util.find_spec("transforms3d") is None:
        # this package is less important and less standard, so we just return a
        # warning (and NaNs) if it is not found.
        print('\nWARNING: the \'transforms3d\' package is recommended, please install.\n')


# ------------------------------------------------------------------------------
# do qatools

def _do_qatools(subjects_dir, output_dir, subjects, shape=False, screenshots=False, screenshots_html=False, screenshots_base=["default"], screenshots_overlay=["default"], screenshots_surf=["default"], screenshots_views=["default"], screenshots_layout=None, fornix=False, fornix_html=False, outlier=False, outlier_table=None, fastsurfer=False):
    """
    an internal function to run the qatools submodules

    """

    # ------------------------------------------------------------------------------
    # imports

    import os
    import csv
    import time

    import numpy as np

    from qatoolspython.checkSNR import checkSNR
    from qatoolspython.checkCCSize import checkCCSize
    from qatoolspython.checkTopology import checkTopology
    from qatoolspython.checkContrast import checkContrast
    from qatoolspython.checkRotation import checkRotation
    from qatoolspython.evaluateFornixSegmentation import evaluateFornixSegmentation
    from qatoolspython.createScreenshots import createScreenshots
    from qatoolspython.outlierDetection import outlierTable
    from qatoolspython.outlierDetection import outlierDetection

    # ------------------------------------------------------------------------------
    # internal settings (might be turned into command-line arguments in the future)

    SNR_AMOUT_EROSION = 3
    FORNIX_SCREENSHOT = True
    FORNIX_SHAPE = False
    FORNIX_N_EIGEN = 15
    OUTLIER_N_MIN = 5

    SHAPE_EVEC = False
    SHAPE_SKIPCORTEX = False
    SHAPE_NUM = 50
    SHAPE_NORM = "geometry"
    SHAPE_REWEIGHT = True
    SHAPE_ASYMMETRY = True

    # --------------------------------------------------------------------------
    # process

    # start the processing with a message
    print("")
    print("-----------------------------")

    # create metrics dict
    metricsDict = dict()

    # create images dict
    imagesScreenshotsDict = dict()
    imagesFornixDict = dict()    

    # create status dict
    statusDict = dict()

    # loop through the specified subjects
    for subject in subjects:

        #
        print("Starting qatools-python for subject", subject, "at", time.strftime('%Y-%m-%d %H:%M %Z', time.localtime(time.time())))
        print("")

        # ----------------------------------------------------------------------
        # set images

        if fastsurfer is True:
            aparc_image = "aparc+aseg.orig.mgz"
        else:
            aparc_image = "aparc+aseg.mgz"

        # ----------------------------------------------------------------------
        # add subject to dictionary
        
        metricsDict.update( { subject : { 'subject' : subject } } )
        statusDict.update( { subject : { 'subject' : subject } } )
        
        # ----------------------------------------------------------------------
        # compute core metrics

        # set status
        metrics_ok = True

        # get WM and GM SNR for orig.mgz
        try:
            wm_snr_orig, gm_snr_orig = checkSNR(subjects_dir, subject, SNR_AMOUT_EROSION, ref_image="orig.mgz", aparc_image=aparc_image)

        except:
            wm_snr_orig = np.nan
            gm_snr_orig = np.nan
            metrics_ok = False

        # get WM and GM SNR for norm.mgz
        try:
            wm_snr_norm, gm_snr_norm = checkSNR(subjects_dir, subject, SNR_AMOUT_EROSION, ref_image="norm.mgz", aparc_image=aparc_image)

        except:
            wm_snr_norm = np.nan
            gm_snr_norm = np.nan
            metrics_ok = False

        # check CC size
        try:
            cc_size = checkCCSize(subjects_dir, subject)

        except:
            cc_size = np.nan
            metrics_ok = False

        # check topology
        try:
            holes_lh, holes_rh, defects_lh, defects_rh, topo_lh, topo_rh = checkTopology(subjects_dir, subject)

        except:
            holes_lh = np.nan
            holes_rh = np.nan
            defects_lh = np.nan
            defects_rh = np.nan
            topo_lh = np.nan
            topo_rh = np.nan
            metrics_ok = False

        # check contrast
        try:
            con_snr_lh, con_snr_rh = checkContrast(subjects_dir, subject)

        except:
            con_snr_lh = np.nan
            con_snr_rh = np.nan
            metrics_ok = False

        # check rotation
        try:
            rot_tal_x, rot_tal_y, rot_tal_z = checkRotation(subjects_dir, subject)

        except:
            rot_tal_x = np.nan
            rot_tal_y = np.nan
            rot_tal_z = np.nan
            metrics_ok = False

        # store data
        metricsDict[subject].update({
            'wm_snr_orig': wm_snr_orig, 'gm_snr_orig' : gm_snr_orig,
            'wm_snr_norm' : wm_snr_norm, 'gm_snr_norm' : gm_snr_norm,
            'cc_size' : cc_size,
            'holes_lh' : holes_lh, 'holes_rh' : holes_rh, 'defects_lh' : defects_lh, 'defects_rh' : defects_rh, 'topo_lh' : topo_lh, 'topo_rh' : topo_rh,
            'con_snr_lh' : con_snr_lh, 'con_snr_rh' : con_snr_rh,
            'rot_tal_x' : rot_tal_x, 'rot_tal_y' : rot_tal_y , 'rot_tal_z' : rot_tal_z
            })

        # store data
        statusDict[subject].update( { 'metrics' : metrics_ok } )

        #
        print("")

        # ----------------------------------------------------------------------
        # run optional modules: shape analysis

        if shape is True:

            #
            try:

                # message
                print("-----------------------------")
                print("Running brainPrint analysis ...")
                print("")

                # compute brainprint (will also compute shapeDNA)
                from brainprint import brainprint

                # check / create subject-specific brainprint_outdir
                brainprint_outdir = os.path.join(output_dir, 'brainprint', subject)

                # run brainPrint
                evMat, evecMat, dstMat = brainprint.run_brainprint(sdir=subjects_dir, sid=subject, outdir=brainprint_outdir, evec=SHAPE_EVEC, skipcortex=SHAPE_SKIPCORTEX, num=SHAPE_NUM, norm=SHAPE_NORM, reweight=SHAPE_REWEIGHT, asymmetry=SHAPE_ASYMMETRY)

                # get a subset of the brainprint results
                distDict = { subject : dstMat }

                # return
                shape_ok = True

                # check / create subject-specific brainprint_outdir
                brainprint_outdir = os.path.join(output_dir, 'brainprint', subject)

                # run brainPrint
                evMat, evecMat, dstMat = brainprint.run_brainprint(sdir=subjects_dir, sid=subject, outdir=brainprint_outdir, evec=SHAPE_EVEC, skipcortex=SHAPE_SKIPCORTEX, num=SHAPE_NUM, norm=SHAPE_NORM, reweight=SHAPE_REWEIGHT, asymmetry=SHAPE_ASYMMETRY)

                # get a subset of the brainprint results
                distDict = { subject : dstMat }

                # return
                shape_ok = True

            #
            except:

                distDict = { subject : [] }
                print("ERROR: the shape module failed for subject "+subject)
                shape_ok = False

            # store data
            metricsDict[subject].update(distDict[subject])

            # store data
            statusDict[subject].update( { 'shape' : shape_ok } )
        
        # ----------------------------------------------------------------------
        # run optional modules: screenshots

        if screenshots is True:

            #
            try:

                # message
                print("-----------------------------")
                print("Creating screenshots ...")
                print("")

                # check / create subject-specific screenshots_outdir
                screenshots_outdir = os.path.join(output_dir, 'screenshots', subject)
                if not os.path.isdir(screenshots_outdir):
                    os.mkdir(screenshots_outdir)
                outfile = os.path.join(screenshots_outdir, subject+'.png')

                # process
                createScreenshots(SUBJECT=subject, SUBJECTS_DIR=subjects_dir, OUTFILE=outfile, INTERACTIVE=False, BASE=screenshots_base, OVERLAY=screenshots_overlay, SURF=screenshots_surf, VIEWS=screenshots_views, LAYOUT=screenshots_layout)

                # return
                screenshots_ok = True

            #
            except:

                print("ERROR: screenshots module failed for subject "+subject)
                screenshots_ok = False

            # store data
            imagesScreenshotsDict[subject] = outfile

            # store data
            statusDict[subject].update( { 'screenshots' : screenshots_ok } )

        # ----------------------------------------------------------------------
        # run optional modules: fornix

        if fornix is True:

            #
            try:

                # message
                print("-----------------------------")
                print("Checking fornix segmentation ...")
                print("")

                # check / create subject-specific fornix_outdir
                fornix_outdir = os.path.join(output_dir, 'fornix', subject)
                if not os.path.isdir(fornix_outdir):
                    os.mkdir(fornix_outdir)
                fornix_screenshot_outfile = os.path.join(fornix_outdir, "cc.png")

                # process
                fornixShapeOutput = evaluateFornixSegmentation(SUBJECT=subject, SUBJECTS_DIR=subjects_dir, OUTPUT_DIR=fornix_outdir, CREATE_SCREENSHOT=FORNIX_SCREENSHOT, SCREENSHOTS_OUTFILE=fornix_screenshot_outfile, RUN_SHAPEDNA=FORNIX_SHAPE, N_EIGEN=FORNIX_N_EIGEN)

                # create a dictionary from fornix shape ouput
                fornixShapeDict = { subject : dict(zip(map("fornixShapeEV{:0>3}".format, range(FORNIX_N_EIGEN)), fornixShapeOutput)) }

                # return
                fornix_ok = True

            #
            except:

                fornixShapeDict = { subject : dict(zip(map("fornixShapeEV{:0>3}".format, range(FORNIX_N_EIGEN)), np.full(FORNIX_N_EIGEN, np.nan))) }
                print("ERROR: fornix module failed for subject "+subject)
                fornix_ok = False

            # store data
            if FORNIX_SHAPE:
                metricsDict[subject].update(fornixShapeDict[subject])
                
            # store data
            if FORNIX_SCREENSHOT:
                imagesFornixDict[subject] = fornix_screenshot_outfile
            else:
                imagesFornixDict[subject] = []

            # store data
            statusDict[subject].update( { 'fornix' : fornix_ok } )

        # --------------------------------------------------------------------------
        # message
        print("Finished subject", subject, "at", time.strftime('%Y-%m-%d %H:%M %Z', time.localtime(time.time())))
        print("")

    # --------------------------------------------------------------------------
    # run optional modules: outlier detection

    if outlier is True:

        #
        try:

            # message
            print("---------------------------------------")
            print("Running outlier detection module ...")
            print("")

            # determine outlier-table and get data
            if outlier_table is None:
                outlierDict = outlierTable()
            else:
                outlierDict = dict()
                with open(outlier_table, newline='') as csvfile:
                    outlierCsv = csv.DictReader(csvfile, delimiter=',')
                    for row in outlierCsv:
                        outlierDict.update({row['label']: {'lower': float(row['lower']), 'upper': float(row['upper'])}})

            # process
            outlier_outdir = os.path.join(output_dir, 'outliers')
            n_outlier_sample_nonpar, n_outlier_sample_param, n_outlier_norms = outlierDetection(subjects, subjects_dir, outlier_outdir, outlierDict, min_no_subjects=OUTLIER_N_MIN)

            # create a dictionary from outlier module ouput
            outlierDict = dict()
            for subject in subjects:
                outlierDict.update({subject : {
                    'n_outlier_sample_nonpar' : n_outlier_sample_nonpar[subject],
                    'n_outlier_sample_param': n_outlier_sample_param[subject],
                    'n_outlier_norms': n_outlier_norms[subject]
                    }
                })

            # return
            outlier_ok = True

        #
        except:

            # create a dictionary from outlier module ouput
            outlierDict = dict()
            for subject in subjects:
                outlierDict.update({subject : {
                    'n_outlier_sample_nonpar' : np.nan,
                    'n_outlier_sample_param': np.nan,
                    'n_outlier_norms': np.nan
                    }
                })

            print("ERROR: outlier module failed")
            outlier_ok = False

        # store data
        for subject in subjects:
            metricsDict[subject].update(outlierDict[subject])

        # message
        print("Done")
        print("")

    # --------------------------------------------------------------------------
    # generate output

    metricsFieldnames = ['subject']

    # we pre-specify the fieldnames because we want to have this particular order
    metricsFieldnames.extend(['wm_snr_orig', 'gm_snr_orig', 'wm_snr_norm', 'gm_snr_norm', 'cc_size', 'holes_lh', 'holes_rh', 'defects_lh', 'defects_rh', 'topo_lh', 'topo_rh', 'con_snr_lh', 'con_snr_rh', 'rot_tal_x', 'rot_tal_y', 'rot_tal_z'])

    # collect other keys; need to iterate over subjects, because not all of them
    # necessarily have the same set of keys
    if shape is True:
        shapeKeys = list()
        for subject in distDict.keys():
            if len(distDict[subject])>0:
                shapeKeys = list(np.unique(shapeKeys + list(distDict[subject].keys())))
        metricsFieldnames.extend(shapeKeys)

    if fornix is True and FORNIX_SHAPE is True:
        fornixKeys = list()
        for subject in fornixShapeDict.keys():
            if len(fornixShapeDict[subject])>0:
                fornixKeys = list(np.unique(fornixKeys + list(fornixShapeDict[subject].keys())))
        metricsFieldnames.extend(sorted(fornixKeys))

    if outlier is True:
        outlierKeys = list()
        for subject in outlierDict.keys():
            if len(outlierDict[subject])>0:
                outlierKeys = list(np.unique(outlierKeys + list(outlierDict[subject].keys())))
        metricsFieldnames.extend(sorted(outlierKeys))

    # determine output file names
    path_data_file = os.path.join(output_dir, 'qatools-results.csv')
    path_html_file = os.path.join(output_dir, 'qatools-results.html')

    # write csv
    with open(path_data_file, 'w') as datafile:
        csvwriter = csv.DictWriter(datafile, fieldnames=metricsFieldnames, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writeheader()
        for subject in sorted(list(metricsDict.keys())):
            csvwriter.writerow(metricsDict[subject])

    # generate html output
    if (screenshots is True and screenshots_html is True) or (fornix is True and fornix_html is True):
        with open(path_html_file, 'w') as htmlfile:
            print("<html>", file=htmlfile)
            print("<head>", file=htmlfile)
            print("<title>FreeSurfer QAtools screenshots</title>", file=htmlfile)
            print("</head>", file=htmlfile)
            print("<style> body, h1, h2, h3, h4, h5, h6  { font-family: Arial, Helvetica, sans-serif ; } </style>)", file=htmlfile)
            print("<body style=\"background-color:Black\">", file=htmlfile)
            
            # screenshots
            if screenshots is True and screenshots_html is True:
                print("<h1 style=\"color:white\">Screenshots</h1>", file=htmlfile)
                for subject in sorted(list(imagesScreenshotsDict.keys())):
                    print("<h2 style=\"color:white\">Subject "+subject+"</h2>", file=htmlfile)
                    print("<p><a href=\""+os.path.join('screenshots', subject, os.path.basename(imagesScreenshotsDict[subject]))+"\">"
                        +"<img src=\""+os.path.join('screenshots', subject, os.path.basename(imagesScreenshotsDict[subject]))+"\" "
                        +"alt=\"Image for subject "+subject+"\" style=\"width:75vw;min_width:200px;\"></img></a></p>", file=htmlfile)
            # fornix           
            if fornix is True and fornix_html is True:
                print("<h1 style=\"color:white\">Fornix</h1>", file=htmlfile)
                for subject in sorted(list(imagesFornixDict.keys())):
                    print("<h2 style=\"color:white\">Subject "+subject+"</h2>", file=htmlfile)
                    print("<p><a href=\""+os.path.join('fornix', subject, os.path.basename(imagesFornixDict[subject]))+"\">"
                        +"<img src=\""+os.path.join('fornix', subject, os.path.basename(imagesFornixDict[subject]))+"\" "
                        +"alt=\"Image for subject "+subject+"\" style=\"width:75vw;min_width:200px;\"></img></a></p>", file=htmlfile)
            #
            print("</body>", file=htmlfile)
            print("</html>", file=htmlfile)
            



# ------------------------------------------------------------------------------
# run qatools

def run_qatools(subjects_dir, output_dir, subjects=None, subjects_file=None, shape=False, screenshots=False, screenshots_html=False, screenshots_base="default", screenshots_overlay="default", screenshots_surf="default", screenshots_views="default", screenshots_layout=None, fornix=False, fornix_html=False, outlier=False, outlier_table=None, fastsurfer=False):
    """
    a function to run the qatools submodules

    """

    # ------------------------------------------------------------------------------
    #

    # check arguments
    subjects_dir, output_dir, subjects, subjects_file, shape, screenshots, screenshots_html, screenshots_base, screenshots_overlay, screenshots_surf, screenshots_views, screenshots_layout, fornix, fornix_html, outlier, outlier_table, fastsurfer = _check_arguments(subjects_dir, output_dir, subjects, subjects_file, shape, screenshots, screenshots_html, screenshots_base, screenshots_overlay, screenshots_surf, screenshots_views, screenshots_layout, fornix, fornix_html, outlier, outlier_table, fastsurfer)

    # check packages
    _check_packages()

    # run qatools
    _do_qatools(subjects_dir, output_dir, subjects, shape, screenshots, screenshots_html, screenshots_base, screenshots_overlay, screenshots_surf, screenshots_views, screenshots_layout, fornix, fornix_html, outlier, outlier_table, fastsurfer)
