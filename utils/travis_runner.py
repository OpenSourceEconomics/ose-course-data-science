#!/usr/bin/env python
"""This script manages all tasks for the travis build server."""
import glob
import os

from execute_all_notebooks import run_notebook

if __name__ == '__main__':

    # We want to ensure a build of all notebooks at all times.
    os.chdir('lectures')
    for dirname in glob.glob('0*_*'):
        os.chdir(dirname)
        run_notebook()
        os.chdir('../')
    os.chdir('../')

