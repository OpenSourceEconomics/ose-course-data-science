"""This module contains auxiliary functions for Task B of the grmpy problem set.
"""
import linecache
import shlex
import json

import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as mpatches

import json
import shlex
import linecache

from pylab import rcParams
from scipy.stats import norm
from linearmodels.iv import IV2SLS

import grmpy

from grmpy.read.read import read
from grmpy.test.random_init import print_dict
from grmpy.estimate.estimate_output import calculate_mte
from grmpy.simulate.simulate_auxiliary import simulate_unobservables


def plot_benefits(data):
    """This function plots the distribution of benefits
    effects.
    """
    rcParams["figure.figsize"] = 10, 8

    benefit = data["Y1"] - data["Y0"]

    ay = plt.figure().add_subplot(111)

    sns.distplot(benefit, kde=True, hist=False)

    ay.set_xlim(-1.5, 2.5)
    ay.set_ylim(0.0, None)
    ay.set_yticks([])
    ay.tick_params(labelsize=14)

    # Rename axes
    ay.set_ylabel("$f_{Y_1 - Y_0}$", fontsize=18)
    ay.set_xlabel("$Y_1 - Y_0$", fontsize=18)


def plot_benefits_and_effects(data):
    """This function plots the distribution of benefits and the related conventional
    effects.
    """
    rcParams["figure.figsize"] = 10, 8

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
    ay.tick_params(labelsize=14)

    # Rename axes
    ay.set_ylabel("$f_{Y_1 - Y_0}$", fontsize=18)
    ay.set_xlabel("$Y_1 - Y_0$", fontsize=18)

    for effect in [ATE, TT, TUT]:
        if effect == ATE:
            label = "$ATE$"
        elif effect == TT:
            label = "$TT$"
        else:
            label = "$TUT$"
        ay.plot([effect, effect], [0, 5], label=label)
    plt.legend(prop={"size": 15})


def monte_carlo(file, which, grid_points=10):
    """This function estimates various effect parameters for
    increasing presence of essential heterogeneity, which is reflected
    by increasing correlation between U_1 and V.
    """
    # simulate a new data set with essential heterogeneity present
    model_dict = read(file)
    original_correlation = model_dict["DIST"]["params"][2]

    model_dict["DIST"]["params"][2] = -0.191
    print_dict(model_dict, file.replace(".grmpy.yml", ""))
    grmpy.simulate(file)

    effects = []

    # Loop over different correlations between V and U_1
    for rho in np.linspace(0.00, -0.99, grid_points):
        # effects["rho"] += [rho]
        # Readjust the initialization file values to add correlation
        model_spec = read(file)
        X = model_spec["TREATED"]["order"]
        update_correlation_structure(file, model_spec, rho)
        sim_spec = read(file)
        # Simulate a Data set and specify exogeneous and endogeneous variables
        df_mc = create_data(file)
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

        elif label in ["random", "randomization"]:
            random = np.mean(df_mc[df_mc.D == 1]["Y"]) - np.mean(
                df_mc[df_mc.D == 0]["Y"]
            )
            stat = random

        elif label in ["ordinary_least_squares", "ols"]:
            results = sm.OLS(df_mc["Y"], df_mc[["const", "D"]]).fit()
            stat = results.params[1]

        elif label in ["instrumental_variables", "iv"]:
            iv = IV2SLS(df_mc["Y"], Xvar, df_mc["D"], df_mc[instr]).fit()
            stat = iv.params["D"]

        elif label in ["grmpy", "grmpy-par"]:
            rslt = grmpy.fit(file)
            beta_diff = rslt["TREATED"]["params"] - rslt["UNTREATED"]["params"]
            stat = np.dot(np.mean(Xvar), beta_diff)

        elif label in ["grmpy-semipar", "grmpy-liv"]:
            rslt = grmpy.fit(file, semipar=True)

            y0_fitted = np.dot(rslt["X"], rslt["b0"])
            y1_fitted = np.dot(rslt["X"], rslt["b1"])

            mte_x_ = y1_fitted - y0_fitted
            mte_u = rslt["mte_u"]

            us = np.linspace(0.005, 0.995, len(rslt["quantiles"]))
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


def plot_effects(effects):
    """This function plots the effects of treatment."""
    effects = np.array(effects)

    ax = plt.figure(figsize=(10, 8)).add_subplot(111)

    grid = np.linspace(0.0, 0.99, len(effects[:, 0]))

    ax.set_xlim(0, 1)
    ax.set_ylim(0.35, 0.65)
    ax.set_ylabel(r"Effect", fontsize=18)
    ax.set_xlabel(r"$\rho_{U_1, V}$", fontsize=18)
    ax.tick_params(labelsize=14)

    ax.plot(grid, effects[:, 0], label=r"$ATE$", linewidth=4)
    ax.plot(grid, effects[:, 1], label=r"$TT$", linewidth=4)

    ax.yaxis.get_major_ticks()[0].set_visible(False)

    plt.legend(loc="upper right", prop={"size": 14})

    plt.show()


def plot_estimates(true, estimates):
    """This function plots the estimates of the ATE along with its
    true parameter for increasing levels of essential heterogeneity."""
    ax = plt.figure(figsize=(10, 8)).add_subplot(111)

    grid = np.linspace(0.0, 0.99, len(estimates))
    true = np.tile(true, len(estimates))

    ax.set_xlim(0, 1)
    ax.set_ylim(0.35, 0.65)
    ax.set_ylabel(r"ATE", fontsize=18)
    ax.set_xlabel(r"$\rho_{U_1, V}$", fontsize=18)
    ax.tick_params(labelsize=14)

    ax.plot(grid, estimates, label="Estimate", linewidth=4)
    ax.plot(grid, true, label="True", linewidth=4)

    ax.yaxis.get_major_ticks()[0].set_visible(False)

    plt.legend(loc="upper right", prop={"size": 14})

    plt.show()


def create_data(file):
    """This function creates a data set based for the monte carlo simulation
    setup.
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


def update_correlation_structure(file, model_dict, rho):
    """This function takes a valid model specification and updates the correlation
    structure among the unobservables."""

    # We first extract the baseline information from the model dictionary.
    sd_v = model_dict["DIST"]["params"][-1]
    sd_u1 = model_dict["DIST"]["params"][0]

    # Now we construct the implied covariance, which is relevant for the initialization
    # file.
    cov1v = rho * sd_v * sd_u1

    model_dict["DIST"]["params"][2] = cov1v

    # We print out the specification to an initialization file with the name
    # mc_init.grmpy.ini.
    print_dict(model_dict, file.replace(".grmpy.yml", ""))


def get_effect_grmpy(file):
    """This function simply returns the ATE of the data set."""
    dict_ = read(file)
    df = pd.read_pickle(dict_["SIMULATION"]["source"] + ".grmpy.pkl")
    beta_diff = dict_["TREATED"]["params"] - dict_["UNTREATED"]["params"]
    covars = dict_["TREATED"]["order"]
    ATE = np.dot(np.mean(df[covars]), beta_diff)

    return ATE


def create_plots(effects, true):
    """The function creates the figures that illustrates the behavior of each estimator
    of the ATE when the correlation structure changes from 0 to 1."""

    grid = np.linspace(0.00, 0.99, len(effects["ols"]))

    # Plot all graphs in one plot
    ax2 = plt.figure(figsize=(17.5, 10)).add_subplot(111)
    ax2.set_xlim([-0.005, 1.005])
    ax2.set_ylim(0.375, 0.575)
    ax2.tick_params(axis="both", which="major", labelsize=18)
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(0.05))
    ax2.set_ylabel(r"$ATE$", fontsize=20)
    ax2.set_xlabel(r"$\rho_{U_1, V}$", fontsize=20)
    ax2.plot(grid, true, label="True", color="blue", linewidth=3.0)
    ax2.plot(grid, effects["grmpy"], label="grmpy", color="orange", linewidth=3.0)
    ax2.plot(
        grid, effects["random"], label="Naive comparison", color="green", linewidth=3.0
    )
    ax2.plot(
        grid, effects["iv"], label="Instrumental variables", color="red", linewidth=3.0
    )
    ax2.plot(
        grid,
        effects["ols"],
        label="Ordinary Least Squares",
        color="purple",
        linewidth=3.0,
    )
    plt.rc("xtick", labelsize=18)
    plt.rc("ytick", labelsize=18)

    blue_patch = mpatches.Patch(color="blue", label="True")
    orange_patch = mpatches.Patch(color="orange", label="grmpy")
    green_patch = mpatches.Patch(color="green", label="Naive comparison")
    red_patch = mpatches.Patch(color="red", label="Instrumental Variables")
    purple_patch = mpatches.Patch(color="purple", label="Ordinary Least Squares")

    plt.legend(
        handles=[blue_patch, orange_patch, green_patch, red_patch, purple_patch],
        prop={"size": 13},
    )

    plt.show()


def plot_joint_distribution_unobservables(df):
    """This function plots the joint distribution of the relevant unobservables."""
    g = sns.jointplot(df["V"], df["U1"], stat_func=None).set_axis_labels(
        "$V$", "$U_1$", fontsize=18
    )
    g.fig.subplots_adjust(top=0.9)


def investigate_mte(info_file):
    """This function reads the info file of a simulated data set
    and plots the corresponding marginal treatment effect (MTE).
    """
    ax = plt.figure(figsize=(10, 8)).add_subplot(111)

    ax.set_xlim(0, 1)
    ax.set_ylabel("$MTE$", fontsize=18)
    ax.set_xlabel("$u_D$", fontsize=18)
    ax.tick_params(labelsize=14)

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

    plt.legend(prop={"size": 18})

    plt.show()


def plot_joint_distribution_outcomes(df):
    """This function plots the joint distribution of potential outcomes."""
    sns.jointplot(df["Y1"], df["Y0"], stat_func=None).set_axis_labels(
        "$Y_1$", r"$Y_0$", fontsize=18
    )
