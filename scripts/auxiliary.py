"""This module contains some auxiliary functions shared across the utility scripts."""
import argparse
import difflib
import glob
import os

PROBLEM_SETS_ROOT = os.environ["PROJECT_ROOT"] + "/problem-sets"
HANDOUTS_ROOT = os.environ["PROJECT_ROOT"] + "/handouts"
LECTURES_ROOT = os.environ["PROJECT_ROOT"] + "/lectures"
DATASETS_ROOT = os.environ["PROJECT_ROOT"] + "/datasets"
SPECIALS_ROOT = os.environ["PROJECT_ROOT"] + "/specials"


def parse_arguments(description):
    """This function parses the arguments for the scripts."""
    parser = argparse.ArgumentParser(description=description)

    if "problem set" in description:
        task, task_dir = "problem set", PROBLEM_SETS_ROOT
    elif "lecture" in description or "notebook" in description:
        task, task_dir = "lecture", LECTURES_ROOT
    elif "handout" in description:
        task, task_dir = "handout", HANDOUTS_ROOT
    elif "special" in description:
        task, task_dir = "special", SPECIALS_ROOT
    else:
        raise NotImplementedError

    parser.add_argument(
        "-n", "--name", type=str, help=f"name of {task}", default="all", dest="name"
    )

    args = parser.parse_args()

    # We can either request a single lecture or just act on all of them. We use string matching
    # to ease workflow.
    if args.name != "all":
        request = difflib.get_close_matches(args.name, get_list_tasks(task_dir), n=1, cutoff=0.1)
        if not request:
            raise AssertionError(f"unable to match {task}")
    else:
        request = get_list_tasks(task_dir)

    request.sort()

    return request


def get_list_tasks(task_dir):
    cwd = os.getcwd()

    os.chdir(task_dir)
    lectures = [name for name in glob.glob("*-*")]
    os.chdir(cwd)

    return lectures
