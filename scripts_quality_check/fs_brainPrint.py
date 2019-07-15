#!/usr/bin/env python
# -*- coding: latin-1 -*-

#
# fs_shapeDNA
#
# script to compute ShapeDNA of FreeSurfer structures
#
# Original Author: Martin Reuter
# Date: Dec-16-2014
#

from __future__ import print_function
from builtins import zip
from builtins import str
from builtins import object

import warnings
import os
import sys
import shlex
import optparse
import subprocess
import fs_shapeDNA

warnings.filterwarnings('ignore', '.*negative int.*')

def my_print(message):
    """
    print message, then flush stdout
    """
    print(message) 
    sys.stdout.flush()

HELPTEXT = """

fs_brainprint.py V2.0
Author: Martin Reuter, 2015

SUMMARY

Computes the BrainPrint for a FreeSurfer subject.

The BrainPrint consists of the shape descriptors (Shape-DNA) [1]
of a selection of both cortical and subcortical structures [2].

Here is a list of structures and FreeSurfer aseg label ids:

CorpusCallosum                  [251, 252, 253, 254, 255]
Cerebellum                      [7, 8, 16, 46, 47]
Ventricles                      [4, 5, 14, 24, 31, 43, 44, 63]
3rd-Ventricle                   [14, 24]
4th-Ventricle                   15
Brain-Stem                      16
Left-Striatum                   [11, 12, 26]
Left-Lateral-Ventricle          [4, 5, 31]
Left-Cerebellum-White-Matter    7
Left-Cerebellum-Cortex          8
Left-Thalamus-Proper            10
Left-Caudate                    11
Left-Putamen                    12
Left-Pallidum                   13
Left-Hippocampus                17
Left-Amygdala                   18
Left-Accumbens-area             26
Left-VentralDC                  28
Right-Striatum                  [50, 51, 58]
Right-Lateral-Ventricle         [43, 44, 63]
Right-Cerebellum-White-Matter   46
Right-Cerebellum-Cortex         47
Right-Thalamus-Proper           49
Right-Caudate                   50
Right-Putamen                   51
Right-Pallidum                  52
Right-Hippocampus               53
Right-Amygdala                  54
Right-Accumbens-area            58
Right-VentralDC                 60

And the following cortical structures:

lh-white-2d    (left white matter surface triangles)
lh-pial-2d     (left pial surface triangles)
rh-white-2d    (same for right hemisphere ...)
rh-pial-2d

lh-white-3d    (left white matter volume tetrahedra)
lh-pial-3d     (left pial+white volume tetrahedra)
rh-pial-3d
rh-white-3d

Processing of the cortical structures can be skipped (--skipcortex).
The 3d (tetrahedra) descriptors are only computed if --do3d
is passed and the necessary software (meshfix, gmsh and
shapeDNA-tetra) are available in the $SHAPEDNA_HOME path.
For regular processing the file shapeDNA-tria and the key.txt
file need to exist and the  environment variable $SHAPEDNA_HOME
needs to point to that directory. The key file and shapeDNA-tria
can be obtained from http://reuter.mit.edu/software/shapedna/
Regular (2d) processing takes approx. 5 mins per subject, adding
3d processing (--do3d) adds 30 mins.

Implicit Inputs:
The mri/aseg.mgz and mri/norm.mgz should be available.
Also surf/?h.pial and surf/?h.white need to be
available unless --skipcortex is passed. norm.mgz is not 
absolutely necessary but highly recommended to fix the labels
and obtain improved meshes. 

Output:
The brainprint CSV table containing column headers for the 
structures, a row of areas, a row of volumes and N rows of 
the first N eigenvalues for each structure.


If used for a publication, please cite both [1] for the shape
descriptor method and [2] for the application to brain MRI and
definiton of the BrainPrint.


REFERENCES
==========

[1] M. Reuter, F.-E. Wolter and N. Peinecke.
Laplace-Beltrami spectra as "Shape-DNA" of surfaces and solids.
Computer-Aided Design 38 (4), pp.342-366, 2006.
http://dx.doi.org/10.1016/j.cad.2005.10.011

[2] C. Wachinger, P. Golland, W. Kremen, B. Fischl, M. Reuter.
BrainPrint: A discriminative characterization of brain morphology.
NeuroImage Volume 109, pp.232-248, 2015.
http://dx.doi.org/10.1016/j.neuroimage.2015.01.032

"""

def options_parse():
    """
    Command Line Options Parser:
    initiate the option parser and return the parsed object
    """
    parser = optparse.OptionParser(version='$Id: fs_brainPrint,v 1.21 2013/05/17 15:14:08 mreuter Exp $', usage=HELPTEXT)
    
    # help text
    h_sid        = '(REQUIRED) subject ID (FS processed directory inside the subjects directory)'
    h_sdir       = 'FS subjects directory (or set environment $SUBJECTS_DIR)'
    h_num        = 'Number of eigenvalues/vectors to compute (default: 50)'
    h_outdir     = 'Output directory (default: <sdir>/<sid>/brainprint/ )'
    h_brainprint = 'Output BrainPrint file (default: <outdir>/<sid>.brainprint_<num>.csv )'
    h_keeptmp    = 'Keep intermediate surface, tet-mesh and ev files (default:off)'
    h_gsmooth    = 'Geometry smoothing iterations (for surfaces) (default: 0)'
    h_tsmooth    = 'Tangential smoothing iterations (for surface mesh improvement) (default: 3)'
    h_do3d       = 'Do 3D tet-meshing and computation (default: off)'
    h_skipcortex = 'Skip cortical surfaces (in 2D and 3D) (default: off)'
    h_evec       = 'Switch on eigenvector computation.  This option turns on --keeptmp and cannot be used with --do3d (default: off)'
    
    parser.add_option('--sid',        dest='sid',        help=h_sid)
    parser.add_option('--sdir',       dest='sdir',       help=h_sdir)
    parser.add_option('--num' ,       dest='num',        help=h_num,        default=50, type='int')
    parser.add_option('--outdir',     dest='outdir',     help=h_outdir)
    parser.add_option('--brainprint', dest='brainprint', help=h_brainprint)
    parser.add_option('--keeptmp',    dest='keeptmp',    help=h_keeptmp,    default=False, action='store_true')
    parser.add_option('--tsmooth',    dest='tsmooth',    help=h_tsmooth,    default=3, type='int')   
    parser.add_option('--gsmooth',    dest='gsmooth',    help=h_gsmooth,    default=0, type='int')   
    parser.add_option('--do3d',       dest='do3d',       help=h_do3d,       default=False, action='store_true')
    parser.add_option('--skipcortex', dest='skipcortex', help=h_skipcortex, default=False, action='store_true')
    parser.add_option('--evec',       dest='evec',       help=h_evec,       default=False, action='store_true')

    (options, args) = parser.parse_args()

    # WITHOUT FREESURFER DO NOTHING
    fshome = os.getenv('FREESURFER_HOME')
    if fshome is None:
        parser.print_help()
        my_print('\nERROR: Environment variable FREESURFER_HOME not set.')
        my_print('        You need to source FreeSurfer 5.3 or newer.\n')
        sys.exit(1)

    sdnahome = os.getenv('SHAPEDNA_HOME')
    if sdnahome is None:
        parser.print_help()
        my_print('\nERROR: Environment variable SHAPEDNA_HOME not set.')
        my_print('       Set that variable to point to the directory containing')
        my_print('       shapeDNA-tria, e.g.')
        my_print('       setenv SHAPEDNA_HOME /user/me/shapedna/ (cshell)')
        my_print('       export SHAPEDNA_HOME=/user/me/shapedna/ (bash)\n')
        sys.exit(1)

    sdna = os.path.join(sdnahome,"shapeDNA-tria")
    if not os.path.exists(sdna):
        parser.print_help()
        my_print('\nERROR: Cannot find shapeDNA-tria in $SHAPEDNA_HOME\n')
        my_print('       Set that variable to point to the directory containing')
        my_print('       shapeDNA-tria, e.g.')
        my_print('       setenv SHAPEDNA_HOME /user/me/shapedna/ (cshell)')
        my_print('       export SHAPEDNA_HOME=/user/me/shapedna/ (bash)\n')
        sys.exit(1)
        
    if options.sdir is None:
        options.sdir = os.getenv('SUBJECTS_DIR')

    if options.sdir is None:
        parser.print_help()
        my_print('\nERROR: specify subjects directory via --sdir or $SUBJECTS_DIR\n')
        sys.exit(1)
        
    if options.sid is None:
        parser.print_help()
        my_print('\nERROR: Specify --sid\n')
        sys.exit(1)
            
    subjdir = os.path.join(options.sdir,options.sid)
    if not os.path.exists(subjdir):
        parser.print_help()
        my_print('\nERROR: cannot find sid in subjects directory\n')
        sys.exit(1)
    
    if options.outdir is None:
        options.outdir = os.path.join(subjdir,'brainprint')
    try:
        os.mkdir(options.outdir)
    except OSError as e:
        if e.errno != os.errno.EEXIST:
            raise e
        pass
        
    if options.brainprint is None:
        options.brainprint = os.path.join(options.outdir,options.sid+'.brainprint_'+str(options.num)+'.csv')

    if options.do3d:
        required_executables = ['shapeDNA-tetra', 'meshfix', 'gmsh']
        for program in required_executables:
            if fs_shapeDNA.which(program) is None:
                my_print('\nERROR: Cannot find ' + program + ' in $SHAPEDNA_HOME')
                my_print(  '       Make sure that this binary is in $SHAPEDNA_HOME:')
                my_print(  '       ' + sdnahome)
                my_print(  '       or re-run without the --do3d flag!\n')
                sys.exit(1)
        if options.skipcortex:
            my_print('\nERROR: cannot combine --do3d and --skipcortex\n')
            sys.exit(1)

    if options.evec:
        if options.do3d:
            my_print('\nERROR: Cannot use the --evec option with --do3d')
            my_print(  '       Re-run without --do3d to turn on eigenvector computations,')
            my_print(  '       or without --evec to do 3D tet-meshing computations.')
            sys.exit(1)
        options.keeptmp = True
    
    return options



def run_cmd(cmd,err_msg):
    """
    execute the comand
    """
    my_print('#@# Command: ' + cmd+'\n')
    args = shlex.split(cmd)
    retcode = subprocess.call(args)
    if retcode != 0 :
        my_print('ERROR: '+err_msg)
        sys.exit(1)
    my_print('\n')


def get_evals(evfile):
    """
    returns string list of area, volume and evals
    """
    if not os.path.isfile(evfile) :
        return []
    area = ''
    volume = ''
    evals = []
    with open(evfile, 'r') as inF:
        for line in inF:
            if 'Area:' in line:
                strlst = line.split()
                area = strlst[1]
            if 'Volume:' in line:
                strlst = line.split()
                volume = strlst[1]
            if 'Eigenvalues:' in line:
                evline = next(inF)
                evstr = ''
                while (evline is not None) and (not '}' in evline):
                    evstr = evstr+evline
                    evline = next(inF)
                evstr = evstr+evline
                #evstr = evstr.translate(None,'{} \n')
                evstr = evstr.replace("{","").replace("}","").replace(" ","").replace("\n","")
                evals = evstr.split(';')
                if abs(float(evals[0])) < 10e-16 :
                    evals[0] = "0"
                evals.insert(0,volume)
                evals.insert(0,area)
                return evals
    return []


def compute_shapeDNAs(options):

    # combined and individual aseg labels
    # combined:
    # Left  Striatum: left  Caudate+Putamen+Accumbens
    # Right Striatum: right Caudate+Putamen+Accumbens
    # CorpusCallosum: (5 sub regions combinded)
    # Cerebellum: brainstem+ (left+right) cerebellum WM and GM
    # Ventricles: (left+right) lat.vent+inf.lat.vent+choroidplexus +3rdVent+CSF
    # Lateral-Ventricle: lat.vent+inf.lat.vent+choroidplexus
    # 3rd-Ventricle: 3rd-Ventricle + CSF
    
    
    ## Original BrainPrint definition, but not everything of this was used in Wachinger, 2015
    ## some structures such as choroid-plexus were excluded in analysis scripts
    ## names for table output:
    #structures = ['Left-Striatum','Right-Striatum','CorpusCallosum','Cerebellum','Ventricles',
    #              'Left-Lateral-Ventricle','Left-Inf-Lat-Vent','Left-Cerebellum-White-Matter',
    #              'Left-Cerebellum-Cortex','Left-Thalamus-Proper','Left-Caudate','Left-Putamen',
    #              'Left-Pallidum','3rd-Ventricle','4th-Ventricle','Brain-Stem','Left-Hippocampus',
    #              'Left-Amygdala','CSF','Left-Accumbens-area','Left-VentralDC','Left-choroid-plexus',
    #              'Right-Lateral-Ventricle','Right-Inf-Lat-Vent','Right-Cerebellum-White-Matter',
    #              'Right-Cerebellum-Cortex','Right-Thalamus-Proper','Right-Caudate','Right-Putamen',
    #              'Right-Pallidum','Right-Hippocampus','Right-Amygdala','Right-Accumbens-area',
    #              'Right-VentralDC','Right-choroid-plexus',
    #              'lh-white-2d','lh-white-3d','lh-pial-2d','lh-pial-3d',
    #              'rh-white-2d','rh-white-3d','rh-pial-2d','rh-pial-3d']
    ## label ids for aseg structures
    #labels = [[11, 12, 26], [50, 51, 58], [251, 252, 253, 254, 255], [7, 8, 16, 46, 47], [4, 5, 14, 24, 31, 43, 44, 63], 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 24, 26, 28, 31, 43, 44, 46, 47, 49, 50, 51, 52, 53, 54, 58, 60, 63]

    # new definition for better ventricle treatment
    # (i)  choroid plexus is partially in Lat.Vent and Inf.Lat.Vent, so we merge those three (call em Lateral-Ventricle)
    # (ii) merge 3rd Ventricle and CSF (separation not clear), call 3rd-Ventricle
    # now we therefore drop Inf.Lat.Vent,ChoroidPlexus,CSF
    # maybe exclude brainstem and ventralDC ?
    # names for table output:
    structures = ['CorpusCallosum','Cerebellum','Ventricles',
                     '3rd-Ventricle','4th-Ventricle','Brain-Stem',
                     'Left-Striatum','Left-Lateral-Ventricle',
                     'Left-Cerebellum-White-Matter','Left-Cerebellum-Cortex',
                     'Left-Thalamus-Proper','Left-Caudate','Left-Putamen',
                     'Left-Pallidum','Left-Hippocampus','Left-Amygdala',
                     'Left-Accumbens-area','Left-VentralDC',
                     'Right-Striatum','Right-Lateral-Ventricle',
                     'Right-Cerebellum-White-Matter','Right-Cerebellum-Cortex',
                     'Right-Thalamus-Proper','Right-Caudate','Right-Putamen',
                     'Right-Pallidum','Right-Hippocampus','Right-Amygdala',
                     'Right-Accumbens-area','Right-VentralDC']
    cortex_2d = ['lh-white-2d', 'lh-pial-2d','rh-white-2d','rh-pial-2d']
    cortex_3d = ['lh-white-3d', 'lh-pial-3d','rh-white-3d','rh-pial-3d']
   
    if not options.skipcortex:
        structures = structures + cortex_2d   
        if options.do3d:
            structures = structures + cortex_3d

    # label ids for aseg structures
    labels = [[251, 252, 253, 254, 255], [7, 8, 16, 46, 47], [4, 5, 14, 24, 31, 43, 44, 63],
              [14, 24], 15, 16,
              [11, 12, 26], [4, 5, 31],
               7, 8,
               10, 11, 12,
               13, 17, 18,
               26, 28,
              [50, 51, 58],[43, 44, 63],
               46, 47,
               49, 50, 51,
               52, 53, 54,
               58, 60]
    


    class sdnaopt(object):
        num      = options.num
        degree   = 1
        refmin   = 3000
        ignorelq = True
        bcond    = 1 #Neumann (for tet mesh)
        tsmooth  = options.tsmooth
        gsmooth  = options.gsmooth
        evec     = options.evec
        param2d  = None
 
    evmat = []
 
    for lab in labels:
        if type(lab) == list:
            astring  = '_'.join(str(x) for x in lab)
        else:
            astring = str(lab)
        
        my_print("\n\n===========================================================")
        my_print("Aseg label id str "+astring+"\n")
        
        surfnamei = 'aseg.init.'+astring+'.vtk'
        asegsurfi  = os.path.join(options.outdir,surfnamei)
        surfnameo = 'aseg.final.'+astring+'.vtk'
        asegsurfo  = os.path.join(options.outdir,surfnameo)
        outev    = asegsurfo+'.ev'
        failed = False
        evs = []
        try:
            fs_shapeDNA.get_aseg_surf(options.sdir,options.sid,astring.split('_'),asegsurfi)
            fs_shapeDNA.run_shapeDNAtria(asegsurfi,outev,asegsurfo,sdnaopt)
            evs = get_evals(outev)
        except subprocess.CalledProcessError as e:
            my_print('Error occured, skipping label '+astring)
            failed = True
            
        if not evs or failed:
            evs = ['NaN'] * (sdnaopt.num+2)
        evmat.append(evs)
        if not options.keeptmp and not failed:
            cmd ='rm '+asegsurfi
            run_cmd(cmd,'rm temp asegsurfi failed?')
            cmd ='rm '+asegsurfo
            run_cmd(cmd,'rm temp asegsurfo failed?')
            cmd ='rm '+outev
            run_cmd(cmd,'rm temp outev failed?')
       
        
        #lstring  = ','.join(lab)
        #cmd = 'fs_shapeDNA.py --sid '+options.sid+' --sdir '+options.sdir+' --asegid '+lstring+' --num '+options.num
        #if options.outdir is not None:
        #    cmd = cmd+' --outdir '+options.outdir
        #run_cmd(cmd,'fs_shapeDNA.py '+lstring+' failed?')


    # if skip cortex, return here
    if options.skipcortex:
        return(structures, evmat)
    
    # 2D Surfaces:
    for hem in ['lh','rh']:
        for typeSurf in ['white', 'pial']:
            surfname = hem+'.'+typeSurf
            my_print("\n\n===========================================================")
            my_print("2D Cortical Surface "+surfname+"\n")
            insurf   = os.path.join(options.sdir,options.sid,'surf',surfname)
            outsurf  = os.path.join(options.outdir,surfname+'.final.vtk')
            outev2d  = os.path.join(options.outdir,surfname+'.ev')
            failed = False

            try:
                fs_shapeDNA.run_shapeDNAtria(insurf,outev2d,outsurf,sdnaopt)
                evs = get_evals(outev2d)
            except subprocess.CalledProcessError as e:
                my_print('Error occured, skipping 2D surface '+surfname)
                failed = True

            if not evs or failed:
                evs = ['NaN'] * (sdnaopt.num+2)
            evmat.append(evs)
            if not options.keeptmp and not failed:
                cmd ='rm '+outev2d
                run_cmd(cmd,'rm temp outev2d failed?')
                cmd ='rm '+outsurf
                run_cmd(cmd,'rm temp outsurf failed?')

    # Surfaces: 3D tet
    if options.do3d:
        for hem in ['lh','rh']:
            for typeSurf in ['white', 'pial']:
                surfname = hem+'.'+typeSurf
                my_print("\n\n===========================================================")
                my_print("3D Cortical Structure "+surfname+"\n")
                insurf   = os.path.join(options.sdir,options.sid,'surf',surfname)
                outsurf  = os.path.join(options.outdir,surfname+'.final.vtk')
                outev3d  = os.path.join(options.outdir,surfname+'.msh.ev')
                outtet   = os.path.join(options.outdir,surfname+'.msh')

                # try with 3 mesh fix iterations:    
                failed = False
                try:
                    fixiter = 3
                    fs_shapeDNA.get_tetmesh(insurf,outtet,fixiter)
                    fs_shapeDNA.run_shapeDNAtetra(outtet,outev3d,sdnaopt)
                    evs = get_evals(outev3d)
                except subprocess.CalledProcessError as e:
                    my_print('Error occured, skipping 3D surface '+surfname)
                    failed = True

                # if failed, try with 4 mesh fix iterations:    
                if not evs or failed:
                    failed = False
                    try:
                        fixiter = 4
                        fs_shapeDNA.get_tetmesh(insurf,outtet,fixiter)
                        fs_shapeDNA.run_shapeDNAtetra(outtet,outev3d,sdnaopt)
                        evs = get_evals(outev3d)
                    except subprocess.CalledProcessError as e:
                        my_print('Error occured, skipping 3D surface '+surfname)
                        failed = True

                if not evs or failed:
                    evs = ['NaN'] * (sdnaopt.num+2)
                evmat.append(evs)
                if not options.keeptmp and not failed:
                    cmd ='rm '+outev3d
                    run_cmd(cmd,'rm temp outev3d failed?')
                    cmd ='rm '+outtet
                    run_cmd(cmd,'rm temp outtet failed?')
                
        #cmd = 'fs_shapeDNA.py --sid '+options.sid+' --sdir '+options.sdir+' --surf '+surfname+' --num '+options.num
        #if options.outdir is not None:
        #    cmd = cmd+' --outdir '+options.outdir
        #run_cmd(cmd,'fs_shapeDNA.py --surf '+sstring+' failed?')
        #sstring=hem+'.'+typeSurf
        #cmd = 'fs_shapeDNA.py --sid '+options.sid+' --sdir '+options.sdir+' --surf '+surfname+' --num '+options.num+' --dotet'
        #if options.outdir is not None:
        #    cmd = cmd+' --outdir '+options.outdir
        #run_cmd(cmd,'fs_shapeDNA.py --dotet --surf '+sstring+' failed?')

    return (structures, evmat)



def write_evs(outfile,structures,evmat):
    # write final csv
    text_file = open(outfile, "w")
    text_file.write((','.join(structures))+'\n')
    evstrans= list(zip(*evmat))
    for item in evstrans:
        text_file.write("%s\n" % ','.join(item))
    text_file.close()
    

if __name__=="__main__":
    # Command Line options and error checking done here
    options = options_parse()

    (structures , evmat) = compute_shapeDNAs(options)
    write_evs(options.brainprint,structures,evmat)

    # always exit with 0 exit code
    sys.exit(0)
