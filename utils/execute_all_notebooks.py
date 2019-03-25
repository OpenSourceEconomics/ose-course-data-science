#!/usr/bin/env python
"""This module executes all notebooks. It serves the main purpose to ensure that all can be
executed and work proper independently."""
import subprocess as sp
import glob


def run_notebook():
    for notebook in sorted(glob.glob('*.ipynb')):
        cmd = ' jupyter nbconvert --execute {}  --ExecutePreprocessor.timeout=-1'.format(notebook)
        sp.check_call(cmd, shell=True)


if __name__ == '__main__':

    run_notebook()

