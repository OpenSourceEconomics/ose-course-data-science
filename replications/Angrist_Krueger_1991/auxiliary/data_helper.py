import numpy as np
import pandas as pd
import patsy

FILE_PATH_CENSUS80_EXTRACT = "data/QOB.txt"
FILE_PATH_FULL_CENSUS7080 = "data/NEW7080.dta"


def get_df_census80():

    cols = [0, 1, 3, 4, 5, 8, 9, 10, 11, 12, 15, 16, 17, 18, 19, 20, 23, 24, 26]

    cols_names = [
        "AGE",
        "AGEQ",
        "EDUC",
        "ENOCENT",
        "ESOCENT",
        "LWKLYWGE",
        "MARRIED",
        "MIDATL",
        "MT",
        "NEWENG",
        "CENSUS",
        "STATE",
        "QOB",
        "RACE",
        "SMSA",
        "SOATL",
        "WNOCENT",
        "WSOCENT",
        "YOB",
    ]

    df = pd.read_csv(FILE_PATH_CENSUS80_EXTRACT, sep=" ", usecols=cols, names=cols_names)

    # correct AGEQ
    df.loc[df["CENSUS"] == 80, "AGEQ"] = df["AGEQ"] - 1900

    return df


def get_df_census70():

    cols = [
        "v1",
        "v2",
        "v4",
        "v5",
        "v6",
        "v9",
        "v10",
        "v11",
        "v12",
        "v13",
        "v16",
        "v17",
        "v18",
        "v19",
        "v20",
        "v21",
        "v24",
        "v25",
        "v27",
    ]

    cols_names = [
        "AGE",
        "AGEQ",
        "EDUC",
        "ENOCENT",
        "ESOCENT",
        "LWKLYWGE",
        "MARRIED",
        "MIDATL",
        "MT",
        "NEWENG",
        "CENSUS",
        "STATE",
        "QOB",
        "RACE",
        "SMSA",
        "SOATL",
        "WNOCENT",
        "WSOCENT",
        "YOB",
    ]

    df = pd.read_stata(FILE_PATH_FULL_CENSUS7080, columns=cols)

    df = df.rename(columns=dict(zip(cols, cols_names)))

    return df.loc[df["CENSUS"] == 70]


def get_df_census70_census_80():

    cols = [
        "v1",
        "v2",
        "v4",
        "v5",
        "v6",
        "v9",
        "v10",
        "v11",
        "v12",
        "v13",
        "v16",
        "v17",
        "v18",
        "v19",
        "v20",
        "v21",
        "v24",
        "v25",
        "v27",
    ]

    cols_names = [
        "AGE",
        "AGEQ",
        "EDUC",
        "ENOCENT",
        "ESOCENT",
        "LWKLYWGE",
        "MARRIED",
        "MIDATL",
        "MT",
        "NEWENG",
        "CENSUS",
        "STATE",
        "QOB",
        "RACE",
        "SMSA",
        "SOATL",
        "WNOCENT",
        "WSOCENT",
        "YOB",
    ]

    df = pd.read_stata(FILE_PATH_FULL_CENSUS7080, columns=cols)

    df = df.rename(columns=dict(zip(cols, cols_names)))

    return df


def prepare_census_data(
    df,
    const=True,
    qob=True,
    yob=True,
    age=True,
    state_of_birth=False,
    qob_x_yob=False,
    qob_x_state=False,
):

    if const:
        df = add_constant(df)
    if qob or qob_x_yob or qob_x_state:
        df = add_quarter_of_birth_dummies(df)
    if yob or qob_x_yob:
        df = add_year_of_birth_dummies(df)
    if age:
        df = add_age_squared(df)
    if state_of_birth or qob_x_state:
        df = add_state_of_birth_dummies(df)
    if qob_x_yob:
        df = add_qob_yob_interactions(df)
    if qob_x_state:
        df = add_qob_state_interactions(df, qob_x_state)

    return df


def add_constant(df):
    df["CONST"] = 1
    df["CONST"] = df["CONST"].astype(np.uint8)
    return df


def get_constant_name():
    return ["CONST"]


def add_quarter_of_birth_dummies(df):
    return pd.concat((df, pd.get_dummies(df["QOB"], prefix="DUMMY_QOB")), axis=1)


def get_quarter_of_birth_dummy_names(start=1, end=3):
    return [f"DUMMY_QOB_{j}" for j in range(start, end + 1)]


def add_year_of_birth_dummies(df):
    return pd.concat((df, pd.get_dummies(df["YOB"] % 10, prefix="DUMMY_YOB")), axis=1)


def get_year_of_birth_dummy_names(start=0, end=8):
    return [f"DUMMY_YOB_{i}" for i in range(start, end + 1)]


def add_age_squared(df):

    df["AGESQ"] = df["AGEQ"].pow(2)
    return df


def get_age_control_names(ageq=True, agesq=True):

    lst = []
    if ageq:
        lst.append("AGEQ")
    if agesq:
        lst.append("AGESQ")

    return lst


def add_state_of_birth_dummies(df):
    return pd.concat((df, pd.get_dummies(df["STATE"], prefix="DUMMY_STATE")), axis=1)


def get_state_of_birth_dummy_names(state_list):
    return [f"DUMMY_STATE_{i}" for i in state_list]


def get_state_list(df, rm_state=1):

    state_list = set(df["STATE"])
    state_list.remove(rm_state)
    return state_list


def add_qob_yob_interactions(df):

    interact_qob_yob = patsy.dmatrix(
        " + ".join(get_qob_yob_interaction_names()), df, return_type="dataframe"
    )
    interact_qob_yob.drop("Intercept", axis=1, inplace=True)

    return pd.concat((df, interact_qob_yob.astype(np.uint8)), axis=1)


def get_qob_yob_interaction_names(qob_start=1, qob_end=3, yob_start=0, yob_end=9):
    return [
        f"DUMMY_YOB_{i}:DUMMY_QOB_{j}"
        for j in range(qob_start, qob_end + 1)
        for i in range(yob_start, yob_end + 1)
    ]


def add_qob_state_interactions(df, state_list):

    interact_qob_state = patsy.dmatrix(
        " + ".join(get_qob_state_of_birth_interaction_names(state_list)),
        df,
        return_type="dataframe",
    )
    interact_qob_state.drop("Intercept", axis=1, inplace=True)

    return pd.concat((df, interact_qob_state.astype(np.uint8)), axis=1)


def get_qob_state_of_birth_interaction_names(state_list):
    return [f"DUMMY_STATE_{i}:DUMMY_QOB_{j}" for j in range(1, 4) for i in state_list]


def get_further_exogenous_regressors(race=True, smsa=True, married=True):

    lst = []
    if race:
        lst.append("RACE")
    if smsa:
        lst.append("SMSA")
    if married:
        lst.append("MARRIED")

    return lst


def get_region_of_residence_dummies():
    return ["NEWENG", "MIDATL", "ENOCENT", "WNOCENT", "SOATL", "ESOCENT", "WSOCENT", "MT"]


def get_education_name():
    return ["EDUC"]


def get_log_weekly_wage_name():
    return ["LWKLYWGE"]


def add_education_dummies(df):

    # dummy variable high school degree (12 or more years of education)
    df["DUMMY_HIGH_SCHOOL"] = [1 if x >= 12 else 0 for x in df["EDUC"]]

    # dummy variable college degree (16 or more years of education)
    df["DUMMY_COLLEGE"] = [1 if x >= 16 else 0 for x in df["EDUC"]]

    # dummy variable master's degree (18 or more years of education)
    df["DUMMY_MASTER"] = [1 if x >= 18 else 0 for x in df["EDUC"]]

    # dummy variable doctoral degree (20 or more years of education)
    df["DUMMY_DOCTOR"] = [1 if x >= 20 else 0 for x in df["EDUC"]]

    return df


def add_detrended_educational_variables(df, educ_vars=("EDUC")):

    for ev in educ_vars:

        mean_ev = df.groupby(["YOB", "QOB"])[ev].mean().to_frame()
        mean_ev["MV_AVG"] = two_sided_moving_average(mean_ev.values)

        for yob in set(df["YOB"]):
            for qob in set(df["QOB"]):
                df.loc[(df["YOB"] == yob) & (df["QOB"] == qob), f"MV_AVG_{ev}"] = mean_ev.loc[
                    (yob, qob), "MV_AVG"
                ]

        df[f"DTRND_{ev}"] = df[ev] - df[f"MV_AVG_{ev}"]

    return df


def two_sided_moving_average(x):

    ma = np.full_like(x, np.nan)

    for i in range(2, len(x) - 2):
        ma[i] = (x[i - 2] + x[i - 1] + x[i + 1] + x[i + 2]) / 4

    return ma
