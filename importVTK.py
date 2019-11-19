#!/usr/bin/env python
# -*- coding: latin-1 -*-

#
# 
#
# 
#
# Original Author: Martin Reuter
# Date: Feb-26-2016
#

def importVTK(infile):
    """
    Load VTK triangle mesh
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
        if (npt != 4.0) :
            print("[having: " + str(npt)+ " data per tria, expected trias 3+1] --> FAILED\n")
            return
        t = np.fromfile(f,'int',ttnum,' ')
        t.shape = (tnum, 4)
        if t[tnum-1][0] != 3:
            print("[can only read triangles] --> FAILED\n")
            return
        t = np.delete(t,0,1)
        
    elif larr[0]=="TRIANGLE_STRIPS":
        tnum = int(larr[1])
        ttnum = int(larr[2])
        tt = []
        for i in xrange(tnum):
            larr = f.readline().split()
            if len(larr)==0:
                print("[error reading triangle strip (i)] --> FAILED\n")
                return
            n = larr[0]
            if len(larr)!=n+1:
                print("[error reading triangle strip (ii)] --> FAILED\n")
                return
            # create triangles from strip
            # note that larr tria info starts at index 1
            for ii in range(2,n):
                if (ii%2 == 0):
                    tria = [larr[ii-1], larr[ii], larr[ii+1]]
                else:
                    tria = [larr[ii], larr[ii-1], larr[ii+1]]
                tt.append(tria)
        t = np.array(tt)
        
    else:
        print("[read: "+line+ " expected POLYGONS or TRIANGLE_STRIPS] --> FAILED\n")
        return
    
    f.close()
    
    print(" --> DONE ( V: " + str(v.shape[0]) + " , T: " + str(t.shape[0]) + " )\n")
    
    return v, t
