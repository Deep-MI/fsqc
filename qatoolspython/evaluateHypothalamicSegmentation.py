"""
This module provides a function to evaluate potential missegmentation of the hypothalamus

"""

# -----------------------------------------------------------------------------

def evaluateHypothalamicSegmentation(SUBJECT, SUBJECTS_DIR, OUTPUT_DIR, CREATE_SCREENSHOT = True, SCREENSHOTS_OUTFILE = []):
    """
    A function to evaluate potential missegmentation of the hypothalamus.

    This script evaluates potential missegmentation of the hypothalamus as
    created by FreeSurfer 7.2's module for hypothalamic segmentation:
    https://surfer.nmr.mgh.harvard.edu/fswiki/HypothalamicSubunits.

    If the corresponding arguments are set to 'True', the script will also
    create screenshots. Resulting files will be saved to the same directory
    as indicated above.

    Required arguments:
        - SUBJECT
        - SUBJECTS_DIR
        - OUTPUT_DIR

    Optional arguments:
        - CREATE_SCREENSHOT <bool> (default: True)
        - SCREENSHOTS_OUTFILE <string> or empty list (default: [])

    Requires (if not found, returns NaNs):
        - mri/hypothalamic_subunits_seg.v1.mgz
        - mri/norm.mgz

    """

    # --------------------------------------------------------------------------
    # imports

    import os
    import sys
    import shlex
    import subprocess
    import numpy as np
    from qatoolspython.createScreenshots import createScreenshots

    # --------------------------------------------------------------------------
    # auxiliary functions

    def split_callback(option, opt, value, parser):
      setattr(parser.values, option.dest, value.split(','))

    def which(program):
        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file
            if is_exe(os.path.join('.',program)):
                return os.path.join('.',program)

        return None

    def my_print(message):
        """
        print message, then flush stdout
        """
        print(message)
        sys.stdout.flush()

    def run_cmd(cmd,err_msg):
        """
        execute the comand
        """
        clist = cmd.split()
        progname=which(clist[0])
        if (progname) is None:
            my_print('ERROR: '+ clist[0] +' not found in path!')
            sys.exit(1)
        clist[0]=progname
        cmd = ' '.join(clist)
        my_print('#@# Command: ' + cmd+'\n')

        args = shlex.split(cmd)
        try:
            subprocess.check_call(args)
        except subprocess.CalledProcessError as e:
            my_print('ERROR: '+err_msg)
            #sys.exit(1)
            raise
        my_print('\n')

    # --------------------------------------------------------------------------
    # main part

    # check files

    if not os.path.isfile(os.path.join(SUBJECTS_DIR,SUBJECT,"mri","norm.mgz")):

        print('ERROR: could not find '+os.path.join(SUBJECTS_DIR,SUBJECT,"mri","norm.mgz")+', not running hypothalamus module.')

        return

    if not os.path.isfile(os.path.join(SUBJECTS_DIR,SUBJECT,"mri","hypothalamic_subunits_seg.v1.mgz")):

        print('ERROR: could not find '+os.path.join(SUBJECTS_DIR,SUBJECT,"mri","hypothalamic_subunits_seg.v1.mgz")+', not running hypothalamus module.')

        return

    if not SCREENSHOTS_OUTFILE:
        SCREENSHOTS_OUTFILE = os.path.join(OUTPUT_DIR,"hypothalamus.png")

    # create mask and surface

    cmd = "mri_binarize --i "+os.path.join(SUBJECTS_DIR,SUBJECT,"mri","hypothalamic_subunits_seg.v1.mgz")+" --match 801 802 803 804 805 806 807 808 809 810 --surf "+os.path.join(OUTPUT_DIR,"hypothalamus.surf")+" --surf-smooth 1 --o "+os.path.join(OUTPUT_DIR,"hypothalamus.mgz")
    run_cmd(cmd,"Could not create hypothalamus mask and surface")

    # get centroids
    if which("mri_segcentroids") is None:

        # fs6 version
        centroids = list()

        for i in range(801, 811):

            #
            cmd = "mri_vol2label --i " + os.path.join(SUBJECTS_DIR,SUBJECT, "mri", "hypothalamic_subunits_seg.v1.mgz") + " --id " + str(i) + " --l " + os.path.join(OUTPUT_DIR, "hypothalamus_labels_" + str(i) + ".txt")
            run_cmd(cmd, "Could not create hypothalamus centroids")

            #
            dat = np.loadtxt(os.path.join(OUTPUT_DIR, "hypothalamus_labels_" + str(i) + ".txt.label"), skiprows=2)

            #
            centroids.append(np.mean(dat, axis=0))

        centroids = np.array(centroids)

    else:

        # fs7 version
        cmd = "mri_segcentroids --i " + os.path.join(SUBJECTS_DIR, SUBJECT, "mri", "hypothalamic_subunits_seg.v1.mgz") + " --o " + os.path.join(OUTPUT_DIR, "hypothalamus_centroids.txt")
        run_cmd(cmd, "Could not create hypothalamus centroids")

        #
        centroids = np.loadtxt(os.path.join(OUTPUT_DIR,"hypothalamus_centroids.txt"), skiprows=2)

    centroids_x0 = centroids[3,1]
    centroids_x1 = centroids[8,1]
    centroids_y0 = (centroids[0,2]+centroids[5,2])/2
    centroids_y1 = (centroids[1,2]+centroids[6,2])/2
    centroids_y2 = (centroids[3,2]+centroids[8,2])/2
    centroids_y3 = (centroids[4,2]+centroids[9,2])/2
    centroids_y4 = (centroids[2,2]+centroids[7,2])/2
    centroids_z0 = (centroids[2,3]+centroids[7,3])/2
    centroids_z1 = (centroids[4,3]+centroids[9,3])/2

    # --------------------------------------------------------------------------
    # create screenshot

    if CREATE_SCREENSHOT is True:
        createScreenshots(SUBJECT = SUBJECT, SUBJECTS_DIR = SUBJECTS_DIR, INTERACTIVE = False, VIEWS = [('x', centroids_x0), ('x', centroids_x1), ('y', centroids_y0), ('y', centroids_y1), ('y', centroids_y2), ('y', centroids_y3), ('y', centroids_y4), ('z', centroids_z0), ('z', centroids_z1)], LAYOUT = (1, 9), BASE = [os.path.join(SUBJECTS_DIR,SUBJECT,"mri","norm.mgz")], OVERLAY = [os.path.join(SUBJECTS_DIR,SUBJECT,"mri","hypothalamic_subunits_seg.v1.mgz")], SURF = None, OUTFILE = SCREENSHOTS_OUTFILE)
