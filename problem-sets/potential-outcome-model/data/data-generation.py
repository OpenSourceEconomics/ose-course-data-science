import pandas as pd
import numpy as np
import scipy.stats

np.random.seed(123)

# clean the initial data set
# "ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NHIS/2018/personsxcsv.zip"
df = pd.read_csv("personsx.csv")
pd.options.display.float_format = "{:,.0f}".format

df = df[["SEX", "AGE_P", "EDUC1", "WRKHRS2", "ERNYR_P", "PHOSPYR2", "PHSTAT"]]
df = df.dropna().reset_index(drop=True)
df = df.drop(df[(df.EDUC1 > 95) & (df.EDUC1 < 100)].index)
df = df.drop(df[(df.ERNYR_P > 95) & (df.ERNYR_P < 100)].index)
df = df.drop(df[(df.PHOSPYR2 > 2)].index)
df = df.drop(df[(df.PHSTAT > 5)].index)
df.loc[(df.SEX == 1), "sex"] = "male"
df.loc[(df.SEX == 2), "sex"] = "female"
df["age"] = df["AGE_P"]
df.loc[(df.EDUC1 == 0), "education"] = "never attended"
df.loc[(df.EDUC1 < 15) & (df.EDUC1 > 0), "education"] = "high school"
df.loc[(df.EDUC1 < 19) & (df.EDUC1 > 14), "education"] = "bachelor"
df.loc[(df.EDUC1 < 20) & (df.EDUC1 > 18), "education"] = "master"
df.loc[(df.EDUC1 < 22) & (df.EDUC1 > 19), "education"] = "PhD"
df["hours"] = df["WRKHRS2"]
df.loc[(df.ERNYR_P < 11) & (df.ERNYR_P > 7), "earnings"] = "middle"
df.loc[(df.ERNYR_P < 8), "earnings"] = "low"
df.loc[(df.ERNYR_P > 10), "earnings"] = "high"
df.loc[(df.PHOSPYR2 == 1), "hospitalized"] = 1
df.loc[(df.PHOSPYR2 == 2), "hospitalized"] = 0
df.loc[(df.PHSTAT == 1), "health"] = 5
df.loc[(df.PHSTAT == 2), "health"] = 4
df.loc[(df.PHSTAT == 3), "health"] = 3
df.loc[(df.PHSTAT == 4), "health"] = 2
df.loc[(df.PHSTAT == 5), "health"] = 1
df.drop(df.iloc[:, 0:7], inplace=True, axis=1)
df.reset_index(drop=True)

df.to_excel("nhis-initial.xls")

# Adjust the data set for the POM framework
is_treated = df["hospitalized"] == 1

df["Y"] = df["health"]
df["Y_0"] = df.loc[~is_treated, "health"]
df["Y_1"] = df.loc[is_treated, "health"]

df["D"] = np.nan
df.loc[~is_treated, "D"] = 0
df.loc[is_treated, "D"] = 1

# simulate the second data set
lower = 1
upper = 5
mu01 = 4.9
mu10 = 3.9
sigma = 0.1
N01 = df["Y_1"].isna().sum()
N10 = df["Y_0"].isna().sum()
pd.options.display.float_format = "{:,.f}".format
df.loc[df["D"] == 0, "Y_1"] = scipy.stats.truncnorm.rvs(
    (lower - mu01) / sigma, (upper - mu01) / sigma, loc=mu01, scale=sigma, size=N01
)
df.loc[df["D"] == 1, "Y_0"] = scipy.stats.truncnorm.rvs(
    (lower - mu10) / sigma, (upper - mu10) / sigma, loc=mu10, scale=sigma, size=N10
)

E_Y1_D1 = df.loc[df["D"] == 1, "Y_1"].mean()
E_Y1_D0 = df.loc[df["D"] == 0, "Y_1"].mean()
E_Y0_D1 = df.loc[df["D"] == 1, "Y_0"].mean()
E_Y0_D0 = df.loc[df["D"] == 0, "Y_0"].mean()
table = pd.DataFrame(
    {
        "Group": ["Treatment group(D = 1)", "Control group(D = 0)"],
        "E[Y_1|.]": [E_Y1_D1, E_Y1_D0],
        "E[Y_0|.]": [E_Y0_D1, E_Y0_D0],
    }
)

df.to_excel("nhis-simulated.xls")
