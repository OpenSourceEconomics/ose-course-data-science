import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf


def get_quick_sample(num_samples):

    df = pd.DataFrame(columns=["Y", "D", "X"])

    for i in range(num_samples):
        x = np.random.normal()
        d = (x + np.random.normal()) > 0
        y = d + x + np.random.normal()
        df.loc[i] = [y, d, x]

    df = df.astype({"D": int})
    return df


def plot_freedman_exercise(df):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.hist(df["F-statistic"])
    ax1.set_title("Prob(F-statistic)")

    ax2.hist(df["Regressors"])
    ax2.set_title("Number of regressors")


def run_freedman_exercise():

    columns = ["Y"]
    for i in range(50):
        columns.append(f"X{i}")
    df = pd.DataFrame(np.random.normal(size=(100, 51)), columns=columns)

    formula = "Y ~ " + " + ".join(columns[1:]) + "- 1"
    rslt = smf.ols(formula=formula, data=df).fit()

    final_covariates = list()
    for label in rslt.params.keys():
        if rslt.pvalues[label] > 0.25:
            continue
        final_covariates.append(label)

    formula = "Y ~ " + " + ".join(final_covariates)
    rslt = smf.ols(formula=formula, data=df).fit()
    return rslt


def get_correlation(x, y, df):

    stat = df[x].corr(df[y])

    if pd.isnull(stat):
        return 0.0
    else:
        return stat


def get_sample_bias_illustration(sample, num_agents=1000):
    columns = ["Y", "D", "Y_1", "Y_0", "V_1", "V_0", "C"]
    df = pd.DataFrame(columns=columns, dtype=np.float)

    for i in range(num_agents):
        group = np.random.choice(range(2))

        if sample == 0:
            if group == 0:
                attr_ = 20, 10, 0, 5, 20, 1, 0
            elif group == 1:
                attr_ = 20, 0, 0, -5, 0, 0, -5
            else:
                raise NotImplementedError

        elif sample == 1:
            if group == 0:
                attr_ = 20, 10, 2.5, 0, 20, 1, 2.5
            elif group == 1:
                attr_ = 15, 10, -2.5, 0, 10, 0, 0
            else:
                raise NotImplementedError

        elif sample == 2:
            if group == 0:
                attr_ = 25, 5, 5, -2.5, 25, 1, 5
            elif group == 1:
                attr_ = 15, 10, -5, 2.5, 10, 0, 2.5
            else:
                raise NotImplementedError

        y_1, y_0, v_1, v_0, y, d, c = attr_

        df.loc[i] = [y, d, y_1, y_0, v_1, v_0, c]

    # We set all but the treatment dummy to float values.
    df = df.astype(np.float)
    df = df.astype({"D": np.int})

    return df


def get_sample_regression_adjustment(sample, num_agents=1000, seed=123):
    """There exist six different groups in the population with equal shares"""
    np.random.seed(seed)
    columns = ["Y", "D", "X", "Y_1", "Y_0", "V_1", "V_0"]
    df = pd.DataFrame(columns=columns)

    for i in range(num_agents):

        group = np.random.choice(range(6))

        if sample == 0:

            # This is a direct copy from the top panel in Table 6.4
            if group in [0, 1]:
                attr_ = (
                    20,
                    10,
                    2.5,
                    2.5,
                    20,
                    1,
                    1,
                )
            elif group == 2:
                attr_ = 15, 5, -2.5, -2.5, 15, 1, 0
            elif group == 3:
                attr_ = 20, 10, 2.5, 2.5, 10, 0, 1
            elif group == 4:
                attr_ = 15, 5, -2.5, -2.5, 5, 0, 0
            elif group == 5:
                attr_ = 15, 5, -2.5, -2.5, 5, 0, 0
            else:
                raise NotImplementedError
        elif sample == 1:

            if group in [0, 1]:
                attr_ = 20, 10, 2.83, 2.5, 20, 1, 1
            elif group == 2:
                attr_ = 15, 5, -2.17, -2.5, 15, 1, 0
            elif group == 3:
                attr_ = 18, 10, 0.83, 2.5, 10, 0, 1
            elif group == 4:
                attr_ = 15, 5, -2.17, -2.5, 5, 0, 0
            elif group == 5:
                attr_ = 15, 5, -2.17, -2.5, 5, 0, 0
        else:
            raise NotImplementedError

        y_1, y_0, v_1, v_0, y, d, x = attr_

        df.loc[i] = [y, d, x, y_1, y_0, v_1, v_0]

    df = df.astype({"D": np.int})

    return df


def get_sample_demonstration_1(num_agents):
    data = np.tile(np.nan, (num_agents, 5))
    for i in range(num_agents):
        u = np.random.uniform()

        if 0.00 <= u < 0.36:
            s, d = 1, 0
        elif 0.36 <= u < 0.48:
            s, d = 2, 0
        elif 0.48 <= u < 0.60:
            s, d = 3, 0
        elif 0.60 <= u < 0.68:
            s, d = 1, 1
        elif 0.68 <= u < 0.80:
            s, d = 2, 1
        else:
            s, d = 3, 1

        # get potential outcomes
        def get_potential_outcomes(s):
            if s == 1:
                y_1, y_0 = 4, 2
            elif s == 2:
                y_1, y_0 = 8, 6
            elif s == 3:
                y_1, y_0 = 14, 10
            else:
                raise AssertionError

            # We want some randomness
            y_1 += np.random.normal()
            y_0 += np.random.normal()

            return y_1, y_0

        y_1, y_0 = get_potential_outcomes(s)
        y = d * y_1 + (1 - d) * y_0

        data[i, :] = y, d, s, y_1, y_0

    df = pd.DataFrame(data, columns=["Y", "D", "S", "Y_1", "Y_0"])
    df = df.astype({"D": np.int, "S": np.int})

    return df


def plot_conditional_expectation_demonstration_1(df):

    fig, ax = plt.subplots(1, 1)
    rslt = df[df["D"] == 1].groupby("S")["Y"].mean().to_dict()
    x, y = rslt.keys(), rslt.values()
    ax.plot(list(x), list(y), label="Treated")

    rslt = df[df["D"] == 0].groupby("S")["Y"].mean().to_dict()
    x, y = rslt.keys(), rslt.values()
    ax.plot(list(x), list(y), label="Control")

    # We study the treatment effect heterogeneity.
    plt.plot((1, 1), (2, 4), "k-")
    ax.text(0.95, 6, r"$\Delta Y_{S = 1}$", fontsize=15)
    plt.plot((2, 2), (6, 8), "k-")
    ax.text(1.95, 10, r"$\Delta Y_{S = 2}$", fontsize=15)
    plt.plot((3, 3), (10, 14), "k-")
    ax.text(2.95, 15, r"$\Delta Y_{S = 3}$", fontsize=15)

    ax.set_title("Conditional Expectations")
    ax.set_xticks([1, 2, 3])
    ax.set_ylim([0, 16])

    ax.legend()


def get_predictions_demonstration_1(df):

    df_extend = df.join(pd.get_dummies(df["S"], prefix="S"))
    df_extend["predict_1"] = smf.ols(formula="Y ~ D + S", data=df_extend).fit().predict()
    df_extend["predict_2"] = smf.ols(formula="Y ~ D + S_2 + S_3", data=df_extend).fit().predict()
    df_extend["predict_3"] = (
        smf.ols(formula="Y ~ D + S_2 + S_3 + S_2 * D + S_3 * D", data=df_extend).fit().predict()
    )

    rslt = dict()
    rslt["observed"] = dict()
    rslt["predict_1"] = dict()
    rslt["predict_2"] = dict()
    rslt["predict_3"] = dict()

    for key_, d in [("treated", 1), ("control", 0)]:
        df_subset = df_extend[df_extend["D"] == d]

        # observed outcomes
        rslt["observed"][key_] = df_subset.groupby(["S"])["Y"].mean().to_dict()

        # predicted, model 1
        rslt["predict_1"][key_] = df_subset.groupby(["S"])["predict_1"].mean().to_dict()
        rslt["predict_2"][key_] = df_subset.groupby(["S"])["predict_2"].mean().to_dict()
        rslt["predict_3"][key_] = df_subset.groupby(["S"])["predict_3"].mean().to_dict()

    return rslt


def plot_predictions_demonstration_1(df):
    rslt = get_predictions_demonstration_1(df)

    y = np.array([1, 2, 3])
    fig, (ax1, ax2) = plt.subplots(1, 2)
    for label, ax in [("treated", ax1), ("control", ax2)]:

        ax.bar(y - 0.3, rslt["observed"][label].values(), width=0.2, label="actual")
        ax.bar(y - 0.1, rslt["predict_1"][label].values(), width=0.2, label="first")
        ax.bar(y + 0.1, rslt["predict_2"][label].values(), width=0.2, label="second")
        ax.bar(y + 0.3, rslt["predict_3"][label].values(), width=0.2, label="third")

        ax.set_title(label.title())
        ax.set_ylim([0, 22])
        ax.legend()


def plot_anscombe_dataset():
    df = sns.load_dataset("anscombe")

    sns.lmplot(
        x="x",
        y="y",
        col="dataset",
        hue="dataset",
        data=df,
        col_wrap=2,
        ci=None,
        palette="muted",
        height=4,
        scatter_kws={"s": 50, "alpha": 1},
    )


def get_anscombe_datasets():
    df = sns.load_dataset("anscombe")
    # This is an exmple of a list comprehension
    rslt = list()
    for numeral in ["I", "II", "III", "IV"]:
        rslt.append(df[df["dataset"] == numeral])
    return rslt
