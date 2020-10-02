#!/usr/bin/env python3

# say hello
print("")
print("-----------------------------")
print("qatools-python")
print("-----------------------------")
print("")

# imports
from qatoolspython import qatoolspython

# parse arguments
subjects_dir, output_dir, subjects, shape, screenshots, screenshots_base, screenshots_overlay, screenshots_surf, screenshots_views, fornix, outlier, outlier_table, fastsurfer = qatoolspython._parse_arguments()

# run qatools
qatoolspython.run_qatools(subjects_dir, output_dir, subjects, shape, screenshots, screenshots_base, screenshots_overlay, screenshots_surf, screenshots_views, fornix, outlier, outlier_table, fastsurfer)
