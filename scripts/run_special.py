#!/usr/bin/env python
"""Run specials.

This script allows to run the special notebooks. One can either run all notebooks at once or just a
single lecture. It is enough to provide a substring for the name.

Examples
--------

>> run-special             Run all specials.

>> run-special -n 01      Run special nonstandard-standard_errors.
"""
import subprocess as sp
import glob
import os

from auxiliary import parse_arguments
from auxiliary import SPECIALS_ROOT


def run_notebook(notebook):
    cmd = " jupyter nbconvert --execute {}  --ExecutePreprocessor.timeout=-1".format(notebook)
    sp.check_call(cmd, shell=True)


if __name__ == "__main__":

    request = parse_arguments("Execute special")
    os.chdir(SPECIALS_ROOT)

    for dirname in request:
        os.chdir(dirname)
        for fname in glob.glob("*.ipynb"):
            print(f"\n {os.getcwd().split('/')[-1]}\n")
            run_notebook(fname)
        os.chdir("../")
