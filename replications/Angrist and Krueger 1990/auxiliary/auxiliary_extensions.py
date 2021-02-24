"""
This module contains all the necessary functions for the extensions section in
the notebook.
"""
import itertools
from operator import add

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf
from auxiliary.auxiliary_tables import get_table3


def get_flexible_table4(data_cwhsc_new, years, data_source, cohorts):
    """
    is a flexible version of the function to create table 4 of the paper.
    It allows to create table 4 for different ranges of years for the earnings data
    and for a subset of the three different data sources.

    Parameters
    ----------
    data_cwhsc_new : pd.DataFrame
        The cwshc_new data set.
    years : list
        Range of years for which the 2SIV is supposed to be calculated.
        Within a range no year can be jumped.
        Use for example: np.arange(81, 85) to recreate the original table 4.
    data_source : list
        contains strings with the names for which table 4 is supposed to be recreated.
        To recreate the original table: ["TAXAB", "ADJ", "TOTAL"].
    cohorts : list
        contains the cohorts that are supposed to be included for the calculation.
        For example: [50, 51, 52].

    Returns
    -------
    table_4 : pd.DataFrame
        displays the results.

    """
    data = data_cwhsc_new.copy()

    set_cohorts = {50, 51, 52, 53}
    cohorts_to_drop = list(set_cohorts - set(cohorts))

    for cohort in cohorts_to_drop:
        index = data[data["byr"] == cohort].index
        data.drop(index, inplace=True)

    if len(data_source) == 1:
        data = data.loc[data["type"] == data_source[0]]
    elif len(data_source) == 2:
        data = data.loc[(data["type"] == data_source[0]) | (data["type"] == data_source[1])]
    else:
        pass

    data = data.loc[(data["year"] <= years[-1]) & (data["year"] >= years[0])].reset_index(drop=True)

    # create cohort and year dummies
    year_dummies = pd.get_dummies(data["year"], prefix="year", drop_first=True)
    year_columns = year_dummies.columns.to_list()
    data = data.join(year_dummies)
    byr_dummies = pd.get_dummies(data["byr"], prefix="byr", drop_first=True)
    byr_columns = byr_dummies.columns.to_list()
    data = data.join(byr_dummies)

    # get columns for probability of serving within cohort and
    # a given set of lottery numbers by cohort
    psr = []
    for birthyear in cohorts:
        data["ps_r" + str(birthyear)] = data["ps_r"] * (data["byr"] == birthyear)
        psr.append("ps_r" + str(birthyear))

    data["alpha1"] = 0
    data["alpha2"] = 0

    # get the coefficients from the first stage for the two models
    for race in [1, 2]:
        for source in data_source:
            data_temp = data.loc[(data["race"] == race) & (data["type"] == source)]
            model1 = [
                *byr_columns,
                *year_columns,
                "ps_r",
            ]
            model2 = model1[:-1]
            model2.extend(psr)

            # get an estimate of alpha for model 1 (alpha not varying by cohort)
            wls_model1 = smf.wls(
                formula="earnings ~ " + " + ".join(model1[:]),
                data=data_temp,
                weights=data_temp["iweight_old"],
            ).fit()
            data.loc[
                (data["race"] == race) & (data["type"] == source), "alpha1"
            ] = wls_model1.params["ps_r"]

            # get an estimate of alpha for model 2 (alpha varying by cohort)
            wls_model2 = smf.wls(
                formula="earnings ~ " + " + ".join(model2[:]),
                data=data_temp,
                weights=data_temp["iweight_old"],
            ).fit()
            for cohort in cohorts:
                data.loc[
                    (data["race"] == race) & (data["type"] == source) & (data["byr"] == cohort),
                    "alpha2",
                ] = wls_model2.params["ps_r" + str(cohort)]

    # generate sample size column
    cohort_ethnicity = list(itertools.product(cohorts, np.arange(1, 3)))
    sample = [[351, 70], [16744, 5251], [17662, 5480], [17694, 5294]]
    sample_new = []
    for j in np.array(cohorts) - 50:
        sample_new.extend(sample[j])

    for (cohort, ethnicity), size in zip(cohort_ethnicity, sample_new):
        data.loc[(data["byr"] == cohort) & (data["race"] == ethnicity), "smpl"] = size

    # generate alpha squared times Variance of ps_r for the two models
    # as needed for the GLS tarnsformation on page 325
    data["term1"] = data["alpha1"] ** 2 * data["ps_r"] * (1 - data["ps_r"]) * (1 / data["smpl"])
    data["term2"] = data["alpha2"] ** 2 * data["ps_r"] * (1 - data["ps_r"]) * (1 / data["smpl"])

    data["intercept"] = 1
    data["wts"] = 1 / data["iweight_old"] ** 0.5

    # sort the dataframe
    for number, name in enumerate(data_source):
        data.loc[data["type"] == name, "tctr"] = number + 1

    data.sort_values(by=["byr", "tctr", "race", "interval", "year"], inplace=True)
    data.set_index(["byr", "tctr", "race", "interval", "year"], inplace=True, drop=True)

    # get transformed data for second stage regression
    num_years = len(years)
    num_obs = data.shape[0]
    X1_columns = [
        "intercept",
        *byr_columns,
        *year_columns,
        "ps_r",
    ]
    X2_columns = [
        "intercept",
        *byr_columns,
        *year_columns,
        *psr,
    ]
    ern = len(years) * ["ern"]
    years_string = list(map(str, years))
    ern = list(map(add, ern, years_string))

    Y = data["earnings"].values.reshape((int(num_obs / num_years), num_years, 1))
    X1 = data[X1_columns].values.reshape((int(num_obs / num_years), num_years, len(X1_columns)))
    X2 = data[X2_columns].values.reshape((int(num_obs / num_years), num_years, len(X2_columns)))
    covmtrx = data[ern].values.reshape((int(num_obs / num_years), num_years, num_years))
    term1 = data["term1"].values.reshape((int(num_obs / num_years), num_years, 1))
    term2 = data["term2"].values.reshape((int(num_obs / num_years), num_years, 1))
    wtvec = data["wts"].values.reshape((int(num_obs / num_years), num_years, 1))

    # get the term in the squared brackets on page 325
    covmtrx1 = wtvec * covmtrx * np.transpose(wtvec, (0, 2, 1)) + term1
    covmtrx2 = wtvec * covmtrx * np.transpose(wtvec, (0, 2, 1)) + term2

    # get its inverse and decompose it
    final1 = np.linalg.cholesky(np.linalg.inv(covmtrx1))
    final2 = np.linalg.cholesky(np.linalg.inv(covmtrx2))

    # transform the data for model 1 and 2 by using the above matrices
    Y1 = np.matmul(np.transpose(final1, (0, 2, 1)), Y).reshape((num_obs, 1))
    X1 = np.matmul(np.transpose(final1, (0, 2, 1)), X1).reshape((num_obs, len(X1_columns)))
    data2 = pd.DataFrame(
        data=np.concatenate((Y1, X1), axis=1),
        index=data.index,
        columns=["earnings"] + X1_columns,
    )

    Y2 = np.matmul(np.transpose(final2, (0, 2, 1)), Y).reshape((num_obs, 1))
    X2 = np.matmul(np.transpose(final2, (0, 2, 1)), X2).reshape((num_obs, len(X2_columns)))
    data1 = pd.DataFrame(
        data=np.concatenate((Y2, X2), axis=1),
        index=data.index,
        columns=["earnings"] + X2_columns,
    )

    # Create empty table 4
    table_4 = {}
    statistic = ["Value", "Standard Error"]
    index_beginning = pd.MultiIndex.from_product(
        [["Model 1"], cohorts, statistic],
        names=["Model", "Cohort", "Statistic"],
    )
    index_beginning = index_beginning.append(
        pd.MultiIndex.from_tuples([("Model 1", "Chi Squared", "")])
    )
    index_end = pd.MultiIndex.from_product([["Model 2"], ["All cohorts"], statistic])
    index_end = index_end.append(pd.MultiIndex.from_tuples([("Model 2", "Chi Squared", "")]))
    index = index_beginning.append(index_end)
    columns = data_source

    # for loop to run regressions for the two models and for the different earnings
    # and fill table 4
    for dummy, ethnicity in enumerate(["white", "nonwhite"]):
        table_4[ethnicity] = pd.DataFrame(index=index, columns=columns)
        new_dummy = dummy + 1

        for number, dataset in enumerate(columns):
            model1_result = smf.ols(
                formula="earnings ~ 0 +" + " + ".join(data1.columns[1:]),
                data=data1.loc[(slice(None), number + 1, new_dummy, slice(None), slice(None)), :],
            ).fit()
            table_4[ethnicity].loc[
                ("Model 1", slice(None), "Value"), dataset
            ] = model1_result.params[-len(psr) :].values
            table_4[ethnicity].loc[("Model 1", slice(None), "Standard Error"), dataset] = (
                model1_result.bse[-len(psr) :].values / model1_result.mse_resid ** 0.5
            )
            table_4[ethnicity].loc[
                ("Model 1", "Chi Squared", slice(None)), dataset
            ] = model1_result.ssr

            model2_result = smf.ols(
                formula="earnings ~ 0 +" + " + ".join(data2.columns[1:]),
                data=data2.loc[(slice(None), number + 1, new_dummy, slice(None), slice(None)), :],
            ).fit()
            table_4[ethnicity].loc[
                ("Model 2", slice(None), "Value"), dataset
            ] = model2_result.params[-1]
            table_4[ethnicity].loc[("Model 2", slice(None), "Standard Error"), dataset] = (
                model2_result.bse[-1] / model2_result.mse_resid ** 0.5
            )
            table_4[ethnicity].loc[
                ("Model 2", "Chi Squared", slice(None)), dataset
            ] = model2_result.ssr

        table_4[ethnicity] = table_4[ethnicity].astype(float).round(1)

    return table_4


def get_figure1_extension1(results_model1, results_model2):
    """
    Plot the results of Table 4 for white men in Model 1 and 2 using different
    years of earnings.

    Parameters
    ----------
    results_model1 : np.array
        results from looping over different years of earnings for model 1 in table 4.
    results_model2 : np.array
        results from looping over different years of earnings for model 2 in table 4.

    Returns
    -------
    None.

    """
    cohorts = [1950, 1951, 1952, 1953]
    fig, (axis1, axis2) = plt.subplots(1, 2, sharex=True, sharey=True)
    for number, cohort in enumerate(cohorts):
        axis1.plot(
            np.arange(74, 82),
            results_model1[:, number],
            marker=".",
            color="red"
            if cohort == 1953
            else np.random.choice(np.array([sns.color_palette()]).flatten(), 4),
        )
        axis1.legend(cohorts)
        axis1.set_xlabel("Starting Year")
        axis1.set_ylabel("Treatment Effect")
        axis1.set_title("Model 1")
        axis1.yaxis.set_ticks(np.arange(-3500, 1100, 500))
        axis1.xaxis.set_ticks(np.arange(74, 82))

    axis2.plot(
        np.arange(74, 82),
        results_model2,
        marker=".",
        color=np.random.choice(np.array([sns.color_palette()]).flatten(), 3),
    )
    axis2.legend(["1950-53"])
    axis2.set_xlabel("Starting Year")
    axis2.set_ylabel("Treatment Effect")
    axis2.set_title("Model 2")


def get_figure2_extension1(results_model2, results_model2_53):
    """
    Plot comparison of Model 2 results for several different years of earnings
    when excluding cohort 1953 as opposed to including it.

    Parameters
    ----------
    results_model2 : np.array
        results from looping over different years of earnings for model 2 in table 4.
    results_model2_53 : np.array
        same as above but excluding cohort of 1953.

    Returns
    -------
    None.

    """
    fig, axis = plt.subplots()
    axis.plot(
        np.arange(74, 82),
        results_model2,
        marker=".",
        color=np.random.choice(np.array([sns.color_palette()]).flatten(), 3),
    )
    axis.plot(
        np.arange(74, 82),
        results_model2_53,
        marker=".",
        color=np.random.choice(np.array([sns.color_palette()]).flatten(), 3),
    )
    axis.legend(["1950-53", "1950-52"])
    axis.set_xlabel("Starting Year")
    axis.set_ylabel("Treatment Effect")
    axis.set_title("Model 2")
    axis.yaxis.set_ticks(np.arange(-3000, -900, 500))
    axis.xaxis.set_ticks(np.arange(74, 82))


def get_bias(data_cwhsa, data_cwhsb, data_dmdc, data_sipp, data_cwhsc_new, interval):
    """
    Get the original wald estimates from Table 3. Calculate their bias and the
    resulting true delta depending on an interval of possible effects of work experience
    on earnings.

    Parameters
    ----------
    data_cwhsa : pd.DataFrame
        CWHS data until 1978.
    data_cwhsb : pd.DataFrame
        CWHS data from 1978 on.
    data_dmdc : pd.DataFrame
        DMDC data with fraction of veterans.
    data_sipp : pd.DataFrame
        SIPP data fraction of veterans.
    data_cwhsc_new : pd.DataFrame
        CWSH data with real earnings of also adjusted FICA.
    interval : np.array
        interval of possible effects of work experience on real earnings.

    Returns
    -------
    bias : pd.DataFrame
        results of the bias.
    true_delta : pd.DataFrame
        results of the true delta.
    wald : pd.DataFrame
        the wald estimates from table 3.

    """

    table_3 = get_table3(data_cwhsa, data_cwhsb, data_dmdc, data_sipp, data_cwhsc_new)

    data = data_cwhsc_new.copy()
    data["smplsz"] = data["nj"] - data["nj0"]
    data = data.loc[(data["year"] >= 81) & (data["byr"] >= 50) & (data["byr"] <= 52)]

    # create ethnicity dummy
    data["white"] = 1 - pd.get_dummies(data["race"], drop_first=True)

    # get the sample size by group
    sumwt = (
        data.groupby(["white", "byr", "year", "type"])["smplsz"]
        .sum()
        .to_frame()
        .rename(columns={"smplsz": "sumwt"})
    )
    data = pd.merge(data, sumwt, how="outer", on=["white", "byr", "year", "type"])

    # get weighted average of the real earnings by group
    data = data.groupby(["white", "byr", "year", "type"]).apply(
        lambda x: np.average(x[["earnings"]], weights=x["smplsz"], axis=0)
    )
    data = pd.DataFrame(
        data.to_list(),
        columns=["earnings"],
        index=data.index,
    )
    # only keep adjusted FICA data
    data = data.loc[(1, slice(None), slice(None), "ADJ"), :]
    data.reset_index("type", drop=True, inplace=True)

    # Calculate the difference E[epsilon|Z] for the interval of different estimates
    # for the reduction in real earnings due to 6 months loss in working experience
    for reduction in interval:
        data[str(reduction)] = -reduction * data["earnings"]
    data.drop(columns="earnings", inplace=True)
    data.reset_index("white", drop=True, inplace=True)

    # get the denominator of the bias from Table 3
    denominator = pd.DataFrame(index=[50, 51, 52])
    denominator.index.set_names("byr", inplace=True)
    denominator["denominator"] = (
        table_3["white"]
        .loc[(slice(None), 1981, "Value"), ("", "P(V|eligible) - P(V|ineligible)")]
        .astype(float)
        .values
    )

    # join the data
    data = data.join(denominator, on="byr")

    # calculate the bias by group for the interval
    bias = pd.DataFrame(index=data.index, columns=data.columns)
    bias.drop(columns="denominator", inplace=True)
    bias.loc[:, :] = (
        1
        / data["denominator"].to_numpy().reshape((12, 1))
        * data.loc[:, data.columns != "denominator"].to_numpy()
    )

    # get the "true" delta when accounting for the bias
    wald = (
        table_3["white"]
        .loc[(slice(None), slice(None), "Value"), ("", "Service Effect in 1978 $")]
        .values
    )

    true_delta = pd.DataFrame(
        wald.reshape((12, 1)) - bias.values, index=bias.index, columns=bias.columns
    )
    wald = pd.DataFrame(wald, index=bias.index)

    return bias, true_delta, wald


def get_figure1_extension2(bias, interval):
    """
    Plot bias on the interval.

    Parameters
    ----------
    bias : pd.DataFrame
        contains results from get_bias().
    interval : np.array
        interval over which the resulting bias was calculated.

    Returns
    -------
    None.

    """
    fig, (ax0, ax1, ax2) = plt.subplots(
        1, 3, sharey=True, sharex=True, gridspec_kw={"wspace": 0.05}
    )
    for number, cohort in enumerate([50, 51, 52]):
        for year in [81, 82, 83, 84]:
            eval("ax" + str(number)).plot(
                100 * interval,
                bias.loc[(cohort, year), :].values.T,
                color=np.random.choice(np.array([sns.color_palette()]).flatten(), 3),
            )
        eval("ax" + str(number)).set_title("Cohort 19" + str(cohort), fontsize=13, weight="bold")
        eval("ax" + str(number)).legend(["19" + str(year) for year in [81, 82, 83, 84]])
    ax1.set_xlabel("Effect of Work Experience in Percent", fontsize=13)
    ax0.set_ylabel("Bias", fontsize=13)


def get_figure2_extension2(true_delta, wald, interval):
    """
    Plot true delta in comparison to the wald estimate depending on the interval
    chosen in get_bias().

    Parameters
    ----------
    true_delta : pd.DataFrame
        the true delta calulated in get_bias().
    wald : pd.DataFrame
        wald estimate calculated in get_bias().
    interval : np.array
        interval over which the resulting true_delta was calculated.

    Returns
    -------
    None.

    """
    fig, axs = plt.subplots(
        4, 3, sharey="row", sharex=True, gridspec_kw={"hspace": 0.1, "wspace": 0}
    )
    for num_year, year in enumerate([81, 82, 83, 84]):
        axs[num_year, 0].set_ylabel("Year " + str(year), fontsize=12, weight="bold")
        for num_cohort, cohort in enumerate([50, 51, 52]):
            color = np.random.choice(np.array([sns.color_palette()]).flatten(), 3)
            axs[num_year, num_cohort].plot(
                100 * interval, np.full(50, wald.loc[(cohort, year), :]), color=color
            )
            axs[num_year, num_cohort].plot(
                100 * interval, true_delta.loc[(cohort, year), :], color=color
            )
    axs[0, 0].set_title("Cohort 1950", fontsize=12, weight="bold")
    axs[0, 1].set_title("Cohort 1951", fontsize=12, weight="bold")
    axs[0, 2].set_title("Cohort 1952", fontsize=12, weight="bold")
