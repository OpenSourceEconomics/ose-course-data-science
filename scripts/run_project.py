#!/usr/bin/env python
"""Run project.

This script allows to run the whole project. It simply calls the other scripts tailored to run
the slides, notebooks, and problem sets.

Examples
--------

>> run-project           Run all slides, notebooks, and problems sets.

"""
import subprocess as sp

[sp.check_call(f"run-{task}") for task in ["slide", "notebook", "problem"]]
