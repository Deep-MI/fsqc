# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 12:44:21 2019

@author: Tobias Wolff
This function computes the WM/GM contrast based on the output of the pctsurfcon 
function. 
Required arguments: 
    - Subjects directory
    - Subject
"""

import struct
import numpy
import os 
import nibabel

def read_mgh(filename):
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
      
      
      
def contrast_control(subjects_dir, subject):
    # Define the different paths
    path_pct_lh = str(subjects_dir) + str(subject) + "/surf/lh.w-g.pct.mgh"
    path_pct_rh = str(subjects_dir) + str(subject) + "/surf/rh.w-g.pct.mgh"
    path_label_cortex_lh  = str(subjects_dir) + str(subject) + "/label/lh.cortex.label"
    path_label_cortex_rh = str(subjects_dir) + str(subject) + "/label/rh.cortex.label"
    
    
    # Check if files exist
    if not os.path.exists(path_pct_lh):
        print("In the contrast control function, the path to the lh.w-g.pct.mgh file is wrong")
        exit()
    if not os.path.exists(path_pct_rh):
        print("In the contrast control function, the path to the rh.w-g.pct.mgh file is wrong")
        exit()
    if not os.path.exists(path_label_cortex_lh):
        print("In the contrast control function, the path to the lh.cortex.label file is wrong")
        exit()
    if not os.path.exists(path_label_cortex_rh):
        print("In the contrast control function, the path to the rh.cortex.label file is wrong")
        exit()
    
    # Get the data fromt the mgh files
    con_lh = read_mgh(path_pct_lh)
    con_rh = read_mgh(path_pct_rh)
    
    label_array_lh = nibabel.freesurfer.io.read_label(path_label_cortex_lh)
    label_array_rh = nibabel.freesurfer.io.read_label(path_label_cortex_rh)    
    
    # Only take the values of the cortex to compute the contrast control
    con_lh = numpy.take(con_lh, label_array_lh)
    con_rh = numpy.take(con_rh, label_array_rh)
    
    # Compute the Contrast to noise ratio
    con_lh_mean = numpy.mean(con_lh)
    con_lh_std = numpy.std(con_lh)
    con_lh_snr = con_lh_mean/con_lh_std
    print("The wm/gm contrast snr for the left hemisphere is:", con_lh_snr)
    
    con_rh_mean = numpy.mean(con_rh)
    con_rh_std = numpy.std(con_rh)
    con_rh_snr = con_rh_mean/con_rh_std 
    print("The wm/gm contrast snr for the right hemisphere is: ", con_rh_snr)
    
    return con_lh_snr, con_rh_snr
    