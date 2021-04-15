"""
This module contains auxiliary functions for Task B of the grmpy problem set.

Functions beginning with an underscore("_") are internal functions and
are not meant to be run by the user.

The following functions will help you answer the questions in TASK B
(sorted alhphabetically):
- investigate_mte
- monte_carlo
- plot_benefits
- plot_benefits_and_effects
- plot_effects
- plot_estimates
- plot_joint_distribution_outcomes
- plot_joint_distribution_unobservables

"""
import linecache
import shlex

import grmpy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from grmpy.read.read import read
from grmpy.simulate.simulate_auxiliary import simulate_unobservables
from grmpy.test.random_init import print_dict
from linearmodels.iv import IV2SLS


def investigate_mte(info_file):
    """
    This function reads the info file of a simulated data set
    and plots the corresponding marginal treatment effect (MTE).

    The info file is prodcued when running grmpy.simulate(init).
    It is saved in the same directory where the init file
    (required for the simulation) is located.
    If "test.yml" is the relevant init file, the
    corresponding info file will be named "test.info".

    Parameters
    ----------
    info_file: info
        Info file, which is created automatically
        when grmpy.simulate() is run.
    """
    ax = plt.figure().add_subplot(111)

    ax.set_xlim(0, 1)
    ax.set_ylabel("$MTE$")
    ax.set_xlabel("$u_D$")

    parameter = []
    linecache.clearcache()
    for num in range(40, 60):
        line = linecache.getline(info_file, num)
        parameter += [float(shlex.split(line)[1])]

    if parameter.count(parameter[0]) == len(parameter):
        label = "Absence"
    else:
        label = "Presence"

    grid = np.linspace(0.01, 1, num=20, endpoint=True)
    ax.plot(grid, parameter, label=label)

    plt.legend()

    plt.show()


def monte_carlo(file, which, grid_points=10):
    """
    This function conducts a Monte Carlo simulation to compare
    the true and estimated treatment parameters for increasing
    (absolute) correlation between U_1 and V (i.e essential
    heterogeneity).

    In the example here, the correlation between U_1 and V becomes
    increasingly more negative. As we consider the absolute value
    of the correlation coefficient, values closer to -1
    (or in the analogous case closer to +1)
    denote a higher degree of essential heterogeneity.

    The results of the Monte Carlo simulation can be used
    to evaluate the performance of different estimation strategies
    in the presence of essential heterogeneity.

    Depending on the specification of *which*, either the true ATE
    and TT, or an estimate of the ATE are returned.

    Options for *which*:

        Comparison of ATE and TT
        - "conventional_average_effects"

        Different estimation strategies for ATE
        - "randomization" ("random")
        - "ordinary_least_squares" ("ols")
        - "instrumental_variables" ("iv")
        - "grmpy_par" ("grmpy")
        - "grmpy_semipar"("grmpy-liv")

    Post-estimation: To plot the comparison between the true ATE
    and the respective parameter, use the function
    - plot_effects() for *which* = "conventional_average_effects", and
    - plot_estimates() else.

    Parameters
    ----------
    file: yaml
        grmpy initialization file, provides information for the simulation process.
    which: string
        String denoting whether conventional average effects shall be computed
        or, alternatively, which estimation approach shall be implemented for the ATE.
    grid_points: int, default 10
        Number of different values for rho, the correlation coefficient
        between U_1 and V, on the interval [0, -1), along which the parameters
        shall be evaluated.

    Returns
    -------
    effects: list
        If *which* = "conventional_average_effects",
            list of lenght *grid_points* * 2 containing the true ATE and TT.
        Else, list of length *grid_points* * 1 containing an estimate
            of the ATE.
    """
    # simulate a new data set with essential heterogeneity present
    model_dict = read(file)
    original_correlation = model_dict["DIST"]["params"][2]

    model_dict["DIST"]["params"][2] = -0.191
    print_dict(model_dict, file.replace(".grmpy.yml", ""))
    grmpy.simulate(file)

    effects = []

    # Loop over different correlations between U_1 and V
    for rho in np.linspace(0.00, -0.99, grid_points):
        # effects["rho"] += [rho]
        # Readjust the initialization file values to add correlation
        model_spec = read(file)
        X = model_spec["TREATED"]["order"]
        _update_correlation_structure(file, model_spec, rho)
        sim_spec = read(file)
        # Simulate a Data set and specify exogeneous and endogeneous variables
        df_mc = _create_data(file)
        treated = df_mc["D"] == 1
        Xvar = df_mc[X]
        instr = sim_spec["CHOICE"]["order"]
        instr = [i for i in instr if i != "const"]

        # We calculate our parameter of interest
        label = which.lower()

        if label == "conventional_average_effects":
            ATE = np.mean(df_mc["Y1"] - df_mc["Y0"])
            TT = np.mean(df_mc["Y1"].loc[treated] - df_mc["Y0"].loc[treated])
            stat = (ATE, TT)

        elif label in ["randomization", "random"]:
            random = np.mean(df_mc[df_mc.D == 1]["Y"]) - np.mean(df_mc[df_mc.D == 0]["Y"])
            stat = random

        elif label in ["ordinary_least_squares", "ols"]:
            results = sm.OLS(df_mc["Y"], df_mc[["const", "D"]]).fit()
            stat = results.params[1]

        elif label in ["instrumental_variables", "iv"]:
            iv = IV2SLS(df_mc["Y"], Xvar, df_mc["D"], df_mc[instr]).fit()
            stat = iv.params["D"]

        elif label in ["grmpy", "grmpy-par"]:
            rslt = grmpy.fit(file)
            beta_diff = (
                rslt["opt_rslt"].loc["TREATED"].params.values
                - rslt["opt_rslt"].loc["UNTREATED"].params.values
            )
            stat = np.dot(np.mean(Xvar), beta_diff)

        elif label in ["grmpy-semipar", "grmpy-liv"]:
            rslt = grmpy.fit(file, semipar=True)

            y0_fitted = np.dot(rslt["X"], rslt["b0"])
            y1_fitted = np.dot(rslt["X"], rslt["b1"])

            mte_x_ = y1_fitted - y0_fitted
            mte_u = rslt["mte_u"]

            mte_mat = np.zeros((len(mte_x_), len(mte_u)))

            for i in range(len(mte_x_)):
                for j in range(len(mte_u)):
                    mte_mat[i, j] = mte_x_[i] + mte_u[j]

            ate_tilde_p = np.mean(mte_mat, axis=1)
            stat = ate_tilde_p.mean()

        else:
            raise NotImplementedError

        effects += [stat]

    # Restore original init file
    model_dict = read(file)
    model_dict["DIST"]["params"][2] = original_correlation
    print_dict(model_dict, file.replace(".grmpy.yml", ""))
    grmpy.simulate(file)

    return effects


def plot_benefits(data):
    """
    This function plots the distribution of benefits for a data set
    that has been simulated via grmpy.

    Parameters
    ----------
    data: pandas.DataFrame
        Output of grmpy.simulate().
    """
    benefit = data["Y1"] - data["Y0"]

    ay = plt.figure().add_subplot(111)

    sns.distplot(benefit, kde=True, hist=False)

    ay.set_xlim(-1.5, 2.5)
    ay.set_ylim(0.0, None)
    ay.set_yticks([])

    # Rename axes
    ay.set_ylabel("$f_{Y_1 - Y_0}$")
    ay.set_xlabel("$Y_1 - Y_0$")


def plot_benefits_and_effects(data):
    """
    This function plots the distribution of benefits and the related
    conventional average treatment effects (ATE, TT, TUT)
    for a data set that has been simulated via grmpy.

    Parameters
    ----------
    data: pandas.DataFrame
        Output of grmpy.simulate().
    """
    benefit = data["Y1"] - data["Y0"]
    TT = np.mean(data[data.D == 1]["Y1"] - data[data.D == 1]["Y0"])
    TUT = np.mean(data[data.D == 0]["Y1"] - data[data.D == 0]["Y0"])
    ATE = np.mean(benefit)
    fmt = "ATE: {}\nTT:  {}\nTUT: {} \n"
    print(fmt.format(ATE, TT, TUT))
    ay = plt.figure().add_subplot(111)

    sns.distplot(benefit, kde=True, hist=False)

    ay.set_xlim(-1.5, 2.5)
    ay.set_ylim(0.0, None)
    ay.set_yticks([])

    # Rename axes
    ay.set_ylabel("$f_{Y_1 - Y_0}$")
    ay.set_xlabel("$Y_1 - Y_0$")

    for effect in [ATE, TT, TUT]:
        if effect == ATE:
            label = "$ATE$"
        elif effect == TT:
            label = "$TT$"
        else:
            label = "$TUT$"
        ay.plot([effect, effect], [0, 5], label=label)
    plt.legend()


def plot_effects(effects):
    """
    This function plots the population ATE along with the TT
    for increasing levels of essential heterogeneity.

    In the example here, the correlation between U_1 and V
    becomes increasingly more negative. Note that we consider
    the absolute value of the correlation coefficient.
    Hence, values closer to -1 (or in the analogous case
    closer to +1) denote a higher degree of essential heterogeneity.

    Parameters
    ----------
    effects: list
        List containing values of the population ATE and TT
        for increasing (absolute) correlation between U_1 and V.
    """
    effects = np.array(effects)

    ax = plt.figure().add_subplot(111)

    grid = np.linspace(0.0, 0.99, len(effects[:, 0]))

    ax.set_xlim(0, 1)
    ax.set_ylim(0.35, 0.65)
    ax.set_ylabel(r"Effect")
    ax.set_xlabel(r"$\rho_{U_1, V}$")
    # ax.tick_params(labelsize=14)

    ax.plot(grid, effects[:, 0], label=r"$ATE$", linewidth=4)
    ax.plot(grid, effects[:, 1], label=r"$TT$", linewidth=4)

    ax.yaxis.get_major_ticks()[0].set_visible(False)

    plt.legend(loc="upper center")

    plt.show()


def plot_estimates(true, estimates):
    """
    This function plots the true ATE parameter along with its
    estimates for increasing levels of essential heterogeneity.

    In the example here, the correlation between U_1 and V
    becomes increasingly more negative. Note that we consider
    the absolute value of the correlation coefficient.
    Hence, values closer to -1 (or in the analogous case
    closer to +1) denote a higher degree of essential heterogeneity.

    Parameters
    ----------
    true: float
        The true population parameter of the ATE.
    estimates: list
        List containing estimates of the ATE for increasing
        (absolute) correlation between U_1 and V.
    """
    ax = plt.figure().add_subplot(111)

    grid = np.linspace(0.0, 0.99, len(estimates))
    true = np.tile(true, len(estimates))

    ax.set_xlim(0, 1)
    ax.set_ylim(0.35, 0.65)
    ax.set_ylabel(r"ATE")
    ax.set_xlabel(r"$\rho_{U_1, V}$")
    # ax.tick_params(labelsize=14)

    ax.plot(grid, estimates, label="Estimate", linewidth=4)
    ax.plot(grid, true, label="True", linewidth=4)

    ax.yaxis.get_major_ticks()[0].set_visible(False)

    plt.legend(loc="upper center")

    plt.show()


def plot_joint_distribution_outcomes(df):
    """
    This function plots the joint distribution of potential outcomes.

    Parameters
    ----------
    df: pandas.DataFrame
        Output of grmpy.simulate().
    """
    sns.jointplot(df["Y1"], df["Y0"], height=8).set_axis_labels("$Y_1$", r"$Y_0$")


def plot_joint_distribution_unobservables(df):
    """
    This function plots the joint distribution of the unobservables.

    Parameters
    ----------
    df: pandas.DataFrame
        Output of grmpy.simulate().
    """
    g = sns.jointplot(df["V"], df["U1"], height=8).set_axis_labels("$V$", "$U_1$")
    g.fig.subplots_adjust(top=0.9)


def _create_data(file):
    """
    This function creates the data set used in the Monte Carlo simulation.

    In particular, the unobservables, choice, and output are simulated for
    each indiviudal based on the grmpy initialization file.
    Thereafter, the data is both returned as a pandas.DataFrame
    and saved locally in pickle format.

    Parameters
    ----------
    file: yaml
        grmpy initialization file.

    Returns
    -------
    df: pandas.DataFrame
        DataFrame
    """
    # Read in initialization file and the data set
    init_dict = read(file)
    df = pd.read_pickle(init_dict["SIMULATION"]["source"] + ".grmpy.pkl")

    # Distribute information
    indicator, dep = (
        init_dict["ESTIMATION"]["indicator"],
        init_dict["ESTIMATION"]["dependent"],
    )
    label_out = init_dict["TREATED"]["order"]
    label_choice = init_dict["CHOICE"]["order"]
    seed = init_dict["SIMULATION"]["seed"]

    # Set random seed to ensure recomputabiltiy
    np.random.seed(seed)

    # Simulate unobservables
    U = simulate_unobservables(init_dict)

    df["U1"], df["U0"], df["V"] = U["U1"], U["U0"], U["V"]

    # Simulate choice and output
    df[dep + "1"] = np.dot(df[label_out], init_dict["TREATED"]["params"]) + df["U1"]
    df[dep + "0"] = np.dot(df[label_out], init_dict["UNTREATED"]["params"]) + df["U0"]
    df[indicator] = np.array(
        np.dot(df[label_choice], init_dict["CHOICE"]["params"]) - df["V"] > 0
    ).astype(int)
    df[dep] = df[indicator] * df[dep + "1"] + (1 - df[indicator]) * df[dep + "0"]

    # Save the data
    df.to_pickle(init_dict["SIMULATION"]["source"] + ".grmpy.pkl")

    return df


def _update_correlation_structure(file, model_dict, rho):
    """
    This function takes a valid model specification and updates the correlation
    structure among the unobservables.

    The information is saved to a new init file replacing the input file.

    Parameters
    ----------
    file: yaml
        grmpy initialization file.
    model_dict: dict
        grmpy initialization dictionary, the output of grmpy.read()
    rho: float
        The correlation coefficient between U_1 and V, which
        takes values between [0, -1). Values closer to -1 denote a larger
        degree of essential heterogeneity in the sample.
    """
    # We first extract the baseline information from the model dictionary.
    sd_v = model_dict["DIST"]["params"][-1]
    sd_u1 = model_dict["DIST"]["params"][0]

    # Now we construct the implied covariance, which is relevant for the
    # initialization file.
    cov1v = rho * sd_v * sd_u1

    model_dict["DIST"]["params"][2] = cov1v

    # We print the specification of the covariance to a new init file,
    # which has the same name as the input file and replaces the original one.
    print_dict(model_dict, file.replace(".grmpy.yml", ""))
