#!/usr/bin/env python
"""This module compiles the lecture notes."""
import subprocess
import shutil

for task in ['pdflatex', 'bibtex', 'pdflatex', 'pdflatex']:
    subprocess.check_call(task + ' main', shell=True)
shutil.copy('main.pdf', '../00_course_outline.pdf')
