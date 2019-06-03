#!/usr/bin/env python

import os
import subprocess
import shutil

def compile_single():
    """Compile a single lecture."""
    for task in ['pdflatex', 'bibtex', 'pdflatex', 'pdflatex']:
        subprocess.check_call(task + ' main', shell=True)


os.chdir('slides')
compile_single()
shutil.copy('main.pdf', '../slides.pdf')