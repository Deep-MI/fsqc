#!/usr/bin/env python
# -*- coding: latin-1 -*-

def exportVTK(v,t,outfile):
    """
    Save VTK file
    
    usage: exportVTK(vertices,triangles,outfile)

    """

    # imports
    import numpy as np

    # open file
    try:
        f = open(outfile,'w')
    except IOError:
        print("[File "+outfile+" not writable]")
        return

    # check data structure

    # ...

    #
    f.write('# vtk DataFile Version 1.0\n')
    f.write('vtk output\n')
    f.write('ASCII\n')
    f.write('DATASET POLYDATA\n')
    f.write('POINTS '+str(np.shape(v)[0])+' float\n')
    
    for i in range(np.shape(v)[0]):
        f.write(' '.join(map(str,v[i,:])))
        f.write('\n')
      
    f.write('POLYGONS '+str(np.shape(t)[0])+' '+str(4*np.shape(t)[0])+'\n')

    for i in range(np.shape(t)[0]):
        f.write(' '.join(map(str,np.append(3,t[i,:]))))
        f.write('\n')

    # close file
    f.close()
