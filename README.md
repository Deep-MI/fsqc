# qatools-python

___

## Description

This is a set of quality assurance / quality control scripts for Freesurfer 6.0
processed structural MRI data. 

It is a revision, extension, and translation to the Python language of the 
Freesurfer QA Tools that are provided at https://surfer.nmr.mgh.harvard.edu/fswiki/QATools

It has been augmented by additional functions from the MRIQC toolbox, available 
at https://github.com/poldracklab/mriqc and https://osf.io/haf97, and with code
derived from the shapeDNA and brainPrint toolboxes, available at 
https://reuter.mit.edu.

**The current version is a development version that can be used for testing 
purposes. It will be revised and extended in the future.**

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
segmentation quality, a screenshot of the contours of the corpus callosum 
segmentation overlaid on the norm.mgz will be saved as 'cc.png' for each 
subject within the 'fornix' subdirectory of the output directory. Further, a 
shapeDNA / brainPrint analysis will be conducted on a surface model of the 
corpus callosum. By comparing the resulting shape descriptors, which will 
appear in the main csv table, deviant segmentations may be detected. 

___

## Usage

```
python3 qatools.py --subjects_dir <directory> --output_dir <directory>
                          [--subjects SubjectID [SubjectID ...]] [--shape]
                          [--screenshots] [--fornix] [-h]


required arguments:
  --subjects_dir <directory>
                        subjects directory with a set of Freesurfer 6.0 processed
                        individual datasets.
  --output_dir <directory>
                        output directory

optional arguments:
  --subjects SubjectID [SubjectID ...]
                        list of subject IDs
  --screenshots         create screenshots
  --shape               run shape analysis (requires additional scripts)
  --fornix              check fornix segmentation

getting help:
  -h, --help            display this help message and exit
  
```

___

## Examples

- Run the QC pipeline for all subjects found in `/my/subjects/directory`:

    `python3 /my/scripts/directory/qatoolspython/qatools.py --subjects_dir /my/subjects/directory --output_dir /my/output/directory`

- Run the QC pipeline for two specific subjects that need to present in `/my/subjects/directory`:

    `python3 /my/scripts/directory/qatoolspython/qatools.py --subjects_dir /my/subjects/directory --output_dir /my/output/directory --subjects mySubjectID1 mySubjectID2`

- Run the QC pipeline plus the screenshots module for all subjects found in `/my/subjects/directory`:

    `python3 /my/scripts/directory/qatoolspython/qatools.py --subjects_dir /my/subjects/directory --output_dir /my/output/directory --screenshots`

- Run the QC pipeline plus the shape pipeline for all subjects found in `/my/subjects/directory`:

    `python3 /my/scripts/directory/qatoolspython/qatools.py --subjects_dir /my/subjects/directory --output_dir /my/output/directory --shape`

- Run the QC pipeline plus the fornix pipeline for all subjects found in `/my/subjects/directory`:

    `python3 /my/scripts/directory/qatoolspython/qatools.py --subjects_dir /my/subjects/directory --output_dir /my/output/directory --fornix`


___

## Installation

This software can be cloned from its github repository so that the `qatools.py` 
script is directly executable from the command line, as detailed above.

`git clone https://github.com/reuter-lab/qatools-python`

Alternatively, if the scripts will primarily be run from within a python 
environment, they can also be installed as a python package. Use the following 
code to download, build and install a package from its github repository into 
your local python package directory:

`pip3 install --user git+https://github.com/reuter-lab/qatools-python.git@freesurfer-module#egg=qatoolspython`

Use the following code to install the package in editable mode to a location of
your choice:

`pip3 install --user --src /my/preferred/location --editable git+https://github.com/reuter-lab/qatools-python.git@freesurfer-module#egg=qatoolspython`

Use `import qatoolspython` to import the package within a python environment.

The (optional) shape analysis module of this software depends on the 
`brainprintpython` package, which can be installed as follows:

`pip3 install --user git+https://github.com/reuter-lab/BrainPrint-python.git@freesurfer-module#egg=brainprintpython`

___

## Known Issues

The program will analyze recon-all logfiles, and may fail or return erroneous
results if the logfile is append by multiple restarts of recon-all runs. 
Ideally, the logfile should therefore consist of just a single, successful 
recon-all run.

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
  Analysis; Computer-Aided Design: 41, 739-755, doi:10.1016/j.cad.2009.02.007.

___

## Requirements

- A working installation of Freesurfer 6.0 or later must be sourced.

- At least one structural MR image that was processed with Freesurfer 6.0.

- A Python version >= 3.4 is required to run this script.

- Required packages include the nibabel and skimage package for the core
  functionality, plus the the matplotlib, pandas, and transform3d packages for 
  some optional functions and modules.

- For (optional) shape analysis, an installation of the brainprintpython
  package is required.

___

## License

This software is licensed under the MIT License, see associated LICENSE file 
for details.

Copyright (c) 2019 Image Analysis Group, DZNE e.V.

