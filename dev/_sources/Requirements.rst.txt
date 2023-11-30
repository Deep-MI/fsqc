Requirements
============

- At least one structural MR image that was processed with Freesurfer 6.0, 7.x, or FastSurfer 1.1 or later (including the surface pipeline).

- A Python version >= 3.8 is required to run this script.

- Required packages include (among others) the `nibabel` and `skimage` packages for the core functionality, plus the `matplotlib`, `pandas`, and `transform3d` packages for some optional functions and modules. See the `requirements.txt` file for a complete list.
  Use the following command to install these packages:

  ```
  bash
  pip install -r requirements.txt
  ```
- If installing the toolbox as a Python package or if using the Docker image, all required packages will be installed automatically, and manual installation as detailed above will not be necessary.

- This software has been tested on Ubuntu 20.04.

- A working `FreeSurfer <https://freesurfer.net/>`_ installation (version 6 or newer) is required for running the 'shape' module of this toolbox. Also, make sure that FreeSurfer is sourced (i.e., FREESURFER_HOME is set as an environment variable) before running an analysis.



Known issues
------------

- Aborted / restarted recon-all runs: the program will analyze recon-all logfiles, and may fail or return erroneous results if the logfile is appended by multiple restarts of recon-all runs. Ideally, the logfile should therefore consist of just a single, successful recon-all run.