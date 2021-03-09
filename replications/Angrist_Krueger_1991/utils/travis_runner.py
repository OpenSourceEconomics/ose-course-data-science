#!/usr/bin/env python
"""This script manages all tasks for the TRAVIS build server."""
import glob
import subprocess as sp

if __name__ == "__main__":

    for notebook in glob.glob("*.ipynb"):
        cmd = f" jupyter nbconvert --execute {notebook}  --ExecutePreprocessor.timeout=-1"
        sp.check_call(cmd, shell=True)
