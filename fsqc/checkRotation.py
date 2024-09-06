"""
This module provides a function to determine rotation angles of the Talairach transform

"""
# -------------------------------------------------------------------------------------


def checkRotation(subjects_dir, subject):
    """
    CheckRotation determines rotation angles of the Talairach transform.

    Parameters
    ----------
    subjects_dir : str
        The directory containing subject data.
    subject : str
        The name of the subject.

    Returns
    -------
    rot_tal_x : float
        Rotation angle around the x-axis in radians.
    rot_tal_y : float
        Rotation angle around the y-axis in radians.
    rot_tal_z : float
        Rotation angle around the z-axis in radians.

    Notes
    -----
    The unit of rotations is radians.

    Requires a valid mri/transforms/talairach.lta file and the 'transforms3d'
    python package. If not found, NaNs will be returned.
    """
    import importlib.util
    import logging
    import os
    import re
    import warnings

    import numpy as np

    # settings

    logging.captureWarnings(True)

    # message

    logging.info("Computing Talairach rotation angles ...")

    if importlib.util.find_spec("transforms3d") is None:
        warnings.warn(
            "WARNING: 'transforms3d' package required for running this script, returning NaNs.",
            stacklevel = 2
        )
        return np.nan, np.nan, np.nan
    else:
        import transforms3d as tr

    # read talairach.lta

    if not os.path.isfile(
        os.path.join(subjects_dir, subject, "mri", "transforms", "talairach.lta")
    ):
        warnings.warn(
            "WARNING: could not open "
            + os.path.join(subjects_dir, subject, "mri", "transforms", "talairach.lta")
            + ", returning NaNs.",
            stacklevel = 2
        )
        return np.nan, np.nan, np.nan

    with open(
        os.path.join(subjects_dir, subject, "mri", "transforms", "talairach.lta")
    ) as datafile:
        lines = datafile.readlines()

    # get first four rows with three entries in exp notation

    mat = list()
    for line in lines:
        res = re.search(
            "^[\\-0-9]+\\.[0-9]+e[\\-\\+][0-9]+ [\\-0-9]+\\.[0-9]+e[\\-\\+][0-9]+ [\\-0-9]+\\.[0-9]+e[\\-\\+][0-9]+ [\\-0-9]+\\.[0-9]+e[\\-\\+][0-9]+",
            line,
        )
        if res is not None:
            mat.append(
                [
                    float(x)
                    for x in res.group().replace("\n", "").replace(";", "").split()
                ]
            )
    mat = np.array(mat)

    # get translation, rotation, scale/zoom, and shear matrices

    T, R, Z, S = tr.affines.decompose44(mat)

    # now need to decompose R into euler angles; note this implies 'sxyz'
    # (=static/extrinsic, 1:x, 2:y, 3:z rotation type and sequence)
    # https://matthew-brett.github.io/transforms3d/reference/transforms3d.euler.html

    rot_x, rot_y, rot_z = tr.euler.mat2euler(R)

    logging.info(
        "Found Talairach rotation angles: x = "
        + f"{rot_x:.3}"
        + ", y = "
        + f"{rot_y:.3}"
        + ", z = "
        + f"{rot_z:.3}"
        + " radians.",
    )

    return rot_x, rot_y, rot_z
