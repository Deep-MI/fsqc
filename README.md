# qatools-python

___

## Description

This is a set of quality assurance / quality control scripts for Freesurfer 6.0
processed structural MRI data. It is a revision and translation to python of 
the original Freesurfer QA Tools that are provided at 
https://surfer.nmr.mgh.harvard.edu/fswiki/QATools

It has been augmented by additional functions from the MRIQC toolbox, available 
at https://github.com/poldracklab/mriqc and https://osf.io/haf97, and with the
shapeDNA and brainPrint toolboxes, available at https://reuter.mit.edu.

**The current version is a development version that can be used for testing 
purposes. It will almost certainly be revised, corrected, and extended in the 
future.**

The program will use an existing output directory (or try to create it) and 
write a csv table (`qatools-results.csv`) into that location. The csv table 
will contain the following variables/metrics:

variable       |   description
---------------|----------------------------------------------------------------
subject        |   subject ID
wm_snr_orig    |   signal-to-noise for white matter in orig.mgz
gm_snr_orig    |   signal-to-noise for gray matter in orig.mgz
wm_snr_norm    |   signal-to-noise for white matter in norm.mgz
gm_snr_norm    |   signal-to-noise for gray matter in norm.mgz
cc_size        |   size of the corpus callosum
lh_holes       |   number of holes in the left hemisphere
rh_holes       |   number of holes in the right hemisphere
lh_defects     |   number of defects in the left hemisphere
rh_defects     |   number of defects in the right hemisphere
topo_lh        |   topological fixing time for the left hemisphere
topo_rh        |   topological fixing time for the right hemisphere
con_lh_snr     |   wm/gm contrast signal-to-noise ration in the left hemisphere
con_rh_snr     |   wm/gm contrast signal-to-noise ration in the right hemisphere

If the (optional) shape pipeline was run in addition to the core pipeline, the 
output directory will also contain results files of the brainPrint analysis, 
and the above csv table will contain several additional metrics: for a number 
of lateralized brain structures (e.g., ventricles, subcortical structures, 
gray and white matter), the lateral asymmetry will be computed, i.e. distances
between numerical shape descriptors, where large values indicate large 
asymmetries and hence potential issues with the segmentation of these 
structures.

___

## Usage

```
python3 quality_checker.py --subjects_dir <directory> --output_dir <directory>
                          [--subjects SubjectID [SubjectID ...]] [--shape]
                          [--norms <file>] [-h]
                      

required arguments:
  --subjects_dir <directory>
                        subjects directory with a set of Freesurfer 6.0 processed
                        individual datasets.
  --output_dir <directory>
                        output directory

optional arguments:
  --subjects SubjectID [SubjectID ...]
                        list of subject IDs
  --shape               run shape analysis (requires additional scripts)
  --norms <file>        path to file with normative values

getting help:
  -h, --help            display this help message and exit
  
```

___

## Examples

- The following example will run the QC pipeline for all subjects found in `/my/subjects/directory`:

    `python3 /my/scripts/directory/quality_checker.py --subjects_dir /my/subjects/directory --output_dir /my/output/directory`

- The following example will run the QC pipeline plus the shape pipeline for all subjects found in `/my/subjects/directory`:

    `python3 /my/scripts/directory/quality_checker.py --subjects_dir /my/subjects/directory --output_dir /my/output/directory --shape`

- The following example will run the QC pipeline for two specific subjects that need to present in `/my/subjects/directory`:

    `python3 /my/scripts/directory/quality_checker.py --subjects_dir /my/subjects/directory --output_dir /my/output/directory --subjects mySubjectID1 mySubjectID2`

___

## Authors

- qatools-python: Tobias Wolff, Kersten Diers, and Martin Reuter.
- Freesurfer QA Tools: David Koh, Stephanie Lee, Jenni Pacheco, Vasanth Pappu, 
  and Louis Vinke. 
- MRIQC toolbox: Oscar Esteban, Daniel Birman, Marie Schaer, Oluwasanmi Koyejo, 
  Russell Poldrack, and Krzysztof Gorgolewski.
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

- At least one structural MR image that was processed with Freesurfer 6.0.

- A Python version >= 3.4 is required to run this script.

- Required packages include the skimage and nibabel packages.

- For (optional) shape analysis, a working version of Freesurfer, the shapeDNA 
  scripts and the brainPrint scripts are required. See https://reuter.mit.edu 
  for download options.

___

## License

