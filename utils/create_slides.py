#!/usr/bin/env python

import subprocess
import argparse
import difflib
import shutil
import glob
import os

PROJECT_ROOT = os.environ['PROJECT_ROOT']


def compile_single(dirname):
    """Compile a single lecture."""
    cwd = os.getcwd()
    os.chdir(dirname)
    for task in ['pdflatex', 'bibtex', 'pdflatex', 'pdflatex']:
        subprocess.check_call(task + ' main', shell=True)
    shutil.copy('main.pdf', cwd + '/slides.pdf')
    os.chdir(cwd)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Create lecture slides")

    parser.add_argument("-n", "--name", type=str, help="name of lecture", default='all',
                        dest="name")

    args = parser.parse_args()

    os.chdir(PROJECT_ROOT + '/lectures')

    lecture_names = list()
    for dirname in glob.glob("*_*"):
        if not dirname[0].isdigit():
            continue
        lecture_names.append(dirname)

    # Depending on how the name attribute is set, we compile either all slides or just in a
    # selected directory.
    dirnames = lecture_names
    if args.name != "all":
        dirnames = difflib.get_close_matches(args.name, lecture_names, n=1, cutoff=0.0)

    for dirname in dirnames:
        os.chdir(dirname)
        if os.path.exists('slides'):
            compile_single('slides')
        os.chdir('../')