"""
This module provides a function to evaluate potential missegmentation of the hypothalamus

"""

# -----------------------------------------------------------------------------


def evaluateHypothalamicSegmentation(
    SUBJECT,
    SUBJECTS_DIR,
    OUTPUT_DIR,
    CREATE_SCREENSHOT=True,
    SCREENSHOTS_OUTFILE=None,
    SCREENSHOTS_ORIENTATION="radiological",
):
    """
    Evaluate potential missegmentation of the hypothalamus.

    This script evaluates potential missegmentation of the hypothalamus as
    created by FreeSurfer 7.2's module for hypothalamic segmentation:
    https://surfer.nmr.mgh.harvard.edu/fswiki/HypothalamicSubunits.

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

    Returns
    -------
    None
        This function return nothing.

    Notes
    -----
    Required Files:
    - mri/hypothalamic_subunits_seg.v1.mgz
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
            + ", not running hypothalamus module."
        )

        raise ValueError("File not found")

    if not os.path.isfile(
        os.path.join(SUBJECTS_DIR, SUBJECT, "mri", "hypothalamic_subunits_seg.v1.mgz")
    ):
        logging.error(
            "ERROR: could not find "
            + os.path.join(
                SUBJECTS_DIR, SUBJECT, "mri", "hypothalamic_subunits_seg.v1.mgz"
            )
            + ", not running hypothalamus module."
        )

        raise ValueError("File not found")

    if SCREENSHOTS_OUTFILE is None:
        SCREENSHOTS_OUTFILE = os.path.join(OUTPUT_DIR, "hypothalamus.png")

    # --------------------------------------------------------------------------
    # create mask

    binarizeImage(
        os.path.join(SUBJECTS_DIR, SUBJECT, "mri", "hypothalamic_subunits_seg.v1.mgz"),
        os.path.join(OUTPUT_DIR, "hypothalamus.mgz"),
        match=[801, 802, 803, 804, 805, 806, 807, 808, 809, 810],
    )

    # --------------------------------------------------------------------------
    # get centroids

    seg = nb.load(
        os.path.join(SUBJECTS_DIR, SUBJECT, "mri", "hypothalamic_subunits_seg.v1.mgz")
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

    #

    ctr_tkr_x0 = ctr_tkr[3, 1]
    ctr_tkr_x1 = ctr_tkr[8, 1]
    ctr_tkr_y0 = (ctr_tkr[0, 2] + ctr_tkr[5, 2]) / 2
    ctr_tkr_y1 = (ctr_tkr[1, 2] + ctr_tkr[6, 2]) / 2
    ctr_tkr_y2 = (ctr_tkr[3, 2] + ctr_tkr[8, 2]) / 2
    ctr_tkr_y3 = (ctr_tkr[4, 2] + ctr_tkr[9, 2]) / 2
    ctr_tkr_y4 = (ctr_tkr[2, 2] + ctr_tkr[7, 2]) / 2
    ctr_tkr_z0 = (ctr_tkr[2, 3] + ctr_tkr[7, 3]) / 2
    ctr_tkr_z1 = (ctr_tkr[4, 3] + ctr_tkr[9, 3]) / 2

    # set ranges for cropping the image (assuming RAS coordinates)

    ctr_tkr_x0_xlim = [ctr_tkr[3, 2] - 20, ctr_tkr[3, 2] + 20]
    ctr_tkr_x1_xlim = [ctr_tkr[8, 2] - 20, ctr_tkr[8, 2] + 20]

    ctr_tkr_y0_xlim = [
        (ctr_tkr[0, 1] + ctr_tkr[5, 1]) / 2 - 20,
        (ctr_tkr[0, 1] + ctr_tkr[5, 1]) / 2 + 20,
    ]
    ctr_tkr_y1_xlim = [
        (ctr_tkr[1, 1] + ctr_tkr[6, 1]) / 2 - 20,
        (ctr_tkr[1, 1] + ctr_tkr[6, 1]) / 2 + 20,
    ]
    ctr_tkr_y2_xlim = [
        (ctr_tkr[3, 1] + ctr_tkr[8, 1]) / 2 - 20,
        (ctr_tkr[3, 1] + ctr_tkr[8, 1]) / 2 + 20,
    ]
    ctr_tkr_y3_xlim = [
        (ctr_tkr[4, 1] + ctr_tkr[9, 1]) / 2 - 20,
        (ctr_tkr[4, 1] + ctr_tkr[9, 1]) / 2 + 20,
    ]
    ctr_tkr_y4_xlim = [
        (ctr_tkr[2, 1] + ctr_tkr[7, 1]) / 2 - 20,
        (ctr_tkr[2, 1] + ctr_tkr[7, 1]) / 2 + 20,
    ]

    ctr_tkr_z0_xlim = [
        (ctr_tkr[2, 1] + ctr_tkr[7, 1]) / 2 - 20,
        (ctr_tkr[2, 1] + ctr_tkr[7, 1]) / 2 + 20,
    ]
    ctr_tkr_z1_xlim = [
        (ctr_tkr[4, 1] + ctr_tkr[9, 1]) / 2 - 20,
        (ctr_tkr[4, 1] + ctr_tkr[9, 1]) / 2 + 20,
    ]

    ctr_tkr_x0_ylim = [ctr_tkr[3, 3] - 20, ctr_tkr[3, 3] + 20]
    ctr_tkr_x1_ylim = [ctr_tkr[8, 3] - 20, ctr_tkr[8, 3] + 20]

    ctr_tkr_y0_ylim = [
        (ctr_tkr[0, 3] + ctr_tkr[5, 3]) / 2 - 20,
        (ctr_tkr[0, 3] + ctr_tkr[5, 3]) / 2 + 20,
    ]
    ctr_tkr_y1_ylim = [
        (ctr_tkr[1, 3] + ctr_tkr[6, 3]) / 2 - 20,
        (ctr_tkr[1, 3] + ctr_tkr[6, 3]) / 2 + 20,
    ]
    ctr_tkr_y2_ylim = [
        (ctr_tkr[3, 3] + ctr_tkr[8, 3]) / 2 - 20,
        (ctr_tkr[3, 3] + ctr_tkr[8, 3]) / 2 + 20,
    ]
    ctr_tkr_y3_ylim = [
        (ctr_tkr[4, 3] + ctr_tkr[9, 3]) / 2 - 20,
        (ctr_tkr[4, 3] + ctr_tkr[9, 3]) / 2 + 20,
    ]
    ctr_tkr_y4_ylim = [
        (ctr_tkr[2, 3] + ctr_tkr[7, 3]) / 2 - 20,
        (ctr_tkr[2, 3] + ctr_tkr[7, 3]) / 2 + 20,
    ]

    ctr_tkr_z0_ylim = [
        (ctr_tkr[2, 2] + ctr_tkr[7, 2]) / 2 - 20,
        (ctr_tkr[2, 2] + ctr_tkr[7, 2]) / 2 + 20,
    ]
    ctr_tkr_z1_ylim = [
        (ctr_tkr[4, 2] + ctr_tkr[9, 2]) / 2 - 20,
        (ctr_tkr[4, 2] + ctr_tkr[9, 2]) / 2 + 20,
    ]

    XLIM = [
        ctr_tkr_x0_xlim,
        ctr_tkr_x1_xlim,
        ctr_tkr_y0_xlim,
        ctr_tkr_y1_xlim,
        ctr_tkr_y2_xlim,
        ctr_tkr_y3_xlim,
        ctr_tkr_y4_xlim,
        ctr_tkr_z0_xlim,
        ctr_tkr_z1_xlim,
    ]

    YLIM = [
        ctr_tkr_x0_ylim,
        ctr_tkr_x1_ylim,
        ctr_tkr_y0_ylim,
        ctr_tkr_y1_ylim,
        ctr_tkr_y2_ylim,
        ctr_tkr_y3_ylim,
        ctr_tkr_y4_ylim,
        ctr_tkr_z0_ylim,
        ctr_tkr_z1_ylim,
    ]

    # --------------------------------------------------------------------------
    # create screenshot

    if CREATE_SCREENSHOT is True:
        createScreenshots(
            SUBJECT=SUBJECT,
            SUBJECTS_DIR=SUBJECTS_DIR,
            INTERACTIVE=False,
            VIEWS=[
                ("x", ctr_tkr_x0),
                ("x", ctr_tkr_x1),
                ("y", ctr_tkr_y0),
                ("y", ctr_tkr_y1),
                ("y", ctr_tkr_y2),
                ("y", ctr_tkr_y3),
                ("y", ctr_tkr_y4),
                ("z", ctr_tkr_z0),
                ("z", ctr_tkr_z1),
            ],
            LAYOUT=(1, 9),
            BASE=os.path.join(SUBJECTS_DIR, SUBJECT, "mri", "norm.mgz"),
            OVERLAY=os.path.join(
                SUBJECTS_DIR, SUBJECT, "mri", "hypothalamic_subunits_seg.v1.mgz"
            ),
            SURF=None,
            OUTFILE=SCREENSHOTS_OUTFILE,
            ORIENTATION=SCREENSHOTS_ORIENTATION,
            XLIM=XLIM,
            YLIM=YLIM,
        )
