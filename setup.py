from setuptools import setup, find_packages
from os import path

with open("README.md", "r") as fh:
    long_description = fh.read()

# see: https://packaging.python.org/guides/distributing-packages-using-setuptools/#setup-py for a description
# see: https://github.com/pypa/sampleproject/blob/master/setup.py for an example
# see: https://pip.pypa.io/en/stable/reference/pip_install for a description how to use pip install in conjunction with a git repository

setup(
    name="qatoolspython",
    version="1.5.1",
    author="Kersten Diers, Martin Reuter, and others (see README)",
    description="A set of quality assurance / quality control scripts for Freesurfer-processed structural MRI data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/reuter-lab/qatools-python",
    packages=['qatoolspython'],
    entry_points ={
    'console_scripts': [
        'qatools = qatoolspython.qatools_cmd:_qatools'
    ]
    },
    # see https://pypi.org/classifiers/
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT",
#        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    keywords='Freesurfer',
    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['numpy','scipy','pandas','matplotlib','transforms3d', 'nibabel', 'scikit-image']
)
