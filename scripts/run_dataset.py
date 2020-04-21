#!/usr/bin/env python
import os

import pandas as pd
from auxiliary import DATASETS_ROOT

def from_dta_to_csv(textbook, dataset):
    """This function transfers the dataset from *.dta to a csv file."""
    substring = textbook + '/' + dataset
    df = pd.read_stata('sources/' + substring + '.dta')
    df.to_csv('processed/' + substring + '.csv', index=False)
    return df


os.chdir(DATASETS_ROOT)

# This is a  cross-sectional dataset on low birth weight from the Wooldrige textbook.
df = from_dta_to_csv('wooldrige', 'lowbrth')


## Lee (2008), regression discontinutiy design, https://rdrr.io/cran/rddtools/man/house.html, required transfered the
# `rda` file manually to `csv`.
df = pd.read_csv('sources/msc/house.csv', index_col=0)

# We want more interpretable columnn names.
df.rename(columns={'x': 'vote_last', 'y': 'vote_next'}, inplace=True)
df.to_csv('processed/msc/house.csv', index=False)

## Krueger (1999), STAR experiment, clustering on group level. There was a lot of pre-processig required using the replication material
# from the MHE website.
df = from_dta_to_csv('angrist_pischke', 'webstar')
df.head()



## nswre74.dta https://users.nber.org/~rdehejia/nswdata.html
df = from_dta_to_csv('angrist_pischke', 'nswre74')

## Morgan & Winship # These are the datasets for the matching illustration in Chapter 5.
for num in range(1, 11):
    fname = 'mw_cath{}'.format(num)
    df = from_dta_to_csv('morgan_winship', fname)

# This is the data for the re-analysis of the LaLonde Paper as (temporarily published on the Dehaja website)
from_dta_to_csv('dehejia_waba', 'nsw')
for source in ['psid', 'cps']:
    for num in range(1, 4):
        fname = f'{source}_controls{num}'
        from_dta_to_csv('dehejia_waba', fname)