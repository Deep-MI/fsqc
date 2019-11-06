#!/usr/bin/env python
# -*- coding: latin-1 -*-

#
# Modified for tetras: Kersten Diers
# Date: Feb-02-2019
#
# Modified for python3: Kersten Diers
# Date: Apr-12-2018
#
# Original Author: Martin Reuter
# Date: Feb-26-2016
#

def importVTKtetra(infile):
    """
    Load VTK tetrahedron mesh
    """
    import numpy as np

    verbose = 1
    if (verbose > 0):
        print("--> VTK format         ... ")

    try:
        f = open(infile,'r')
    except IOError:
        print("[file not found or not readable]\n")
        return
       
    # skip comments
    line = f.readline()
    while line[0] == '#':
        line = f.readline()
        
    # search for ASCII keyword in first 5 lines:
    count = 0
    while count < 5 and not line.startswith("ASCII"):
        line = f.readline()
        #print line
        count = count+1       
    if not line.startswith("ASCII"):
        print("[ASCII keyword not found] --> FAILED\n")
        return
   
    # expect Dataset Polydata line after ASCII:
    line = f.readline()
    if not line.startswith("DATASET POLYDATA"):
        print("[read: "+ line+" expected DATASET POLYDATA] --> FAILED\n")
        return
    
    # read number of points
    line = f.readline()
    larr = line.split()
    if larr[0]!="POINTS" or larr[2] != "float":
        print("[read: " + line + " expected POINTS # float] --> FAILED\n")
        return
    pnum = int(larr[1])
    
    # read points as chunk
    v=np.fromfile(f,'float32',3*pnum,' ')
    v.shape = (pnum, 3)
    
    # expect polygon or tria_strip line
    line = f.readline()
    larr = line.split()
    
    if larr[0]=="POLYGONS":
        tnum = int(larr[1])
        ttnum = int(larr[2])
        npt = float(ttnum) / tnum;
        if (npt != 5.0) :
            print("[having: " + str(npt)+ " data per tetra, expected 4+1] --> FAILED\n")
            return
        t = np.fromfile(f,'int',ttnum,' ')
        t.shape = (tnum, 5)
        if t[tnum-1][0] != 4:
            print("[can only read tetras] --> FAILED\n")
            return
        t = np.delete(t,0,1)
        
    else:
        print("[read: "+line+ " expected POLYGONS] --> FAILED\n")
        return
    
    f.close()
    
    print(" --> DONE ( V: " + str(v.shape[0]) + " , T: " + str(t.shape[0]) + " )\n")
    
    return v, t
