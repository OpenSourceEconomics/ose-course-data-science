#!/usr/bin/env python
import os
from itertools import product

import pandas as pd
from auxiliary import DATASETS_ROOT


def from_dta_to_csv(textbook, dataset):
    """This function transfers the dataset from *.dta to a csv file."""
    substring = textbook + "/" + dataset
    df = pd.read_stata("sources/" + substring + ".dta")
    df.to_csv("processed/" + substring + ".csv", index=False)
    return df


os.chdir(DATASETS_ROOT)

# This is a  cross-sectional dataset on low birth weight from the Wooldrige textbook.
df = from_dta_to_csv("wooldrige", "lowbrth")

# Lee (2008), regression discontinuity design, https://rdrr.io/cran/rddtools/man/house.html,
# required transferred the `rda` file manually to `csv`.
df = pd.read_csv("sources/msc/house.csv", index_col=0)

# We want more interpretable column names.
df.rename(columns={"x": "vote_last", "y": "vote_next"}, inplace=True)
df.to_csv("processed/msc/house.csv", index=False)

# Krueger (1999), STAR experiment, clustering on group level. There was a lot of pre-processing
# required using the replication material from the MHE website.
df = from_dta_to_csv("angrist_pischke", "webstar")
df.head()

# Morgan & Winship, these are the datasets for the matching illustration in Chapter 5.
for num in range(1, 11):
    fname = f"mw_cath{num}"
    df = from_dta_to_csv("morgan_winship", fname)

# All data related to LaLonde (1986) and Dehejia and Waba (1999) is available on the following
# NBER website: https://users.nber.org/~rdehejia/nswdata.html. The sample originally used by
# LaLonde is larger as it does not require information on earnings in 1974, while this is used
# as a pre-treatment variable in the follow-up work.
from_dta_to_csv("dehejia_waba", "nsw_lalonde")

from_dta_to_csv("dehejia_waba", "nsw_dehejia")
for source, num in product(["psid", "cps"], range(1, 4)):
    from_dta_to_csv("dehejia_waba", f"{source}_controls{num}")
