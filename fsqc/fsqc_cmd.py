def _fsqc():
    # say hello
    print("")
    print("-----------------------------")
    print("fsqc")
    print("-----------------------------")
    print("")

    # imports
    from fsqc import fsqc

    # parse arguments
    argsDict = fsqc._parse_arguments()

    # run fsqc
    if argsDict is not None:
        fsqc.run_fsqc(subjects_dir=None, output_dir=None, argsDict=argsDict)
