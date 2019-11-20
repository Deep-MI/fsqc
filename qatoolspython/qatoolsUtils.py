#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module provides various import/export functions

"""

# -----------------------------------------------------------------------------

def importMGH(filename):
    """
    A function read Freesurfer MGH files.

    Required arguments:
        - filename

    Returns:
        - vol

    Requires valid mgh file. If not found, NaNs will be returned.

    """

    import os
    import struct
    import numpy

    if not os.path.exists(filename):
        print("WARNING: could not find "+filename+", returning NaNs")
        return numpy.nan

    fp = open(filename,'rb')
    intsize = struct.calcsize('>i')
    shortsize = struct.calcsize('>h')
    floatsize = struct.calcsize('>f')
    charsize = struct.calcsize('>b')

    v = struct.unpack('>i',fp.read(intsize))[0]
    ndim1 = struct.unpack('>i',fp.read(intsize))[0]
    ndim2 = struct.unpack('>i',fp.read(intsize))[0]
    ndim3 = struct.unpack('>i',fp.read(intsize))[0]
    nframes = struct.unpack('>i',fp.read(intsize))[0]
    vtype = struct.unpack('>i',fp.read(intsize))[0]
    dof = struct.unpack('>i',fp.read(intsize))[0]

    UNUSED_SPACE_SIZE = 256
    USED_SPACE_SIZE = (3*4) + (4*3*4) # space for ras transform
    unused_space_size = UNUSED_SPACE_SIZE - 2

    ras_good_flag = struct.unpack('>h',fp.read(shortsize))[0]
    if ras_good_flag:
        # We read these in but don't process them
        # as we just want to move to the volume data
        delta = struct.unpack('>fff',fp.read(floatsize*3))
        Mdc = struct.unpack('>fffffffff',fp.read(floatsize*9))
        Pxyz_c = struct.unpack('>fff',fp.read(floatsize*3))

    unused_space_size = unused_space_size - USED_SPACE_SIZE

    for i in range(unused_space_size):
        struct.unpack('>b',fp.read(charsize))[0]

    nv = ndim1 * ndim2 * ndim3 * nframes
    vol = numpy.fromstring(fp.read(floatsize*nv),dtype=numpy.float32).byteswap()

    nvert = max([ndim1,ndim2,ndim3])
    vol = numpy.reshape(vol,(ndim1,ndim2,ndim3,nframes),order='F')
    vol = numpy.squeeze(vol)
    fp.close()

    return vol
