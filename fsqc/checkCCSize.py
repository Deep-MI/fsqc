"""
This module provides a function to check the relative size of the corpus callosum

"""
# -----------------------------------------------------------------------------


def checkCCSize(subjects_dir, subject):
    """
    Check the relative size of the corpus callosum.

    This function evaluates the relative size of the corpus callosum by computing
    the sum of its volumes from the aseg.stats file and dividing it by the total
    intracranial volume.

    Parameters
    ----------
    subjects_dir : str
        The directory containing subject data.
    subject : str
        The name of the subject.

    Returns
    -------
    relative_cc : float
        The relative size of the corpus callosum.

    Notes
    -----
    It requires a valid stats/aseg.stats file.
    """
    # Imports
    import logging
    import os

    import numpy as np

    # Message
    logging.info("Checking size of the corpus callosum ...")

    # Get file name and read contents
    path_stats_file = os.path.join(subjects_dir, subject, "stats", "aseg.stats")

    with open(path_stats_file) as stats_file:
        aseg_stats = stats_file.read().splitlines()

    # Initialize
    cc_elements = [
        "CC_Posterior",
        "CC_Mid_Posterior",
        "CC_Central",
        "CC_Mid_Anterior",
        "CC_Anterior",
    ]

    relative_cc = np.nan

    sum_cc = 0.0

    # Loop through the cc elements
    for cc_segmentation in cc_elements:
        # Look for the element in the aseg.stats line
        for aseg_stat_line in aseg_stats:
            # If the segmentation is found, compute the sum and return it.
            if cc_segmentation in aseg_stat_line:
                sum_cc += float(aseg_stat_line.split()[3])
            elif "EstimatedTotalIntraCranialVol" in aseg_stat_line:
                intracranial_volume = float(aseg_stat_line.split(",")[3])

    relative_cc = sum_cc / intracranial_volume

    logging.info(
        "Relative size of the corpus callosum is " + f"{relative_cc:.4}"
    )

    # Return
    return relative_cc
