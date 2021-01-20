#!/usr/bin/env python
"""Run notebooks.

This script allows to run the lecture notebooks. One can either run all notebooks at once or just a
single lecture. It is enough to provide a substring for the name.

Examples
--------
>> run-notebook             Run all lectures.

>> run-notebook -n 01      Run lecture 01-introduction.
"""
import glob
import os

from auxiliary import LECTURES_ROOT
from auxiliary import parse_arguments
from auxiliary import run_notebook


if __name__ == "__main__":

    request = parse_arguments("Execute notebook")
    os.chdir(LECTURES_ROOT)

    for dirname in request:

        os.chdir(dirname)
        for fname in glob.glob("*.ipynb"):
            print(f"\n {os.getcwd().split('/')[-1]}\n")
            run_notebook(fname)
        os.chdir("../")
