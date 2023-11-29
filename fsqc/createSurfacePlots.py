"""
This module provides a function to create surface plots
"""
# -----------------------------------------------------------------------------


def createSurfacePlots(SUBJECT, SUBJECTS_DIR, SURFACES_OUTDIR, VIEWS, FASTSURFER):
    """
    Create surface plots.

    Parameters
    ----------
    SUBJECT : str
        The subject.
    SUBJECTS_DIR : str
        The subjects directory.
    SURFACES_OUTDIR : str
        The output directory for surface plots.
    VIEWS : list
        List of views for which surface plots should be created.
    FASTSURFER : bool
        Flag indicating whether FastSurfer processing was used.

    Returns
    -------
    None
        The function returns nothing.
    """
    # imports

    import os

    import lapy as lp
    import nibabel as nb
    import numpy as np
    from lapy import plot as lpp

    # -----------------------------------------------------------------------------
    # settings
    _views_available = [
        ("anterior", 0, 2, 0),
        ("posterior", 0, -2, 0),
        ("left", -2, 0, 0),
        ("right", 2, 0, 0),
        ("superior", 0, 0, 2),
        ("inferior", 0, 0, -2),
    ]
    scale_png = 0.8

    # -----------------------------------------------------------------------------
    # import surfaces and overlays

    triaPialL = nb.freesurfer.read_geometry(
        os.path.join(SUBJECTS_DIR, SUBJECT, "surf", "lh.pial")
    )
    triaPialR = nb.freesurfer.read_geometry(
        os.path.join(SUBJECTS_DIR, SUBJECT, "surf", "rh.pial")
    )
    triaInflL = nb.freesurfer.read_geometry(
        os.path.join(SUBJECTS_DIR, SUBJECT, "surf", "lh.inflated")
    )
    triaInflR = nb.freesurfer.read_geometry(
        os.path.join(SUBJECTS_DIR, SUBJECT, "surf", "rh.inflated")
    )

    triaPialL = lp.TriaMesh(triaPialL[0], triaPialL[1])
    triaPialR = lp.TriaMesh(triaPialR[0], triaPialR[1])
    triaInflL = lp.TriaMesh(triaInflL[0], triaInflL[1])
    triaInflR = lp.TriaMesh(triaInflR[0], triaInflR[1])

    if FASTSURFER is True:
        annotL = nb.freesurfer.read_annot(
            os.path.join(SUBJECTS_DIR, SUBJECT, "label", "lh.aparc.DKTatlas.annot"),
            orig_ids=False,
        )
        annotR = nb.freesurfer.read_annot(
            os.path.join(SUBJECTS_DIR, SUBJECT, "label", "rh.aparc.DKTatlas.annot"),
            orig_ids=False,
        )
    else:
        annotL = nb.freesurfer.read_annot(
            os.path.join(SUBJECTS_DIR, SUBJECT, "label", "lh.aparc.annot"),
            orig_ids=False,
        )
        annotR = nb.freesurfer.read_annot(
            os.path.join(SUBJECTS_DIR, SUBJECT, "label", "rh.aparc.annot"),
            orig_ids=False,
        )

    # -----------------------------------------------------------------------------
    # plots

    # check if annotation has labels that are not included in the colortable
    if any(annotL[0] == -1):
        # prepend colortable and update indices
        ctabL = np.concatenate((np.mat([127, 127, 127]), annotL[1][:, 0:3]), axis=0)
        indsL = annotL[0] + 1
    else:
        ctabL = annotL[1][:, 0:3]
        indsL = annotL[0]

    vAnnotL = ctabL[indsL, :]

    # check if annotation has labels that are not included in the colortable
    if any(annotR[0] == -1):
        # prepend colortable and update indices
        ctabR = np.concatenate((np.mat([127, 127, 127]), annotR[1][:, 0:3]), axis=0)
        indsR = annotR[0] + 1
    else:
        ctabR = annotR[1][:, 0:3]
        indsR = annotR[0]

    vAnnotR = ctabR[indsR, :]

    # -----------------------------------------------------------------------------
    # plots

    for view, x, y, z in _views_available:
        fpath_lp = os.path.join(SURFACES_OUTDIR, f"lh.pial.{view}.png")
        fpath_rp = os.path.join(SURFACES_OUTDIR, f"rh.pial.{view}.png")
        fpath_li = os.path.join(SURFACES_OUTDIR, f"lh.inflated.{view}.png")
        fpath_ri = os.path.join(SURFACES_OUTDIR, f"rh.inflated.{view}.png")

        if view in VIEWS:
            camera = dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=x, y=y, z=z),
            )

            lpp.plot_tria_mesh(
                triaPialL,
                vcolor=vAnnotL,
                background_color="black",
                camera=camera,
                export_png=fpath_lp,
                no_display=True,
                scale_png=scale_png,
            )
            lpp.plot_tria_mesh(
                triaPialR,
                vcolor=vAnnotR,
                background_color="black",
                camera=camera,
                export_png=fpath_rp,
                no_display=True,
                scale_png=scale_png,
            )
            lpp.plot_tria_mesh(
                triaInflL,
                vcolor=vAnnotL,
                background_color="black",
                camera=camera,
                export_png=fpath_li,
                no_display=True,
                scale_png=scale_png,
            )
            lpp.plot_tria_mesh(
                triaInflR,
                vcolor=vAnnotR,
                background_color="black",
                camera=camera,
                export_png=fpath_ri,
                no_display=True,
                scale_png=scale_png,
            )
        else:
            # remove images potentially created in earlier run but not updated now
            for fpath in [fpath_lp, fpath_rp, fpath_li, fpath_ri]:
                if os.path.isfile(fpath):
                    os.remove(fpath)
