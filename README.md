# qatools-python

## Description

This is a set of quality assurance / quality control scripts for Fastsurfer- or
Freesurfer-processed structural MRI data.

It is a revision, extension, and translation to the Python language of the
Freesurfer QA Tools that are provided at https://surfer.nmr.mgh.harvard.edu/fswiki/QATools

It has been augmented by additional functions from the MRIQC toolbox, available
at https://github.com/poldracklab/mriqc and https://osf.io/haf97, and with code
derived from the shapeDNA and brainPrint toolboxes, available at
https://reuter.mit.edu.

The core functionality of this toolbox is to compute the following features:

variable       |   description
---------------|----------------------------------------------------------------
subject        |   subject ID
wm_snr_orig    |   signal-to-noise ratio for white matter in orig.mgz
gm_snr_orig    |   signal-to-noise ratio for gray matter in orig.mgz
wm_snr_norm    |   signal-to-noise ratio for white matter in norm.mgz
gm_snr_norm    |   signal-to-noise ratio for gray matter in norm.mgz
cc_size        |   relative size of the corpus callosum
lh_holes       |   number of holes in the left hemisphere
rh_holes       |   number of holes in the right hemisphere
lh_defects     |   number of defects in the left hemisphere
rh_defects     |   number of defects in the right hemisphere
topo_lh        |   topological fixing time for the left hemisphere
topo_rh        |   topological fixing time for the right hemisphere
con_lh_snr     |   wm/gm contrast signal-to-noise ratio in the left hemisphere
con_rh_snr     |   wm/gm contrast signal-to-noise ratio in the right hemisphere
rot_tal_x      |   rotation component of the Talairach transform around the x axis
rot_tal_y      |   rotation component of the Talairach transform around the y axis
rot_tal_z      |   rotation component of the Talairach transform around the z axis

The program will use an existing output directory (or try to create it) and
write a csv table into that location. The csv table will contain the above
metrics plus a subject identifier.

The program can also be run on images that were processed with [FastSurfer](https://github.com/Deep-MI/FastSurfer)
instead of FreeSurfer. In that case, simply add a `--fastsurfer` switch to your
shell command. Note that the full processing stream FastSurfer must have been
run, including surface reconstruction (i.e. brain segmentation alone is not
sufficient).

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
within the output directory. These images can be used for quickly glimpsing
through the processing results. Note that no display manager is required for
this module, i.e. it can be run on a remote server, for example.

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
segmentation overlaid on the norm.mgz will be saved as 'cc.png' for each
subject within the 'fornix' subdirectory of the output directory.

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
directory will also contain a 'brainprint' subdirectory.

- outlier module

This is a module to detect extreme values among the subcortical ('aseg')
segmentations as well as the cortical parcellations. If present, hypothalamic
and hippocampal subsegmentations will also be included.

The outlier detection is based on comparisons with the
distributions of the sample as well as normative values taken from the
literature (see References).

For comparisons with the sample distributions, extreme values are defined in
two ways: nonparametrically, i.e. values that are 1.5 times the interquartile
range below or above the 25th or 75th percentile of the sample, respectively,
and parametrically, i.e. values that are more than 2 standard deviations above
or below the sample mean. Note that a minimum of 10 supplied subjects is
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
with aparc.stats values, the labels must have a 'lh.' or 'rh.' prefix. file.
`upper` and `lower` are user-specified upper and lower bounds.

The main csv table will be appended with the following summary variables, and
more detailed output about will be saved as csv tables in the 'outliers'
subdirectory of the main output directory.

variable                 |   description
-------------------------|---------------------------------------------------
n_outliers_sample_nonpar | number of structures that are 1.5 times the IQR above/below the 75th/25th percentile
n_outliers_sample_param  | number of structures that are 2 SD above/below the mean
n_outliers_norms         | number of structures exceeding the upper and lower bounds of the normative values

___

## Recent changes and roadmap

The goal of the `qatools-python` project is to create a modular and extensible
software package that provides quantitative metrics and visual information for
the quality control of FreeSurfer-processed MR images. The package is currently
under development, and new features are continuously added.

New features will initially be available in the development branch (`freesurfer-module-dev`)
of this toolbox and will be included in the main branch (`freesurfer-module-releases`)
after a period of testing and evaluation. Unless explicitly announced, all new
features will preserve compatibility with earlier versions.

The current version is 1.5: recent changes in comparison to the previous
versions include the addition of the hipopcampus and hypothalamus modules as
well as the addition of a surface visualization module.

Upcoming extensions include modules for the quality control of FreeSurfer's
brainstem and thalamic segmentations. Another planned extension is support for
parallel processing of many cases.

Feedback, suggestions, and contributions are always welcome.

___

## Usage

```
python3 qatools.py --subjects_dir <directory> --output_dir <directory>
                          [--subjects SubjectID [SubjectID ...]]
                          [--subjects-file <file>] [--screenshots]
                          [--screenshots-html] [--surfaces] [--surfaces-html]
                          [--skullstrip] [--skullstrip-html]
                          [--fornix] [--fornix-html] [--hippocampus]
                          [--hippocampus-html] [--hippocampus-label ... ]
                          [--hypothalamus] [--hypothalamus-html] [--shape]
                          [--outlier] [--fastsurfer] [-h] [--more-help]
                          [...]


required arguments:
  --subjects_dir <directory>
                         subjects directory with a set of Freesurfer 6.0 processed
                         individual datasets.
  --output_dir <directory>
                         output directory

optional arguments:
  --subjects SubjectID [SubjectID ...]
                         list of subject IDs
  --subjects-file <file> filename of a file with subject IDs (one per line)
  --screenshots          create screenshots of individual brains
  --screenshots-html     create screenshots of individual brains incl.
                         html summary page
  --surfaces             create screenshots of individual brain surfaces
  --surfaces-html        create screenshots of individual brain surfaces
                         and html summary page  
  --skullstrip           create screenshots of individual brainmasks
  --skullstrip-html      create screenshots of individual brainmasks and
                         html summary page                                                
  --fornix               check fornix segmentation
  --fornix-html          check fornix segmentation and create html summary
                         page of fornix evaluation
  --hypothalamus         check hypothalamic segmentation
  --hypothalamus-html    check hypothalamic segmentation and create html
                         summary page
  --hippocampus          check segmentation of hippocampus and amygdala
  --hippocampus-html     check segmentation of hippocampus and amygdala
                         and create html summary page
  --hippocampus-label    specify label for hippocampus segmentation files
                         (default: T1.v21). The full filename is then
                         [lr]h.hippoAmygLabels-<LABEL>.FSvoxelSpace.mgz
  --shape                run shape analysis
  --outlier              run outlier detection
  --outlier-table        specify normative values (only in conjunction with
                         --outlier)
  --fastsurfer           use FastSurfer instead of FreeSurfer output

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
                        layout matrix for screenshot images.
  --screenshots_orientation <neurological|radiological>
                        left-right orientation for screenshot outputs. Must be
                        either 'neurological' (left is left; default) or
                        'radiological' (left is right; as in the 'freeview'
                        program).

```

___

## Examples

- Run the QC pipeline for all subjects found in `/my/subjects/directory`:

    `python3 /my/scripts/directory/qatools.py --subjects_dir /my/subjects/directory --output_dir /my/output/directory`

- Run the QC pipeline for two specific subjects that need to present in `/my/subjects/directory`:

    `python3 /my/scripts/directory/qatools.py --subjects_dir /my/subjects/directory --output_dir /my/output/directory --subjects mySubjectID1 mySubjectID2`

- Run the QC pipeline for all subjects found in `/my/subjects/directory` after full FastSurfer processing:

    `python3 /my/scripts/directory/qatools.py --subjects_dir /my/subjects/directory --output_dir /my/output/directory --fastsurfer`

- Run the QC pipeline plus the screenshots module for all subjects found in `/my/subjects/directory`:

    `python3 /my/scripts/directory/qatools.py --subjects_dir /my/subjects/directory --output_dir /my/output/directory --screenshots`

- Run the QC pipeline plus the fornix pipeline for all subjects found in `/my/subjects/directory`:

    `python3 /my/scripts/directory/qatools.py --subjects_dir /my/subjects/directory --output_dir /my/output/directory --fornix`

- Run the QC pipeline plus the shape analysis pipeline for all subjects found in `/my/subjects/directory`:

    `python3 /my/scripts/directory/qatools.py --subjects_dir /my/subjects/directory --output_dir /my/output/directory --shape`

- Run the QC pipeline plus the outlier detection module for all subjects found in `/my/subjects/directory`:

    `python3 /my/scripts/directory/qatools.py --subjects_dir /my/subjects/directory --output_dir /my/output/directory --outlier`

- Run the QC pipeline plus the outlier detection module with a user-specific table of normative values for all subjects found in `/my/subjects/directory`:

    `python3 /my/scripts/directory/qatools.py --subjects_dir /my/subjects/directory --output_dir /my/output/directory --outlier --outlier-table /my/table/with/normative/values.csv`

- Note that the `--screenshots`, `--fornix`, `--shape`, and `--outlier` arguments can also be used in conjunction.

___

## Main branch and development branch

There are two branches in this repository, the main brach (freesurfer-module-releases) and the development branch (freesurfer-module-dev). New features will first be added to the development branch, and eventually be merged with the main branch. You are currently on the development branch. To go to the main branch, select it from the drop-down menu on the top left, or [click here](https://github.com/Deep-MI/qatools-python/tree/freesurfer-module-releases).

___

## Installation

This software can be downloaded from its github repository at `https://github.com/Deep-MI/qatools-python`.

Alternatively, it can be cloned directly from its repository via `git clone https://github.com/Deep-MI/qatools-python`.

The `qatools.py` script will then be executable from the command line, as
detailed above.

Optional packages (if running the shape analysis module) include the `brainprint-python`
and `lapy` packages from https://github.com/Deep-MI. They can be installed using
`pip3 install --user git+https://github.com/Deep-MI/BrainPrint-python.git`
and `pip3 install --user git+https://github.com/Deep-MI/LaPy.git`. They should
both be version 0.2 or newer.
___

## Use as a python package

As an alternative to their command-line usage, the qc scripts can also be run
within a pure python environment, i.e. installed and imported as a python
package.

Use the following code to download, build and install a package from its github
repository into your local python package directory:

`pip3 install git+https://github.com/reuter-lab/qatools-python.git@freesurfer-module-dev`

Use `import qatoolspython` (or sth. equivalent) to import the package within a
python environment.

Use the `run_qatools` function from the `qatoolspython` module to run an
analysis:

`from qatoolspython import qatoolspython`

`qatoolspython.run_qatools(subjects_dir='/my/subjects/dir', output_dir='/my/output/dir')`

See `help(qatoolspython)` for further usage info and additional options.

___

## Running from a Docker image

We provide a `Dockerfile` that can be used to create a Docker image for the qatools-python scripts. Documentation is provided on the [Docker page](docker/Docker.md).

___

## Testing

Included with this toolbox is a `testing` subdirectory which contains two
testing routines, `testing.sh` and `testing.py`. These can be used to test the
installation and verify results.

These operate on a subset of the [Freesurfer tutorial data](https://surfer.nmr.mgh.harvard.edu/fswiki/FsTutorial/Data),
which must be downloaded separately.

Extracting the downloaded file with `tar -xzvf tutorial_data.tar.gz` should
give a `tutorial_data` directory. From `tutorial_data/buckner_data/tutorial_subjs/group_analysis_tutorial`,
copy the following subjects to the `testing/data` subdirectory within the
toolbox directory: `017`, `091`, `092`, `124`, `129`, `130`, `136`, and `145`.

Run the tests by executing `testing.sh` and/or `python3 testing.py` from within
the `testing` subdirectory of this toolbox.

___

## Known Issues

- Aborted / restarted recon-all runs: the program will analyze recon-all
  logfiles, and may fail or return erroneous results if the logfile is
  append by multiple restarts of recon-all runs. Ideally, the logfile should
  therefore consist of just a single, successful recon-all run.
- High-resolution data: Prior to update v1.4, the screenshots and fornix module
  did not work well with high-resolution data that was processed using the
  -cm flag in recon-all. With update v1.4 this has been fixed for the
  screenhots module, but the fornix module is still experimental for
  high-resolution data.

___

## Authors

- qatools-python: Kersten Diers, Tobias Wolff, and Martin Reuter.
- Freesurfer QA Tools: David Koh, Stephanie Lee, Jenni Pacheco, Vasanth Pappu,
  and Louis Vinke.
- shapeDNA and brainPrint toolboxes: Martin Reuter.

___

## Citations

- Esteban O, Birman D, Schaer M, Koyejo OO, Poldrack RA, Gorgolewski KJ; 2017;
  MRIQC: Advancing the Automatic Prediction of Image Quality in MRI from Unseen
  Sites; PLOS ONE 12(9):e0184661; doi:10.1371/journal.pone.0184661.

- Wachinger C, Golland P, Kremen W, Fischl B, Reuter M; 2015; BrainPrint: a
  Discriminative Characterization of Brain Morphology; Neuroimage: 109, 232-248;
  doi:10.1016/j.neuroimage.2015.01.032.

- Reuter M, Wolter FE, Shenton M, Niethammer M; 2009; Laplace-Beltrami
  Eigenvalues and Topological Features of Eigenfunctions for Statistical Shape
  Analysis; Computer-Aided Design: 41, 739-755; doi:10.1016/j.cad.2009.02.007.

- Potvin O, Mouiha A, Dieumegarde L, Duchesne S, & Alzheimer's Disease Neuroimaging
  Initiative; 2016; Normative data for subcortical regional volumes over the lifetime
  of the adult human brain; Neuroimage: 137, 9-20; doi.org/10.1016/j.neuroimage.2016.05.016

___

## Requirements

- A working installation of Freesurfer (6.0 or 7.x) must be sourced.

- At least one structural MR image that was processed with Freesurfer 6.0, 7.x,
  or FastSurfer 1.1 or later (including the surface pipeline).

- A Python version >= 3.5 is required to run this script.

- Required packages include (among others) the nibabel and skimage package for
  the core functionality, plus the matplotlib, pandas, and transform3d
  packages for some optional functions and modules. See the `requirements.txt`
  file for a complete list. Use `pip3 install -r requirements.txt` to install
  these packages.

- For the shape analysis module, the brainprint and lapy packages from https://github.com/Deep-MI
  are required (both version 0.2 or newer).

- This software has been tested on Ubuntu 22.04 and MacOS 10.15.

___

## License

This software is licensed under the MIT License, see associated LICENSE file
for details.

Copyright (c) 2019 Image Analysis Group, DZNE e.V.
