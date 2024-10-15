"""
This module provides the main functionality of the fsqc package.
"""

# ==============================================================================
# FUNCTIONS

# ------------------------------------------------------------------------------
# get_version()


def get_version():
    """
    A function to get the version of the 'fsqc' package.

    Returns
    -------
    str
        The version of the 'fsqc' package if installed; otherwise, "unknown".

    Notes
    -----
    This function uses the 'importlib.metadata' module to retrieve the package version.
    If the package is not installed, it returns "unknown".
    """
    from importlib import metadata

    try:
        # requires existing installation
        version = metadata.version("fsqc")
    except Exception:
        # fall-back if package is not installed, but run directly
        version = "unknown"

    return version


def get_help(print_help=True, return_help=False):
    """
    A function to return a help message.

    Parameters
    ----------
    print_help : bool, optional, default: True
        Whether to print the help message.
    return_help : bool, optional, default: False
        Whether to return the help message as a string.

    Returns
    -------
    None or str
        If `print_help` is True, the help message is printed. If `return_help`
        is True, the help message is returned as a string.
    """
    HELPTEXT = """

    fsqc


    ============
    Description:
    ============

    This is a set of quality assurance / quality control scripts for Fastsurfer-
    or Freesurfer-processed structural MRI data.

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

    - surfaces module

    This module allows for the automated generation of surface renderings of the
    left and right pial and inflated surfaces, overlaid with the aparc annotation.
    These images will be saved to the 'surfaces' subdirectory that will be created
    within the output directory.

    - skullstrip module

    This module allows for the automated generation cross-sections of the brain
    that are overlaid with the colored and semi-transparent brainmask. this allows
    to check the quality of the skullstripping in FreeSurfer. The resulting images
    will be saved to the 'skullstrip' subdirectory that will be created within the
    output directory.

    - fornix module

    This is a module to assess potential issues with the segmentation of the
    corpus callosum, which may incorrectly include parts of the fornix. To assess
    segmentation quality, a screenshot of the contours of the corpus callosum
    segmentation overlaid on the norm.mgz will be saved in the 'fornix'
    subdirectory of the output directory.

    - modules for the amygdala, hippocampus, and hypothalamus

    These modules evaluate potential missegmentations of the amygdala, hippocampus,
    and hypothalamus. To assess segmentation quality, screenshots will be created
    These modules require prior processing of the MR images with FreeSurfer's
    dedicated toolboxes for the segmentation of the amygdala and hippocampus, and
    the hypothalamus, respectively.

    - shape module

    The shape module will run a shapeDNA / brainprint analysis to compute distances
    of shape descriptors between lateralized brain structures. This can be used
    to identify discrepancies and irregularities between pairs of corresponding
    structures. The results will be included in the main csv table, and the output
    directory will also contain a "brainprint" subdirectory.

    - outlier module

    This is a module to detect extreme values among the subcortical ('aseg')
    segmentations as well as the cortical parcellations ('aparc'). If present,
    hypothalamic and hippocampal subsegmentations will also be included.

    The outlier detection is based on comparisons with the distributions of the
    sample as well as normative values taken from the literature (see References).

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
    match the nomenclature of the 'aseg.stats' and/or '[lr]h.aparc.stats' file.
    If cortical parcellations are included in the outlier table for a comparison
    with aparc.stats values, the labels must have a 'lh.' or 'rh.' prefix.
    `upper` and `lower` are user-specified upper and lower bounds.

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

        run_fsqc --subjects_dir <directory> --output_dir <directory>
                                  [--subjects SubjectID [SubjectID ...]]
                                  [--subjects-file <file>]
                                  [--screenshots] [--screenshots-html]
                                  [--surfaces] [--surfaces-html]
                                  [--skullstrip] [--skullstrip-html]
                                  [--fornix] [--fornix-html] [--hypothalamus]
                                  [--hypothalamus-html] [--hippocampus]
                                  [--hippocampus-html] [--hippocampus-label <label>]
                                  [--shape] [--outlier] [--fastsurfer]
                                  [--no-group] [--group-only]
                                  [--exit-on-error] [--skip-existing] [-h]

        required arguments:
          --subjects_dir <directory>
                                subjects directory with a set of Freesurfer- or
                                Fastsurfer-processed individual datasets.
          --output_dir <directory>
                                output directory

        optional arguments:
          --subjects SubjectID [SubjectID ...]
                                list of subject IDs
          --subjects-file <file>
                                filename of a file with subject IDs (one per line)
          --screenshots         create screenshots of individual brains
          --screenshots-html    create screenshots of individual brains and
                                html summary page
          --surfaces            create screenshots of individual brain surfaces
          --surfaces-html       create screenshots of individual brain surfaces
                                and html summary page
          --skullstrip          create screenshots of individual brainmasks
          --skullstrip-html     create screenshots of individual brainmasks and
                                html summary page
          --fornix              check fornix segmentation
          --fornix-html         check fornix segmentation and create html summary
                                page of fornix evaluation
          --hypothalamus        check hypothalamic segmentation
          --hypothalamus-html   check hypothalamic segmentation and create html
                                summary page
          --hippocampus         check segmentation of hippocampus and amygdala
          --hippocampus-html    check segmentation of hippocampus and amygdala
                                and create html summary page
          --hippocampus-label   specify label for hippocampus segmentation files
                                (default: None). The full filename is then
                                [lr]h.hippoAmygLabels-<LABEL>.FSvoxelSpace.mgz
          --shape               run shape analysis
          --outlier             run outlier detection
          --outlier-table       specify normative values (only in conjunction with
                                --outlier)
          --fastsurfer          use FastSurfer instead of FreeSurfer output
          --no-group            run script in subject-level mode. will compute
                                individual files and statistics, but not create
                                group-level summaries.
          --group-only          run script in group mode. will create group-level
                                summaries from existing inputs. needs to be run
                                on output  directory with already existing
                                results
          --exit-on-error       terminate the program when encountering an error;
                                otherwise, try to continue with the next module or
                                case
          --skip-existing       skips processing for a given case if output
                                already exists, even with possibly different
                                parameters or settings.

        getting help:
          -h, --help            display this help message and exit
          --more-help           display extensive help message and exit

        expert options:
          --screenshots_base <image>
                                filename of an image that should be used instead of
                                norm.mgz as the base image for the screenshots. Can be
                                an individual file (which would not be appropriate for
                                multi-subject analysis) or can be a file without
                                pathname and with the same filename across subjects
                                within the 'mri' subdirectory of an individual FreeSurfer
                                results directory (which would be appropriate for multi-
                                subject analysis).
          --screenshots_overlay <image>
                                path to an image that should be used instead of
                                aseg.mgz as the overlay image for the screenshots;
                                can also be none. Can be an individual file (which would
                                not be appropriate for multi-subject analysis) or can be
                                a file without pathname and with the same filename across
                                subjects within the 'mri' subdirectory of an individual
                                FreeSurfer results directory (which would be appropriate
                                for multi-subject analysis).
          --screenshots_surf <surf> [<surf> ...]
                                one or more surface files that should be used instead
                                of [lr]h.white and [lr]h.pial; can also be none.
                                Can be one or more individual file(s) (which would not be
                                appropriate for multi-subject analysis) or can be a (list
                                of) file(s) without pathname and with the same filename
                                across subjects within the 'surf' subdirectory of an
                                individual FreeSurfer results directory (which would be
                                appropriate for multi-subject analysis).
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

    As an alternative to their command-line usage, the fsqc scripts can also be run
    within a pure Python environment, i.e. installed and imported as a Python package.

    Use `import fsqc` (or sth. equivalent) to import the package within a
    Python environment, and use the `run_fsqc` function from the `fsqc` module to
    run an analysis:

    ```python
    import fsqc
    fsqc.run_fsqc(subjects_dir='/my/subjects/dir', output_dir='/my/output/dir')
    ```

    See `fsqc.get_help()` for further usage info and additional options.


    =============
    Requirements:
    =============

    At least one subject whose structural MR image was processed with Freesurfer
    6.0 or later, or FastSurfer v1.1 or later (including the surface pipeline).

    A Python version >= 3.8 is required to run this script.

    Required packages include (among others) the nibabel and skimage package for
    the core functionality, plus the the matplotlib, pandas, and transform3d
    packages for some optional functions and modules. See the `requirements.txt`
    file for a complete list. Use `pip3 install -r requirements.txt` to install
    these packages.

    This software has been tested on Ubuntu 20.04.

    A working [FreeSurfer](https://freesurfer.net) installation (version 6 or
    newer) is required for running the 'shape' module of this toolbox. Also make
    sure that FreeSurfer is sourced (i.e., `FREESURFER_HOME` is set as an
    environment variable) before running an analysis.

    =============
    Known Issues:
    =============

    - Aborted / restarted recon-all runs: the program will analyze recon-all
      logfiles, and may fail or return erroneous results if the logfile is
      appended by multiple restarts of recon-all runs. Ideally, the logfile should
      therefore consist of just a single, successful recon-all run.
    - High-resolution data: Prior to update v1.4, the screenshots and fornix module
      did not work well with high-resolution data that was processed using the
      -cm flag in recon-all. With update v1.4 this has been fixed for the
      screenhots module, but the fornix module is still experimental for
      high-resolution data.


    ========
    Authors:
    ========

    - fsqc: Kersten Diers, Tobias Wolff, and Martin Reuter.
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
    An internal function to parse input arguments.

    Returns
    -------
    argparse.Namespace or None
        An object holding parsed command-line arguments or None if extensive help is requested.

    Notes
    -----
    This function is for internal use and parses input arguments using the 'argparse' module.
    The returned object contains the values of the parsed arguments.
    """
    # imports
    import argparse
    import sys

    # parse
    parser = argparse.ArgumentParser(
        description="""
        This program takes existing Freesurfer or Fastsurfer analysis results of
        one or more subjects and computes a set of quality metrics. These will
        be reported in a summary csv table.

        For a description of these metrics, see the gitlab/github page or the
        header section of this script.

        Further modules are available to produce graphical outputs.
        """,
        add_help=False,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "--subjects_dir",
        dest="subjects_dir",
        help="subjects directory with a set of Freesurfer processed individual datasets.",
        metavar="<directory>",
        required=True,
    )
    required.add_argument(
        "--output_dir",
        dest="output_dir",
        help="output directory",
        metavar="<directory>",
        required=True,
    )

    optional = parser.add_argument_group("optional arguments")
    optional.add_argument(
        "--subjects",
        dest="subjects",
        help="list of subject IDs. If omitted, all suitable sub-directories within the subjects directory will be used.",
        default=None,
        nargs="+",
        metavar="SubjectID",
        required=False,
    )
    optional.add_argument(
        "--subjects-file",
        dest="subjects_file",
        help="filename with list of subject IDs (one per line). If omitted, all suitable sub-directories within the subjects directory will be used.",
        default=None,
        metavar="<filename>",
        required=False,
    )
    optional.add_argument(
        "--shape",
        dest="shape",
        help="run shape analysis",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--screenshots",
        dest="screenshots",
        help="create screenshots of individual brains",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--screenshots-html",
        dest="screenshots_html",
        help="create screenshots of individual brains with html summary page",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--surfaces",
        dest="surfaces",
        help="create surface plots of individual brains",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--surfaces-html",
        dest="surfaces_html",
        help="create surface plots of individual brains with html summary page",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--surfaces_views",
        dest="surfaces_views",
        help="Specify camera views for surface images. Choose from: anterior, posterior, left, right, superior, inferior",
        default=["left", "right", "superior", "inferior"],
        type=str,
        nargs="+",
        required=False,
    )
    optional.add_argument(
        "--skullstrip",
        dest="skullstrip",
        help="create brainmask plots of individual brains",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--skullstrip-html",
        dest="skullstrip_html",
        help="create brainmask plots of individual brains with html summary page",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--fornix",
        dest="fornix",
        help="check fornix segmentation",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--fornix-html",
        dest="fornix_html",
        help="check fornix segmentation and create html summary page",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--hypothalamus",
        dest="hypothalamus",
        help="check hypothalamus segmentation",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--hypothalamus-html",
        dest="hypothalamus_html",
        help="check hypothalamus segmentation and create html summary page for evaluation",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--hippocampus",
        dest="hippocampus",
        help="check hippocampus segmentation",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--hippocampus-html",
        dest="hippocampus_html",
        help="check hippocampus segmentation and create html summary page for evaluation",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--hippocampus-label",
        dest="hippocampus_label",
        help="specify custom label for hippocampal segmentation files",
        default=None,
        metavar="<string>",
        required=False,
    )
    optional.add_argument(
        "--outlier",
        dest="outlier",
        help="run outlier detection",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--outlier-table",
        dest="outlier_table",
        help="specify normative values",
        default=None,
        metavar="<filename>",
        required=False,
    )
    optional.add_argument(
        "--fastsurfer",
        dest="fastsurfer",
        help="use FastSurfer output",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--no-group",
        dest="no_group",
        help="run script in subject-level mode",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--group-only",
        dest="group_only",
        help="run script in group mode",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--exit-on-error",
        dest="exit_on_error",
        help="terminate the program when encountering an error",
        default=False,
        action="store_true",
        required=False,
    )
    optional.add_argument(
        "--skip-existing",
        dest="skip_existing",
        help="skip processing if output already exists",
        default=False,
        action="store_true",
        required=False,
    )

    expert = parser.add_argument_group("expert arguments")
    expert.add_argument(
        "--screenshots_base",
        dest="screenshots_base",
        help="base image for screenshots",
        default="default",
        metavar="<base image for screenshots>",
        required=False,
    )
    expert.add_argument(
        "--screenshots_overlay",
        dest="screenshots_overlay",
        help="overlay image for screenshots",
        default="default",
        metavar="<overlay image for screenshots>",
        required=False,
    )
    expert.add_argument(
        "--screenshots_surf",
        dest="screenshots_surf",
        help="surface(s) for screenshots",
        default="default",
        nargs="+",
        metavar="<surface(s) for screenshots>",
        required=False,
    )
    expert.add_argument(
        "--screenshots_views",
        dest="screenshots_views",
        help="view specification for screenshots",
        default="default",
        nargs="+",
        metavar="<dimension=coordinate>",
        required=False,
    )
    expert.add_argument(
        "--screenshots_layout",
        dest="screenshots_layout",
        help="layout for screenshots",
        default="default",
        nargs=2,
        metavar="<num>",
        required=False,
    )
    expert.add_argument(
        "--screenshots_orientation",
        dest="screenshots_orientation",
        help=argparse.SUPPRESS,
        default="radiological",
        nargs=1,
        metavar="<neurological|radiological>",
        required=False,
    )  # this is currently a hidden "expert" option

    help = parser.add_argument_group("getting help")
    help.add_argument(
        "-h", "--help", help="display this help message and exit", action="help"
    )
    help.add_argument(
        "--more-help",
        dest="more_help",
        help="display extensive help message and exit",
        default=False,
        action="store_true",
        required=False,
    )

    # check if there are any inputs; if not, print help and exit
    if len(sys.argv) == 1:
        args = parser.parse_args(["--help"])
    elif len(sys.argv) == 2 and sys.argv[1] == "--more-help":
        get_help()
        return None
    else:
        args = parser.parse_args()

    # check for extensive help (if it exists among other arguments)
    if args.more_help:
        get_help()
        return None

    # prepare output
    argsDict = dict()
    argsDict["subjects_dir"] = args.subjects_dir
    argsDict["output_dir"] = args.output_dir
    argsDict["subjects"] = args.subjects
    argsDict["subjects_file"] = args.subjects_file
    argsDict["shape"] = args.shape
    argsDict["screenshots"] = args.screenshots
    argsDict["screenshots_html"] = args.screenshots_html
    argsDict["screenshots_base"] = args.screenshots_base
    argsDict["screenshots_overlay"] = args.screenshots_overlay
    argsDict["screenshots_surf"] = args.screenshots_surf
    argsDict["screenshots_views"] = args.screenshots_views
    argsDict["screenshots_layout"] = args.screenshots_layout
    argsDict["screenshots_orientation"] = args.screenshots_orientation
    argsDict["surfaces"] = args.surfaces
    argsDict["surfaces_html"] = args.surfaces_html
    argsDict["surfaces_views"] = args.surfaces_views
    argsDict["skullstrip"] = args.skullstrip
    argsDict["skullstrip_html"] = args.skullstrip_html
    argsDict["fornix"] = args.fornix
    argsDict["fornix_html"] = args.fornix_html
    argsDict["hypothalamus"] = args.hypothalamus
    argsDict["hypothalamus_html"] = args.hypothalamus_html
    argsDict["hippocampus"] = args.hippocampus
    argsDict["hippocampus_html"] = args.hippocampus_html
    argsDict["hippocampus_label"] = args.hippocampus_label
    argsDict["outlier"] = args.outlier
    argsDict["outlier_table"] = args.outlier_table
    argsDict["fastsurfer"] = args.fastsurfer
    argsDict["no_group"] = args.no_group
    argsDict["group_only"] = args.group_only
    argsDict["exit_on_error"] = args.exit_on_error
    argsDict["skip_existing"] = args.skip_existing

    #
    return argsDict


# ------------------------------------------------------------------------------
# check arguments


def _check_arguments(argsDict):
    """
    Check input arguments for validity.

    Parameters
    ----------
    argsDict : dict
        Dictionary containing input arguments.

    Raises
    ------
    FileNotFoundError
        If the specified subjects directory does not exist.
    ValueError
        If both --subjects and --subjects-file are specified.
        If subjects file is specified but does not exist.
        If neither --subjects nor --subjects-file is specified and no subjects are found in the subjects directory.
        If --screenshots and --screenshots-html are both True and the screenshots directory cannot be created.
        If --hippocampus or --hippocampus-html is True but --hippocampus-label is not specified.
        If no subjects are found after file checks.

    Returns
    -------
    dict
        Updated dictionary of input arguments.
    """
    # --------------------------------------------------------------------------
    # imports

    import logging
    import os
    import tempfile
    import warnings

    logging.captureWarnings(True)

    # --------------------------------------------------------------------------
    # check arguments
    # check if subject directory exists
    if os.path.isdir(argsDict["subjects_dir"]):
        logging.info("Found subjects directory " + argsDict["subjects_dir"])
    else:
        raise FileNotFoundError(
            "ERROR: subjects directory "
            + argsDict["subjects_dir"]
            + " is not an existing directory"
        )

    # check if output directory exists or can be created and is writable
    # -> this is now done during start_logging()

    # check if both subjects and subjects-file were specified
    if argsDict["subjects"] is not None and argsDict["subjects_file"] is not None:
        raise ValueError(
            "ERROR: Use either --subjects or --subjects-file (but not both)."
        )

    # check if subjects-file exists and get data
    if argsDict["subjects_file"] is not None:
        if os.path.isfile(argsDict["subjects_file"]):
            # read file
            with open(argsDict["subjects_file"]) as subjects_file_f:
                argsDict["subjects"] = subjects_file_f.read().splitlines()
        else:
            raise FileNotFoundError(
                "ERROR: Could not find subjects file", argsDict["subjects_file"]
            )

    # if neither subjects nor subjects_file are given, get contents of the subject
    # directory and check if aseg.stats (as a proxy) exists
    if argsDict["subjects"] is None and argsDict["subjects_file"] is None:
        argsDict["subjects"] = []
        for subject in os.listdir(argsDict["subjects_dir"]):
            path_aseg_stat = os.path.join(
                argsDict["subjects_dir"], subject, "stats", "aseg.stats"
            )
            if os.path.isfile(path_aseg_stat):
                logging.info("Found subject " + subject)
                argsDict["subjects"].extend([subject])

    # check if only one of no_group and group_only is true
    if argsDict["no_group"] is True and argsDict["group_only"] is True:
        raise ValueError("ERROR: Use either --no-group or --group-only (but not both).")

    # skip-existing cannot be used with group-only
    if argsDict["skip_existing"] is True and argsDict["group_only"] is True:
        raise ValueError(
            "ERROR: Use either --skip_existing or --group-only (but not both)."
        )

    # check if screenshots subdirectory exists or can be created and is writable
    if argsDict["screenshots"] is True or argsDict["screenshots_html"] is True:
        if os.path.isdir(os.path.join(argsDict["output_dir"], "screenshots")):
            logging.info(
                "Found screenshots directory "
                + os.path.join(argsDict["output_dir"], "screenshots")
            )
        else:
            try:
                os.mkdir(os.path.join(argsDict["output_dir"], "screenshots"))
            except Exception as e:
                logging.error(
                    "ERROR: cannot create screenshots directory "
                    + os.path.join(argsDict["output_dir"], "screenshots")
                )
                logging.error("Reason: " + str(e))
                raise

            try:
                testfile = tempfile.TemporaryFile(
                    dir=os.path.join(argsDict["output_dir"], "screenshots")
                )
                testfile.close()
            except Exception as e:
                logging.error(
                    "ERROR: "
                    + os.path.join(argsDict["output_dir"], "screenshots")
                    + " not writeable"
                )
                logging.error("Reason: " + str(e))
                raise

    # check screenshots_overlay (this is either 'default' or 'none' or a single file or a single generic filename; further checks prior to execution of the screenshots module)
    if argsDict["screenshots_overlay"].lower() == "none":
        argsDict["screenshots_overlay"] = None
        logging.info("Found screenshot overlays set to None")

    # check screenshots_surf (this is either 'default' or 'none' or a single file or a list; further checks prior to execution of the screenshots module)
    if not isinstance(argsDict["screenshots_surf"], list):
        if argsDict["screenshots_surf"].lower() == "none":
            argsDict["screenshots_surf"] = None
            logging.info("Found screenshot surfaces set to None")

    # check if screenshots_views argument can be evaluated
    if isinstance(argsDict["screenshots_views"], list):
        for x in argsDict["screenshots_views"]:
            isXYZ = (
                x.split("=")[0] == "x"
                or x.split("=")[0] == "y"
                or x.split("=")[0] == "z"
            )
            try:
                int(x.split("=")[1])
                isConvertible = True
            except Exception:
                isConvertible = False
            if not isXYZ or not isConvertible:
                logging.error("ERROR: could not understand " + x)
                logging.error(
                    "       the --screenshots_views argument can only contain one or more x=<numeric> y=<numeric> z=<numeric> expressions."
                )
                logging.error("       for example: --screenshots_views x=0")
                logging.error("                    --screenshots_views x=-10 x=10 y=0")
                logging.error("                    --screenshots_views x=0 z=0")
                raise ValueError

        logging.info(
            "Found screenshot coordinates " + " ".join(argsDict["screenshots_views"])
        )
        argsDict["screenshots_views"] = [
            (y[0], int(y[1]))
            for y in [x.split("=") for x in argsDict["screenshots_views"]]
        ]

    # check screenshots_layout
    if argsDict["screenshots_layout"] != "default":
        if all([x.isdigit() for x in argsDict["screenshots_layout"]]):
            argsDict["screenshots_layout"] = [
                int(x) for x in argsDict["screenshots_layout"]
            ]
        else:
            raise TypeError(
                "ERROR: screenshots_layout argument can only contain integer numbers."
            )

    # check screenshots_orientation
    if argsDict["screenshots_orientation"] != "neurological" and argsDict[
        "screenshots_orientation"
    ] != "radiological":
        raise TypeError(
            "ERROR: screenshots_orientation argument must be either 'neurological' or 'radiological'."
        )
    else:
        logging.info(
            "Found screenshot orientation set to "
            + argsDict["screenshots_orientation"]
        )

    # check if skullstrip subdirectory exists or can be created and is writable
    if argsDict["skullstrip"] is True or argsDict["skullstrip_html"] is True:
        if os.path.isdir(os.path.join(argsDict["output_dir"], "skullstrip")):
            logging.info(
                "Found skullstrip directory "
                + os.path.join(argsDict["output_dir"], "skullstrip")
            )
        else:
            try:
                os.mkdir(os.path.join(argsDict["output_dir"], "skullstrip"))
            except Exception as e:
                logging.error(
                    "ERROR: cannot create skullstrip directory "
                    + os.path.join(argsDict["output_dir"], "skullstrip")
                )
                logging.error("Reason: " + str(e))
                raise

            try:
                testfile = tempfile.TemporaryFile(
                    dir=os.path.join(argsDict["output_dir"], "skullstrip")
                )
                testfile.close()
            except Exception as e:
                logging.error(
                    "ERROR: "
                    + os.path.join(argsDict["output_dir"], "skullstrip")
                    + " not writeable"
                )
                logging.error("Reason: " + str(e))
                raise

    # check if fornix subdirectory exists or can be created and is writable
    if argsDict["fornix"] is True or argsDict["fornix_html"] is True:
        if os.path.isdir(os.path.join(argsDict["output_dir"], "fornix")):
            logging.info(
                "Found fornix directory "
                + os.path.join(argsDict["output_dir"], "fornix")
            )
        else:
            try:
                os.mkdir(os.path.join(argsDict["output_dir"], "fornix"))
            except Exception as e:
                logging.error(
                    "ERROR: cannot create fornix directory "
                    + os.path.join(argsDict["output_dir"], "fornix")
                )
                logging.error("Reason: " + str(e))
                raise

            try:
                testfile = tempfile.TemporaryFile(
                    dir=os.path.join(argsDict["output_dir"], "fornix")
                )
                testfile.close()
            except Exception as e:
                logging.error(
                    "ERROR: "
                    + os.path.join(argsDict["output_dir"], "fornix")
                    + " not writeable"
                )
                logging.error("Reason: " + str(e))
                raise

    # check if hypothalamus subdirectory exists or can be created and is writable
    if argsDict["hypothalamus"] is True or argsDict["hypothalamus_html"] is True:
        if os.path.isdir(os.path.join(argsDict["output_dir"], "hypothalamus")):
            logging.info(
                "Found hypothalamus directory "
                + os.path.join(argsDict["output_dir"], "hypothalamus")
            )
        else:
            try:
                os.mkdir(os.path.join(argsDict["output_dir"], "hypothalamus"))
            except Exception as e:
                logging.error(
                    "ERROR: cannot create hypothalamus directory "
                    + os.path.join(argsDict["output_dir"], "hypothalamus")
                )
                logging.error("Reason: " + str(e))
                raise

            try:
                testfile = tempfile.TemporaryFile(
                    dir=os.path.join(argsDict["output_dir"], "hypothalamus")
                )
                testfile.close()
            except Exception as e:
                logging.error(
                    "ERROR: "
                    + os.path.join(argsDict["output_dir"], "hypothalamus")
                    + " not writeable"
                )
                logging.error("Reason: " + str(e))
                raise

    # check if hippocampus subdirectory exists or can be created and is writable
    if argsDict["hippocampus"] is True or argsDict["hippocampus_html"] is True:
        if os.path.isdir(os.path.join(argsDict["output_dir"], "hippocampus")):
            logging.info(
                "Found hippocampus directory "
                + os.path.join(argsDict["output_dir"], "hippocampus")
            )
        else:
            try:
                os.mkdir(os.path.join(argsDict["output_dir"], "hippocampus"))
            except Exception as e:
                logging.error(
                    "ERROR: cannot create hippocampus directory "
                    + os.path.join(argsDict["output_dir"], "hippocampus")
                )
                logging.error("Reason: " + str(e))
                raise

            try:
                testfile = tempfile.TemporaryFile(
                    dir=os.path.join(argsDict["output_dir"], "hippocampus")
                )
                testfile.close()
            except Exception as e:
                logging.error(
                    "ERROR: "
                    + os.path.join(argsDict["output_dir"], "hippocampus")
                    + " not writeable"
                )
                logging.error("Reason: " + str(e))
                raise

    # check if label file is given
    if (
        argsDict["hippocampus"] is True or argsDict["hippocampus_html"] is True
    ) and argsDict["hippocampus_label"] is None:
        logging.error(
            "ERROR: The --hippocampus-label <LABEL> argument must be specified if using --hippocampus or --hippocampus-html"
        )
        logging.error(
            "       The filename of the segmentation file must correspond to [lr]h.hippoAmygLabels-<LABEL>.FSvoxelSpace.mgz"
        )
        raise ValueError

    # check if shape subdirectory exists or can be created and is writable
    if argsDict["shape"] is True:
        if os.path.isdir(os.path.join(argsDict["output_dir"], "brainprint")):
            logging.info(
                "Found brainprint directory "
                + os.path.join(argsDict["output_dir"], "brainprint")
            )
        else:
            try:
                os.makedirs(os.path.join(argsDict["output_dir"], "brainprint"))
            except Exception as e:
                logging.error(
                    "ERROR: cannot create brainprint directory "
                    + os.path.join(argsDict["output_dir"], "brainprint")
                )
                logging.error("Reason: " + str(e))
                raise

            try:
                testfile = tempfile.TemporaryFile(
                    dir=os.path.join(argsDict["output_dir"], "brainprint")
                )
                testfile.close()
            except Exception as e:
                logging.error(
                    "ERROR: "
                    + os.path.join(argsDict["output_dir"], "brainprint")
                    + " not writeable"
                )
                logging.error("Reason: " + str(e))
                raise

    # check if outlier subdirectory exists or can be created and is writable
    if argsDict["outlier"] is True:
        if os.path.isdir(os.path.join(argsDict["output_dir"], "outliers")):
            logging.info(
                "Found outliers directory "
                + os.path.join(argsDict["output_dir"], "outliers")
            )
        else:
            try:
                os.makedirs(os.path.join(argsDict["output_dir"], "outliers"))
            except Exception as e:
                logging.error(
                    "ERROR: cannot create outliers directory "
                    + os.path.join(argsDict["output_dir"], "outliers")
                )
                logging.error("Reason: " + str(e))
                raise

            try:
                testfile = tempfile.TemporaryFile(
                    dir=os.path.join(argsDict["output_dir"], "outliers")
                )
                testfile.close()
            except Exception as e:
                logging.error(
                    "ERROR: "
                    + os.path.join(argsDict["output_dir"], "outliers")
                    + " not writeable"
                )
                logging.error("Reason: " + str(e))
                raise

    # check if outlier-table exists if it was given, otherwise exit
    if argsDict["outlier_table"] is not None:
        if os.path.isfile(argsDict["outlier_table"]):
            logging.info(
                "Found table with normative values " + argsDict["outlier_table"]
            )
        else:
            raise FileNotFoundError(
                "ERROR: Could not find table with normative values ",
                argsDict["outlier_table"],
            )

    # check for required files
    subjects_to_remove = list()
    for subject in argsDict["subjects"]:
        # -files: stats/aseg.stats
        path_check = os.path.join(
            argsDict["subjects_dir"], subject, "stats", "aseg.stats"
        )
        if not os.path.isfile(path_check):
            warnings.warn("Could not find " + path_check + " for subject " + subject,
                    stacklevel = 2)
            subjects_to_remove.extend([subject])

        # -files: surf/[lr]h.w-g.pct.mgh, label/[lr]h.cortex.label
        path_check = os.path.join(
            argsDict["subjects_dir"], subject, "surf", "lh.w-g.pct.mgh"
        )
        if not os.path.isfile(path_check):
            warnings.warn("Could not find " + path_check + " for subject " + subject,
                    stacklevel = 2)
            subjects_to_remove.extend([subject])

        path_check = os.path.join(
            argsDict["subjects_dir"], subject, "surf", "rh.w-g.pct.mgh"
        )
        if not os.path.isfile(path_check):
            warnings.warn("Could not find " + path_check + " for subject " + subject,
                    stacklevel = 2)
            subjects_to_remove.extend([subject])

        path_check = os.path.join(
            argsDict["subjects_dir"], subject, "label", "lh.cortex.label"
        )
        if not os.path.isfile(path_check):
            warnings.warn("Could not find " + path_check + " for subject " + subject,
                    stacklevel = 2)
            subjects_to_remove.extend([subject])

        path_check = os.path.join(
            argsDict["subjects_dir"], subject, "label", "rh.cortex.label"
        )
        if not os.path.isfile(path_check):
            warnings.warn("Could not find " + path_check + " for subject " + subject,
                    stacklevel = 2)
            subjects_to_remove.extend([subject])

        # -files: mri/transforms/talairach.lta
        path_check = os.path.join(
            argsDict["subjects_dir"], subject, "mri", "transforms", "talairach.lta"
        )
        if not os.path.isfile(path_check):
            warnings.warn("Could not find " + path_check + " for subject " + subject,
                    stacklevel = 2)
            subjects_to_remove.extend([subject])

        # -files: mri/norm.mgz, mri/aseg.mgz, mri/aparc+aseg.mgz for FreeSurfer
        # -files: mri/norm.mgz, mri/aseg.mgz, mri/aparc.DKTatlas+aseg.deep.mgz for FastSurfer
        path_check = os.path.join(argsDict["subjects_dir"], subject, "mri", "norm.mgz")
        if not os.path.isfile(path_check):
            warnings.warn("Could not find " + path_check + " for subject " + subject,
                    stacklevel = 2)
            subjects_to_remove.extend([subject])

        path_check = os.path.join(argsDict["subjects_dir"], subject, "mri", "aseg.mgz")
        if not os.path.isfile(path_check):
            warnings.warn("Could not find " + path_check + " for subject " + subject,
                    stacklevel = 2)
            subjects_to_remove.extend([subject])

        if argsDict["fastsurfer"] is True:
            path_check = os.path.join(
                argsDict["subjects_dir"], subject, "mri", "aparc.DKTatlas+aseg.deep.mgz"
            )
        else:
            path_check = os.path.join(
                argsDict["subjects_dir"], subject, "mri", "aparc+aseg.mgz"
            )
        if not os.path.isfile(path_check):
            warnings.warn("Could not find " + path_check + " for subject " + subject,
                    stacklevel = 2)
            subjects_to_remove.extend([subject])

        # -files: scripts/recon-all.log
        path_check = os.path.join(
            argsDict["subjects_dir"], subject, "scripts", "recon-all.log"
        )
        if not os.path.isfile(path_check):
            warnings.warn("Could not find " + path_check + " for subject " + subject,
                    stacklevel = 2)
            subjects_to_remove.extend([subject])

        # check screenshots
        if (
            argsDict["screenshots"] is True or argsDict["screenshots_html"] is True
        ) and argsDict["screenshots_surf"] == "default":
            # -files: surf/[lr]h.white (optional), surf/[lr]h.pial (optional)
            path_check = os.path.join(
                argsDict["subjects_dir"], subject, "surf", "lh.white"
            )
            if not os.path.isfile(path_check):
                warnings.warn(
                    "Could not find " + path_check + " for subject " + subject,
                    stacklevel = 2
                )
                subjects_to_remove.extend([subject])

            path_check = os.path.join(
                argsDict["subjects_dir"], subject, "surf", "rh.white"
            )
            if not os.path.isfile(path_check):
                warnings.warn(
                    "Could not find " + path_check + " for subject " + subject,
                    stacklevel = 2
                )
                subjects_to_remove.extend([subject])

            path_check = os.path.join(
                argsDict["subjects_dir"], subject, "surf", "lh.pial"
            )
            if not os.path.isfile(path_check):
                warnings.warn(
                    "Could not find " + path_check + " for subject " + subject,
                    stacklevel = 2
                )
                subjects_to_remove.extend([subject])

            path_check = os.path.join(
                argsDict["subjects_dir"], subject, "surf", "rh.pial"
            )
            if not os.path.isfile(path_check):
                warnings.warn(
                    "Could not find " + path_check + " for subject " + subject,
                    stacklevel = 2
                )
                subjects_to_remove.extend([subject])

        # check surfaces
        if argsDict["surfaces"] is True or argsDict["surfaces_html"] is True:
            # -files: surf/[lr]h.white (optional), surf/[lr]h.inflated (optional), label/[lr]h.aparc.annot (optional) for freesurfer
            # -files: surf/[lr]h.white (optional), surf/[lr]h.inflated (optional), label/[lr]h.aparc.DKTatlas.annot (optional) for fastsurfer
            path_check = os.path.join(
                argsDict["subjects_dir"], subject, "surf", "lh.inflated"
            )
            if not os.path.isfile(path_check):
                warnings.warn(
                    "Could not find " + path_check + " for subject " + subject,
                    stacklevel = 2
                )
                subjects_to_remove.extend([subject])

            path_check = os.path.join(
                argsDict["subjects_dir"], subject, "surf", "rh.inflated"
            )
            if not os.path.isfile(path_check):
                warnings.warn(
                    "Could not find " + path_check + " for subject " + subject,
                    stacklevel = 2
                )
                subjects_to_remove.extend([subject])

            path_check = os.path.join(
                argsDict["subjects_dir"], subject, "surf", "lh.pial"
            )
            if not os.path.isfile(path_check):
                warnings.warn(
                    "Could not find " + path_check + " for subject " + subject,
                    stacklevel = 2
                )
                subjects_to_remove.extend([subject])

            path_check = os.path.join(
                argsDict["subjects_dir"], subject, "surf", "rh.pial"
            )
            if not os.path.isfile(path_check):
                warnings.warn(
                    "Could not find " + path_check + " for subject " + subject,
                    stacklevel = 2
                )
                subjects_to_remove.extend([subject])

            if argsDict["fastsurfer"] is True:
                path_check = os.path.join(
                    argsDict["subjects_dir"],
                    subject,
                    "label",
                    "lh.aparc.DKTatlas.annot",
                )
            else:
                path_check = os.path.join(
                    argsDict["subjects_dir"], subject, "label", "lh.aparc.annot"
                )
            if not os.path.isfile(path_check):
                warnings.warn(
                    "Could not find " + path_check + " for subject " + subject,
                    stacklevel = 2
                )
                subjects_to_remove.extend([subject])

            if argsDict["fastsurfer"] is True:
                path_check = os.path.join(
                    argsDict["subjects_dir"],
                    subject,
                    "label",
                    "rh.aparc.DKTatlas.annot",
                )
            else:
                path_check = os.path.join(
                    argsDict["subjects_dir"], subject, "label", "rh.aparc.annot"
                )
            if not os.path.isfile(path_check):
                warnings.warn(
                    "Could not find " + path_check + " for subject " + subject,
                    stacklevel = 2
                )
                subjects_to_remove.extend([subject])

        if len(argsDict["surfaces_views"]) > 0:
            _views_available = [
                "anterior",
                "posterior",
                "left",
                "right",
                "superior",
                "inferior",
            ]
            for v in argsDict["surfaces_views"].copy():
                if v not in _views_available:
                    logging.error(f"ERROR: Skip unexpected view for surface plots: {v}")
                    argsDict["surfaces_views"].remove(v)

        # check skullstrip
        if argsDict["skullstrip"] is True or argsDict["skullstrip_html"] is True:
            # -files: surf/[lr]h.white (optional), surf/[lr]h.inflated (optional), label/[lr]h.aparc.annot (optional)
            path_check = os.path.join(
                argsDict["subjects_dir"], subject, "mri", "orig.mgz"
            )
            if not os.path.isfile(path_check):
                warnings.warn(
                    "Could not find " + path_check + " for subject " + subject,
                    stacklevel = 2
                )
                subjects_to_remove.extend([subject])

            path_check = os.path.join(
                argsDict["subjects_dir"], subject, "mri", "brainmask.mgz"
            )
            if not os.path.isfile(path_check):
                warnings.warn(
                    "Could not find " + path_check + " for subject " + subject,
                    stacklevel = 2
                )
                subjects_to_remove.extend([subject])

        # check fornix
        if argsDict["fornix"] is True or argsDict["fornix_html"] is True:
            # -files: mri/transforms/cc_up.lta
            path_check = os.path.join(
                argsDict["subjects_dir"], subject, "mri", "transforms", "cc_up.lta"
            )
            if not os.path.isfile(path_check):
                warnings.warn(
                    "Could not find " + path_check + " for subject " + subject,
                    stacklevel = 2
                )
                subjects_to_remove.extend([subject])

    # remove subjects with missing files after creating unique list
    [argsDict["subjects"].remove(x) for x in list(set(subjects_to_remove))]

    # check if we have any subjects after all
    if not argsDict["subjects"]:
        raise ValueError("ERROR: no subjects to process")

    # now return
    return argsDict


# ------------------------------------------------------------------------------
# check packages


def _check_packages():
    """
    an internal function to check required / recommended packages

    """

    import importlib.util

    import packaging.version

    if importlib.util.find_spec("skimage") is None:
        raise ImportError(
            "ERROR: the 'skimage' package is required for running this script, please install.\n"
        )

    if importlib.util.find_spec("pandas") is None:
        raise ImportError(
            "ERROR: the 'pandas' package is required for running this script, please install.\n"
        )

    if importlib.util.find_spec("matplotlib") is None:
        raise ImportError(
            "ERROR: the 'matplotlib' package is required for running this script, please install.\n"
        )

    if importlib.util.find_spec("lapy") is not None:
        import lapy as lp

        if not hasattr(lp, "__version__"):
            raise ImportError(
                "ERROR: Could not determine version of the 'lapy' package (see README.md for details on installation)"
            )
        elif packaging.version.parse(lp.__version__) < packaging.version.parse("1.0"):
            raise ImportError(
                "ERROR: A version >=1.0 of the 'lapy' package is required for surface plots (see README.md for details on installation)"
            )
    else:
        raise ImportError(
            "ERROR: Could not find the 'lapy' package (see README.md for details on installation)"
        )

    if importlib.util.find_spec("brainprint") is None:
        raise ImportError(
            "ERROR: could not import the brainprint package, is it installed?"
        )


# ------------------------------------------------------------------------------
# do fsqc


def _do_fsqc(argsDict):
    """
    Run the fsqc submodules.

    Parameters
    ----------
    argsDict : dict
        Dictionary containing input arguments.

    Returns
    -------
    None
        This function returns nothing.
    """

    # ------------------------------------------------------------------------------
    # imports

    import csv
    import logging
    import os
    import time
    from pathlib import Path

    import numpy as np
    import pandas as pd

    from fsqc.checkCCSize import checkCCSize
    from fsqc.checkContrast import checkContrast
    from fsqc.checkRotation import checkRotation
    from fsqc.checkSNR import checkSNR
    from fsqc.checkTopology import checkTopology
    from fsqc.createScreenshots import createScreenshots
    from fsqc.createSurfacePlots import createSurfacePlots
    from fsqc.evaluateFornixSegmentation import evaluateFornixSegmentation
    from fsqc.evaluateHippocampalSegmentation import evaluateHippocampalSegmentation
    from fsqc.evaluateHypothalamicSegmentation import evaluateHypothalamicSegmentation
    from fsqc.outlierDetection import outlierDetection, outlierTable

    # ------------------------------------------------------------------------------
    # internal settings (might be turned into command-line arguments in the future)

    SNR_AMOUT_EROSION = 3
    FORNIX_SCREENSHOT = True
    FORNIX_SHAPE = False
    FORNIX_N_EIGEN = 15
    FORNIX_WRITE_EIGEN = True
    HYPOTHALAMUS_SCREENSHOT = True
    HIPPOCAMPUS_SCREENSHOT = True
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
    imagesSurfacesDict = dict()
    imagesSkullstripDict = dict()
    imagesFornixDict = dict()
    imagesHypothalamusDict = dict()
    imagesHippocampusLeftDict = dict()
    imagesHippocampusRightDict = dict()

    # create status dict
    statusDict = dict()

    # --------------------------------------------------------------------------
    # subject-level processing

    if argsDict["group_only"] is False:
        # loop through the specified subjects
        for subject in argsDict["subjects"]:
            #
            logging.info(
                "Starting fsqc for subject "
                + subject
                + " at "
                + time.strftime("%Y-%m-%d %H:%M %Z", time.localtime(time.time())),
            )

            # ----------------------------------------------------------------------
            # set images

            if argsDict["fastsurfer"] is True:
                aparc_image = "aparc.DKTatlas+aseg.deep.mgz"
            else:
                aparc_image = "aparc+aseg.mgz"

            # ----------------------------------------------------------------------
            # add subject to dictionary

            metricsDict.update({subject: {"subject": subject}})
            statusDict.update({subject: {"subject": subject}})

            # ----------------------------------------------------------------------
            # check for existing statusfile

            # check / create subject-specific status_outdir
            status_outdir = os.path.join(argsDict["output_dir"], "status", subject)
            if not os.path.isdir(status_outdir):
                os.makedirs(status_outdir)

            # if it already exists, read statusfile
            status_dict = dict()
            if os.path.exists(os.path.join(status_outdir, "status.txt")):
                status_dict = dict(
                    pd.read_csv(
                        os.path.join(status_outdir, "status.txt"),
                        sep=":",
                        header=None,
                        comment="#",
                        names=["module", "status"],
                        dtype=str,
                    ).to_dict(orient="split")["data"]
                )
                for x in [
                    "metrics",
                    "shape",
                    "screenshots",
                    "surfaces",
                    "skullstrip",
                    "fornix",
                    "hypothalamus",
                    "hippocampus",
                ]:
                    status_dict[x] = int(status_dict[x])
                statusDict[subject] = status_dict

            # note:
            # 0: OK
            # 1: Failed
            # 2: Not done
            # 3: Skipped

            # ----------------------------------------------------------------------
            # compute core metrics

            # check / create subject-specific metrics_outdir
            metrics_outdir = os.path.join(argsDict["output_dir"], "metrics", subject)
            if not os.path.isdir(metrics_outdir):
                os.makedirs(metrics_outdir)

            #
            metrics_status = 0
            if argsDict["skip_existing"] is True:
                if len(status_dict) > 0:
                    if (
                        statusDict[subject]["metrics"] == 0
                        or statusDict[subject]["metrics"] == 3
                    ):
                        metrics_status = 3
                        logging.info("Skipping metrics computation for " + subject)
                    else:
                        logging.info(
                            "Not skipping metrics computation for "
                            + subject
                            + ": statusfile did not indicate ok or skipped"
                        )
                else:
                    logging.info(
                        "Not skipping metrics computation for "
                        + subject
                        + ": no statusfile was found"
                    )

            if metrics_status == 0:
                # get WM and GM SNR for orig.mgz
                try:
                    wm_snr_orig, gm_snr_orig = checkSNR(
                        argsDict["subjects_dir"],
                        subject,
                        SNR_AMOUT_EROSION,
                        ref_image="orig.mgz",
                        aparc_image=aparc_image,
                    )

                except Exception as e:
                    logging.error("ERROR: SNR computation failed for " + subject)
                    logging.error("Reason: " + str(e))
                    wm_snr_orig = np.nan
                    gm_snr_orig = np.nan
                    metrics_status = 1
                    if argsDict["exit_on_error"] is True:
                        raise

                # get WM and GM SNR for norm.mgz
                try:
                    wm_snr_norm, gm_snr_norm = checkSNR(
                        argsDict["subjects_dir"],
                        subject,
                        SNR_AMOUT_EROSION,
                        ref_image="norm.mgz",
                        aparc_image=aparc_image,
                    )

                except Exception as e:
                    logging.error("ERROR: SNR computation failed for " + subject)
                    logging.error("Reason: " + str(e))
                    wm_snr_norm = np.nan
                    gm_snr_norm = np.nan
                    metrics_status = 1
                    if argsDict["exit_on_error"] is True:
                        raise

                # check CC size
                try:
                    cc_size = checkCCSize(argsDict["subjects_dir"], subject)

                except Exception as e:
                    logging.error("ERROR: CC size computation failed for " + subject)
                    logging.error("Reason: " + str(e))
                    cc_size = np.nan
                    metrics_status = 1
                    if argsDict["exit_on_error"] is True:
                        raise

                # check topology
                try:
                    (
                        holes_lh,
                        holes_rh,
                        defects_lh,
                        defects_rh,
                        topo_lh,
                        topo_rh,
                    ) = checkTopology(argsDict["subjects_dir"], subject)

                except Exception as e:
                    logging.error("ERROR: Topology check failed for " + subject)
                    logging.error("Reason: " + str(e))
                    holes_lh = np.nan
                    holes_rh = np.nan
                    defects_lh = np.nan
                    defects_rh = np.nan
                    topo_lh = np.nan
                    topo_rh = np.nan
                    metrics_status = 1
                    if argsDict["exit_on_error"] is True:
                        raise

                # check contrast
                try:
                    con_snr_lh, con_snr_rh = checkContrast(
                        argsDict["subjects_dir"], subject
                    )

                except Exception as e:
                    logging.error("ERROR: Contrast check failed for " + subject)
                    logging.error("Reason: " + str(e))
                    con_snr_lh = np.nan
                    con_snr_rh = np.nan
                    metrics_status = 1
                    if argsDict["exit_on_error"] is True:
                        raise

                # check rotation
                try:
                    rot_tal_x, rot_tal_y, rot_tal_z = checkRotation(
                        argsDict["subjects_dir"], subject
                    )

                except Exception as e:
                    logging.error("ERROR: Rotation failed for " + subject)
                    logging.error("Reason: " + str(e))
                    rot_tal_x = np.nan
                    rot_tal_y = np.nan
                    rot_tal_z = np.nan
                    metrics_status = 1
                    if argsDict["exit_on_error"] is True:
                        raise

                # store data
                metricsDict[subject].update(
                    {
                        "wm_snr_orig": wm_snr_orig,
                        "gm_snr_orig": gm_snr_orig,
                        "wm_snr_norm": wm_snr_norm,
                        "gm_snr_norm": gm_snr_norm,
                        "cc_size": cc_size,
                        "holes_lh": holes_lh,
                        "holes_rh": holes_rh,
                        "defects_lh": defects_lh,
                        "defects_rh": defects_rh,
                        "topo_lh": topo_lh,
                        "topo_rh": topo_rh,
                        "con_snr_lh": con_snr_lh,
                        "con_snr_rh": con_snr_rh,
                        "rot_tal_x": rot_tal_x,
                        "rot_tal_y": rot_tal_y,
                        "rot_tal_z": rot_tal_z,
                    }
                )

                # write to file
                pd.DataFrame(metricsDict[subject], index=[subject]).to_csv(
                    os.path.join(
                        argsDict["output_dir"], "metrics", subject, "metrics.csv"
                    )
                )

            elif metrics_status == 3:
                metricsDict[subject] = (
                    metricsDict[subject]
                    | pd.read_csv(
                        os.path.join(metrics_outdir, "metrics.csv"),
                        dtype={"Unnamed: 0": str, "subject": str},
                    )
                    .set_index("Unnamed: 0")
                    .to_dict(orient="index")[subject]
                )

            # note that we cannot "not do" the metrics module, only skipping is possible.
            # hence no metrics_status == 2 possible.

            # store data
            statusDict[subject].update({"metrics": metrics_status})

            # ----------------------------------------------------------------------
            # run optional modules: shape analysis

            if argsDict["shape"] is True:
                # determine status
                shape_status = 0
                if argsDict["skip_existing"] is True:
                    if len(status_dict) > 0:
                        if (
                            statusDict[subject]["shape"] == 0
                            or statusDict[subject]["shape"] == 3
                        ):
                            shape_status = 3
                            logging.info("Skipping shape computation for " + subject)
                        else:
                            logging.info(
                                "Not skipping shape computation for "
                                + subject
                                + ": statusfile did not indicate ok or skipped"
                            )
                    else:
                        logging.info(
                            "Not skipping shape computation for "
                            + subject
                            + ": no statusfile was found"
                        )

                # check / create subject-specific brainprint_outdir
                brainprint_outdir = Path(
                    os.path.join(argsDict["output_dir"], "brainprint", subject)
                )

                #
                if shape_status == 0:
                    #
                    try:
                        # message
                        print("-----------------------------")
                        print("Running brainPrint analysis ...")
                        print("")

                        # compute brainprint (will also compute shapeDNA)
                        import brainprint

                        # run brainPrint
                        evMat, evecMat, dstMat = brainprint.brainprint.run_brainprint(
                            subjects_dir=argsDict["subjects_dir"],
                            subject_id=subject,
                            destination=brainprint_outdir,
                            keep_eigenvectors=SHAPE_EVEC,
                            skip_cortex=SHAPE_SKIPCORTEX,
                            num=SHAPE_NUM,
                            norm=SHAPE_NORM,
                            reweight=SHAPE_REWEIGHT,
                            asymmetry=SHAPE_ASYMMETRY,
                        )

                        # get a subset of the brainprint results
                        distDict = {subject: dstMat}

                        # return
                        shape_status = 0

                    #
                    except Exception as e:
                        distDict = {subject: []}
                        logging.error(
                            "ERROR: the shape module failed for subject " + subject
                        )
                        logging.error("Reason: " + str(e))
                        shape_status = 1
                        if argsDict["exit_on_error"] is True:
                            raise

                elif shape_status == 3:
                    # read results from previous run
                    dstMat = pd.read_csv(
                        brainprint_outdir / (subject + ".brainprint.asymmetry.csv")
                    ).to_dict(orient="index")[0]
                    distDict = {subject: dstMat}

                # store data
                metricsDict[subject].update(distDict[subject])

            else:
                shape_status = 2

            # store data
            statusDict[subject].update({"shape": shape_status})

            # ----------------------------------------------------------------------
            # run optional modules: screenshots

            if argsDict["screenshots"] is True or argsDict["screenshots_html"] is True:

                # determine status
                screenshots_status = 0
                if argsDict["skip_existing"] is True:
                    if len(status_dict) > 0:
                        if (
                            statusDict[subject]["screenshots"] == 0
                            or statusDict[subject]["screenshots"] == 3
                        ):
                            screenshots_status = 3
                            logging.info(
                                "Skipping screenshots computation for " + subject
                            )
                        else:
                            logging.info(
                                "Not skipping screenshots computation for "
                                + subject
                                + ": statusfile did not indicate ok or skipped"
                            )
                    else:
                        logging.info(
                            "Not skipping screenshots computation for "
                            + subject
                            + ": no statusfile was found"
                        )

                # check / create subject-specific screenshots_outdir
                screenshots_outdir = os.path.join(
                    argsDict["output_dir"], "screenshots", subject
                )
                if not os.path.isdir(screenshots_outdir):
                    os.makedirs(screenshots_outdir)
                outfile = os.path.join(screenshots_outdir, subject + ".png")

                #
                if screenshots_status == 0:
                    #
                    try:
                        # message
                        print("-----------------------------")
                        print("Creating screenshots ...")
                        print("")

                        # re-initialize
                        screenshots_base_subj = list()
                        screenshots_overlay_subj = list()
                        screenshots_surf_subj = list()

                        # check screenshots_base
                        if argsDict["screenshots_base"] == "default":
                            screenshots_base_subj = argsDict["screenshots_base"]
                            logging.info("Using default for screenshot base image")
                        elif os.path.isfile(argsDict["screenshots_base"]):
                            screenshots_base_subj = argsDict["screenshots_base"]
                            logging.info(
                                "Using "
                                + screenshots_base_subj
                                + " as screenshot base image"
                            )
                        elif os.path.isfile(
                            os.path.join(
                                argsDict["subjects_dir"],
                                subject,
                                "mri",
                                argsDict["screenshots_base"],
                            )
                        ):
                            screenshots_base_subj = os.path.join(
                                argsDict["subjects_dir"],
                                subject,
                                "mri",
                                argsDict["screenshots_base"],
                            )
                            logging.info(
                                "Using "
                                + screenshots_base_subj
                                + " as screenshot base image"
                            )
                        else:
                            raise FileNotFoundError(
                                "ERROR: cannot find the screenshots base file "
                                + argsDict["screenshots_base"]
                            )

                        # check screenshots_overlay
                        if argsDict["screenshots_overlay"] is not None:
                            if argsDict["screenshots_overlay"] == "default":
                                screenshots_overlay_subj = argsDict[
                                    "screenshots_overlay"
                                ]
                                logging.info(
                                    "Using default for screenshot overlay image"
                                )
                            elif os.path.isfile(argsDict["screenshots_overlay"]):
                                screenshots_overlay_subj = argsDict[
                                    "screenshots_overlay"
                                ]
                                logging.info(
                                    "Using "
                                    + screenshots_overlay_subj
                                    + " as screenshot overlay image"
                                )
                            elif os.path.isfile(
                                os.path.join(
                                    argsDict["subjects_dir"],
                                    subject,
                                    "mri",
                                    argsDict["screenshots_overlay"],
                                )
                            ):
                                screenshots_overlay_subj = os.path.join(
                                    argsDict["subjects_dir"],
                                    subject,
                                    "mri",
                                    argsDict["screenshots_overlay"],
                                )
                                logging.info(
                                    "Using "
                                    + screenshots_overlay_subj
                                    + " as screenshot overlay image"
                                )
                            else:
                                raise FileNotFoundError(
                                    "ERROR: cannot find the screenshots overlay file "
                                    + argsDict["screenshots_overlay"]
                                )
                        else:
                            screenshots_overlay_subj = argsDict["screenshots_overlay"]

                        # check screenshots_surf
                        if argsDict["screenshots_surf"] is not None:
                            if isinstance(argsDict["screenshots_surf"], str):
                                if argsDict["screenshots_surf"] == "default":
                                    screenshots_surf_subj = "default"
                                    logging.info("Using default for screenshot surface")
                                else:
                                    if os.path.isfile(argsDict["screenshots_surf"]):
                                        logging.info(
                                            "Using "
                                            + argsDict["screenshots_surf"]
                                            + " as screenshot surface"
                                        )
                                        screenshots_surf_subj = [argsDict["screenshots_surf"]]
                                    else:
                                        raise FileNotFoundError(
                                            "ERROR: cannot find the screenshots surface file "
                                            + argsDict["screenshots_surf"]
                                        )
                            elif isinstance(argsDict["screenshots_surf"], list):
                                for screenshots_surf_i in argsDict["screenshots_surf"]:
                                    if os.path.isfile(screenshots_surf_i):
                                        logging.info(
                                            "Using "
                                            + screenshots_surf_i
                                            + " as screenshot surface"
                                        )
                                    elif os.path.isfile(
                                        os.path.join(
                                            argsDict["subjects_dir"],
                                            subject,
                                            "surf",
                                            screenshots_surf_i,
                                        )
                                    ):
                                        screenshots_surf_i = os.path.join(
                                            argsDict["subjects_dir"],
                                            subject,
                                            "surf",
                                            screenshots_surf_i,
                                        )
                                        logging.info(
                                            "Using "
                                            + screenshots_surf_i
                                            + " as screenshot surface"
                                        )
                                    else:
                                        raise FileNotFoundError(
                                            "ERROR: cannot find the screenshots surface file "
                                            + screenshots_surf_i
                                        )
                                    screenshots_surf_subj.append(screenshots_surf_i)
                        else:
                            screenshots_surf_subj = None

                        # process
                        createScreenshots(
                            SUBJECT=subject,
                            SUBJECTS_DIR=argsDict["subjects_dir"],
                            OUTFILE=outfile,
                            INTERACTIVE=False,
                            BASE=screenshots_base_subj,
                            OVERLAY=screenshots_overlay_subj,
                            SURF=screenshots_surf_subj,
                            VIEWS=argsDict["screenshots_views"],
                            LAYOUT=argsDict["screenshots_layout"],
                            ORIENTATION=argsDict["screenshots_orientation"],
                        )

                        # return
                        screenshots_status = 0

                    #
                    except Exception as e:
                        logging.error(
                            "ERROR: screenshots module failed for subject " + subject
                        )
                        logging.error("Reason: " + str(e))
                        screenshots_status = 1
                        if argsDict["exit_on_error"] is True:
                            raise

                # store data
                if screenshots_status == 0 or screenshots_status == 3:
                    imagesScreenshotsDict[subject] = outfile
                else:
                    imagesScreenshotsDict[subject] = []

            else:
                screenshots_status = 2

            # store data
            statusDict[subject].update({"screenshots": screenshots_status})

            # ----------------------------------------------------------------------
            # run optional modules: surface plots

            if argsDict["surfaces"] is True or argsDict["surfaces_html"] is True:
                # determine status
                surfaces_status = 0
                if argsDict["skip_existing"] is True:
                    if len(status_dict) > 0:
                        if (
                            statusDict[subject]["surfaces"] == 0
                            or statusDict[subject]["surfaces"] == 3
                        ):
                            surfaces_status = 3
                            logging.info("Skipping surfaces computation for " + subject)
                        else:
                            logging.info(
                                "Not skipping surfaces computation for "
                                + subject
                                + ": statusfile did not indicate ok or skipped"
                            )
                    else:
                        logging.info(
                            "Not skipping surfaces computation for "
                            + subject
                            + ": no statusfile was found"
                        )

                # check / create subject-specific surfaces_outdir
                surfaces_outdir = os.path.join(
                    argsDict["output_dir"], "surfaces", subject
                )
                if not os.path.isdir(surfaces_outdir):
                    os.makedirs(surfaces_outdir)

                #
                if surfaces_status == 0:
                    #
                    try:
                        # message
                        print("-----------------------------")
                        print("Creating surface plots ...")
                        print("")

                        # process
                        createSurfacePlots(
                            SUBJECT=subject,
                            SUBJECTS_DIR=argsDict["subjects_dir"],
                            SURFACES_OUTDIR=surfaces_outdir,
                            VIEWS=argsDict["surfaces_views"],
                            FASTSURFER=argsDict["fastsurfer"],
                        )
                        # return
                        surfaces_status = 0

                    #
                    except Exception as e:
                        logging.error(
                            "ERROR: surfaces module failed for subject " + subject
                        )
                        logging.error("Reason: " + str(e))
                        surfaces_status = 1
                        if argsDict["exit_on_error"] is True:
                            raise

                # store data
                if surfaces_status == 0 or surfaces_status == 3:
                    imagesSurfacesDict[subject] = surfaces_outdir
                else:
                    imagesSurfacesDict[subject] = []

            else:
                surfaces_status = 2

            # store data
            statusDict[subject].update({"surfaces": surfaces_status})

            # ----------------------------------------------------------------------
            # run optional modules: skullstrip

            if argsDict["skullstrip"] is True or argsDict["skullstrip_html"] is True:
                # determine status
                skullstrip_status = 0
                if argsDict["skip_existing"] is True:
                    if len(status_dict) > 0:
                        if (
                            statusDict[subject]["skullstrip"] == 0
                            or statusDict[subject]["skullstrip"] == 3
                        ):
                            skullstrip_status = 3
                            logging.info(
                                "Skipping skullstrip computation for " + subject
                            )
                        else:
                            logging.info(
                                "Not skipping skullstrip computation for "
                                + subject
                                + ": statusfile did not indicate ok or skipped"
                            )
                    else:
                        logging.info(
                            "Not skipping skullstrip computation for "
                            + subject
                            + ": no statusfile was found"
                        )

                # check / create subject-specific skullstrip_outdir
                skullstrip_outdir = os.path.join(
                    argsDict["output_dir"], "skullstrip", subject
                )
                if not os.path.isdir(skullstrip_outdir):
                    os.makedirs(skullstrip_outdir)
                outfile = os.path.join(skullstrip_outdir, subject + ".png")

                #
                if skullstrip_status == 0:
                    #
                    try:
                        # message
                        print("-----------------------------")
                        print("Creating skullstrip evaluation  ...")
                        print("")

                        # re-initialize
                        skullstrip_base_subj = list()
                        skullstrip_overlay_subj = list()

                        # check skullstrip_base
                        if os.path.isfile(
                            os.path.join(
                                argsDict["subjects_dir"], subject, "mri", "orig.mgz"
                            )
                        ):
                            skullstrip_base_subj = os.path.join(
                                argsDict["subjects_dir"], subject, "mri", "orig.mgz"
                            )
                            logging.info(
                                "Using " + "orig.mgz" + " as skullstrip base image"
                            )
                        else:
                            raise FileNotFoundError(
                                "ERROR: cannot find the skullstrip base file "
                                + "orig.mgz"
                            )

                        # check skullstrip_overlay
                        if os.path.isfile(
                            os.path.join(
                                argsDict["subjects_dir"],
                                subject,
                                "mri",
                                "brainmask.mgz",
                            )
                        ):
                            skullstrip_overlay_subj = os.path.join(
                                argsDict["subjects_dir"],
                                subject,
                                "mri",
                                "brainmask.mgz",
                            )
                            logging.info(
                                "Using "
                                + "brainmask.mgz"
                                + " as skullstrip overlay image"
                            )
                        else:
                            raise FileNotFoundError(
                                "ERROR: cannot find the skullstrip overlay file "
                                + "brainmask.mgz"
                            )

                        # process
                        createScreenshots(
                            SUBJECT=subject,
                            SUBJECTS_DIR=argsDict["subjects_dir"],
                            OUTFILE=outfile,
                            INTERACTIVE=False,
                            BASE=skullstrip_base_subj,
                            OVERLAY=skullstrip_overlay_subj,
                            SURF=None,
                            VIEWS=argsDict["screenshots_views"],
                            LAYOUT=argsDict["screenshots_layout"],
                            BINARIZE=True,
                            ORIENTATION=argsDict["screenshots_orientation"],
                        )

                        # return
                        skullstrip_status = 0

                    #
                    except Exception as e:
                        logging.error(
                            "ERROR: skullstrip module failed for subject " + subject
                        )
                        logging.error("Reason: " + str(e))
                        skullstrip_status = 1
                        if argsDict["exit_on_error"] is True:
                            raise

                # store data
                if skullstrip_status == 0 or skullstrip_status == 3:
                    imagesSkullstripDict[subject] = outfile
                else:
                    imagesSkullstripDict[subject] = []

            else:
                skullstrip_status = 2

            # store data
            statusDict[subject].update({"skullstrip": skullstrip_status})

            # ----------------------------------------------------------------------
            # run optional modules: fornix

            if argsDict["fornix"] is True or argsDict["fornix_html"] is True:
                # determine status
                fornix_status = 0
                if argsDict["skip_existing"] is True:
                    if len(status_dict) > 0:
                        if (
                            statusDict[subject]["fornix"] == 0
                            or statusDict[subject]["fornix"] == 3
                        ):
                            fornix_status = 3
                            logging.info("Skipping fornix computation for " + subject)
                        else:
                            logging.info(
                                "Not skipping fornix computation for "
                                + subject
                                + ": statusfile did not indicate ok or skipped"
                            )
                    else:
                        logging.info(
                            "Not skipping fornix computation for "
                            + subject
                            + ": no statusfile was found"
                        )

                # check / create subject-specific fornix_outdir
                fornix_outdir = os.path.join(argsDict["output_dir"], "fornix", subject)
                if not os.path.isdir(fornix_outdir):
                    os.makedirs(fornix_outdir)
                fornix_screenshot_outfile = os.path.join(fornix_outdir, "cc.png")

                #
                if fornix_status == 0:
                    #
                    try:
                        # message
                        print("-----------------------------")
                        print("Checking fornix segmentation ...")
                        print("")

                        # process
                        fornixShapeOutput = evaluateFornixSegmentation(
                            SUBJECT=subject,
                            SUBJECTS_DIR=argsDict["subjects_dir"],
                            OUTPUT_DIR=fornix_outdir,
                            CREATE_SCREENSHOT=FORNIX_SCREENSHOT,
                            SCREENSHOTS_OUTFILE=fornix_screenshot_outfile,
                            RUN_SHAPEDNA=FORNIX_SHAPE,
                            N_EIGEN=FORNIX_N_EIGEN,
                            WRITE_EIGEN=FORNIX_WRITE_EIGEN,
                        )

                        # create a dictionary from fornix shape output
                        fornixShapeDict = {
                            subject: dict(
                                zip(
                                    map(
                                        "fornixShapeEV{:0>3}".format,
                                        range(FORNIX_N_EIGEN),
                                    ),
                                    fornixShapeOutput,
                                )
                            )
                        }

                        # return
                        fornix_status = 0

                    #
                    except Exception as e:
                        fornixShapeDict = {
                            subject: dict(
                                zip(
                                    map(
                                        "fornixShapeEV{:0>3}".format,
                                        range(FORNIX_N_EIGEN),
                                    ),
                                    np.full(FORNIX_N_EIGEN, np.nan),
                                )
                            )
                        }
                        logging.error(
                            "ERROR: fornix module failed for subject " + subject
                        )
                        logging.error("Reason: " + str(e))
                        fornix_status = 1
                        if argsDict["exit_on_error"] is True:
                            raise

                    # store data
                    if FORNIX_SHAPE:
                        metricsDict[subject].update(fornixShapeDict[subject])

                elif fornix_status == 3:
                    if FORNIX_SHAPE:
                        # read results from previous run
                        fornixShapeOutput = np.array(
                            pd.read_csv(
                                os.path.join(fornix_outdir, subject + ".fornix.csv")
                            )
                        )[0]
                        fornixShapeDict = {
                            subject: dict(
                                zip(
                                    map(
                                        "fornixShapeEV{:0>3}".format,
                                        range(FORNIX_N_EIGEN),
                                    ),
                                    fornixShapeOutput,
                                )
                            )
                        }
                        metricsDict[subject].update(fornixShapeDict[subject])

                # store data
                if FORNIX_SCREENSHOT and (fornix_status == 0 or fornix_status == 3):
                    imagesFornixDict[subject] = fornix_screenshot_outfile
                else:
                    imagesFornixDict[subject] = []

            else:
                fornix_status = 2

            # store data
            statusDict[subject].update({"fornix": fornix_status})

            # ----------------------------------------------------------------------
            # run optional modules: hypothalamus

            if (
                argsDict["hypothalamus"] is True
                or argsDict["hypothalamus_html"] is True
            ):
                # determine status
                hypothalamus_status = 0
                if argsDict["skip_existing"] is True:
                    if len(status_dict) > 0:
                        if (
                            statusDict[subject]["hypothalamus"] == 0
                            or statusDict[subject]["hypothalamus"] == 3
                        ):
                            hypothalamus_status = 3
                            logging.info(
                                "Skipping hypothalamus computation for " + subject
                            )
                        else:
                            logging.info(
                                "Not skipping hypothalamus computation for "
                                + subject
                                + ": statusfile did not indicate ok or skipped"
                            )
                    else:
                        logging.info(
                            "Not skipping hypothalamus computation for "
                            + subject
                            + ": no statusfile was found"
                        )

                # check / create subject-specific hypothalamus_outdir
                hypothalamus_outdir = os.path.join(
                    argsDict["output_dir"], "hypothalamus", subject
                )
                if not os.path.isdir(hypothalamus_outdir):
                    os.makedirs(hypothalamus_outdir)
                hypothalamus_screenshot_outfile = os.path.join(
                    hypothalamus_outdir, "hypothalamus.png"
                )

                #
                if hypothalamus_status == 0:
                    #
                    try:
                        # message
                        print("-----------------------------")
                        print("Checking hypothalamus segmentation ...")
                        print("")

                        # process
                        evaluateHypothalamicSegmentation(
                            SUBJECT=subject,
                            SUBJECTS_DIR=argsDict["subjects_dir"],
                            OUTPUT_DIR=hypothalamus_outdir,
                            CREATE_SCREENSHOT=HYPOTHALAMUS_SCREENSHOT,
                            SCREENSHOTS_OUTFILE=hypothalamus_screenshot_outfile,
                            SCREENSHOTS_ORIENTATION=argsDict["screenshots_orientation"],
                        )

                        # return
                        hypothalamus_status = 0

                    #
                    except Exception as e:
                        logging.error(
                            "ERROR: hypothalamus module failed for subject " + subject
                        )
                        logging.error("Reason: " + str(e))
                        hypothalamus_status = 1
                        if argsDict["exit_on_error"] is True:
                            raise

                # store data
                if HYPOTHALAMUS_SCREENSHOT and (
                    hypothalamus_status == 0 or hypothalamus_status == 3
                ):
                    imagesHypothalamusDict[subject] = hypothalamus_screenshot_outfile
                else:
                    imagesHypothalamusDict[subject] = []

            else:
                hypothalamus_status = 2

            # store data
            statusDict[subject].update({"hypothalamus": hypothalamus_status})

            # ----------------------------------------------------------------------
            # run optional modules: hippocampus

            if argsDict["hippocampus"] is True or argsDict["hippocampus_html"] is True:
                # determine status
                hippocampus_status = 0
                if argsDict["skip_existing"] is True:
                    if len(status_dict) > 0:
                        if (
                            statusDict[subject]["hippocampus"] == 0
                            or statusDict[subject]["hippocampus"] == 3
                        ):
                            hippocampus_status = 3
                            logging.info(
                                "Skipping hippocampus computation for " + subject
                            )
                        else:
                            logging.info(
                                "Not skipping hippocampus computation for "
                                + subject
                                + ": statusfile did not indicate ok or skipped"
                            )
                    else:
                        logging.info(
                            "Not skipping hippocampus computation for "
                            + subject
                            + ": no statusfile was found"
                        )

                # check / create subject-specific hippocampus_outdir
                hippocampus_outdir = os.path.join(
                    argsDict["output_dir"], "hippocampus", subject
                )
                if not os.path.isdir(hippocampus_outdir):
                    os.makedirs(hippocampus_outdir)
                hippocampus_screenshot_outfile_left = os.path.join(
                    hippocampus_outdir, "hippocampus-left.png"
                )
                hippocampus_screenshot_outfile_right = os.path.join(
                    hippocampus_outdir, "hippocampus-right.png"
                )

                #
                if hippocampus_status == 0:
                    #
                    try:
                        # message
                        print("-----------------------------")
                        print("Checking hippocampus segmentation ...")
                        print("")

                        # process left
                        evaluateHippocampalSegmentation(
                            SUBJECT=subject,
                            SUBJECTS_DIR=argsDict["subjects_dir"],
                            OUTPUT_DIR=hippocampus_outdir,
                            CREATE_SCREENSHOT=HIPPOCAMPUS_SCREENSHOT,
                            SCREENSHOTS_OUTFILE=hippocampus_screenshot_outfile_left,
                            SCREENSHOTS_ORIENTATION=argsDict["screenshots_orientation"],
                            HEMI="lh",
                            LABEL=argsDict["hippocampus_label"],
                        )
                        evaluateHippocampalSegmentation(
                            SUBJECT=subject,
                            SUBJECTS_DIR=argsDict["subjects_dir"],
                            OUTPUT_DIR=hippocampus_outdir,
                            CREATE_SCREENSHOT=HIPPOCAMPUS_SCREENSHOT,
                            SCREENSHOTS_OUTFILE=hippocampus_screenshot_outfile_right,
                            SCREENSHOTS_ORIENTATION=argsDict["screenshots_orientation"],
                            HEMI="rh",
                            LABEL=argsDict["hippocampus_label"],
                        )

                        # return
                        hippocampus_status = 0

                    #
                    except Exception as e:
                        logging.error(
                            "ERROR: hippocampus module failed for subject " + subject
                        )
                        logging.error("Reason: " + str(e))
                        hippocampus_status = 1
                        if argsDict["exit_on_error"] is True:
                            raise

                # store data
                if HIPPOCAMPUS_SCREENSHOT and (
                    hippocampus_status == 0 or hippocampus_status == 3
                ):
                    imagesHippocampusLeftDict[
                        subject
                    ] = hippocampus_screenshot_outfile_left
                    imagesHippocampusRightDict[
                        subject
                    ] = hippocampus_screenshot_outfile_right
                else:
                    imagesHippocampusLeftDict[subject] = []
                    imagesHippocampusRightDict[subject] = []

            else:
                hippocampus_status = 2

            # store data
            statusDict[subject].update({"hippocampus": hippocampus_status})

            # --------------------------------------------------------------------------
            # write statusfile
            # 0: OK
            # 1: Failed
            # 2: Not done
            # 3: Skipped
            pd.DataFrame(statusDict[subject], index=[subject]).T.to_csv(
                os.path.join(argsDict["output_dir"], "status", subject, "status.txt"),
                header=False,
                sep=":",
            )

            # --------------------------------------------------------------------------
            # message
            logging.info(
                "Finished subject "
                + subject
                + " at "
                + time.strftime("%Y-%m-%d %H:%M %Z", time.localtime(time.time()))
            )

    # --------------------------------------------------------------------------
    # run optional modules: outlier detection

    if argsDict["no_group"] is False:
        #
        if argsDict["outlier"] is True:
            # message
            logging.info("Running outlier detection")

            #
            try:
                # message
                print("---------------------------------------")
                print("Running outlier detection module ...")
                print("")

                # determine outlier-table and get data
                if argsDict["outlier_table"] is None:
                    outlierDict = outlierTable()
                else:
                    outlierDict = dict()
                    with open(argsDict["outlier_table"], newline="") as csvfile:
                        outlierCsv = csv.DictReader(csvfile, delimiter=",")
                        for row in outlierCsv:
                            outlierDict.update(
                                {
                                    row["label"]: {
                                        "lower": float(row["lower"]),
                                        "upper": float(row["upper"]),
                                    }
                                }
                            )

                # process
                outlier_outdir = os.path.join(argsDict["output_dir"], "outliers")
                (
                    n_outlier_sample_nonpar,
                    n_outlier_sample_param,
                    n_outlier_norms,
                ) = outlierDetection(
                    argsDict["subjects"],
                    argsDict["subjects_dir"],
                    outlier_outdir,
                    outlierDict,
                    min_no_subjects=OUTLIER_N_MIN,
                    hypothalamus=argsDict["hypothalamus"],
                    hippocampus=argsDict["hippocampus"],
                    hippocampus_label=argsDict["hippocampus_label"],
                    fastsurfer=argsDict["fastsurfer"],
                )
                # create a dictionary from outlier module output
                outlierDict = dict()
                for subject in argsDict["subjects"]:
                    outlierDict.update(
                        {
                            subject: {
                                "n_outlier_sample_nonpar": n_outlier_sample_nonpar[
                                    subject
                                ],
                                "n_outlier_sample_param": n_outlier_sample_param[
                                    subject
                                ],
                                "n_outlier_norms": n_outlier_norms[subject],
                            }
                        }
                    )

                # return
                # outlier_status = 0 # not used currently

            #
            except Exception as e:
                # create a dictionary from outlier module output
                outlierDict = dict()
                for subject in argsDict["subjects"]:
                    outlierDict.update(
                        {
                            subject: {
                                "n_outlier_sample_nonpar": np.nan,
                                "n_outlier_sample_param": np.nan,
                                "n_outlier_norms": np.nan,
                            }
                        }
                    )

                logging.error("ERROR: outlier module failed")
                logging.error("Reason: " + str(e))
                if argsDict["exit_on_error"] is True:
                    raise

            # store data
            for subject in argsDict["subjects"]:
                if argsDict["group_only"] is True:
                    metricsDict.update({subject: {"subject": subject}})
                metricsDict[subject].update(outlierDict[subject])

    # --------------------------------------------------------------------------
    # generate output

    if argsDict["no_group"] is True:
        logging.info("Not generating group output")

    else:
        #
        logging.info("Generating group output")

        #
        metricsFieldnames = ["subject"]

        # we pre-specify the fieldnames because we want to have this particular order
        metricsFieldnames.extend(
            [
                "wm_snr_orig",
                "gm_snr_orig",
                "wm_snr_norm",
                "gm_snr_norm",
                "cc_size",
                "holes_lh",
                "holes_rh",
                "defects_lh",
                "defects_rh",
                "topo_lh",
                "topo_rh",
                "con_snr_lh",
                "con_snr_rh",
                "rot_tal_x",
                "rot_tal_y",
                "rot_tal_z",
            ]
        )

        # check if data needs to be read from disk; note that skip-existing is
        # mutually exclusive with group-only; in case of skip-existing, data
        # that is already present will have been read earlier already
        if argsDict["group_only"] is True:
            for subject in argsDict["subjects"]:
                # metricsDict may (or not) be populated from previous outlier module
                if subject not in metricsDict.keys():
                    metricsDict.update({subject: {"subject": subject}})
                metricsDict[subject] = (
                    metricsDict[subject]
                    | pd.read_csv(
                        os.path.join(
                            argsDict["output_dir"], "metrics", subject, "metrics.csv"
                        ),
                        dtype={"Unnamed: 0": str, "subject": str},
                    )
                    .set_index("Unnamed: 0")
                    .to_dict(orient="index")[subject]
                )
                #
                if argsDict["shape"] is True:
                    dstMat = pd.read_csv(
                        Path(
                            os.path.join(argsDict["output_dir"], "brainprint", subject)
                        )
                        / (subject + ".brainprint.asymmetry.csv")
                    ).to_dict(orient="index")[0]
                    distDict = {subject: dstMat}
                    metricsDict[subject].update(distDict[subject])
                #
                if (
                    argsDict["fornix"] is True or argsDict["fornix_html"] is True
                ) and FORNIX_SHAPE is True:
                    fornixShapeOutput = np.array(
                        pd.read_csv(
                            os.path.join(
                                argsDict["output_dir"],
                                "fornix",
                                subject,
                                subject + ".fornix.csv",
                            )
                        )
                    )[0]
                    fornixShapeDict = {
                        subject: dict(
                            zip(
                                map(
                                    "fornixShapeEV{:0>3}".format, range(FORNIX_N_EIGEN)
                                ),
                                fornixShapeOutput,
                            )
                        )
                    }
                    metricsDict[subject].update(fornixShapeDict[subject])

        # check if other dictionaries need to be populated
        if argsDict["group_only"] is True:
            for subject in argsDict["subjects"]:
                if argsDict["screenshots_html"] is True:
                    imagesScreenshotsDict[subject] = os.path.join(
                        argsDict["output_dir"], "screenshots", subject, subject + ".png"
                    )
                if argsDict["surfaces_html"] is True:
                    imagesSurfacesDict[subject] = os.path.join(
                        argsDict["output_dir"], "surfaces", subject
                    )
                if argsDict["skullstrip_html"] is True:
                    imagesSkullstripDict[subject] = os.path.join(
                        argsDict["output_dir"], "skullstrip", subject, subject + ".png"
                    )
                if argsDict["fornix_html"] is True:
                    imagesFornixDict[subject] = os.path.join(
                        argsDict["output_dir"], "fornix", subject, "cc.png"
                    )
                if argsDict["hypothalamus_html"] is True:
                    imagesHypothalamusDict[subject] = os.path.join(
                        argsDict["output_dir"],
                        "hypothalamus",
                        subject,
                        "hypothalamus.png",
                    )
                if argsDict["hippocampus_html"] is True:
                    imagesHippocampusLeftDict[subject] = os.path.join(
                        argsDict["output_dir"],
                        "hippocampus",
                        subject,
                        "hippocampus-left.png",
                    )
                    imagesHippocampusRightDict[subject] = os.path.join(
                        argsDict["output_dir"],
                        "hippocampus",
                        subject,
                        "hippocampus-right.png",
                    )

        # collect other keys; need to iterate over subjects, because not all of them
        # necessarily have the same set of keys
        if argsDict["shape"] is True:
            shapeKeys = list()
            for subject in distDict.keys():
                if len(distDict[subject]) > 0:
                    shapeKeys = list(
                        np.unique(shapeKeys + list(distDict[subject].keys()))
                    )
            metricsFieldnames.extend(shapeKeys)

        #
        if (
            argsDict["fornix"] is True or argsDict["fornix_html"] is True
        ) and FORNIX_SHAPE is True:
            fornixKeys = list()
            for subject in fornixShapeDict.keys():
                if len(fornixShapeDict[subject]) > 0:
                    fornixKeys = list(
                        np.unique(fornixKeys + list(fornixShapeDict[subject].keys()))
                    )
            metricsFieldnames.extend(sorted(fornixKeys))

        #
        if argsDict["outlier"] is True:
            outlierKeys = list()
            for subject in outlierDict.keys():
                if len(outlierDict[subject]) > 0:
                    outlierKeys = list(
                        np.unique(outlierKeys + list(outlierDict[subject].keys()))
                    )
            metricsFieldnames.extend(sorted(outlierKeys))

        # determine output file names
        path_data_file = os.path.join(argsDict["output_dir"], "fsqc-results.csv")
        path_html_file = os.path.join(argsDict["output_dir"], "fsqc-results.html")

        # write csv
        with open(path_data_file, "w") as datafile:
            csvwriter = csv.DictWriter(
                datafile,
                fieldnames=metricsFieldnames,
                delimiter=",",
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
            )
            csvwriter.writeheader()
            for subject in sorted(list(metricsDict.keys())):
                csvwriter.writerow(metricsDict[subject])

        # generate html output
        if (
            (argsDict["screenshots_html"] is True)
            or (argsDict["surfaces_html"] is True)
            or (argsDict["skullstrip_html"] is True)
            or (argsDict["fornix_html"] is True)
            or (argsDict["hypothalamus_html"] is True)
            or (argsDict["hippocampus_html"] is True)
        ):
            with open(path_html_file, "w") as htmlfile:
                print("<html>", file=htmlfile)
                print("<head>", file=htmlfile)
                print("<title>fsqc screenshots</title>", file=htmlfile)
                print("</head>", file=htmlfile)
                print(
                    "<style> body, h1, h2, h3, h4, h5, h6  { font-family: Arial, Helvetica, sans-serif ; } </style>)",
                    file=htmlfile,
                )
                print('<body style="background-color:Black">', file=htmlfile)

                # screenshots
                if argsDict["screenshots_html"] is True:
                    print('<h1 style="color:white">Screenshots</h1>', file=htmlfile)
                    for subject in sorted(list(imagesScreenshotsDict.keys())):
                        print(
                            '<h2 style="color:white">Subject ' + subject + "</h2>",
                            file=htmlfile,
                        )
                        if imagesScreenshotsDict[
                            subject
                        ]:  # should be False for empty string or empty list
                            if os.path.isfile(
                                os.path.join(
                                    argsDict["output_dir"],
                                    "screenshots",
                                    subject,
                                    os.path.basename(imagesScreenshotsDict[subject]),
                                )
                            ):
                                print(
                                    '<p><a href="'
                                    + os.path.join(
                                        "screenshots",
                                        subject,
                                        os.path.basename(
                                            imagesScreenshotsDict[subject]
                                        ),
                                    )
                                    + '">'
                                    + '<img src="'
                                    + os.path.join(
                                        "screenshots",
                                        subject,
                                        os.path.basename(
                                            imagesScreenshotsDict[subject]
                                        ),
                                    )
                                    + '" '
                                    + 'alt="Image for subject '
                                    + subject
                                    + '" style="width:75vw;min_width:200px;"></img></a></p>',
                                    file=htmlfile,
                                )

                # skullstrip
                if argsDict["skullstrip_html"] is True:
                    print('<h1 style="color:white">Skullstrip</h1>', file=htmlfile)
                    for subject in sorted(list(imagesSkullstripDict.keys())):
                        print(
                            '<h2 style="color:white">Subject ' + subject + "</h2>",
                            file=htmlfile,
                        )
                        if imagesSkullstripDict[
                            subject
                        ]:  # should be False for empty string or empty list
                            if os.path.isfile(
                                os.path.join(
                                    argsDict["output_dir"],
                                    "skullstrip",
                                    subject,
                                    os.path.basename(imagesSkullstripDict[subject]),
                                )
                            ):
                                print(
                                    '<p><a href="'
                                    + os.path.join(
                                        "skullstrip",
                                        subject,
                                        os.path.basename(imagesSkullstripDict[subject]),
                                    )
                                    + '">'
                                    + '<img src="'
                                    + os.path.join(
                                        "skullstrip",
                                        subject,
                                        os.path.basename(imagesSkullstripDict[subject]),
                                    )
                                    + '" '
                                    + 'alt="Image for subject '
                                    + subject
                                    + '" style="width:75vw;min_width:200px;"></img></a></p>',
                                    file=htmlfile,
                                )

                # surfaces
                if argsDict["surfaces_html"] is True:
                    print('<h1 style="color:white">Surfaces</h1>', file=htmlfile)
                    for subject in sorted(list(imagesSurfacesDict.keys())):
                        print(
                            '<h2 style="color:white">Subject ' + subject + "</h2>",
                            file=htmlfile,
                        )
                        if imagesSurfacesDict[
                            subject
                        ]:  # should be False for empty string or empty list
                            # Produce first all plots for pial then for inflated surface.
                            # Each view contains a left and right hemispheric plot.
                            _views_per_row = 2

                            from PIL import Image

                            filepath = os.path.join(
                                argsDict["output_dir"],
                                "surfaces",
                                subject,
                                f'lh.pial.{argsDict["surfaces_views"][0]}.png',
                            )
                            img = Image.open(filepath)
                            width, height = img.size
                            width *= 2 * _views_per_row + 0.1

                            print("<p>", file=htmlfile)
                            print(
                                f'<div style="width:{width}; background-color:black; ">',
                                file=htmlfile,
                            )
                            print("<p>", file=htmlfile)
                            for i, v in enumerate(argsDict["surfaces_views"], start=1):
                                if os.path.isfile(
                                    os.path.join(
                                        argsDict["output_dir"],
                                        "surfaces",
                                        subject,
                                        f"lh.pial.{v}.png",
                                    )
                                ):
                                    print(
                                        '<a href="'
                                        + os.path.join(
                                            "surfaces", subject, f"lh.pial.{v}.png"
                                        )
                                        + '">'
                                        + '<img src="'
                                        + os.path.join(
                                            "surfaces", subject, f"lh.pial.{v}.png"
                                        )
                                        + '" '
                                        + 'alt="Image for subject '
                                        + subject
                                        + '" style=""></img></a>',
                                        file=htmlfile,
                                    )
                                if os.path.isfile(
                                    os.path.join(
                                        argsDict["output_dir"],
                                        "surfaces",
                                        subject,
                                        f"rh.pial.{v}.png",
                                    )
                                ):
                                    print(
                                        '<a href="'
                                        + os.path.join(
                                            "surfaces", subject, f"rh.pial.{v}.png"
                                        )
                                        + '">'
                                        + '<img src="'
                                        + os.path.join(
                                            "surfaces", subject, f"rh.pial.{v}.png"
                                        )
                                        + '" '
                                        + 'alt="Image for subject '
                                        + subject
                                        + '" style=""></img></a>',
                                        file=htmlfile,
                                    )
                                if i % _views_per_row == 0:
                                    print("</p> <p>", file=htmlfile)
                            print("</p> <p>", file=htmlfile)
                            for i, v in enumerate(argsDict["surfaces_views"], start=1):
                                if os.path.isfile(
                                    os.path.join(
                                        argsDict["output_dir"],
                                        "surfaces",
                                        subject,
                                        f"lh.inflated.{v}.png",
                                    )
                                ):
                                    print(
                                        '<a href="'
                                        + os.path.join(
                                            "surfaces", subject, f"lh.inflated.{v}.png"
                                        )
                                        + '">'
                                        + '<img src="'
                                        + os.path.join(
                                            "surfaces", subject, f"lh.inflated.{v}.png"
                                        )
                                        + '" '
                                        + 'alt="Image for subject '
                                        + subject
                                        + '" style=""></img></a>',
                                        file=htmlfile,
                                    )
                                if os.path.isfile(
                                    os.path.join(
                                        argsDict["output_dir"],
                                        "surfaces",
                                        subject,
                                        f"rh.inflated.{v}.png",
                                    )
                                ):
                                    print(
                                        '<a href="'
                                        + os.path.join(
                                            "surfaces", subject, f"rh.inflated.{v}.png"
                                        )
                                        + '">'
                                        + '<img src="'
                                        + os.path.join(
                                            "surfaces", subject, f"rh.inflated.{v}.png"
                                        )
                                        + '" '
                                        + 'alt="Image for subject '
                                        + subject
                                        + '" style=""></img></a>',
                                        file=htmlfile,
                                    )
                                if i % _views_per_row == 0:
                                    print("</p> <p>", file=htmlfile)
                            print("</p>", file=htmlfile)
                            print("</div>", file=htmlfile)
                            print("</p>", file=htmlfile)

                # fornix
                if argsDict["fornix_html"] is True:
                    print('<h1 style="color:white">Fornix</h1>', file=htmlfile)
                    for subject in sorted(list(imagesFornixDict.keys())):
                        print(
                            '<h2 style="color:white">Subject ' + subject + "</h2>",
                            file=htmlfile,
                        )
                        if imagesFornixDict[
                            subject
                        ]:  # should be False for empty string or empty list
                            if os.path.isfile(
                                os.path.join(
                                    argsDict["output_dir"],
                                    "fornix",
                                    subject,
                                    os.path.basename(imagesFornixDict[subject]),
                                )
                            ):
                                print(
                                    '<p><a href="'
                                    + os.path.join(
                                        "fornix",
                                        subject,
                                        os.path.basename(imagesFornixDict[subject]),
                                    )
                                    + '">'
                                    + '<img src="'
                                    + os.path.join(
                                        "fornix",
                                        subject,
                                        os.path.basename(imagesFornixDict[subject]),
                                    )
                                    + '" '
                                    + 'alt="Image for subject '
                                    + subject
                                    + '" style="width:75vw;min_width:200px;"></img></a></p>',
                                    file=htmlfile,
                                )

                # hypothalamus
                if argsDict["hypothalamus_html"] is True:
                    print('<h1 style="color:white">Hypothalamus</h1>', file=htmlfile)
                    for subject in sorted(list(imagesHypothalamusDict.keys())):
                        print(
                            '<h2 style="color:white">Subject ' + subject + "</h2>",
                            file=htmlfile,
                        )
                        if imagesHypothalamusDict[
                            subject
                        ]:  # should be False for empty string or empty list
                            if os.path.isfile(
                                os.path.join(
                                    argsDict["output_dir"],
                                    "hypothalamus",
                                    subject,
                                    os.path.basename(imagesHypothalamusDict[subject]),
                                )
                            ):
                                print(
                                    '<p><a href="'
                                    + os.path.join(
                                        "hypothalamus",
                                        subject,
                                        os.path.basename(
                                            imagesHypothalamusDict[subject]
                                        ),
                                    )
                                    + '">'
                                    + '<img src="'
                                    + os.path.join(
                                        "hypothalamus",
                                        subject,
                                        os.path.basename(
                                            imagesHypothalamusDict[subject]
                                        ),
                                    )
                                    + '" '
                                    + 'alt="Image for subject '
                                    + subject
                                    + '" style="width:75vw;min_width:200px;"></img></a></p>',
                                    file=htmlfile,
                                )

                # hippocampus
                if argsDict["hippocampus_html"] is True:
                    print('<h1 style="color:white">hippocampus</h1>', file=htmlfile)
                    for subject in sorted(list(imagesHippocampusLeftDict.keys())):
                        print(
                            '<h2 style="color:white">Subject ' + subject + "</h2>",
                            file=htmlfile,
                        )
                        if imagesHippocampusLeftDict[
                            subject
                        ]:  # should be False for empty string or empty list
                            if os.path.isfile(
                                os.path.join(
                                    argsDict["output_dir"],
                                    "hippocampus",
                                    subject,
                                    os.path.basename(
                                        imagesHippocampusLeftDict[subject]
                                    ),
                                )
                            ):
                                print(
                                    '<p><a href="'
                                    + os.path.join(
                                        "hippocampus",
                                        subject,
                                        os.path.basename(
                                            imagesHippocampusLeftDict[subject]
                                        ),
                                    )
                                    + '">'
                                    + '<img src="'
                                    + os.path.join(
                                        "hippocampus",
                                        subject,
                                        os.path.basename(
                                            imagesHippocampusLeftDict[subject]
                                        ),
                                    )
                                    + '" '
                                    + 'alt="Image for subject '
                                    + subject
                                    + '" style="width:75vw;min_width:200px;"></img></a></p>',
                                    file=htmlfile,
                                )
                        if imagesHippocampusRightDict[
                            subject
                        ]:  # should be False for empty string or empty list
                            if os.path.isfile(
                                os.path.join(
                                    argsDict["output_dir"],
                                    "hippocampus",
                                    subject,
                                    os.path.basename(
                                        imagesHippocampusRightDict[subject]
                                    ),
                                )
                            ):
                                print(
                                    '<p><a href="'
                                    + os.path.join(
                                        "hippocampus",
                                        subject,
                                        os.path.basename(
                                            imagesHippocampusRightDict[subject]
                                        ),
                                    )
                                    + '">'
                                    + '<img src="'
                                    + os.path.join(
                                        "hippocampus",
                                        subject,
                                        os.path.basename(
                                            imagesHippocampusRightDict[subject]
                                        ),
                                    )
                                    + '" '
                                    + 'alt="Image for subject '
                                    + subject
                                    + '" style="width:75vw;min_width:200px;"></img></a></p>',
                                    file=htmlfile,
                                )

                #
                print("</body>", file=htmlfile)
                print("</html>", file=htmlfile)


# ------------------------------------------------------------------------------
# _start_logging


def _start_logging(argsDict):
    """
    Start logging.

    Parameters
    ----------
    argsDict : dict
        Dictionary containing input arguments.

    Returns
    -------
    None
        This function returns nothing.
    """
    # imports
    import logging
    import os
    import sys
    import tempfile
    import time
    import traceback

    # setup function to log uncaught exceptions
    def foo(exctype, value, tb):
        # log
        logging.error("Error Information:")
        logging.error("Type: %s", exctype)
        logging.error("Value: %s", value)
        for i in traceback.format_list(traceback.extract_tb(tb)):
            logging.error("Traceback: %s", i)
        # message
        logging.error("Status: program exited with errors")

    sys.excepthook = foo

    # set up logging
    logfile_format = "[%(levelname)s: %(filename)s: %(lineno)4d]: %(message)s"
    logfile_handlers = [logging.StreamHandler(sys.stdout)]
    logging.basicConfig(
        level=logging.INFO, format=logfile_format, handlers=logfile_handlers
    )

    # check if output directory exists or can be created
    if os.path.isdir(argsDict["output_dir"]):
        logging.info("Found output directory " + argsDict["output_dir"])
    else:
        try:
            os.mkdir(argsDict["output_dir"])
        except Exception as e:
            logging.error(
                "ERROR: cannot create output directory " + argsDict["output_dir"]
            )
            logging.error("Reason: " + str(e))
            raise

    # check if mandatory status subdirectory directory exists or can be created
    if os.path.isdir(os.path.join(argsDict["output_dir"], "status")):
        logging.info(
            "Found status directory " + os.path.join(argsDict["output_dir"], "status")
        )
    else:
        try:
            os.mkdir(os.path.join(argsDict["output_dir"], "status"))
        except Exception as e:
            logging.error(
                "ERROR: cannot create status directory "
                + os.path.join(argsDict["output_dir"], "status")
            )
            logging.error("Reason: " + str(e))
            raise

    # check if mandatory metrics subdirectory directory exists or can be created
    if os.path.isdir(os.path.join(argsDict["output_dir"], "metrics")):
        logging.info(
            "Found metrics directory " + os.path.join(argsDict["output_dir"], "metrics")
        )
    else:
        try:
            os.mkdir(os.path.join(argsDict["output_dir"], "metrics"))
        except Exception as e:
            logging.error(
                "ERROR: cannot create metrics directory "
                + os.path.join(argsDict["output_dir"], "metrics")
            )
            logging.error("Reason: " + str(e))
            raise

    # check if logfile can be written in output directory
    try:
        testfile = tempfile.TemporaryFile(dir=argsDict["output_dir"])
        testfile.close()
    except Exception as e:
        logging.error("ERROR: " + argsDict["output_dir"] + " not writeable")
        logging.error("Reason: " + str(e))
        raise

    #
    logfile = os.path.join(argsDict["output_dir"], "logfile.txt")
    logging.getLogger().addHandler(logging.FileHandler(filename=logfile, mode="w"))

    # initial messages
    logging.info("Starting logging for fsqctools ...")
    logging.info("Logfile: %s", logfile)
    logging.info("Version: %s", get_version())
    logging.info("Date: %s", time.strftime("%d/%m/%Y %H:%M:%S"))

    # log args
    logging.info("Command: " + " ".join(sys.argv))

    # update args
    argsDict["logfile"] = logfile

    # return
    return argsDict


# ------------------------------------------------------------------------------
# run fsqc


def run_fsqc(
    subjects_dir,
    output_dir,
    argsDict=None,
    subjects=None,
    subjects_file=None,
    shape=False,
    screenshots=False,
    screenshots_html=False,
    screenshots_base="default",
    screenshots_overlay="default",
    screenshots_surf="default",
    screenshots_views="default",
    screenshots_layout="default",
    screenshots_orientation="radiological",
    surfaces=False,
    surfaces_html=False,
    surfaces_views=None,
    skullstrip=False,
    skullstrip_html=False,
    fornix=False,
    fornix_html=False,
    hypothalamus=False,
    hypothalamus_html=False,
    hippocampus=False,
    hippocampus_html=False,
    hippocampus_label=None,
    outlier=False,
    outlier_table=None,
    fastsurfer=False,
    no_group=False,
    group_only=False,
    exit_on_error=False,
    skip_existing=False,
    logfile=None,
):
    """
    Run the fsqc submodules.

    This is the main function to run the fsqc submodules.

    Parameters
    ----------
    subjects_dir : str
        Subjects directory.
    output_dir : str
        Output directory.
    argsDict : dict, default: None
        Dictionary of input arguments.
    subjects : list of str, default: None
        List of subjects to process. If None, all valid cases in the input
        directory will be processed. Cannot be used with `subjects_file`.
    subjects_file : str, default: None
        A text file that contains a list of subjects to be processed. Cannot
        be used with `subjects`.
    shape : bool, default: False
        Conduct shape analysis using brainprint.
    screenshots : bool, default: False
        Create screenshots of MR image with optional overlays.
    screenshots_html : bool, default: False
        Create screenshots and html summary page.
    screenshots_base : str, default: "default"
        Filename for base image for screenshots.
    screenshots_overlay : str, default: "default"
        Filename for overlay image for screenshots.
    screenshots_surf : (list of) str, default: "default"
        List of filenames of surface files to include in screenshots.
    screenshots_views : (list of) str, default: "default"
        List of parameters to set the views of the screenshots.
        Example: ['x=0', 'x=-10', 'x=10', 'y=20', 'z=0'].
    screenshots_layout : str or list of int, default: "default"
        Layout describing rows and columns of the screenshots.
        Example: [1, 4] (one row, four columns).
    screenshots_orientation : str, default: "radiological"
        Orientation of screenshots. Either "radiological" or "neurological".
    surfaces : bool, default: False
        Create screenshots of pial and inflated surfaces.
    surfaces_html : bool, default: False
        Create screenshots of pial and inflated surfaces and html summary page.
    surfaces_views : list of str, default: ["left", "right", "superior", "inferior"]
        List of parameters to set the views of the surface plots.
    skullstrip : bool, default: False
        Create screeenshot of MR image and skullstrip overlay.
    skullstrip_html : bool, default: False
        Create screeenshot of MR image and skullstrip overlay, and create html
        summary page.
    fornix : bool, default: False
        Create screenshot of MR imge and corpus callosum overlay to identify
        fornix oversegmentation.
    fornix_html : bool, default: False
        Create screenshot of MR imge and corpus callosum overlay with html
        summary page.
    hypothalamus : bool, default: False
        Create screenhots of hypothalamic segmentation. Requires running
        FreeSurfer's hypothalamus add-on module.
    hypothalamus_html : bool, default: False
        Create screenhots of hypothalamic segmentation with html summary page.
        Requires running FreeSurfer's hypothalamus add-on module.
    hippocampus : bool, default: False
        Create screenhots of hippocampal segmentation. Requires running
        FreeSurfer's hippocampus add-on module.
    hippocampus_html : bool, default: False
        Create screenhots of hippocampal segmentation with html summary page.
        Requires running FreeSurfer's hippocampus add-on module.
    hippocampus_label : str, default: None
        Label used for the hippocampal segmentations. Example: "T1.v21". The
        full filename would be [lr]h.hippoAmygLabels-<LABEL>.FSvoxelSpace.mgz.
    outlier : bool, default: False
        Conduct outlier analysis.
    outlier_table : str, default: None
        Specify custom norms table for outlier analysis.
    fastsurfer : bool, default: False
        Use FastSurfer instead of FreeSurfer input.
    no_group : bool, default: False
        Run script in subject-level mode. will compute individual files and
        statistics, but not create group-level summaries.
    group_only : bool, default: False
        Run script in group mode. will create group-level summaries from
        existing inputs.
    exit_on_error : bool, default: False
        Exit on error. If False, a warning is thrown and the analysis
        continues.
    skip_existing : bool, default: False
        Skip processing for a given case if output already exists, even with
        possibly different parameters or settings.
    logfile : str, default: None
        Specify a custom location for the logfile. Default location is the
        output directory.

    Returns
    -------
    dict
        A dictionary of input arguments and processing directives.
    """
    # set defaults here to avoid mutable datastructures for default argument B006
    if screenshots_orientation is None:
        screenshots_orientation = ["radiological"]
    if surfaces_views is None:
        surfaces_views = ["left", "right", "superior", "inferior"]

    # create argsDict
    if argsDict is None and (subjects_dir is None or output_dir is None):
        raise ValueError(
            "ERROR: nothing to do. Need to specify either the argsDict argument or the subjects_dir / output_dir arguments."
        )

    elif argsDict is None and subjects_dir is not None and output_dir is not None:
        argsDict = dict()
        argsDict["subjects_dir"] = subjects_dir
        argsDict["output_dir"] = output_dir
        argsDict["subjects"] = subjects
        argsDict["subjects_file"] = subjects_file
        argsDict["shape"] = shape
        argsDict["screenshots"] = screenshots
        argsDict["screenshots_html"] = screenshots_html
        argsDict["screenshots_base"] = screenshots_base
        argsDict["screenshots_overlay"] = screenshots_overlay
        argsDict["screenshots_surf"] = screenshots_surf
        argsDict["screenshots_views"] = screenshots_views
        argsDict["screenshots_layout"] = screenshots_layout
        argsDict["screenshots_orientation"] = screenshots_orientation
        argsDict["surfaces"] = surfaces
        argsDict["surfaces_html"] = surfaces_html
        argsDict["surfaces_views"] = surfaces_views
        argsDict["skullstrip"] = skullstrip
        argsDict["skullstrip_html"] = skullstrip_html
        argsDict["fornix"] = fornix
        argsDict["fornix_html"] = fornix_html
        argsDict["hypothalamus"] = hypothalamus
        argsDict["hypothalamus_html"] = hypothalamus_html
        argsDict["hippocampus"] = hippocampus
        argsDict["hippocampus_html"] = hippocampus_html
        argsDict["hippocampus_label"] = hippocampus_label
        argsDict["outlier"] = outlier
        argsDict["outlier_table"] = outlier_table
        argsDict["fastsurfer"] = fastsurfer
        argsDict["no_group"] = no_group
        argsDict["group_only"] = group_only
        argsDict["exit_on_error"] = exit_on_error
        argsDict["skip_existing"] = skip_existing
        argsDict["logfile"] = logfile

    elif (argsDict is not None) and (
        subjects_dir is not None or output_dir is not None
    ):
        raise ValueError(
            "ERROR: cannot specify the argsDict and the subjects_dir / output_dir arguments at the same time."
        )

    # start logging
    argsDict = _start_logging(argsDict)

    # check arguments
    argsDict = _check_arguments(argsDict)

    # check packages
    _check_packages()

    # run fsqc
    _do_fsqc(argsDict)

    # return
    return argsDict
