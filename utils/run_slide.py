#!/usr/bin/env python
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