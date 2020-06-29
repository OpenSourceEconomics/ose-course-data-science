#!/usr/bin/env python
"""Run project.

This script allows to run the whole project. It simply calls the other scripts tailored to run
the slides, notebooks, problem sets, handouts, and data.

Examples
--------

>> run-project           Run all slides, notebooks, problems sets, handouts, data, and specials.

"""
import subprocess as sp

tasks = ["slide", "notebook", "problem", "dataset", "special"]
[sp.check_call(f"run-{task}") for task in tasks]
