Usage
=====

As a Command Line Tool
----------------------

.. code-block:: sh

    run_fsqc 
    --subjects_dir <directory> 
    --output_dir <directory>
    [--subjects SubjectID]
    [--subjects-file <file>] [--screenshots]
    [--screenshots-html] [--surfaces] [--surfaces-html]
    [--skullstrip] [--skullstrip-html]
    [--fornix] [--fornix-html] [--hippocampus]
    [--hippocampus-html] [--hippocampus-label ... ]
    [--hypothalamus] [--hypothalamus-html] [--shape]
    [--outlier] [--fastsurfer] [-h] [--more-help]
    [...]

    Required Arguments:
    -------------------
    --subjects_dir <directory>
        Subjects directory with a set of Freesurfer- or 
        Fastsurfer-processed individual datasets.

    --output_dir <directory>
        Output directory

    Optional Arguments:
    -------------------
    --subjects SubjectID [SubjectID ...]
        List of subject IDs

    --subjects-file <file>
        Filename of a file with subject IDs (one per line)

    --screenshots
        Create screenshots of individual brains

    --screenshots-html
        Create screenshots of individual brains incl. HTML summary page

    --surfaces
        Create screenshots of individual brain surfaces

    --surfaces-html
        Create screenshots of individual brain surfaces and HTML summary page

    --skullstrip
        Create screenshots of individual brainmasks

    --skullstrip-html
        Create screenshots of individual brainmasks and HTML summary page

    --fornix
        Check fornix segmentation

    --fornix-html
        Check fornix segmentation and create HTML summary page of fornix evaluation

    --hypothalamus
        Check hypothalamic segmentation

    --hypothalamus-html
        Check hypothalamic segmentation and create HTML summary page

    --hippocampus
        Check segmentation of hippocampus and amygdala

    --hippocampus-html
        Check segmentation of hippocampus and amygdala and create HTML summary page

    --hippocampus-label
        Specify label for hippocampus segmentation files (default: T1.v21). The full filename is then
        [lr]h.hippoAmygLabels-<LABEL>.FSvoxelSpace.mgz

    --shape
        Run shape analysis

    --outlier
        Run outlier detection

    --outlier-table
        Specify normative values (only in conjunction with --outlier)

    --fastsurfer
        Use FastSurfer instead of FreeSurfer output

    --exit-on-error
        Terminate the program when encountering an error; otherwise, try to continue with the next module or case

    Getting Help:
    -------------
    -h, --help
        Display this help message and exit
    --more-help
        Display extensive help message and exit

    Expert Options:
    ---------------
    --screenshots_base <image>
        Filename of an image that should be used instead of
        norm.mgz as the base image for the screenshots. Can be 
        an individual file (which would not be appropriate for 
        multi-subject analysis) or can be a file without 
        pathname and with the same filename across subjects within the 'mri'
        subdirectory of an individual FreeSurfer results directory 
        (which would be appropriate for multi-subject analysis).

    --screenshots_overlay <image>
        Path to an image that should be used instead of aseg.mgz 
        as the overlay image for the screenshots can also be none. 
        Can be an individual file (which would not be appropriate 
        for multi-subject analysis) or can be a file without pathname
        and with the same filename across subjects within the 'mri' subdirectory
        of an individual FreeSurfer results directory 
        (which would be appropriate for multi-subject analysis).

    --screenshots_surf <surf> [<surf> ...]
        One or more surface files that should be used instead of 
        [lr]h.white and [lr]h.pial; can also be none.
        Can be one or more individual file(s) (which would not 
        be appropriate for multi-subject analysis) or
        can be a (list of) file(s) without pathname and with the same 
        filename across subjects within the 'surf'
        subdirectory of an individual FreeSurfer results directory 
        (which would be appropriate for multi-subject analysis).

    --screenshots_views <view> [<view> ...]
        One or more views to use for the screenshots in the form of 
        x=<numeric> y=<numeric> and/or z=<numeric>.
        Order does not matter. Default views are x=-10 x=10 y=0 z=0.

    --screenshots_layout <rows> <columns>
        Layout matrix for screenshot images.

Examples:
---------
- Run the QC pipeline for all subjects found in /my/subjects/directory:
  ::

  ``run_fsqc --subjects_dir /my/subjects/directory --output_dir /my/output/directory``

- Run the QC pipeline for two specific subjects that need to be present in /my/subjects/directory:
  ::

  ``run_fsqc --subjects_dir /my/subjects/directory --output_dir /my/output/directory --subjects mySubjectID1 mySubjectID2``

- Run the QC pipeline for all subjects found in /my/subjects/directory after full FastSurfer processing:
  ::

  ``run_fsqc --subjects_dir /my/subjects/directory --output_dir /my/output/directory --fastsurfer``

- Run the QC pipeline plus the screenshots module for all subjects found in /my/subjects/directory:
  ::

  ``run_fsqc --subjects_dir /my/subjects/directory --output_dir /my/output/directory --screenshots``

- Run the QC pipeline plus the fornix pipeline for all subjects found in /my/subjects/directory:
  ::

  ``run_fsqc --subjects_dir /my/subjects/directory --output_dir /my/output/directory --fornix``

- Run the QC pipeline plus the shape analysis pipeline for all subjects found in /my/subjects/directory:
  ::

  ``run_fsqc --subjects_dir /my/subjects/directory --output_dir /my/output/directory --shape``

- Note that the ``--screenshots``, ``--fornix``, ``--shape``, and ``--outlier`` (and other) arguments can also be used in conjunction.


As a Python Package
-------------------

As an alternative to their command-line usage, the `fsqc` scripts can also be run within a pure Python environment, i.e., installed and imported as a Python package.

Use ``import fsqc`` (or equivalent) to import the package within a Python environment, and use the ``run_fsqc`` function from the ``fsqc`` module to run an analysis.

In its most basic form:

.. code-block:: python

   import fsqc
   fsqc.run_fsqc(subjects_dir='/my/subjects/dir', output_dir='/my/output/dir')

Specify subjects as a list:

.. code-block:: python

   import fsqc
   fsqc.run_fsqc(subjects_dir='/my/subjects/dir', output_dir='/my/output/dir', subjects=['subject1', 'subject2', 'subject3'])

And as a more elaborate example:

.. code-block:: python

   import fsqc
   fsqc.run_fsqc(subjects_dir='/my/subjects/dir', output_dir='/my/output/dir', subject_file='/my/subjects/file.txt', screenshots_html=True, surfaces_html=True, skullstrip_html=True, fornix_html=True, hypothalamus_html=True, hippocampus_html=True, hippocampus_label="T1.v21", shape=True, outlier=True)

Call ``help(fsqc.run_fsqc)`` for further usage info and additional options.


As a Docker Image
-----------------

We provide configuration files that can be used to create a Docker or Singularity image for the `fsqc` scripts.
Documentation can be found on the `Docker <https://github.com/Deep-MI/fsqc/blob/stable/docker/Docker.md>`_ and `Singularity <https://github.com/Deep-MI/fsqc/blob/stable/singularity/Singularity.md>`_ pages.

