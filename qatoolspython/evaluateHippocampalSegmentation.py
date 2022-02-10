"""
This module provides a function to evaluate potential missegmentation of the
hippocampus and amygdala

"""

# -----------------------------------------------------------------------------

def evaluateHippocampalSegmentation(SUBJECT, SUBJECTS_DIR, OUTPUT_DIR, CREATE_SCREENSHOT = True, SCREENSHOTS_OUTFILE = [], HEMI = "lh", LABEL = "T1.v21"):
    """
    A function to evaluate potential missegmentation of the hippocampus and
    amygdala.

    This script evaluates potential missegmentation of the hippocampus and
    amygdala as created by FreeSurfer 7.1's dedicated module:
    https://surfer.nmr.mgh.harvard.edu/fswiki/HippocampalSubfieldsAndNucleiOfAmygdala

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
        - HEMI (default: lh)
        - LABEL (default: T1.v21)

    Required files:
        - mri/[lr]h.hippoAmygLabels-<LABEL>.FSvoxelSpace.mgz
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

        print('ERROR: could not find '+os.path.join(SUBJECTS_DIR,SUBJECT,"mri","norm.mgz")+', not running hippocampus module.')

        raise ValueError("File not found")

    if not os.path.isfile(os.path.join(SUBJECTS_DIR,SUBJECT,"mri",HEMI+".hippoAmygLabels-"+LABEL+".FSvoxelSpace.mgz")):

        print('ERROR: could not find '+os.path.join(SUBJECTS_DIR,SUBJECT,"mri",HEMI+".hippoAmygLabels-"+LABEL+".FSvoxelSpace.mgz")+', not running hippocampus module.')

        raise ValueError("File not found")

    if not SCREENSHOTS_OUTFILE:
        SCREENSHOTS_OUTFILE = os.path.join(OUTPUT_DIR,"hippocampus.png")

    # create mask and surface

    cmd = "mri_binarize --i "+os.path.join(SUBJECTS_DIR,SUBJECT,"mri",HEMI+".hippoAmygLabels-"+LABEL+".FSvoxelSpace.mgz")+" --min 1 --surf "+os.path.join(OUTPUT_DIR,"hippocampus-"+HEMI+".surf")+" --surf-smooth 1 --o "+os.path.join(OUTPUT_DIR,"hippocampus-"+HEMI+".mgz")
    run_cmd(cmd,"Could not create hippocampus mask and surface")

    # get centroids

    if which("mri_segcentroids") is None:

        # fs6 version
        centroids = list()

        for i in [237, 238]:

            #
            cmd = "mri_vol2label --i " + os.path.join(SUBJECTS_DIR,SUBJECT, "mri", HEMI+".hippoAmygLabels-"+LABEL+".FSvoxelSpace.mgz") + " --id " + str(i) + " --l " + os.path.join(OUTPUT_DIR, "hippocampus_labels_" + str(i) + "-"+HEMI+".txt")
            run_cmd(cmd, "Could not create hippocampus centroids")

            #
            dat = np.loadtxt(os.path.join(OUTPUT_DIR, "hippocampus_labels_" + str(i) + "-"+HEMI+".txt.label"), skiprows=2)

            dat[:,0] = i # replace -1 with label id

            #
            centroids.append(np.mean(dat, axis=0))

        centroids = np.array(centroids)

        # already in TkReg RAS format

        ctr_tkr = centroids

    else:

        # fs7 version
        cmd = "mri_segcentroids --i " + os.path.join(SUBJECTS_DIR, SUBJECT, "mri", HEMI+".hippoAmygLabels-"+LABEL+".FSvoxelSpace.mgz") + " --o " + os.path.join(OUTPUT_DIR, "hippocampus_centroids-"+HEMI+".txt")
        run_cmd(cmd, "Could not create hippocampus centroids")

        #
        centroids = np.loadtxt(os.path.join(OUTPUT_DIR,"hippocampus_centroids-"+HEMI+".txt"), skiprows=2)

        # convert from RAS to TkReg RAS
        seg = nb.load(os.path.join(SUBJECTS_DIR, SUBJECT, "mri", HEMI+".hippoAmygLabels-"+LABEL+".FSvoxelSpace.mgz"))

        ras2vox = seg.header.get_ras2vox()
        vox2ras_tkr = seg.header.get_vox2ras_tkr()

        ctr_tkr = np.concatenate((centroids[:,1:4], np.ones((centroids.shape[0],1))), axis=1)
        ctr_tkr = np.matmul(vox2ras_tkr, np.matmul(ras2vox, ctr_tkr.T)).T
        ctr_tkr = np.concatenate((np.array(centroids[:,0], ndmin=2).T, ctr_tkr[:,0:3]), axis=1)

    # [7004, 237, 238]

    ctr_tkr_x0 = ctr_tkr[np.argwhere(ctr_tkr[:,0]==237),1]
    ctr_tkr_y0 = ctr_tkr[np.argwhere(ctr_tkr[:,0]==237),2]
    ctr_tkr_z0 = ctr_tkr[np.argwhere(ctr_tkr[:,0]==237),3]

    # set ranges for cropping the image (assuming RAS coordinates)

    ctr_tkr_x0_xlim = [ctr_tkr_y0-40, ctr_tkr_y0+40]
    ctr_tkr_y0_xlim = [ctr_tkr_x0-20, ctr_tkr_x0+20]
    ctr_tkr_z0_xlim = [ctr_tkr_x0-20, ctr_tkr_x0+20]

    ctr_tkr_x0_ylim = [ctr_tkr_z0-40, ctr_tkr_z0+40]
    ctr_tkr_y0_ylim = [ctr_tkr_z0-40, ctr_tkr_z0+40]
    ctr_tkr_z0_ylim = [ctr_tkr_y0-40, ctr_tkr_y0+40]

    XLIM = [ctr_tkr_x0_xlim, ctr_tkr_y0_xlim, ctr_tkr_z0_xlim]
    YLIM = [ctr_tkr_x0_ylim, ctr_tkr_y0_ylim, ctr_tkr_z0_ylim]

    # --------------------------------------------------------------------------
    # create screenshots

    if CREATE_SCREENSHOT is True:
        createScreenshots(SUBJECT = SUBJECT, SUBJECTS_DIR = SUBJECTS_DIR, INTERACTIVE = False, VIEWS = [('x', ctr_tkr_x0), ('y', ctr_tkr_y0), ('z', ctr_tkr_z0)], LAYOUT = (1, 3), BASE = [os.path.join(SUBJECTS_DIR,SUBJECT,"mri","norm.mgz")], OVERLAY = [os.path.join(SUBJECTS_DIR,SUBJECT,"mri",HEMI+".hippoAmygLabels-"+LABEL+".FSvoxelSpace.mgz")], SURF = None, OUTFILE = SCREENSHOTS_OUTFILE, XLIM = XLIM, YLIM = YLIM)
