Installation
============

Installation as a Python Package
---------------------------------

Use the following command to install the `fsqc` package and all of its dependencies:

.. code-block:: bash

   pip install fsqc

This is the recommended way of installing the package and allows for both command-line execution and execution as a Python function. We also recommend installing the package within a Python virtual environment:

1. Create a virtual environment:

   .. code-block:: bash

      virtualenv /path/to/my/virtual/environment
      source /path/to/my/virtual/environment/bin/activate

2. Activate the virtual environment.

Installation from GitHub
------------------------

To install the `fsqc` package from its GitHub repository, use the following command:

.. code-block:: bash

   pip install git+https://github.com/deep-mi/fsqc.git

This command downloads, builds, and installs the `fsqc` package. If you want to install a specific branch, use the following format:

.. code-block:: bash

   pip install git+https://github.com/deep-mi/fsqc.git@dev

Download from GitHub
--------------------

Alternatively, you can download the software directly from its GitHub repository at https://github.com/Deep-MI/fsqc, or clone it using the following command:

.. code-block:: bash

   git clone https://github.com/Deep-MI/fsqc

After downloading, the `run_fsqc` script will be executable from the command line, as detailed above. However, note that the required dependencies will have to be installed manually. Refer to the requirements section for instructions.
