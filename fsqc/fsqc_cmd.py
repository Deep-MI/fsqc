def _qatools():
    # say hello
    print("")
    print("-----------------------------")
    print("qatools-python")
    print("-----------------------------")
    print("")

    # imports
    from qatoolspython import qatoolspython

    # parse arguments
    argsDict = qatoolspython._parse_arguments()

    # run qatools
    if argsDict is not None:
        qatoolspython.run_qatools(subjects_dir=None, output_dir=None, argsDict=argsDict)
