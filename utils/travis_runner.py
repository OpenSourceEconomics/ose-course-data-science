#!/usr/bin/env python
"""This script manages all tasks for the travis build server."""
import subprocess as sp

if __name__ == '__main__':

    # We want to make sure all notebooks are run.
    cmd = 'python utils/execute_all_notebooks.py'
    sp.check_call(cmd, shell=True)
