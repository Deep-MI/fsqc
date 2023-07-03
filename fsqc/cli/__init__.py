"""
fsqc CLI
"""

from ..fsqcMain import _parse_arguments, run_fsqc


def main():
    # say hello
    print("")
    print("-----------------------------")
    print("fsqc")
    print("-----------------------------")
    print("")

    # parse arguments
    argsDict = _parse_arguments()

    # run fsqc
    if argsDict is not None:
        run_fsqc(subjects_dir=None, output_dir=None, argsDict=argsDict)
