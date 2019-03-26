#!/usr/bin/env python
""" This script updates all files, including the submodules.
"""

# standard library
import subprocess

subprocess.check_call(['git', 'pull'])

subprocess.check_call(['git', 'submodule', 'update', '--recursive', '--remote'])
