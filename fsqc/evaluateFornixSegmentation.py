"""
This module provides a function to evaluate potential missegmentation of the fornix

"""

# -----------------------------------------------------------------------------


def evaluateFornixSegmentation(
    SUBJECT,
    SUBJECTS_DIR,
    OUTPUT_DIR,
    CREATE_SCREENSHOT=True,
    SCREENSHOTS_OUTFILE=[],
    RUN_SHAPEDNA=True,
    N_EIGEN=15,
):
    """
    A function to evaluate potential missegmentation of the fornix.

    This script evaluates potential missegmentation of the fornix, which may
    erroneously be attached to the 'corpus collosum' label.

    It will apply the cc_up.lta transform to the norm.mgz and the aseg files,
    and create a binary corpus callosum mask and surface. Resulting files are
    saved to subject-specific directories within the 'fornix' subdirectory of
    the output directory.

    If the corresponding arguments are set to 'True', the script will also
    create screenshots and run a shape analysis of the corpus callosum surface.
    Resulting files will be saved to the same directory as indicated above.

    Required arguments:
        - SUBJECT
        - SUBJECTS_DIR
        - OUTPUT_DIR

    Optional arguments:
        - CREATE_SCREENSHOT <bool> (default: True)
        - SCREENSHOTS_OUTFILE <string> or empty list (default: [])
        - RUN_SHAPEDNA <bool> (default: True)
        - N_EIGEN <int> number of Eigenvalues for shape analysis (default: 30)

    Requires (if not found, returns NaNs):
        - mri/transforms/cc_up.lta
        - mri/aseg.mgz
        - mri/norm.mgz

    Returns:
        - a numpy array of N_EIGEN eigenvalues if RUN_SHAPEDNA is True,
          otherwise a numpy array of NaNs of the same dimension

    """

    # --------------------------------------------------------------------------
    # imports

    import logging
    import os
    import warnings

    import nibabel as nb
    import numpy as np

    from fsqc.createScreenshots import createScreenshots
    from fsqc.fsqcUtils import applyTransform, binarizeImage

    # --------------------------------------------------------------------------
    # check files

    logging.captureWarnings(True)

    if not os.path.isfile(
        os.path.join(SUBJECTS_DIR, SUBJECT, "mri", "transforms", "cc_up.lta")
    ):
        warnings.warn(
            "WARNING: could not find "
            + os.path.join(SUBJECTS_DIR, SUBJECT, "mri", "transforms", "cc_up.lta")
            + ", returning NaNs"
        )

        out = np.empty(N_EIGEN)
        out[:] = np.nan

        return out

    elif not os.path.isfile(os.path.join(SUBJECTS_DIR, SUBJECT, "mri", "aseg.mgz")):
        warnings.warn(
            "WARNING: could not find "
            + os.path.join(SUBJECTS_DIR, SUBJECT, "mri", "aseg.mgz")
            + ", returning NaNs"
        )

        out = np.empty(N_EIGEN)
        out[:] = np.nan

        return out

    elif not os.path.isfile(os.path.join(SUBJECTS_DIR, SUBJECT, "mri", "norm.mgz")):
        warnings.warn(
            "WARNING: could not find "
            + os.path.join(SUBJECTS_DIR, SUBJECT, "mri", "norm.mgz")
            + ", returning NaNs"
        )

        out = np.empty(N_EIGEN)
        out[:] = np.nan

        return out

    if not SCREENSHOTS_OUTFILE:
        SCREENSHOTS_OUTFILE = os.path.join(OUTPUT_DIR, "cc.png")

    # --------------------------------------------------------------------------
    # conduct transform for aseg and norm

    applyTransform(
        os.path.join(SUBJECTS_DIR, SUBJECT, "mri", "aseg.mgz"),
        os.path.join(OUTPUT_DIR, "asegCCup.mgz"),
        mat_file=os.path.join(SUBJECTS_DIR, SUBJECT, "mri", "transforms", "cc_up.lta"),
        interp="nearest",
    )

    # when using 'make_upright', conducting the transform for norm.mgz is no
    # longer necessary (and will produce the same results)

    applyTransform(
        os.path.join(SUBJECTS_DIR, SUBJECT, "mri", "norm.mgz"),
        os.path.join(OUTPUT_DIR, "normCCup.mgz"),
        mat_file=os.path.join(SUBJECTS_DIR, SUBJECT, "mri", "transforms", "cc_up.lta"),
        interp="cubic",
    )

    # create fornix mask

    binarizeImage(
        os.path.join(OUTPUT_DIR, "asegCCup.mgz"),
        os.path.join(OUTPUT_DIR, "cc.mgz"),
        match=[251, 252, 253, 254, 255],
    )

    # --------------------------------------------------------------------------
    # create screenshot

    if CREATE_SCREENSHOT is True:
        hdr = nb.load(os.path.join(OUTPUT_DIR, "asegCCup.mgz"))
        x_coord = np.matmul(
            hdr.header.get_vox2ras_tkr(), np.array((128, 128, 128, 1))[:, np.newaxis]
        )[0]

        createScreenshots(
            SUBJECT=SUBJECT,
            SUBJECTS_DIR=SUBJECTS_DIR,
            INTERACTIVE=False,
            VIEWS=[("x", x_coord - 1), ("x", x_coord), ("x", x_coord + 1)],
            LAYOUT=(1, 3),
            BASE=[os.path.join(OUTPUT_DIR, "normCCup.mgz")],
            OVERLAY=[os.path.join(OUTPUT_DIR, "cc.mgz")],
            SURF=None,
            OUTFILE=SCREENSHOTS_OUTFILE,
        )

    # --------------------------------------------------------------------------
    # run shapeDNA

    if RUN_SHAPEDNA is True:
        import nibabel as nb
        from lapy import TriaMesh, shapedna

        surf = nb.freesurfer.io.read_geometry(
            os.path.join(OUTPUT_DIR, "cc.surf"), read_metadata=True
        )

        evDict = shapedna.compute_shapedna(TriaMesh(v=surf[0], t=surf[1]), k=N_EIGEN)

        ev = evDict["Eigenvalues"]
        evec = evDict["Eigenvectors"]

        d = dict()
        d["Refine"] = 0
        d["Degree"] = 1
        d["Dimension"] = 2
        d["Elements"] = len(surf[1])
        d["DoF"] = len(surf[0])
        d["NumEW"] = N_EIGEN
        d["Eigenvalues"] = ev
        d["Eigenvectors"] = evec

        # return
        return d["Eigenvalues"]

    else:
        out = np.empty(N_EIGEN)
        out[:] = np.nan

        return out
