# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 10:54:59 2019

@author: Tobias Wolff 

Wrapper function to conduct shape analysis. 

Required arguments:
    - subjects_dir
    - subject
    - output_dir
"""

def runBrainPrint(subjects_dir, subject, output_dir): 

    import os

    from fs_brainPrint import compute_shapeDNAs
    from fs_brainPrint import write_evs
    from fs_brainPrintPostproc import fs_brainPrintPostproc

    class options: 
        sid = subject 
        sdir = subjects_dir
        num = 50
        outdir = output_dir
        brainprint = os.path.join(output_dir,subject+"-brainprint.csv")
        keeptmp = False
        tsmooth = 3
        gsmooth = 0
        do3d = False
        skipcortex = False
        evec = False

    class optionsPostproc:
        file = options.brainprint
        list = None
        out = os.path.join(output_dir,subject+"-brainprintPostproc")
        vol = 1
        lin = True
        asy = "euc"
        outcov = None
        covfile = None
    
    (structures , evmat) = compute_shapeDNAs(options)

    # <todo> do we really need to write these? if not, would require to have an
    # additional input option for the postproc script. it might be possible to 
    # create a dictionary and pass it with optionsPostproc
    write_evs(options.brainprint,structures,evmat)

    brainprint = fs_brainPrintPostproc(optionsPostproc)

    return brainprint
