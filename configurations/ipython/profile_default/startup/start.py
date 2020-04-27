# The basic idea is to NOT have any regular package imports here.
# This just confuses students.
from IPython.core.display import HTML
from IPython import get_ipython

ipython = get_ipython()

ipython.magic('matplotlib inline')
ipython.magic('load_ext autoreload')
ipython.magic('autoreload 2')

