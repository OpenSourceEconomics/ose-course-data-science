import numpy as np

# import pandas as pd

# TODO: Reactivate
# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import LeaveOneOut
# from sklearn.model_selection import cross_val_score

# create two dataframes on either side of the cutoff alligned with your code
# df = pd.read_stata('data/individ_final.dta')
# bins = np.linspace(-1, 1, num=401)
# labels =  np.linspace(0, 399, num=400)
# df['bin'] = pd.cut(df.difshare, bins, labels = labels,include_lowest = True)
# df['bin'] = pd.to_numeric(df['bin'])
# df = df.sort_values(by='bin')
# df = df[(df['outcomenext'] == 1) | (df['outcomenext'] == 0) ]
# df_left = df[(df["difshare"] >= -0.5) & (df["difshare"] < 0)]
# df_right = df[(df["difshare"] > 0) & (df["difshare"] <= 0.5)]
# create necessary arrays
position = np.linspace(0, 99, num=100).astype(int)
width_left = np.linspace(199, 100, num=100).astype(int)
error_mean_left = np.linspace(0, 0, num=100)
width_right = np.linspace(200, 299, num=100).astype(int)
error_mean_right = np.linspace(0, 0, num=100)
# run cross-validation on each side
for h, p in zip(width_left, position):
    pass
    # TODO: Reactivate
    # reg = df_left[(df_left["bin"] >= h)]
    # X = reg["difshare"].values.reshape(-1, 1)
    # y = reg["outcomenext"].values.reshape(-1, 1)
    # loocv = LeaveOneOut()
    # model = LinearRegression()
    # results = cross_val_score(model, X, y, scoring="neg_mean_squared_error", cv=loocv)
    # error_mean_left[p] = results.mean() * (-1)
for h, p in zip(width_right, position):
    pass
    # TODO: reactivate
    # reg = df_right[(df_right["bin"] <= h)]
    # X = reg["difshare"].values.reshape(-1, 1)
    # y = reg["outcomenext"].values.reshape(-1, 1)
    # loocv = LeaveOneOut()
    # model = LinearRegression()
    # results = cross_val_score(model, X, y, scoring="neg_mean_squared_error", cv=loocv)
    # error_mean_right[p] = results.mean() * (-1)
