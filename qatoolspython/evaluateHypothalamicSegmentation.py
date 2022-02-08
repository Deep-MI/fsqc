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

    Required files:
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
    import nibabel as nb
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

            dat[:,0] = i # replace -1 with label id

            #
            centroids.append(np.mean(dat, axis=0))

        centroids = np.array(centroids)

        # already in TkReg RAS format

        ctr_tkr = centroids

    else:

        # fs7 version
        cmd = "mri_segcentroids --i " + os.path.join(SUBJECTS_DIR, SUBJECT, "mri", "hypothalamic_subunits_seg.v1.mgz") + " --o " + os.path.join(OUTPUT_DIR, "hypothalamus_centroids.txt")
        run_cmd(cmd, "Could not create hypothalamus centroids")

        #
        centroids = np.loadtxt(os.path.join(OUTPUT_DIR,"hypothalamus_centroids.txt"), skiprows=2)

        # convert from RAS to TkReg RAS
        seg = nb.load(os.path.join(SUBJECTS_DIR, SUBJECT, "mri", "hypothalamic_subunits_seg.v1.mgz"))

        ras2vox = seg.header.get_ras2vox()
        vox2ras_tkr = seg.header.get_vox2ras_tkr()

        ctr_tkr = np.concatenate((centroids[:,1:4], np.ones((centroids.shape[0],1))), axis=1)
        ctr_tkr = np.matmul(vox2ras_tkr, np.matmul(ras2vox, ctr_tkr.T)).T
        ctr_tkr = np.concatenate((np.array(centroids[:,0], ndmin=2).T, ctr_tkr[:,0:3]), axis=1)

    #

    ctr_tkr_x0 = ctr_tkr[3,1]
    ctr_tkr_x1 = ctr_tkr[8,1]
    ctr_tkr_y0 = (ctr_tkr[0,2]+ctr_tkr[5,2])/2
    ctr_tkr_y1 = (ctr_tkr[1,2]+ctr_tkr[6,2])/2
    ctr_tkr_y2 = (ctr_tkr[3,2]+ctr_tkr[8,2])/2
    ctr_tkr_y3 = (ctr_tkr[4,2]+ctr_tkr[9,2])/2
    ctr_tkr_y4 = (ctr_tkr[2,2]+ctr_tkr[7,2])/2
    ctr_tkr_z0 = (ctr_tkr[2,3]+ctr_tkr[7,3])/2
    ctr_tkr_z1 = (ctr_tkr[4,3]+ctr_tkr[9,3])/2

    # set ranges for cropping the image (assuming RAS coordinates)

    ctr_tkr_x0_xlim = [ctr_tkr[3,2]-20, ctr_tkr[3,2]+20]
    ctr_tkr_x1_xlim = [ctr_tkr[8,2]-20, ctr_tkr[8,2]+20]

    ctr_tkr_y0_xlim = [(ctr_tkr[0,1]+ctr_tkr[5,1])/2-20, (ctr_tkr[0,1]+ctr_tkr[5,1])/2+20]
    ctr_tkr_y1_xlim = [(ctr_tkr[1,1]+ctr_tkr[6,1])/2-20, (ctr_tkr[1,1]+ctr_tkr[6,1])/2+20]
    ctr_tkr_y2_xlim = [(ctr_tkr[3,1]+ctr_tkr[8,1])/2-20, (ctr_tkr[3,1]+ctr_tkr[8,1])/2+20]
    ctr_tkr_y3_xlim = [(ctr_tkr[4,1]+ctr_tkr[9,1])/2-20, (ctr_tkr[4,1]+ctr_tkr[9,1])/2+20]
    ctr_tkr_y4_xlim = [(ctr_tkr[2,1]+ctr_tkr[7,1])/2-20, (ctr_tkr[2,1]+ctr_tkr[7,1])/2+20]

    ctr_tkr_z0_xlim = [(ctr_tkr[2,1]+ctr_tkr[7,1])/2-20, (ctr_tkr[2,1]+ctr_tkr[7,1])/2+20]
    ctr_tkr_z1_xlim = [(ctr_tkr[4,1]+ctr_tkr[9,1])/2-20, (ctr_tkr[4,1]+ctr_tkr[9,1])/2+20]

    ctr_tkr_x0_ylim = [ctr_tkr[3,3]-20, ctr_tkr[3,3]+20]
    ctr_tkr_x1_ylim = [ctr_tkr[8,3]-20, ctr_tkr[8,3]+20]

    ctr_tkr_y0_ylim = [(ctr_tkr[0,3]+ctr_tkr[5,3])/2-20, (ctr_tkr[0,3]+ctr_tkr[5,3])/2+20]
    ctr_tkr_y1_ylim = [(ctr_tkr[1,3]+ctr_tkr[6,3])/2-20, (ctr_tkr[1,3]+ctr_tkr[6,3])/2+20]
    ctr_tkr_y2_ylim = [(ctr_tkr[3,3]+ctr_tkr[8,3])/2-20, (ctr_tkr[3,3]+ctr_tkr[8,3])/2+20]
    ctr_tkr_y3_ylim = [(ctr_tkr[4,3]+ctr_tkr[9,3])/2-20, (ctr_tkr[4,3]+ctr_tkr[9,3])/2+20]
    ctr_tkr_y4_ylim = [(ctr_tkr[2,3]+ctr_tkr[7,3])/2-20, (ctr_tkr[2,3]+ctr_tkr[7,3])/2+20]

    ctr_tkr_z0_ylim = [(ctr_tkr[2,2]+ctr_tkr[7,2])/2-20, (ctr_tkr[2,2]+ctr_tkr[7,2])/2+20]
    ctr_tkr_z1_ylim = [(ctr_tkr[4,2]+ctr_tkr[9,2])/2-20, (ctr_tkr[4,2]+ctr_tkr[9,2])/2+20]

    XLIM = [ctr_tkr_x0_xlim, ctr_tkr_x1_xlim, ctr_tkr_y0_xlim,
        ctr_tkr_y1_xlim, ctr_tkr_y2_xlim, ctr_tkr_y3_xlim,
        ctr_tkr_y4_xlim, ctr_tkr_z0_xlim,  ctr_tkr_z1_xlim]

    YLIM = [ctr_tkr_x0_ylim, ctr_tkr_x1_ylim, ctr_tkr_y0_ylim,
        ctr_tkr_y1_ylim, ctr_tkr_y2_ylim, ctr_tkr_y3_ylim,
        ctr_tkr_y4_ylim, ctr_tkr_z0_ylim,  ctr_tkr_z1_ylim]

    # --------------------------------------------------------------------------
    # create screenshot

    if CREATE_SCREENSHOT is True:
        createScreenshots(SUBJECT = SUBJECT, SUBJECTS_DIR = SUBJECTS_DIR, INTERACTIVE = False, VIEWS = [('x', ctr_tkr_x0), ('x', ctr_tkr_x1), ('y', ctr_tkr_y0), ('y', ctr_tkr_y1), ('y', ctr_tkr_y2), ('y', ctr_tkr_y3), ('y', ctr_tkr_y4), ('z', ctr_tkr_z0), ('z', ctr_tkr_z1)], LAYOUT = (1, 9), BASE = [os.path.join(SUBJECTS_DIR,SUBJECT,"mri","norm.mgz")], OVERLAY = [os.path.join(SUBJECTS_DIR,SUBJECT,"mri","hypothalamic_subunits_seg.v1.mgz")], SURF = None, OUTFILE = SCREENSHOTS_OUTFILE, XLIM = XLIM, YLIM = YLIM)
