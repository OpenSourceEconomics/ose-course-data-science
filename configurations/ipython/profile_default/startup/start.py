from IPython import get_ipython
import pandas as pd

ipython = get_ipython()

ipython.magic('load_ext autoreload')
ipython.magic('autoreload 2')

pd.options.mode.chained_assignment = None
