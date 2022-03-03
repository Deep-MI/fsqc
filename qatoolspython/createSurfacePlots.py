"""
This module provides a function to create surface plots

"""

# -----------------------------------------------------------------------------

def createSurfacePlots(SUBJECT, SUBJECTS_DIR, SURFACES_OUTDIR):

    """
    function createSurfacePlots

    requires the python kaleido package ("pip3 install --user -U kaleido")

    """

    # -----------------------------------------------------------------------------
    # imports

    import os
    import numpy as np
    import nibabel as nb
    import lapy as lp
    from lapy import Plot as lpp
    from lapy import TriaIO as lpio

    # -----------------------------------------------------------------------------
    # settings

    # -----------------------------------------------------------------------------
    # import surfaces and overlays

    triaPialL = lpio.import_fssurf(os.path.join(SUBJECTS_DIR, SUBJECT, 'surf', 'lh.pial'))
    triaPialR = lpio.import_fssurf(os.path.join(SUBJECTS_DIR, SUBJECT, 'surf', 'rh.pial'))
    triaInflL = lpio.import_fssurf(os.path.join(SUBJECTS_DIR, SUBJECT, 'surf', 'lh.inflated'))
    triaInflR = lpio.import_fssurf(os.path.join(SUBJECTS_DIR, SUBJECT, 'surf', 'rh.inflated'))

    annotL = nb.freesurfer.read_annot(os.path.join(SUBJECTS_DIR, SUBJECT, 'label', 'lh.aparc.annot'), orig_ids=False)
    annotR = nb.freesurfer.read_annot(os.path.join(SUBJECTS_DIR, SUBJECT, 'label', 'rh.aparc.annot'), orig_ids=False)

    # -----------------------------------------------------------------------------
    # plots

    # check if annotation has labels that are not included in the colortable
    if any(annotL[0]==-1):
        # prepend colortable and update indices
        ctabL = np.concatenate((np.mat([127, 127, 127]), annotL[1][:,0:3]), axis=0)
        indsL = annotL[0] + 1
    else:
        ctabL = annotL[1][:,0:3]
        indsL = annotL[0]

    vAnnotL = ctabL[annotL[0],:]

    # check if annotation has labels that are not included in the colortable
    if any(annotR[0]==-1):
        # prepend colortable and update indices
        ctabR = np.concatenate((np.mat([127, 127, 127]), annotR[1][:,0:3]), axis=0)
        indsR = annotR[0] + 1
    else:
        ctabR = annotR[1][:,0:3]
        indsR = annotR[0]

    vAnnotR = ctabR[annotR[0],:]

    # -----------------------------------------------------------------------------
    # plots

    camera = dict(
        up=dict(x=0, y=0, z=1),
        center=dict(x=0, y=0, z=0),
        eye=dict(x=-2, y=0, z=0))

    lpp.plot_tria_mesh(triaPialL, vcolor=vAnnotL, background_color="black", camera=camera, export_png=os.path.join(SURFACES_OUTDIR, 'lh.pial.png'), no_display=True, scale_png=0.25)

    camera = dict(
        up=dict(x=0, y=0, z=1),
        center=dict(x=0, y=0, z=0),
        eye=dict(x=2, y=0, z=0))

    lpp.plot_tria_mesh(triaPialR, vcolor=vAnnotR, background_color="black", camera=camera, export_png=os.path.join(SURFACES_OUTDIR, 'rh.pial.png'), no_display=True, scale_png=0.25)

    camera = dict(
        up=dict(x=0, y=0, z=1),
        center=dict(x=0, y=0, z=0),
        eye=dict(x=-2, y=0, z=0))

    lpp.plot_tria_mesh(triaInflL, vcolor=vAnnotL, background_color="black", camera=camera, export_png=os.path.join(SURFACES_OUTDIR, 'lh.inflated.png'), no_display=True, scale_png=0.25)

    camera = dict(
        up=dict(x=0, y=0, z=1),
        center=dict(x=0, y=0, z=0),
        eye=dict(x=2, y=0, z=0))

    lpp.plot_tria_mesh(triaInflR, vcolor=vAnnotR, background_color="black", camera=camera, export_png=os.path.join(SURFACES_OUTDIR, 'rh.inflated.png'), no_display=True, scale_png=0.25)
