"""
Create Figures 1 until 3 from "Lifetime Earnings and the Vietnam Era Draft Lottery:
Evidence from Social Security Administrative Records" by J. Angrist (1990).
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from matplotlib.lines import Line2D


def get_figure1(data_cwhsa, data_cwhsb):
    """
    Creates Figure 1 of the paper.

    Parameters
    ----------
    data_cwhsa : pd.DataFrame
        CWHS data until 1978.
    data_cwhsb : pd.DataFrame
        CWHS data from 1978 on.

    Returns
    -------
    None.

    """
    # get the processed data for plotting
    data = prepare_data_figure12(data_cwhsa, data_cwhsb)[0]

    # create figure 1
    fig1, (ax1, ax2) = plt.subplots(1, 2)
    legend_lines = [
        Line2D([0], [0], color="red", lw=2),
        Line2D([0], [0], color="black", lw=2),
    ]
    for ethnicity, axis in [(1, ax1), (2, ax2)]:
        for cohort in [50, 51, 52, 53]:
            axis.plot(
                "year",
                "real_earnings",
                data=data.loc[(ethnicity, cohort, 0), :],
                marker=".",
                color="red",
            )
            axis.plot(
                "year",
                "real_earnings",
                data=data.loc[(ethnicity, cohort, 1), :],
                marker=".",
                color="black",
            )
        axis.xaxis.set_ticks(np.arange(66, 85, 2))
        axis.set_xlabel("Year")
        axis.legend(legend_lines, ["ineligible", "elgible"])
    ax1.set_ylabel("Whites Earnings in 1978 Dollars")
    ax2.set_ylabel("Nonwhites Earnings in 1978 Dollars")
    fig1.tight_layout()


def get_figure2(data_cwhsa, data_cwhsb):
    """
    Creates Figure 2 of the paper.

    Parameters
    ----------
    data_cwhsa : pd.DataFrame
        CWHS data until 1978.
    data_cwhsb : pd.DataFrame
        CWHS data from 1978 on.

    Returns
    -------
    None.

    """
    # get the processed data for plotting
    data = prepare_data_figure12(data_cwhsa, data_cwhsb)[1]

    # create figure 2
    fig2, axs = plt.subplots(
        4,
        2,
        sharex=True,
        sharey=True,
        gridspec_kw={"hspace": 0},
        constrained_layout=True,
    )
    for ethnicity in [1, 2]:
        for row, cohort in enumerate([50, 51, 52, 53]):
            axs[row, ethnicity - 1].plot(
                "year", "difference", data=data.loc[(ethnicity, cohort), :]
            )
            if ethnicity == 1:
                axs[row, ethnicity - 1].set_ylabel("19" + str(cohort))
            axs[row, ethnicity - 1].axhline(
                0, color="black", linestyle="--", linewidth=1
            )

    axs[0, 0].xaxis.set_ticks(np.arange(66, 85, 2))
    axs[0, 0].set_title("Whites")
    axs[0, 1].set_title("Nonwhites")
    fig2.suptitle("Difference in earnings by cohort and ethnicity", fontsize=13)


def get_figure3(data_cwhsc_new):
    """
    Create Figure 3 of the paper.

    Parameters
    ----------
    data_cwhsc_new : pd.DataFrame
        CWSH data with real earnings of also adjusted FICA.

    Returns
    -------
    None.

    """
    # load data set
    data = data_cwhsc_new

    # keep only Total W-2 compensation
    data = data.loc[
        (data["year"] >= 81) & (data["race"] == 1) & (data["type"] == "TOTAL")
    ]
    data.reset_index(inplace=True, drop=True)

    # create dummies for year and birth year
    data = pd.concat([data, pd.get_dummies(data["year"], prefix="year")], axis=1)
    data = pd.concat([data, pd.get_dummies(data["byr"], prefix="byr")], axis=1)

    # get earnings residuals
    columns = [
        "year_81",
        "year_82",
        "year_83",
        "year_84",
        "byr_50",
        "byr_51",
        "byr_52",
        "byr_53",
    ]
    formula = "earnings ~ " + " + ".join(columns[:])
    data["ernres"] = smf.ols(formula=formula, data=data).fit().resid

    # obtain mean of the earnings residual by interval and birth year
    ernres2 = data.groupby(["byr", "interval"])["ernres"].mean().to_frame()
    data = pd.merge(data, ernres2, how="outer", on=["byr", "interval"])

    # get probability residuals
    columns = ["byr_50", "byr_51", "byr_52", "byr_53"]
    formula = "ps_r ~ " + " + ".join(columns[:])
    data["pres"] = smf.ols(formula=formula, data=data).fit().resid

    # look at it only for the year 1981
    data = data.loc[data["year"] == 81]

    # get fitted values for linear fit plot
    linear_fit = smf.ols(formula="ernres_y ~ pres", data=data).fit()
    fitted_values = linear_fit.predict()

    # plot earnings residuals on probablity residuals
    fig, ax = plt.subplots()
    ax.scatter(x=data["pres"], y=data["ernres_y"], c="black", marker="8")
    ax.plot(data["pres"], fitted_values, color="red")
    ax.set_ylim([-3100, 3100])
    ax.set_xlim([-0.09, 0.17])
    ax.set_ylabel("Earnings Residual")
    ax.set_xlabel("Probability Residual")


def prepare_data_figure12(data_cwhsa, data_cwhsb):
    """
    Take CWHS data set for FICA earnings and prepare it such that it can be used for
    plotting Figure 1 and 2.

    Parameters
    ----------
    data_cwhsa : pd.DataFrame
        CWHS data until 1978.
    data_cwhsb : pd.DataFrame
        CWHS data from 1978 on.

    Returns
    -------
    data_temp : pd.DataFrame
        Contains the FICA earnings in 1978 dollar terms across those eligible for
        the draft lottery for both whites and nonwhites for different years and birth cohorts.
    difference : pd.DataFrame
        Contains the difference in FICA earnings in 1978 dollar terms between eligible
        and ineligible for different groups (by ethnicity, year and birth cohort).

    """
    # read data for years 64 to 77
    data = data_cwhsa
    # declare that it is FICA earnings
    data["type"] = "TAXAB"

    # read data for the years after 77
    temp_data = data_cwhsb
    data = data.append(temp_data)

    data = data.loc[(data["year"] > 65) & (data["byr"] >= 50)]

    # create eligibility dummy
    data["eligible"] = 0
    data.loc[
        ((data["byr"] >= 44) & (data["byr"] <= 50) & (data["interval"] <= 39))
        | ((data["byr"] == 51) & (data["interval"] <= 25))
        | (((data["byr"] == 52) | (data["byr"] == 53)) & (data["interval"] <= 19)),
        "eligible",
    ] = 1

    # add the cpi to the data
    data_cpi = pd.read_stata("data/cpi_angrist1990.dta")
    data = pd.merge(data, data_cpi, on="year")

    # keep only FICA earnings
    data = data.loc[data["type"] == "TAXAB"]

    # create the average earnings for those with nonzero earnings
    data["earnings"] = data["vmn1"] / (1 - data["vfin1"])
    # create the sample size for those with nonzero earnings
    data["weights"] = data["vnu1"] * (1 - data["vfin1"])

    # create real earnings in 1978 terms
    data["cpi"] = (data["cpi"] / data.loc[data["year"] == 78, "cpi"].mean()).round(3)
    data["real_earnings"] = data["earnings"] / data["cpi"]

    # adjust earnings like in description below Figure 1 in the paper
    for cohort, addition in [(50, 3000), (51, 2000), (52, 1000)]:
        data.loc[data["byr"] == cohort, "real_earnings"] = (
            data.loc[data["byr"] == cohort, "real_earnings"] + addition
        )

    table = data.fillna(0)

    # drop groups where the weight sums to zero (i.e. where there are no positive earnings)
    sum_group_weights = (
        table.groupby(["race", "byr", "year", "eligible"])["weights"].sum().to_frame()
    )
    nonzero_weights_index = sum_group_weights.loc[
        sum_group_weights["weights"] != 0
    ].index
    table.set_index(["race", "byr", "year", "eligible"], inplace=True)
    table = table.loc[nonzero_weights_index]
    # get weighted averages within by groups of ethnicity, cohort, year and draft eligibility
    data_temp = table.groupby(["race", "byr", "year", "eligible"]).apply(
        lambda x: np.average(x[["real_earnings"]], weights=x["weights"], axis=0)
    )
    data_temp = pd.DataFrame(
        data_temp.to_list(), columns=["real_earnings"], index=data_temp.index
    )

    # create dataframe with the differences in real earnings
    # for the above groups across eligibility
    difference = pd.DataFrame(index=data_temp.index, columns=["difference"])
    difference = difference.loc[(slice(None), slice(None), slice(None), 0), :]
    difference.reset_index("eligible", drop=True, inplace=True)
    difference["difference"] = (
        data_temp.loc[(slice(None), slice(None), slice(None), 1), :].values
        - data_temp.loc[(slice(None), slice(None), slice(None), 0), :].values
    )

    difference.reset_index("year", inplace=True)
    data_temp.reset_index("year", inplace=True)

    return data_temp, difference
