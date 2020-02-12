#!/usr/bin/env python
"""Run slide.

This script allows to run the lecture slides. One can either run all slides at once or just a
single lecture. It is enough to provide a substring for the name.

Examples
--------

>> run-slide             Run all slides.

>> run-slide -n 01_      Run slide 01_introduction.
"""
import os

from auxiliary import parse_arguments
from auxiliary import compile_single
from auxiliary import LECTURES_ROOT

if __name__ == "__main__":

    request = parse_arguments('Create lecture slides')

    os.chdir(LECTURES_ROOT)

    for dirname in request:
        os.chdir(dirname)
        if os.path.exists('slides'):
            compile_single('slides', "slides")
        os.chdir('../')