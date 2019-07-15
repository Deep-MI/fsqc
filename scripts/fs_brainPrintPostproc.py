#!/usr/bin/env python
# -*- coding: latin-1 -*-

# fs_brainPrintPostProc
#
# This is a script for the post-processing of fs_brainPrint results
#
# This includes:
#
# - volume normalization
# - linear reweighting
# - lateral shape asymmtry mesasures
#
# Original Author:  Kersten Diers, Martin Reuter
# Date:             Oct-06-2017
# Version:          0.9

# -----------------------------------------------------------------------------
# IMPORTS

from __future__ import division
from __future__ import print_function
from builtins import str
from builtins import range
from past.utils import old_div
from io import open
import warnings
import sys
import os
import re
import csv
import errno
import tempfile
import optparse
import numpy as np
import distutils.version as du
import scipy.spatial.distance as di

# note: use 'import pdb; pdb.set_trace()' for debugging

# -----------------------------------------------------------------------------
# SETTINGS

os.environ['OMP_NUM_THREADS'] = '1' # setenv OMP_NUM_THREADS 1
if sys.version_info[0] < 3: 
    WRITECSVSPECIFIER='wb'
else:
    WRITECSVSPECIFIER='w'
                                   
# -----------------------------------------------------------------------------
# DEFINE HELPTEXT

HELPTEXT = """
SUMMARY

Postprocessing of brainPrint results. This includes (any subset of) a) surface 
and / or volume normalization of eigenvalues, b) linear reweighting of the 
eigenvalues, and c) the computation of lateral shape asymmetries. For a
description of these methods, see [3]. 

Briefly, surface / volume normalization multiplies the eigenvalues by the 
corresponding volume or surface area, taken to the power of (2/d), where d is 
'2' for surfaces, and '3' for volumes (see 'NORMALIZATION' for details).

Linear reweighting is a scaling of each eigenvalue by its index, i.e. 
EV1reweighted = EV1/1, EV2reweighted = EV2 / 2, ... EVnreweighted = EVn / n.

Lateral asymmetry consists of the computation of Euclidean, Mahalanobis, or MCD 
distances between bilateral (left-right) structures.

Data need to be processed with the fs_brainPrint.py script prior to applying
the current script. The current script has been developed and tested for the
fs_brainPrint.py script version 1.21 and Python 2.7. The 'sklearn' package is
required for the computation of MCD distances.


INPUTS

Required inputs are either:

--file=<file> : a csv file that was produced by the fs_brainPrint.py script.
                This option will run the script in single-subject mode.

or

--list=<file> : a text file containing a list of files that were produced by
                the fs_brainPrint.py script. This will run the script in group
                mode.

but not both. According to the chosen option, the script will run in either
single-subject mode or in group mode.

- Single-subject mode means that the analysis can be run with a single input
  file.

- Group mode means that the analysis can be run with multiple input files at
  once.

If it is intended to run an analysis of lateral shape asymmetries, this may
require the computation of covariance matrices across subjects unless either
the --covfile=<...> or the --asy=euc argument is specified. In this case (i.e.,
neither is a covariance file specified nor are euclidean distances used), it
will be necessary run the script in group mode so that a covariance matrix can
be computed internally.

It is assumed that multiple input files, if present, share exactly the same
number, order, and labels of eigenvalues and brain structures.

Optional inputs are one or more of the following:

--vol=<value>      : perform surface (2D) and/or volume (3D) normalization;
                     requires one of the following values:
                     - 1: perform default normalization, see below for a
                          description
                     - 2: perform 2D normalization (surface) for all structures
                     - 3: perform 3D normalization (volumne) for all structures

--lin              : perform linear reweighting

--asy=<value>      : compute lateral shape asymmetries; requires one of the
                     following values:
                     - euc: euclidean distance
                     - mah: mahalanobis distance
                     - mcd: robust distance (minimum covariance determinant)

--covfile=<file>   : covariance matrix for Mahalanobis or MCD distance
                     computation. This is can be any comma-separated text file
                     without header that contains an m x n matrix, where m is
                     the number of anatomical structures, and n is the number
                     of upper triangular elements (including the diagonal) of
                     the covariance matrix of the eigenvalues of that
                     structure. The first column of this file must contain the
                     name of the structure without the laterality indicator
                     (i.e. Hippocampus instead of Left-Hippocampus or white
                     instead of rh-white). The ordering of the columns is
                     cov(EV1,EV1), cov(EV1,EV2), cov(EV2,EV2), cov(EV1,EV3),
                     cov(EV2,EV3), cov(EV3,EV3), ..., cov(EVk-1,EVk),
                     cov(EVk,EVk) for k eigenvalues.

--out=<directory> :  common output directory where all individual results will
                     be stored. This requires that each input file must have a
                     unique filename in order to avoid duplicate filenames
                     within the same directory. If this option is specified, no
                     output will be written into the original input directories.

--outcov=<dir>    :  output directory for writing the covariance matrices. If
                     not specified, all calculations will be internal and
                     nothing will be written to file.


OUTPUTS

The program will output (a subset of) normalized eigenvalues, reweighted
eigenvalues and asymmetry measures (distances). Outputs will be written into
each subject's original input directory, unless the --out option is specified.
In that case, a common ouptput directory will be used for all data.


NORMALIZATION

If both --vol and --lin are present, surface / volume normalization is done
first, and linear reweighting is done second.

Default surface / volume normalization means that, in general, surface
normalization will be used, since the brainPrint scripts primarily operates on
surfaces; the only exception are the left and right white and pial, for which
an additional 3D analysis is performed in addition to the 2D analysis if the
--do3d option was supplied for the brainPrint scripts. For this 3D analysis,
volume normalization will be used. The script will use the variable name to
determine which normalization should be used.


EXAMPLE

The recommended way to postprocess the fs_brainPrint.py results is to perform
default normalization and linear reweighting prior to lateral shape asymmetry
analysis. This results in the following sequence of processing steps:

a) example for a single subject using euclidean distance.

The following will perform default normalization, reweighting and asymmetry
calculation using euclidean distances for a single subject. This does not
require a covariance file.

fs_brainPrintPostproc --file=/path/to/subject-directory/brainPrintOutputFile.csv
--vol=1 --lin --asy=euc

b) example for a single subject using Mahalanobis distance.

The following will perform default normalization, reweighting and asymmetry
calculation using the Mahalanobis distance for a single subject. This requires
that a covariance file is supplied:

fs_brainPrintPostproc --file=/path/to/subject-directory/brainPrintOutputFile.csv
--vol=1 --lin --asy=mah --covfile=/path/to/covarianceFile.csv

c) example for multiple subjects

The following will perform default normalization, reweighting and asymmetry
calculation using the Mahalanobis distance for multiple subjects. The covariance
will be computed ad hoc:

fs_brainPrintPostproc --list=/path/to/list-of-brainPrintOutputFiles.txt --vol=1
--lin --asy=mah --out=/path/to/output-directory


REFERENCES

Always cite [1] as it describes the method. If you do statistical shape
analysis you may also want to cite [2] as it discusses medical applications.
The methods used within this script originate from [3].

[1] M. Reuter, F.-E. Wolter and N. Peinecke.
Laplace-Beltrami spectra as "Shape-DNA" of surfaces and solids.
Computer-Aided Design 38 (4), pp.342-366, 2006.
http://dx.doi.org/10.1016/j.cad.2005.10.011

[2] M. Reuter, F.-E. Wolter, M. Shenton, M. Niethammer.
Laplace-Beltrami Eigenvalues and Topological Features of Eigenfunctions for
Statistical Shape Analysis.
Computer-Aided Design 41 (10), pp.739-755, 2009.
http://dx.doi.org/10.1016/j.cad.2009.02.007

[3] C. Wachinger, P. Golland, W. Kremen, B. Fischl, M. Reuter, for the
Alzheimer's Disease Neuroimaging Initiative.
BrainPrint: A Discriminative Characterization of Brain Morphology.
NeuroImage 109, pp.232-248, 2015.
http://dx.doi:10.1016/j.neuroimage.2015.01.032.
"""

# ------------------------------------------------------------------------------
# AUXILIARY FUNCTIONS

# options_parse()

def options_parse():
    """
    Command Line Options Parser:
    initiate the option parser and return the parsed object
    """
    parser = optparse.OptionParser(usage=HELPTEXT)

    # help text
    h_file   = 'a csv file that was produced by the fs_brainPrint.py script'
    h_list   = 'a text file with a list of csv files that were produced by the fs_brainPrint.py script'

    h_vol    = 'perform default (VOL=1), surface (VOL=2), or volume (VOL=3) normalization'
    h_lin    = 'perform linear reweighting'
    h_asy    = 'compute lateral shape asymmetries using euclidean (ASY=euc), mahalanobis (ASY=mah), or robust (ASY=mcd) distances'
    h_covfile= 'a csv file with covariance matrices (in conjunction with --file and mahalanobis or robust distances)'
    h_out    = 'common output directory; will be created if necessary'
    h_outcov = 'covariance output directory; will be created if necessary'

    # specify inputs
    group = optparse.OptionGroup(parser, "Required Options:", "use EITHER --file OR --list (but not both)")
    group.add_option('--file', dest='file', help=h_file)
    group.add_option('--list', dest='list', help=h_list)
    parser.add_option_group(group)

    # processing switches
    group = optparse.OptionGroup(parser, "Processing Options:","use --help for details")
    group.add_option('--vol', dest='vol', help=h_vol, default=0, type='int' )
    group.add_option('--lin', dest='lin', help=h_lin, default=False, action='store_true' )
    group.add_option('--asy', dest='asy', help=h_asy)
    group.add_option('--covfile', dest='covfile', help=h_covfile)
    group.add_option('--out', dest='out', help=h_out)
    group.add_option('--outcov', dest='outcov', help=h_out)
    parser.add_option_group(group)

    # parse arguments
    (options, args) = parser.parse_args()

    # check if there are any inputs
    if len(sys.argv)==1:
        print(HELPTEXT)
        sys.exit(0)

    # check if input file or input list is given (but not both)
    if options.file is None and options.list is None:
        print('\nERROR: Specify either --file or --list (but not both)\n')
        sys.exit(1)
    elif options.file is not None and options.list is not None:
        print('\nERROR: Specify either --file or --list (but not both)\n')
        sys.exit(1)

    # check if input list exists (input file will be checked later)
    if options.file is not None:
            print('... Found input file '+options.file)
    elif options.list is not None:
        print('... Found input list '+options.list)
        if not os.path.isfile(options.list):
            print('ERROR: input list '+options.list+' is not an existing regular file\n')
            sys.exit(1)

    # create list of files (even if --file option was given)
    if  options.file is not None:
        options.csvfiles = [options.file]
    elif options.list is not None:
        with open(options.list,"r") as txt:
            options.csvfiles = txt.read().splitlines()

    # make sure that each csvfile contains the absolute path
    for i,j in enumerate(options.csvfiles):
        options.csvfiles[i]=os.path.abspath(j)

    # check if every csvfile exists
    for i in options.csvfiles:
        if not os.path.isfile(i):
            print('ERROR: input file '+i+' is not an existing regular file\n')
            sys.exit(1)

    # check if covariance file exists if it was given
    if options.covfile is not None:
        if not os.path.isfile(options.covfile):
            print('ERROR: covariance file '+options.covfile+' is not an existing regular file\n')
            sys.exit(1)

    # check that there are at least two subjects if --asy=mah or --asy=mcd and covariance file is not given
    if (options.asy=='mah' or options.asy=='mcd') and options.covfile is None:
        if len(options.csvfiles)<2:
            print('ERROR: need at least 2 csvfiles for covariance computation\n')
            sys.exit(1)

    # check --asy argument
    if options.asy!="euc" and options.asy!="mahEuc" and options.asy!="mahLin" and options.asy!="mah" and options.asy!="mcd" and options.asy!=None:
        print('ERROR: --asy='+options.asy+' is not a recognized input option\n')
        sys.exit(1)

    # check --vol argument
    if options.vol!=1 and options.vol!=2 and options.vol!=3 and options.vol!=0:
        print('ERROR: --vol='+options.vol+' is not a recognized input option\n')
        sys.exit(1)

    # check if we have numpy version >= 1.7
    if du.LooseVersion(np.version.version)<du.LooseVersion("1.7"):
        print('ERROR: numpy version >= 1.7 required, current version is '+np.version.version+'\n')
        sys.exit(1)

    # check common output directory
    if options.out is not None:
        # make sure we are using an absolute pathname
        # check if output dir exists (or can be created)
        if not os.path.isdir(options.out):
            try:
                os.mkdir(options.out)
            except:
                print('ERROR: cannot create output directory '+options.out+'\n')
                sys.exit(1)

        # check if we have write access to output dir
        try:
            testfile = tempfile.TemporaryFile(dir = options.out)
            testfile.close()
        except OSError as e:
            if e.errno != errno.EACCES:  # 13
                e.filename = options.out
                raise
            print('\nERROR: '+options.out+' not writeable (check access)!\n')
            sys.exit(1)

    # check covariance output directory
    if options.outcov is not None:
        # make sure we are using an absolute pathname
        # check if output dir exists (or can be created)
        if not os.path.isdir(options.outcov):
            try:
                os.mkdir(options.outcov)
            except:
                print('ERROR: cannot create covariance output directory '+options.outcov+'\n')
                sys.exit(1)

        # check if we have write access to output dir
        try:
            testfile = tempfile.TemporaryFile(dir = options.outcov)
            testfile.close()
        except OSError as e:
            if e.errno != errno.EACCES:  # 13
                e.filename = options.outcov
                raise
            print('\nERROR: '+options.outcov+' not writeable (check access)!\n')
            sys.exit(1)

    # return
    return options

# split_callback()

def split_callback(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))

# provide_covariance()

def provide_covariance(covInput,evalSize):

    # read covariance file
    covFile=np.genfromtxt(covInput,dtype=['S32']+['float']*(old_div((evalSize[0]**2-evalSize[0]),2)+evalSize[0]),delimiter=',')
    covFileNames=covFile[covFile.dtype.names[0]]
    covFileData=np.array(covFile[list(covFile.dtype.names[1:])].tolist())

    # check for correct size of covFileData, must conform with evals
    expectedSize=(evalSize[1],old_div((evalSize[0]**2-evalSize[0]),2)+evalSize[0])
    if np.shape(covFileData)[0]!=expectedSize[0] or np.shape(covFileData)[1]!=expectedSize[1] :
        print('ERROR: size of covariance file '+str(np.shape(covFileData))+' does not conform with size of eigenvalue matrix '+str(expectedSize)+'\n')
        sys.exit(1)

    # create dict of square matrices from upper diagonal values
    covDict=dict()
    for i in range(len(covFileNames)): # keys
        # we fill covArray in a column-wise manner (i.e. rows iterate faster)
        covArray=np.zeros((evalSize[0],evalSize[0]))
        for k in range(evalSize[0]): # cols
            for j in range(0,k+1): # rows
                #print([i,j,k,j+sum(range(0,k+1))])
                covArray[j,k]=covFileData[i,j+sum(range(0,k+1))]
                covArray[k,j]=covFileData[i,j+sum(range(0,k+1))]
        covDict.update({covFileNames[i] : covArray})

    # return
    return(covDict)

# compute_covariance()

def compute_covariance(data,pairs,method):

    # create multidimensional array
    datArray = np.zeros((np.shape(data[list(data.keys())[0]]['evals'])[0],np.shape(data[list(data.keys())[0]]['evals'])[1],len(list(data.keys()))))
    for k in range(len(list(data.keys()))):
        datArray[:,:,k] = data[list(data.keys())[k]]['evalsNormLin']

    # check for NaNs
    containsNaNs = list()
    for k in range(datArray.shape[2]):
        if np.isnan(datArray[:,:,k]).any():
            print('... Warning: NaNs found for '+list(data.keys())[k])
            containsNaNs.append(k)
    datArray = np.delete(datArray,containsNaNs,axis=2)

    # compute left and right covariances
    leftDict = dict()
    rightDict = dict()
    for s in list(pairs.keys()):
        leftDict.update({s : datArray[:,pairs[s][0],:]})
        rightDict.update({s : datArray[:,pairs[s][1],:]})

    # compute covariance
    covDict = dict()
    if method=='mah':
        # compute classical covariance
        for s in list(leftDict.keys()):
            covDict.update({s : (np.cov(leftDict[s])+np.cov(rightDict[s]))/2})
    elif method=='mcd':
        # check if we can import library
        try:
            import sklearn.covariance as sk
        except ImportError as e:
            print(e)
            print('ERROR: sklearn / scikit-learn package is required for the MCD computation, but could not be imported\n')
            sys.exit(1)
        # compute minimum covariance determinant
        for s in list(leftDict.keys()):
            covDict.update({s : (sk.MinCovDet().fit(np.cov(leftDict[s])).covariance_+sk.MinCovDet().fit(np.cov(leftDict[s])).covariance_)/2})
    elif method=="mahEuc":
        # identity matrix
        for s in list(leftDict.keys()):
            covDict.update({s : np.identity(options.nEV+1)})
    elif method=="mahLin":
        # linear reweighting
        for s in list(leftDict.keys()):
            covDict.update({s : np.diag(list(range(1,options.nEV+2)))})

    # return
    return(covDict)

# identify left-right pairs

def identify_pairs(structures):

    pairs=dict()
    for il,jl  in enumerate(structures):
        if re.search("^Left-",jl):
            tmp=jl.replace("Left-","")
            for ir,jr  in enumerate(structures):
                if re.search("^Right-"+tmp,jr):
                    pairs.update({tmp : (il,ir)})
        elif re.search("^lh-",jl):
            tmp=jl.replace("lh-","")
            for ir,jr  in enumerate(structures):
                if re.search("^rh-"+tmp,jr):
                    pairs.update({tmp : (il,ir)})
    return(pairs)

# -----------------------------------------------------------------------------
# MAIN PART

if __name__=="__main__":

    # --------------------------------------------------------------------------
    # Command Line options and error checking
    print("-----------------------------------------------------------------")
    print("fs_brainPrintPostproc()")
    print("-----------------------------------------------------------------")

    # --------------------------------------------------------------------------
    # Command Line options and error checking

    print("\nReading input options ...")
    options = options_parse()

    # --------------------------------------------------------------------------
    # Read input files and store data in a dict of dicts

    data = dict()
    for f in options.csvfiles:
        # below, we use 'names=None' since names cannot contain hyphens, which is bad
        tmp = np.genfromtxt(f, dtype='str' ,delimiter=',', names=None)
        data.update({ f : {
            'names'  : tmp[0].tolist(),
            'surface': np.array(tmp[1].tolist(),dtype="float"),
            'volume' : np.array(tmp[2].tolist(),dtype="float"),
            'evals'  : np.array(tmp[3:].tolist(),dtype="float")
            }})

    # --------------------------------------------------------------------------
    # Check input (must e.g. have same size, same labels, same order, no missings, etc.)

    print("\nChecking input files ...")

    check_names = list()
    for k in list(data.keys()): check_names.append(data[list(data.keys())[0]]['names'] == data[k]['names'])
    if not all(check_names) :
        print('ERROR: names of structures are not consistent across csv files\n')
        sys.exit(1)

    check_evalSize = list()
    for k in list(data.keys()): check_evalSize.append(np.shape(data[list(data.keys())[0]]['evals']) == np.shape(data[k]['evals']))
    if not all(check_evalSize) :
        print('ERROR: sizes of eigenvalue matrices are not consistent across csv files\n')
        sys.exit(1)

    # --------------------------------------------------------------------------
    # Surface / volume normalization

    if options.vol==1:
        print("\nDefault surface / volume normalization ...")
        for f in options.csvfiles:
            tmp = np.zeros(data[f]['evals'].shape)
            for ni,nj  in enumerate(data[f]['names']):
                if re.search("3d",nj):
                    tmp[:,ni]=data[f]['evals'][:,ni]*data[f]['volume'][ni]**(old_div(2.0,3.0))
                else:
                    tmp[:,ni]=data[f]['evals'][:,ni]*data[f]['surface'][ni]**(old_div(2.0,2.0))
            data[f].update({'evalsNorm' : tmp})
    elif options.vol==2:
        print("\nSurface normalization for all structures ...")
        for f in options.csvfiles:
            tmp = np.zeros(data[f]['evals'].shape)
            for ni,nj  in enumerate(data[f]['names']):
                tmp[:,ni]=data[f]['evals'][:,ni]*data[f]['surface'][ni]**(old_div(2.0,2.0))
            data[f].update({'evalsNorm' : tmp})
    elif options.vol==3:
        print("\nVolume normalization for all structures ...")
        for f in options.csvfiles:
            tmp = np.zeros(data[f]['evals'].shape)
            for ni,nj  in enumerate(data[f]['names']):
                tmp[:,ni]=data[f]['evals'][:,ni]*data[f]['volume'][ni]**(old_div(2.0,3.0))
            data[f].update({'evalsNorm' : tmp})
    else:
        print("\nNot performing surface / volume normalization ...")
        for f in options.csvfiles:
            tmp = np.zeros(data[f]['evals'].shape)
            for ni,nj  in enumerate(data[f]['names']):
                tmp[:,ni]=data[f]['evals'][:,ni]
            data[f].update({'evalsNorm' : tmp})

    # --------------------------------------------------------------------------
    # Linear reweighting

    if options.lin:
        print("\nLinear reweighting ...")
        for f in options.csvfiles:
            tmp = data[f]['evalsNorm']
            tmp = old_div(tmp,(np.tile(np.reshape(np.r_[0:tmp.shape[0]],(tmp.shape[0],1)),(1,tmp.shape[1]))+1.0))
            data[f].update({'evalsNormLin' : tmp})
    else:
        print("\nNot performing linear reweighting ...")
        for f in options.csvfiles:
            tmp = data[f]['evalsNorm']
            data[f].update({'evalsNormLin' : tmp})

    # --------------------------------------------------------------------------
    # Identify matching structures

    if options.asy is not None or options.outcov is not None:

        #
        print("\nIdentifying matching structures ...")

        pairs_idx = identify_pairs(data[list(data.keys())[0]]['names'])
        if len(pairs_idx)==0:
            print('ERROR: could not identify any pairs among '+str(data[list(data.keys())[0]]['names'])+'\n')
            sys.exit(1)

    # --------------------------------------------------------------------------
    # Set the number of EVs used for distance calculations (not including EV1)

    if options.asy is not None or options.outcov is not None:

        # this is currently an internal option; the default is to use all available EVs (except EV1)
        # in small samples and for testing purposes it may make sense to restrict this value manually (e.g. options.nEV = 5)
        # in the future, this may become a command-line argument. In the meantime, use as follows:
        # options.nEV = None # this is the default (=use all)
        # options.nEV = 5

        options.nEV = None
        if options.nEV is None:
            options.nEV = np.shape(data[list(data.keys())[0]]['evals'])[0]-1 # all available EVs (excl. EV1)

        print("\nUsing "+str(options.nEV)+" eigenvalues for distance calculation ...")

    # --------------------------------------------------------------------------
    # Covariance computation

    if options.asy=="mah" or options.asy=="mahEuc" or options.asy=="mahLin" or options.asy=="mcd" or options.outcov is not None:

        #
        print("\nCovariance computation ...")

        if options.covfile is not None:
            print('... Reading covariance file '+options.covfile+'\n')
            covMat = provide_covariance(options.covfile,(np.shape(data[list(data.keys())[0]]['evals'])[0],len(pairs_idx)))
        else:
            print('... Computing covariance from data')
            covMat = compute_covariance(data,pairs_idx,options.asy)

    # --------------------------------------------------------------------------
    # Lateral shape asymmetries

    if options.asy is not None:

        #
        print("\nAnalysis of lateral shape asymmetries ...")

        # distance calculation
        print('... Computing '+options.asy.replace("euc","euclidean").replace("mah","classical").replace("mcd","robust")+' distances')
        for f in list(data.keys()):
            dist = dict()
            if np.isnan(data[f]['evalsNormLin'][1:(options.nEV+1),:]).any():
                print('... Warning: NaNs found for '+f)
            for p in list(pairs_idx.keys()):
                # this is the R formula: xOli.md<-sqrt(apply(xOli,1,function(x,a,b){matrix(x-a,1,length(x))%*%b%*%matrix(x-a,length(x),1)},colMeans(xOli),solve(cov(xOli))))
                # note that we are here (and only here) excluding the first eigenvalue from the computations, both from the values as well as the covariance matrix; the reason is that it will always be zero, and hence produce a singularity problem during matrix inversion
                # note that we also check for NaNs here
                # note that, strictly speaking, we are not comparing different distances, but different covariance matrices. Identity for Euc, classical for "Mahalanobis", and robust for "mcd". maybe we should improve terminology, and also adjust options / flow: replace current --asy= with --cov=, and introduce --asy switch (cf --lin).

                if not np.isnan(data[f]['evalsNormLin'][1:(options.nEV+1),pairs_idx[p]]).any():
                    if options.asy=="euc":
                        dist.update({p : np.float(di.euclidean(data[f]['evalsNormLin'][1:(options.nEV+1),pairs_idx[p][0]],data[f]['evalsNormLin'][1:(options.nEV+1),pairs_idx[p][1]]))})
                    elif options.asy=="mah":
                        dist.update({p : np.float(di.mahalanobis(data[f]['evalsNormLin'][1:(options.nEV+1),pairs_idx[p][0]],data[f]['evalsNormLin'][1:(options.nEV+1),pairs_idx[p][1]],np.matrix(covMat[p][1:(options.nEV+1),1:(options.nEV+1)]).I))})
                    elif options.asy=="mcd":  # it is no mistake that we use mahalanobis below; the covariance matrix will still be different!
                        dist.update({p : np.float(di.mahalanobis(data[f]['evalsNormLin'][1:(options.nEV+1),pairs_idx[p][0]],data[f]['evalsNormLin'][1:(options.nEV+1),pairs_idx[p][1]],np.matrix(covMat[p][1:(options.nEV+1),1:(options.nEV+1)]).I))})
                    elif options.asy=="mahEuc": # internal option
                        dist.update({p : np.float(di.mahalanobis(data[f]['evalsNormLin'][1:(options.nEV+1),pairs_idx[p][0]],data[f]['evalsNormLin'][1:(options.nEV+1),pairs_idx[p][1]],np.matrix(covMat[p][1:(options.nEV+1),1:(options.nEV+1)]).I))})
                    elif options.asy=="mahLin": # internal option
                        dist.update({p : np.float(di.mahalanobis(data[f]['evalsNormLin'][1:(options.nEV+1),pairs_idx[p][0]],data[f]['evalsNormLin'][1:(options.nEV+1),pairs_idx[p][1]],np.matrix(covMat[p][1:(options.nEV+1),1:(options.nEV+1)]).I))})
                else:
                    dist.update({p : np.nan})
                data[f].update({'dist' : dist})

    else:

        print("\nNot performing analysis of lateral shape asymmetries ...")

    # --------------------------------------------------------------------------
    # Write out results

    if options.out is not None:
        print('\nWriting outputs to '+options.out+' ...')
    else:
        print('\nWriting outputs to input directories ...')

    for f in options.csvfiles:
        # get filename base and extension
        outfilebase, outfileext = os.path.splitext(f)
        # group output
        if options.out is not None:
            outfilebase = os.path.join(options.out,os.path.split(outfilebase)[1])
        # write normalized eigenvalues
        if options.vol>0:
            with open(outfilebase+'_norm'+outfileext, WRITECSVSPECIFIER) as outfilehandle:
                csvwriter = csv.writer(outfilehandle, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csvwriter.writerow(data[f]['names'])
                csvwriter.writerow(data[f]['surface'])
                csvwriter.writerow(data[f]['volume'])
                csvwriter.writerows(data[f]['evalsNorm'])
        # write normalized+reweighted eigenvalues
        if options.lin:
            if options.vol>0:
                outfiledescr='_norm_reweighted'
            else:
                outfiledescr='_reweighted'
            with open(outfilebase+outfiledescr+outfileext, WRITECSVSPECIFIER) as outfilehandle:
                csvwriter = csv.writer(outfilehandle, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csvwriter.writerow(data[f]['names'])
                csvwriter.writerow(data[f]['surface'])
                csvwriter.writerow(data[f]['volume'])
                csvwriter.writerows(data[f]['evalsNormLin'])
        # write distances
        if options.asy is not None:
            with open(outfilebase+'_distances'+outfileext, WRITECSVSPECIFIER) as outfilehandle:
                csvwriter = csv.DictWriter(outfilehandle, fieldnames=list(data[f]['dist'].keys()), delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csvwriter.writeheader()
                csvwriter.writerow(data[f]['dist'])

    # --------------------------------------------------------------------------
    # Write out covariance (optional)

    if options.outcov is not None:
        print('\nWriting covariance matrices to '+options.outcov+' ...')
        # upper triangular format
        with open(os.path.join(options.outcov,'brainprint-covariance.csv'), WRITECSVSPECIFIER) as outfilehandle:
            csvwriter = csv.writer(outfilehandle, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for s in list(covMat.keys()):
                # using tril instead of triu is a trick that helps us to fill the matrix column-wise
                csvwriter.writerow([s]+covMat[s][np.tril_indices(covMat[s].shape[0],k=0)].tolist())
        # below is an alternative to write out several (stacked) full matrices, if desired
        with open(os.path.join(options.outcov,'brainprint-covariance-full.csv'), WRITECSVSPECIFIER) as outfilehandle:
            csvwriter = csv.writer(outfilehandle, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for s in list(covMat.keys()):
                csvwriter.writerow([s])
                csvwriter.writerows(covMat[s])

    # --------------------------------------------------------------------------
    # Always exit with 0 exit code

    #import pdb; pdb.set_trace()
    print('\nDone.')
    sys.exit(0)

# END MAIN PART
