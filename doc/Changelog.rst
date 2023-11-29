Changelog
=========

Version 2.0.1
-------------

- This fix addresses two minor issues where output was omitted for the SNR computation and the fornix evaluation whenever hires inputs were used.

Version 2.0.0
-------------

- Name changes for the toolbox, repository, package, and scripts: the toolbox has been renamed to "fsqc tools", the python package name "qatoolspython" has been changed to "fsqc", and the "qatools.py" script has been renamed to "run_fsqc". The github repository is now located at "https://github.com/Deep-MI/fsqc", but requests to the old "https://github.com/Deep-MI/qatools-python" repository will be redirected.
- Name changes for output files (replacing 'qatools' with 'fsqc').
- Interface changes: importing and running the scripts has changed. In particular, `run_fsqc` is now an executable file and replaces the `qatools` or `qatools.py` command. `run_fsqc()` is now also a function that can be used in a Python environment. See `here <https://github.com/Deep-MI/fsqc#usage>`_ for details.
- New names for main and dev branches: the main (default) branch is now called `stable` (was: `freesurfer-module-releases`), and the dev branch is now called `dev` (was: `freesurfer-module-dev`). The old branches will still be kept for a while in a deprecation state, but will not receive further updates or support.
- Screenshots are now in radiological orientation (left is right). Before version 2.0, screenshots were in neurological orientation (left is left).
- Addition of skullstrip, surfaces, hippocampus, and hypothalamus modules.
- Improved logging, error handling, and testing frameworks.
- Enhanced containerization support (docker, singularity, dockerhub).
- Updated requirements, easier installation of the package and its dependencies, availability of the package on `pypi.org <https://pypi.org/>`_.
- FreeSurfer is no longer required as a dependency (except for the optional 'shape analysis' module, which relies on the brainprint package).
- Compatibility with earlier versions is not preserved.

