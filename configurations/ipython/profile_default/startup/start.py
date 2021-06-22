# The basic idea is to NOT have any regular package imports here.
# This just confuses students.
from IPython import get_ipython

ipython = get_ipython()

ipython.magic("load_ext autoreload")
ipython.magic("load_ext lab_black")

ipython.magic("matplotlib inline")
ipython.magic("autoreload 2")
