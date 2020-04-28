import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import LeaveOneOut
from sklearn.model_selection import cross_val_score

# create two dataframes on either side of the cutoff alligned with your code
inf_left = inf[(inf["difshare"] >= -0.5) & (inf["difshare"] < 0)]
inf_right = inf[(inf["difshare"] > 0) & (inf["difshare"] <= 0.5)]
# create necessary arrays
position = np.linspace(0, 99, num=100).astype(int)
width_left = np.linspace(199, 100, num=100).astype(int)
error_mean_left = np.linspace(0, 0, num=100)
width_right = np.linspace(200, 299, num=100).astype(int)
error_mean_right = np.linspace(0, 0, num=100)
# run cross-validation on each side
for h, p in zip(width_left, position):
    infreg = inf_left[(inf_left["bin"] >= h)]
    X = infreg["difshare"].values.reshape(-1, 1)
    y = infreg["outcomenext"].values.reshape(-1, 1)
    loocv = LeaveOneOut()
    model = LinearRegression()
    results = cross_val_score(model, X, y, scoring="neg_mean_squared_error", cv=loocv)
    error_mean_left[p] = results.mean() * (-1)
for h, p in zip(width_right, position):
    infreg = inf_right[(inf_right["bin"] <= h)]
    X = infreg["difshare"].values.reshape(-1, 1)
    y = infreg["outcomenext"].values.reshape(-1, 1)
    loocv = LeaveOneOut()
    model = LinearRegression()
    results = cross_val_score(model, X, y, scoring="neg_mean_squared_error", cv=loocv)
    error_mean_right[p] = results.mean() * (-1)
