"""
This module provides a function to check the SNR of the white and gray matter

"""

# -----------------------------------------------------------------------------


def checkSNR(
    subjects_dir,
    subject,
    nb_erode=3,
    ref_image="norm.mgz",
    aparc_image="aparc+aseg.mgz",
):
    """
    A function to check the SNR of the white and gray matter.

    This function checks the SNR of the white and the gray matter. The white
    matter segmentation is taken from the aparc+aseg image, and the gray matter
    from the aseg image. The white matter is eroded by three voxels to
    ignore partial volumes. For the gray matter, this is not possible because
    the layer is already very thin. An erosion would eliminate nearly the whole
    signal.

    Parameters
    ----------
    subjects_dir : str
        The directory containing subject data.
    subject : str
        The name of the subject.
    nb_erode : int, optional
        The number of erosions, default is 3.
    ref_image : str, optional
        The reference image, default is "norm.mgz", can be changed to "orig.mgz".
    aparc_image : str, optional
        The aparc+aseg image, default is "aparc+aseg.mgz", can
        be changed to "aparc+aseg.orig.mgz" for FastSurfer output.

    Returns
    -------
    wm_snr : float
        The signal-to-noise ratio of the white matter.
    gm_snr : float
        The signal-to-noise ratio of the gray matter.

    Notes
    -----
    It requires valid mri/norm.mgz, mri/aseg.mgz, and mri/aparc+aseg.mgz files for
    FreeSurfer output, and valid mri/norm.mgz, mri/aseg.mgz, and
    mri/aparc+aseg.orig.mgz files for FastSurfer output.
    If not found, NaNs will be returned.
    """
    # Imports

    import logging
    import os
    import warnings

    import nibabel as nib
    import numpy as np
    from skimage.morphology import binary_erosion

    # Settings

    logging.captureWarnings(True)

    # Message

    logging.info("Computing white and gray matter SNR for " + ref_image + " ...")

    # Get data

    path_reference_image = os.path.join(subjects_dir, subject, "mri", ref_image)
    if os.path.exists(path_reference_image):
        norm = nib.load(path_reference_image)
        norm_data = norm.get_fdata()
    else:
        warnings.warn(
            "WARNING: could not open " + path_reference_image + ", returning NaNs.",
            stacklevel = 2
        )
        return np.nan, np.nan

    path_aseg = os.path.join(subjects_dir, subject, "mri", "aseg.mgz")
    if os.path.exists(path_aseg):
        aseg = nib.load(path_aseg)
        data_aseg = aseg.get_fdata()
    else:
        warnings.warn("WARNING: could not open " + path_aseg + ", returning NaNs.",
            stacklevel = 2)
        return np.nan, np.nan

    path_aparc_aseg = os.path.join(subjects_dir, subject, "mri", aparc_image)
    if os.path.exists(path_aparc_aseg):
        inseg = nib.load(path_aparc_aseg)
        data_aparc_aseg = inseg.get_fdata()
    else:
        warnings.warn(
            "WARNING: could not open " + path_aparc_aseg + ", returning NaNs.",
            stacklevel = 2
        )
        return np.nan, np.nan

    # Process white matter image

    # Create 3D binary data where the white matter locations are encoded with 1, all the others with zero
    b_wm_data = np.zeros(norm.shape)

    # The following keys represent the white matter labels in the aparc+aseg image
    wm_labels = [2, 41, 7, 46, 251, 252, 253, 254, 255, 77, 78, 79]

    # Find the wm labels in the aparc+aseg image and set the locations in the binary image to one
    for i in wm_labels:
        x, y, z = np.where(data_aparc_aseg == i)
        b_wm_data[x, y, z] = 1

    # Erode white matter image
    nb_erode = nb_erode
    b_wm_data = binary_erosion(b_wm_data, np.ones((nb_erode, nb_erode, nb_erode)))

    # Computation of the SNR of the white matter
    x, y, z = np.where(b_wm_data == 1)
    signal_wm = norm_data[x, y, z]
    signal_wm_mean = np.mean(signal_wm)
    signal_wm_std = np.std(signal_wm)
    wm_snr = signal_wm_mean / signal_wm_std
    logging.info("White matter signal to noise ratio: " + f"{wm_snr:.4}")

    # Process gray matter image

    # Create 3D binary data where the gray matter locations are encoded with 1, all the others with zero
    b_gm_data = np.zeros(norm.shape)

    # The following keys represent the gray matter labels in the aseg image
    gm_labels = [3, 42]

    # Find the gm labels in the aseg image and set the locations in the binary image to one
    for i in gm_labels:
        x, y, z = np.where(data_aseg == i)
        b_gm_data[x, y, z] = 1

    # Computation of the SNR of the gray matter
    x, y, z = np.where(b_gm_data == 1)
    signal_gm = norm_data[x, y, z]
    signal_gm_mean = np.mean(signal_gm)
    signal_gm_std = np.std(signal_gm)
    gm_snr = signal_gm_mean / signal_gm_std
    logging.info("Gray matter signal to noise ratio: " + f"{gm_snr:.4}")

    # Return
    return wm_snr, gm_snr
