#!/usr/bin/env python
"""This module executes all notebooks. It serves the main purpose to ensure that all can be
executed and work proper independently."""
import subprocess as sp
import glob
import os

from auxiliary import parse_arguments
from auxiliary import LECTURES_ROOT


def run_notebook(notebook):
    cmd = ' jupyter nbconvert --execute {}  --ExecutePreprocessor.timeout=-1'.format(notebook)
    sp.check_call(cmd, shell=True)


if __name__ == '__main__':

    request = parse_arguments('Execute notebook')
    os.chdir(LECTURES_ROOT)

    for dirname in request:
        os.chdir(dirname)
        for fname in glob.glob('*.ipynb'):
            run_notebook(fname)
        os.chdir('../')
