#!/usr/bin/env python
"""Run problem set.

This script allows to run the handouts. One can either run all problem sets at once or just a
single one. It is enough to provide a substring for the name.

Examples
--------

>> run-handout             Run all handouts set.

>> run-handout -n 01      Run handout 01-causal-graphs.
"""
import os

from auxiliary import parse_arguments
from auxiliary import compile_single
from auxiliary import HANDOUTS_ROOT


if __name__ == "__main__":

    request = parse_arguments("Create handout set")

    os.chdir(HANDOUTS_ROOT)

    for dirname in request:
        os.chdir(dirname)
        if os.path.exists("sources"):
            compile_single("sources", "handouts")
        os.chdir("../")
