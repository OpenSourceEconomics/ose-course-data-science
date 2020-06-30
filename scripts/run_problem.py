#!/usr/bin/env python
"""Run problem set.

This script allows to run the problem set. One can either run all problem sets at once or just a
single one. It is enough to provide a substring for the name.

Examples
--------

>> run-problem             Run all problem set.

>> run-problem -n 01      Run slide 01-potential-outcome-model.
"""
import glob
import os

from auxiliary import PROBLEM_SETS_ROOT
from auxiliary import parse_arguments
from auxiliary import run_notebook


if __name__ == "__main__":

    request = parse_arguments("Create problem set")

    os.chdir(PROBLEM_SETS_ROOT)

    for dirname in request:
        os.chdir(dirname)
        [run_notebook(fname) for fname in glob.glob("*.ipynb")]

        os.chdir("../")
