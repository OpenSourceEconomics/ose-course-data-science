# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
# -- Project information -----------------------------------------------------

project = "OSE data science"
copyright = "2020, Prof. Dr. Philipp Eisenhauer"
author = "Prof. Dr. Philipp Eisenhauer"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.mathjax",
    "nbsphinx",
    "sphinx.ext.extlinks",
    "sphinx_rtd_theme",
    "sphinx.ext.doctest",
]
# bibtex_bibfiles = ["refs.bib"]
master_doc = "index"
# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for nbsphinx  ----------------------------------------
nbsphinx_execute = "auto"

nbsphinx_prolog = r"""
{% set docname = env.doc2path(env.docname, base=None) %}
.. |binder| image:: https://mybinder.org/badge_logo.svg
    :target: https://mybinder.org/v2/gh/HumanCapitalAnalysis/ose-data-science/master?filepath={{ docname|e }}

.. only:: html

    .. nbinfo::
        Download the notebook :download:`here <https://nbviewer.jupyter.org/github/HumanCapitalAnalysis/ose-data-science/blob/master/{{ docname }}>`!
        Interactive online version: |binder|

"""
# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
