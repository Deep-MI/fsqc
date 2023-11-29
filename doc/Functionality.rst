Functionality
=============

The core functionality of this toolbox is to compute the following features:

+------------+-----------------------------------------------------------------+
| Variable   | Description                                                     |
+============+=================================================================+
| subject    | Subject ID                                                      |
+------------+-----------------------------------------------------------------+
| wm_snr_orig| Signal-to-noise ratio for white matter in orig.mgz              |
+------------+-----------------------------------------------------------------+
| gm_snr_orig| Signal-to-noise ratio for gray matter in orig.mgz               |
+------------+-----------------------------------------------------------------+
| wm_snr_norm| Signal-to-noise ratio for white matter in norm.mgz              |
+------------+-----------------------------------------------------------------+
| gm_snr_norm| Signal-to-noise ratio for gray matter in norm.mgz               |
+------------+-----------------------------------------------------------------+
| cc_size    | Relative size of the corpus callosum                            |
+------------+-----------------------------------------------------------------+
| lh_holes   | Number of holes in the left hemisphere                          |
+------------+-----------------------------------------------------------------+
| rh_holes   | Number of holes in the right hemisphere                         |
+------------+-----------------------------------------------------------------+
| lh_defects | Number of defects in the left hemisphere                        |
+------------+-----------------------------------------------------------------+
| rh_defects | Number of defects in the right hemisphere                       |
+------------+-----------------------------------------------------------------+
| topo_lh    | Topological fixing time for the left hemisphere                 |
+------------+-----------------------------------------------------------------+
| topo_rh    | Topological fixing time for the right hemisphere                |
+------------+-----------------------------------------------------------------+
| con_lh_snr | WM/GM contrast signal-to-noise ratio in the left hemisphere     |
+------------+-----------------------------------------------------------------+
| con_rh_snr | WM/GM contrast signal-to-noise ratio in the right hemisphere    |
+------------+-----------------------------------------------------------------+
| rot_tal_x  | Rotation component of the Talairach transform around the x axis |
+------------+-----------------------------------------------------------------+
| rot_tal_y  | Rotation component of the Talairach transform around the y axis |
+------------+-----------------------------------------------------------------+
| rot_tal_z  | Rotation component of the Talairach transform around the z axis |
+------------+-----------------------------------------------------------------+

The program will use an existing output directory (or try to create it) and write a CSV table into that location. The CSV table will contain the above metrics plus a subject identifier.

The program can also be run on images that were processed with  `FastSurfer <https://github.com/Deep-MI/FastSurfer>`_ (v1.1 or later) instead of FreeSurfer. In that case, simply add a `--fastsurfer` switch to your shell command. Note that FastSurfer's full processing stream must have been run, including surface reconstruction (i.e. brain segmentation alone is not sufficient).

In addition to the core functionality of the toolbox, there are several optional modules that can be run according to need:

screenshots module
~~~~~~~~~~~~~~~~~~~

This module allows for the automated generation of cross-sections of the brain that are overlaid with the anatomical segmentations (asegs) and the white and pial surfaces. These images will be saved to the 'screenshots' subdirectory that will be created within the output directory. These images can be used for quickly glimpsing through the processing results. Note that no display manager is required for this module, i.e. it can be run on a remote server, for example.

surfaces module
~~~~~~~~~~~~~~~~

This module allows for the automated generation of surface renderings of the left and right pial and inflated surfaces, overlaid with the aparc annotation. These images will be saved to the 'surfaces' subdirectory that will be created within the output directory. These images can be used for quickly glimpsing through the processing results. Note that no display manager is required for this module, i.e. it can be run on a remote server, for example.

skullstrip module
~~~~~~~~~~~~~~~~~

This module allows for the automated generation cross-sections of the brain that are overlaid with the colored and semi-transparent brainmask. This allows checking the quality of the skullstripping in FreeSurfer. The resulting images will be saved to the 'skullstrip' subdirectory that will be created within the output directory.

fornix module
~~~~~~~~~~~~~~

This is a module to assess potential issues with the segmentation of the corpus callosum, which may incorrectly include parts of the fornix. To assess segmentation quality, a screenshot of the contours of the corpus callosum segmentation overlaid on the norm.mgz will be saved as 'cc.png' for each subject within the 'fornix' subdirectory of the output directory.

modules for the amygdala, hippocampus, and hypothalamus
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These modules evaluate potential missegmentations of the amygdala, hippocampus, and hypothalamus. To assess segmentation quality, screenshots will be created. These modules require prior processing of the MR images with FreeSurfer's dedicated toolboxes for the segmentation of the amygdala and hippocampus, and the hypothalamus, respectively.

shape module
~~~~~~~~~~~~~

The shape module will run a shapeDNA / brainprint analysis to compute distances of shape descriptors between lateralized brain structures. This can be used to identify discrepancies and irregularities between pairs of corresponding structures. The results will be included in the main csv table, and the output directory will also contain a 'brainprint' subdirectory.

outlier module
~~~~~~~~~~~~~~~

This is a module to detect extreme values among the subcortical ('aseg') segmentations as well as the cortical parcellations. If present, hypothalamic and hippocampal subsegmentations will also be included.

The outlier detection is based on comparisons with the distributions of the sample as well as normative values taken from the literature (see References).

For comparisons with the sample distributions, extreme values are defined in two ways: nonparametrically, i.e. values that are 1.5 times the interquartile range below or above the 25th or 75th percentile of the sample, respectively, and parametrically, i.e. values that are more than 2 standard deviations above or below the sample mean. Note that a minimum of 10 supplied subjects is required for running these analyses, otherwise NaNs will be returned.

For comparisons with the normative values, lower and upper bounds are computed from the 95% prediction intervals of the regression models given in Potvin et al., 1996, and values exceeding these bounds will be flagged. As an alternative, users may specify their own normative values by using the '--outlier-table' argument. This requires a custom csv table with headers label, upper, and lower, where label indicates a column of anatomical names. It can be a subset and the order is arbitrary, but naming must exactly match the nomenclature of the 'aseg.stats' and/or '[lr]h.aparc.stats' file. If cortical parcellations are included in the outlier table for a comparison with aparc.stats values, the labels must have a 'lh.' or 'rh.' prefix. file. upper and lower are user-specified upper and lower bounds.

The main csv table will be appended with the following summary variables, and more detailed output about will be saved as csv tables in the 'outliers' subdirectory of the main output directory:

+-------------------------+-----------------------------------------------------------------+
| Variable                | Description                                                     |
+=========================+=================================================================+
| n_outliers_sample_nonpar| Number of structures that are 1.5 times the IQR above/below the |
|                         | 75th/25th percentile                                            |
+-------------------------+-----------------------------------------------------------------+
| n_outliers_sample_param | Number of structures that are 2 SD above/below the mean         |
+-------------------------+-----------------------------------------------------------------+
| n_outliers_norms        | Number of structures exceeding the upper and lower bounds of    |
|                         | the normative values                                            |
+-------------------------+-----------------------------------------------------------------+
