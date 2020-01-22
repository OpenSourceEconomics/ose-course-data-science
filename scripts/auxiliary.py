"""This module contains some auxiliary functions shared across the utility scripts."""
import argparse
import difflib
import glob
import os

LECTURES_ROOT = os.environ['PROJECT_ROOT'] + '/lectures'


def parse_arguments(description):
    """This function parses the arguments for the scripts."""
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-n", "--name", type=str, help="name of lecture", default='all',
                        dest="name")

    args = parser.parse_args()

    # We can either request a single lecture or just act on all of them. We use string matching
    # to ease workflow.
    if args.name != "all":
        request = difflib.get_close_matches(args.name, get_list_of_lectures(), n=1, cutoff=0.1)
        if not request:
            raise AssertionError("unable to match lecture")
    else:
        request = get_list_of_lectures()

    return request


def get_list_of_lectures():
    cwd = os.getcwd()

    os.chdir(LECTURES_ROOT)
    lectures = [name for name in glob.glob("*_*")]
    os.chdir(cwd)

    return lectures
