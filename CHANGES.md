# Changelog

This is a document summarizing the changes that are associated with (major) updates and releases. Priority is given to changes that are relevant to the user, and those that introduce new features or break compatibility with prior versions.

## Version 2.0

- Name changes for the toolbox, repository, package, and scripts: the toolbox has been renamed to "fsqc tools", the python package name "qatoolspython" has been changed to "fsqc", and the "qatools.py" script has been renamed to "run_fsqc". The github repository is now located at "https://github.com/Deep-MI/fsqc", but requests to the old "https://github.com/Deep-MI/qatools-python" repository will be redirected.
- Name changes for output files (replacing 'qatools' with 'fsqc').
- Interface changes: importing and running the scripts as a python package has changed. See [here](https://github.com/Deep-MI/fsqc) for details. In particular, 'run_fsqc' is now an executable file and replaces the 'qatools' or 'qatools.py' command.
- New names for main and dev branches: the main (default) branch is now called `stable` (was: `freesurfer-module-releases`), and the dev branch is now called `dev` (was: `freesurfer-module-dev`). The old branches will still be kept for a while in a deprecation state, but will not recieve further updates or support. 
- Screenshots are now in radiological orientation (left is right). Before version 2.0, screenshots were in neurological orientation (left is left).
- Addition of skullstrip, hippocampus and hypothalamus modules.
- Improved logging, error handling, and testing frameworks.
- Enhanced containerization support (docker, singularity, dockerhub).
- Updated requirements, easier installation of lapy and brainprint dependencies.
- FreeSurfer is no longer required as a dependency (except for the optional 'shape analysis' module, which relies on the brainprint package).
- We do not preserve compatibility with earlier versions.
