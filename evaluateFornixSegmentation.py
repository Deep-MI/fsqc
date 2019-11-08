def evaluateFornixSegmentation(SUBJECT,SUBJECTS_DIR,OUTPUT_DIR,CREATE_SCREENSHOT=True,RUN_SHAPEDNA=True):

    # imports

    import os
    import sys
    from createScreenshots import createScreenshots

    from builtins import str
    from builtins import range

    import warnings
    import sys
    import shlex
    import optparse
    import subprocess
    import tempfile
    import uuid
    import errno
    import glob

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
            if is_exe(os.path.join(os.getenv('SHAPEDNA_HOME'),program)):
                return os.path.join(os.getenv('SHAPEDNA_HOME'),program)
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

    # conduct transform for aseg and norm

    cmd = "mri_convert -i "+os.path.join(SUBJECTS_DIR,SUBJECT,"mri","aseg.mgz")+" -at "+os.path.join(SUBJECTS_DIR,SUBJECT,"mri","transforms","cc_up.xfm")+" -rt nearest -o "+os.path.join(OUTPUT_DIR,"asegCCup.mgz")

    run_cmd(cmd,"Could not conduct cc_up.xfm transform")

    cmd = "mri_convert -i "+os.path.join(SUBJECTS_DIR,SUBJECT,"mri","norm.mgz")+" -at "+os.path.join(SUBJECTS_DIR,SUBJECT,"mri","transforms","cc_up.xfm")+" -rt cubic -o "+os.path.join(OUTPUT_DIR,"normCCup.mgz")

    run_cmd(cmd,"Could not conduct cc_up.xfm transform")

    # create fornix mask and surface

    cmd = "mri_binarize --i "+os.path.join(OUTPUT_DIR,"asegCCup.mgz")+" --match 251 252 253 254 255 --dilate 2 --erode 2 --surf "+os.path.join(OUTPUT_DIR,"cc.surf")+" --surf-smooth 1 --o "+os.path.join(OUTPUT_DIR,"cc.mgz")

    run_cmd(cmd,"Could not create fornix mask and surface")

    # create screenshot

    if CREATE_SCREENSHOT is True:
        createScreenshots(SUBJECT = SUBJECT, SUBJECTS_DIR = SUBJECTS_DIR, 
            INTERACTIVE = False, VIEWS = [('x',0)],  
            BASE = [os.path.join(OUTPUT_DIR,"normCCup.mgz")], OVERLAY = None, SURF = [os.path.join(OUTPUT_DIR,"cc.surf")], OUTFILE = os.path.join(OUTPUT_DIR,"cc.png"))

    # run shapeDNA

    if RUN_SHAPEDNA is True:

        from exportEV import exportEV
        from fs_shapeDNA import laplaceTria, computeABtria

        import nibabel as nb

        surf = nb.freesurfer.io.read_geometry(os.path.join(OUTPUT_DIR,"cc.surf"), read_metadata=True)

        ev, evec = laplaceTria(surf[0],surf[1],k=30)

        d=dict()
        d['Refine']=0
        d['Degree']=1
        d['Dimension']=2
        d['Elements']=len(surf[1])
        d['DoF']=len(surf[0])
        d['NumEW']=30
        d['Eigenvalues']=ev
        d['Eigenvectors']=evec

        exportEV(d,os.path.join(OUTPUT_DIR,"cc.surf.ev"))


