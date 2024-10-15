"""
This module provides a function to evaluate potential missegmentation of the
hippocampus and amygdala
"""
# --------------------------------------------------------------------------


def evaluateHippocampalSegmentation(
    SUBJECT,
    SUBJECTS_DIR,
    OUTPUT_DIR,
    CREATE_SCREENSHOT=True,
    SCREENSHOTS_OUTFILE=None,
    SCREENSHOTS_ORIENTATION="radiological",
    HEMI="lh",
    LABEL="T1.v21",
):
    """
    Evaluate potential missegmentation of the hippocampus and amygdala.

    This script evaluates potential missegmentation of the hippocampus and
    amygdala as created by FreeSurfer 7.1's dedicated module:
    https://surfer.nmr.mgh.harvard.edu/fswiki/HippocampalSubfieldsAndNucleiOfAmygdala

    If the corresponding arguments are set to 'True', the script will also
    create screenshots. Resulting files will be saved to the same directory
    as indicated above.

    Parameters
    ----------
    SUBJECT : str
        The subject identifier.
    SUBJECTS_DIR : str
        The directory containing subject data.
    OUTPUT_DIR : str
        The output directory.
    CREATE_SCREENSHOT : bool, optional, default: True
        Whether to create screenshots.
    SCREENSHOTS_OUTFILE : str or list, optional, default: None
        File or list of files for screenshots.
    SCREENSHOTS_ORIENTATION : str, optional, default: "radiological"
        Orientation for screenshots.
    HEMI : str, optional, default: "lh"
        Hemisphere to evaluate, either 'lh' or 'rh'.
    LABEL : str, optional, default: "T1.v21"
        Label for hippocampal and amygdala segmentation.

    Returns
    -------
    None
        This function returns nothing.

    Notes
    -----
    Required Files:
    - mri/[lr]h.hippoAmygLabels-<LABEL>.FSvoxelSpace.mgz
    - mri/norm.mgz
    """
    # imports

    import logging
    import os

    import nibabel as nb
    import numpy as np
    from scipy import ndimage

    from fsqc.createScreenshots import createScreenshots
    from fsqc.fsqcUtils import binarizeImage

    # --------------------------------------------------------------------------
    # check files

    if not os.path.isfile(os.path.join(SUBJECTS_DIR, SUBJECT, "mri", "norm.mgz")):
        logging.error(
            "ERROR: could not find "
            + os.path.join(SUBJECTS_DIR, SUBJECT, "mri", "norm.mgz")
            + ", not running hippocampus module."
        )

        raise ValueError("File not found")

    if not os.path.isfile(
        os.path.join(
            SUBJECTS_DIR,
            SUBJECT,
            "mri",
            HEMI + ".hippoAmygLabels-" + LABEL + ".FSvoxelSpace.mgz",
        )
    ):
        logging.error(
            "ERROR: could not find "
            + os.path.join(
                SUBJECTS_DIR,
                SUBJECT,
                "mri",
                HEMI + ".hippoAmygLabels-" + LABEL + ".FSvoxelSpace.mgz",
            )
            + ", not running hippocampus module."
        )

        raise ValueError("File not found")

    if SCREENSHOTS_OUTFILE is None:
        SCREENSHOTS_OUTFILE = os.path.join(OUTPUT_DIR, "hippocampus.png")

    # --------------------------------------------------------------------------
    # create mask

    binarizeImage(
        os.path.join(
            SUBJECTS_DIR,
            SUBJECT,
            "mri",
            HEMI + ".hippoAmygLabels-" + LABEL + ".FSvoxelSpace.mgz",
        ),
        os.path.join(OUTPUT_DIR, "hippocampus-" + HEMI + ".mgz"),
        match=None,
    )

    # --------------------------------------------------------------------------
    # get centroids

    seg = nb.load(
        os.path.join(
            SUBJECTS_DIR,
            SUBJECT,
            "mri",
            HEMI + ".hippoAmygLabels-" + LABEL + ".FSvoxelSpace.mgz",
        )
    )
    seg_data = seg.get_fdata()
    seg_labels = np.setdiff1d(np.unique(seg_data), 0)

    centroids = np.array(ndimage.center_of_mass(seg_data, seg_data, seg_labels))
    centroids = np.concatenate((seg_labels[:, np.newaxis], centroids), axis=1)

    vox2ras_tkr = seg.header.get_vox2ras_tkr()

    ctr_tkr = np.concatenate(
        (centroids[:, 1:4], np.ones((centroids.shape[0], 1))), axis=1
    )
    ctr_tkr = np.matmul(vox2ras_tkr, ctr_tkr.T).T
    ctr_tkr = np.concatenate(
        (np.array(centroids[:, 0], ndmin=2).T, ctr_tkr[:, 0:3]), axis=1
    )

    # [7004, 237, 238]

    ctr_tkr_x0 = ctr_tkr[np.argwhere(ctr_tkr[:, 0] == 237), 1]
    ctr_tkr_y0 = ctr_tkr[np.argwhere(ctr_tkr[:, 0] == 237), 2]
    ctr_tkr_z0 = ctr_tkr[np.argwhere(ctr_tkr[:, 0] == 237), 3]

    # set ranges for cropping the image (assuming RAS coordinates)

    ctr_tkr_x0_xlim = [ctr_tkr_y0 - 40, ctr_tkr_y0 + 40]
    ctr_tkr_y0_xlim = [ctr_tkr_x0 - 20, ctr_tkr_x0 + 20]
    ctr_tkr_z0_xlim = [ctr_tkr_x0 - 20, ctr_tkr_x0 + 20]

    ctr_tkr_x0_ylim = [ctr_tkr_z0 - 40, ctr_tkr_z0 + 40]
    ctr_tkr_y0_ylim = [ctr_tkr_z0 - 40, ctr_tkr_z0 + 40]
    ctr_tkr_z0_ylim = [ctr_tkr_y0 - 40, ctr_tkr_y0 + 40]

    XLIM = [ctr_tkr_x0_xlim, ctr_tkr_y0_xlim, ctr_tkr_z0_xlim]
    YLIM = [ctr_tkr_x0_ylim, ctr_tkr_y0_ylim, ctr_tkr_z0_ylim]

    # --------------------------------------------------------------------------
    # create screenshots

    if CREATE_SCREENSHOT is True:
        createScreenshots(
            SUBJECT=SUBJECT,
            SUBJECTS_DIR=SUBJECTS_DIR,
            INTERACTIVE=False,
            VIEWS=[("x", ctr_tkr_x0), ("y", ctr_tkr_y0), ("z", ctr_tkr_z0)],
            LAYOUT=(1, 3),
            BASE=os.path.join(SUBJECTS_DIR, SUBJECT, "mri", "norm.mgz"),
            OVERLAY=os.path.join(
                SUBJECTS_DIR,
                SUBJECT,
                "mri",
                HEMI + ".hippoAmygLabels-" + LABEL + ".FSvoxelSpace.mgz",
            ),
            SURF=None,
            OUTFILE=SCREENSHOTS_OUTFILE,
            ORIENTATION=SCREENSHOTS_ORIENTATION,
            XLIM=XLIM,
            YLIM=YLIM,
        )
