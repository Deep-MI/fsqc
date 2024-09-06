"""
This module provides a function to compute the WM/GM contrast SNR.
"""


# -----------------------------------------------------------------------------
def checkContrast(subjects_dir, subject):
    """
    Compute the WM/GM contrast SNR.

    This function computes the WM/GM contrast SNR based on the output of the
    pctsurfcon function.

    Parameters
    ----------
    subjects_dir : str
        The directory containing subject data.
    subject : str
        The name of the subject.

    Returns
    -------
    con_lh_snr : float
        Signal-to-noise ratio (SNR) for the left hemisphere WM/GM contrast.
    con_rh_snr : float
        Signal-to-noise ratio (SNR) for the right hemisphere WM/GM contrast.

    Notes
    -----
    It requires surf/[lr]h.w-g.pct.mgh and label/[lr]h.cortex.label.
    If not found, NaNs will be returned.
    """
    # Imports
    import logging
    import os
    import warnings

    import nibabel
    import numpy

    from fsqc.fsqcUtils import importMGH

    # Settings
    logging.captureWarnings(True)

    # Message
    logging.info("Checking WM/GM contrast SNR ...")

    # Check if files exist
    path_pct_lh = os.path.join(subjects_dir, subject, "surf", "lh.w-g.pct.mgh")
    if not os.path.exists(path_pct_lh):
        warnings.warn("WARNING: could not find " + path_pct_lh + ", returning NaNs",
            stacklevel = 2)
        return numpy.nan

    path_pct_rh = os.path.join(subjects_dir, subject, "surf", "rh.w-g.pct.mgh")
    if not os.path.exists(path_pct_rh):
        warnings.warn("WARNING: could not find " + path_pct_rh + ", returning NaNs",
            stacklevel = 2)
        return numpy.nan

    path_label_cortex_lh = os.path.join(
        subjects_dir, subject, "label", "lh.cortex.label"
    )
    if not os.path.exists(path_label_cortex_lh):
        warnings.warn(
            "WARNING: could not find " + path_label_cortex_lh + ", returning NaNs",
            stacklevel = 2
        )
        return numpy.nan

    path_label_cortex_rh = os.path.join(
        subjects_dir, subject, "label", "rh.cortex.label"
    )
    if not os.path.exists(path_label_cortex_rh):
        warnings.warn(
            "WARNING: could not find " + path_label_cortex_rh + ", returning NaNs",
            stacklevel = 2
        )
        return numpy.nan

    # Get the data from the mgh files
    con_lh = importMGH(path_pct_lh)
    con_rh = importMGH(path_pct_rh)

    label_array_lh = nibabel.freesurfer.io.read_label(path_label_cortex_lh)
    label_array_rh = nibabel.freesurfer.io.read_label(path_label_cortex_rh)

    # Only take the values of the cortex to compute the contrast control
    con_lh = numpy.take(con_lh, label_array_lh)
    con_rh = numpy.take(con_rh, label_array_rh)

    # Compute the Contrast to noise ratio
    con_lh_mean = numpy.mean(con_lh)
    con_lh_std = numpy.std(con_lh)
    con_lh_snr = con_lh_mean / con_lh_std
    logging.info(
        "WM/GM contrast SNR for the left hemisphere: " + f"{con_lh_snr:.4}"
    )

    con_rh_mean = numpy.mean(con_rh)
    con_rh_std = numpy.std(con_rh)
    con_rh_snr = con_rh_mean / con_rh_std
    logging.info(
        "WM/GM contrast SNR for the right hemisphere: " + f"{con_rh_snr:.4}"
    )

    # Return
    return con_lh_snr, con_rh_snr
