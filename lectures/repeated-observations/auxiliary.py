import matplotlib.pyplot as plt
from scipy.stats import logistic
import statsmodels.formula.api as smf

import pandas as pd
import numpy as np


def get_panel_estimates(estimator, df):
    assert estimator in ["naive", "diff"]

    subset = df.loc[(slice(None), 10), :]

    if estimator == "naive":
        rslt = smf.ols(formula="Y ~ D", data=subset).fit()
    elif estimator == "diff":
        subset.loc[(slice(None), slice(None)), "S"] = subset["Y"] - subset["Y_8"]
        rslt = smf.ols(formula="S ~ D ", data=subset).fit()

    return rslt


def get_propensity_score(selection, o, u, additional_effect, y0):

    if selection == "baseline":
        idx = -3.8 + o + u
    elif selection == "self-selection on gains":
        idx = -7.3 + o + u + 5 * additional_effect
    elif selection == "self-selection on pretest":
        idx = -3.8 + o + u + 0.05 * (y0[0] - 98)
    else:
        raise NotImplementedError

    return np.exp(idx) / (1 + np.exp(idx))


def get_sample_panel_demonstration(num_agents, selection, trajectory):
    assert trajectory in ["parallel", "divergent"]

    columns = ["Y", "D", "O", "X", "E", "U", "Y_1", "Y_0", "Y_8"]
    index = list()
    for i in range(num_agents):
        for j in [8, 9, 10]:
            index.append((i, j))
    index = pd.MultiIndex.from_tuples(index, names=("Identifier", "Grade"))
    df = pd.DataFrame(columns=columns, index=index)

    df.loc[(slice(None), 8), "D"] = 0

    for i in range(num_agents):

        o, u, x, e = get_covariates()

        # We first sample the outcomes in the control state.
        y0 = list()
        for level in [98, 99, 100]:
            rslt = level + o + u + x + e + np.random.normal(scale=np.sqrt(10))
            y0.append(rslt)

        # Sampling the effects of treatment
        baseline_effect = np.random.normal(loc=9, scale=1)
        additional_effect = np.random.normal(loc=0, scale=1)

        # The propensity score governs the attributes of selection. This is where the selection
        # on gains or the pretreatment variable is taking place.
        p = get_propensity_score(selection, o, u, additional_effect, y0)
        d = np.random.choice([1, 0], p=[p, 1 - p])

        # If the trajectories are diverging, we need to determine the shift here. This is a
        # violation of the common trend assumption. Students who select into public 
        # schools would have ahad a boost in achievement even if they had remained in public
        # schools, net of all other determinants of the potential outcome in the 
        # absence of treatment.
        if trajectory == "divergent" and d == 1:
            y0[-1] += 0.5
        elif trajectory == "divergent" and d == 0:
            y0[-1] -= 0.5

        # We are not ready to compute the treatment outcomes.
        y1 = list()

        rslt = np.nan
        y1.append(rslt)

        rslt = y0[1] + baseline_effect + additional_effect
        y1.append(rslt)

        rslt = y0[2] + (1 + baseline_effect) + additional_effect
        y1.append(rslt)

        # Housekeeping and the creation of the data set.
        df.loc[(i, slice(None)), "Y_8"] = y0[0]

        df.loc[(i, slice(None)), "D_ever"] = d
        df.loc[(i, [9, 10]), "D"] = d
        df.loc[(i, 8), "D"] = 0

        df.loc[(i, slice(None)), "Y_1"] = y1
        df.loc[(i, slice(None)), "Y_0"] = y0

        df.loc[(i, slice(None)), ["O", "E", "X", "U"]] = [o, e, x, u]

        # Determining the observed outcome based on the choice and potential outcomes.
        df["Y"] = df["D"] * df["Y_1"] + (1 - df["D"]) * df["Y_0"]

    # Finally some type definitions for pretty output.
    df = df.astype(np.float)
    df = df.astype({"D": np.int, "D_ever": np.int})

    return df


def get_covariates():

    o = np.random.normal()
    e = np.random.normal()

    x = o + np.random.normal()
    u = o + np.random.normal()

    return o, u, x, e


def get_plot_probability(version, grid, probs):
    fig, ax = plt.subplots(1, 1)
    ax.yaxis.get_major_ticks()[0].set_visible(False)

    ax.plot(grid, probs)
    plt.plot((0.25, 0.25), (0, 1), "--", color="grey")

    ax.set_title("{:} design".format(version.capitalize()), fontsize=25)
    ax.set_xlabel("Z")
    ax.set_ylabel("Probability")
    ax.set_ylim([0.00, 1.09])
    ax.set_xlim([0, 1])


def get_treatment_probability(version, grid):
    """This function assigns a probability of treatment assignment around
    the example's cutoff.
    """
    probs = list()
    for z in grid:
        if version == "sharp":
            if z > 0.25:
                rslt = 1
            else:
                rslt = 0

        elif version == "fuzzy":
            rslt = logistic.cdf((z - 0.25) * 20)
            if z > 0.25:
                rslt = min(rslt + 0.1, 1.0)
            elif z <= 0.25:
                rslt = max(rslt - 0.1, 0.0)
        probs.append(rslt)

    return probs


def observed_outcome(grid, version):
    y1, y0 = get_potential_outcomes(grid)

    rslt = []
    for i, prob in enumerate(get_treatment_probability(version, grid)):
        rslt += [prob * y1[i] + (1 - prob) * y0[i]]

    return rslt


def get_potential_outcomes(grid):
    y1 = 0.2 + grid * 0.5
    y0 = -0.2 + grid * 0.2

    return y1, y0


def get_sample_regression_discontinuity(num_agents=1000):
    columns = ["Y", "D", "Z"]
    index = pd.Index(range(1000), name="Identifier")
    df = pd.DataFrame(columns=columns, index=index)

    for i in range(1000):
        z = np.random.uniform()

        y1, y0 = get_potential_outcomes(z)

        # TODO: Does it make sense to have the sharp desing here?
        if z > 0.25:
            d = 1
        else:
            d = 0

        y = d * y1 + (1 - d) * y0

        df.loc[i, :] = [y, d, z]

    return df


def plot_sensitivity_regression_discontinuity(grid, rslt):
    fig, ax = plt.subplots(1, 1)
    ax.plot(grid, rslt, label="Estimate")
    ax.set_ylim([0.4, 0.6])
    ax.set_xlabel("Shift")
    ax.set_ylabel("Estimate")

    plt.plot(grid, [0.475] * 50, "--", color="grey", label="True")
    ax.legend()


def plot_outcomes(version, grid):
    ax = plt.figure().add_subplot(111)
    ax.yaxis.get_major_ticks()[0].set_visible(False)

    y1, y0 = get_potential_outcomes(grid)

    ax.plot(grid, y1, label="Treated")
    ax.plot(grid, y0, label="Control")

    y_values = observed_outcome(grid, version)
    ax.plot(grid, y_values, label="Observed", linestyle="--", color="black")
    ax.legend()
    ax.set_title("{:} design".format(version.capitalize()), fontsize=25)

    ax.set_xlabel("Z")
    ax.set_ylabel("Outcomes")
