BrainPrint
==========

BrainPrint represents a set of shape descriptors of a collection of subcortical and cortical structures.

## Dependencies:
- FreeSurfer (MRI data needs to be processed with Freesurfer 5.3 or newer): http://freesurfer.net
- ShapeDNA-tria (to perform the shape analysis): http://reuter.mit.edu/software/shapedna

To also compute shape descriptors of 3D tetrahedra meshes, you additionally need:
- meshfix  1.2-alpha: https://code.google.com/p/meshfix/
- Gmsh: http://geuz.org/gmsh/
- shapeDNA-tetra (currently unavailable, contact author http://reuter.mit.edu/software/shapedna )
These are not required for the software to work, and only add 4 more descriptors for white and pial volumes (each hemisphere).

## Installation:
Set the environment variable $SHAPEDNA_HOME to the directory containing shapeDNA-tria. If you want to perform also 3D tetra processing, also copy gmsh, meshfix and shapeDNA-tetra to that directory. Source your FreeSurfer (5.3 or newer) and you are ready to go. 

## Reference:

If you use this software for a publication please cite both these papers:

[1]
BrainPrint: a discriminative characterization of brain morphology.
Wachinger C, Golland P, Kremen W, Fischl B, Reuter M
Neuroimage. 2015;109:232-48.
http://dx.doi.org/10.1016/j.neuroimage.2015.01.032
http://www.ncbi.nlm.nih.gov/pubmed/25613439

[2]
Laplace-Beltrami spectra as 'Shape-DNA' of surfaces and solids.
Reuter M, Wolter F-E, Peinecke N
Computer-Aided Design. 2006;38(4):342-366.
http://dx.doi.org/10.1016/j.cad.2005.10.011

[1] contains the definition of the BrainPrint ensemble and neuroimaging application, while
[2] introduces the shape descriptor (shapeDNA).

Homepage: http://reuter.mit.edu/software/brainprint

Author: Martin Reuter
