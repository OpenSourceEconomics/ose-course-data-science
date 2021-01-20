import numpy as np
import pandas as pd


def get_sample(scale):
    """This function simulates a sample with different levels of interclass correlation."""
    columns = ["Y", "G", "E"]
    index = pd.Index(range(500), name="Identifier")
    df = pd.DataFrame(columns=columns, index=index)

    # We now construct a sample with a variance decomposition
    # motivated by the random effects model.
    i = 0
    for g in range(10):
        nu = np.random.normal(scale=scale)
        for n in range(50):
            eta = np.random.normal()
            e = nu + eta

            y = g + e
            df.loc[i, :] = [y, g, e]

            i += 1

    df = df.astype(np.float)

    return df
