#!/usr/bin/env python
"""Run slides.

This script allows to run the lecture slides. One can either run all slides at once or just a
single lecture. It is enough to provide a substring for the name.

Examples
--------

>> run-slide             Run all slides.

>> run-slide -n 01_      Run slide 01_introduction.
"""
import subprocess
import shutil
import os

from auxiliary import parse_arguments
from auxiliary import LECTURES_ROOT


def compile_single(dirname):
    """Compile a single lecture."""
    cwd = os.getcwd()
    os.chdir(dirname)
    for task in ['pdflatex', 'bibtex', 'pdflatex', 'pdflatex']:
        subprocess.check_call(task + ' main', shell=True)
    shutil.copy('main.pdf', cwd + '/slides.pdf')
    os.chdir(cwd)


if __name__ == "__main__":

    request = parse_arguments('Create lecture slides')

    os.chdir(LECTURES_ROOT)

    for dirname in request:
        os.chdir(dirname)
        if os.path.exists('slides'):
            compile_single('slides')
        os.chdir('../')