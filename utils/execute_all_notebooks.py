#!/usr/bin/env python
"""This module executes all notebooks. It serves the main purpose to ensure that all can be
executed and work proper independently."""
import subprocess as sp
import os


def run_notebook(notebook):
    cmd = ' jupyter nbconvert --execute {}  --ExecutePreprocessor.timeout=-1'.format(notebook)
    sp.check_call(cmd, shell=True)


if __name__ == '__main__':

    for subdir, dirs, files in os.walk('.'):
        # We want to skip all hidden directories.
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for file in files:
            if 'ipynb' in file:
                run_notebook(subdir + '/' + file)
