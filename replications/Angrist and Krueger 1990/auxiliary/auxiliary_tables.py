"""
Create Tables 1 until 4 from "Lifetime Earnings and the Vietnam Era Draft Lottery:
Evidence from Social Security Administrative Records" by J. Angrist (1990).
"""
import itertools

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


def get_table1(data_cwhsa, data_cwhsb):
    """
    Create Table 1 of the paper.

    Parameters
    ----------
    data_cwhsa : pd.DataFrame
        CWHS data until 1978.
    data_cwhsb : pd.DataFrame
        CWHS data from 1978 on.

    Returns
    -------
    table_1 : dictionairy
        The dict holds the keys "white" and "nonwhite".
        Those are both pd.DataFrame's that contain the parts of Table 1
        for the respective ethnicity specified as key.

    """
    data = data_cwhsa
    # declare it as FICA data
    data["type"] = "TAXAB"

    # reat FICA and Total W-2 data for years 78 and onwards
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

    # create ethnicity dummy
    data = pd.concat([data, pd.get_dummies(data["race"], prefix="race")], axis=1)
    data.rename(columns={"race_1": "white", "race_2": "nonwhite"}, inplace=True)

    # create the average earnings for those with nonzero earnings
    data["earn_nz"] = data["vmn1"] / (1 - data["vfin1"])
    # create the sample size for those with nonzero earnings
    data["wt_nz"] = data["vnu1"] * (1 - data["vfin1"])

    # rename FICA observations properly for the whole data set
    data.loc[data["type"] == "TAXAB", "type"] = "FICA"
    # create variance of the earnings from the reported standard deviations
    var = data["vsd1"] ** 2
    # create variance of nonzero earnings
    data["var_nz"] = var * (data["vnu1"] / data["wt_nz"])

    # get the inverse number of total sample size of nonzero earnings by group
    wtmult = pd.DataFrame()
    wtmult["wtmult"] = (
        1 / data.groupby(["white", "byr", "year", "eligible", "type"])["wt_nz"].sum()
    )
    data = pd.merge(
        data, wtmult, how="outer", on=["white", "byr", "year", "eligible", "type"]
    )

    # get in group variance
    data["var_cm"] = data["wtmult"] * data["var_nz"]

    # get groupby weighted means
    data_temp = data.fillna(0)

    # drop groups where the weight sums to zero
    sum_group_weights = (
        data_temp.groupby(["white", "byr", "year", "eligible", "type"])["wt_nz"]
        .sum()
        .to_frame()
    )
    nonzero_weights_index = sum_group_weights.loc[sum_group_weights["wt_nz"] != 0].index
    data_temp.set_index(["white", "byr", "year", "eligible", "type"], inplace=True)
    data_temp = data_temp.loc[nonzero_weights_index]
    # get weighted mean of the mean and variance of earnings by group
    data_temp = data_temp.groupby(["white", "byr", "year", "eligible", "type"]).apply(
        lambda x: np.average(x[["var_cm", "earn_nz"]], weights=x["wt_nz"], axis=0)
    )
    data_temp = pd.DataFrame(
        data_temp.to_list(), columns=["var_cm", "earn_nz"], index=data_temp.index
    )

    # get the difference in earnings and its standard deviation per group across eligibility
    index_eligible = (slice(None), slice(None), slice(None), 1, slice(None))
    index_non_eligible = (slice(None), slice(None), slice(None), 0, slice(None))
    treatment_effect = data_temp.loc[index_eligible, "earn_nz"].reset_index(
        "eligible", drop=True
    ) - data_temp.loc[index_non_eligible, "earn_nz"].reset_index("eligible", drop=True)

    standard_errors = (
        data_temp.loc[index_eligible, "var_cm"].reset_index("eligible", drop=True)
        + data_temp.loc[index_non_eligible, "var_cm"].reset_index("eligible", drop=True)
    ) ** 0.5

    # get results into a nice looking table
    table_1 = {}
    for dummy, ethnicity in enumerate(["white", "nonwhite"]):
        new_dummy = 1 - dummy
        # extract treatment effect and their standard errors
        treatment_effect_temp = treatment_effect.loc[new_dummy, :, :, :].reset_index(
            "white", drop=True
        )
        standard_errors_temp = standard_errors.loc[new_dummy, :, :, :].reset_index(
            "white", drop=True
        )

        # get dataframes into the right shape for table 1
        treatment_effect_temp = treatment_effect_temp.unstack(
            level=["type", "byr"]
        ).sort_index(level="type", axis=1)
        treatment_effect_temp["Statistic"] = "Average"
        treatment_effect_temp.set_index(
            "Statistic", drop=True, append=True, inplace=True
        )

        standard_errors_temp = standard_errors_temp.unstack(
            level=["type", "byr"]
        ).sort_index(level="type", axis=1)
        standard_errors_temp["Statistic"] = "Standard Error"
        standard_errors_temp.set_index(
            "Statistic", drop=True, append=True, inplace=True
        )

        # Create table 1
        year = np.arange(66, 85)
        statistic = ["Average", "Standard Error"]
        index = pd.MultiIndex.from_product(
            [year, statistic], names=["year", "Statistic"]
        )
        table_1_temp = pd.DataFrame(index=index, columns=treatment_effect_temp.columns)
        table_1_temp.loc[(slice(None), "Average"), :] = treatment_effect_temp
        table_1_temp.loc[(slice(None), "Standard Error"), :] = standard_errors_temp
        table_1_temp = table_1_temp.astype(float).round(2)
        table_1_temp.fillna("", inplace=True)

        # cm = sns.light_palette("green", as_cmap=True, reverse=True)
        # s = table_1_temp.style.background_gradient(
        # cmap=cm, subset=pd.IndexSlice[np.arange(0, 38, 2), ["FICA", "TOTAL"]])
        # table_1_temp = table_1_temp.style.background_gradient(
        # cmap=cm, subset= pd.IndexSlice[[(78, "Average")], :], axis=1)

        table_1[ethnicity] = table_1_temp

    return table_1


# for the CWHS data set I am missing the ingredients for cohort 1950
# for the SIPP I get different standard errors which is most likely due to the
# implementation of the WLS. I get the same results as in stata, though.
def get_table2(data_cwhsa, data_dmdc, data_sipp):
    """
    Create Table 2 of the paper.
    The CWHS data set I have is missing the ingredients to replicate Table 2
    for those born in 1950.
    Further I get different standard errors for the SIPP data which is most likely
    due to my implementation of the Weighted Least Squares.

    Parameters
    ----------
    data_cwhsa : pd.DataFrame
        CWHS data until 1978.
    data_dmdc : pd.DataFrame
        DMDC data with fraction of veterans.
    data_sipp : pd.DataFrame
        SIPP data fraction of veterans.

    Returns
    -------
    table_2 : dictionairy
        The dict holds the keys "white" and "nonwhite".
        Those are both pd.DataFrame's that contain the parts of Table 1
        for the respective ethnicity specified as key.

    """

    data_cwhsa = data_cwhsa.loc[
        (data_cwhsa["year"] == 70) & (data_cwhsa["byr"] >= 51),
        ["race", "byr", "interval", "vnu1"],
    ]

    # create eligibility dummy
    data_cwhsa["eligible"] = 0
    data_cwhsa.loc[
        (
            (data_cwhsa["byr"] >= 44)
            & (data_cwhsa["byr"] <= 50)
            & (data_cwhsa["interval"] <= 39)
        )
        | ((data_cwhsa["byr"] == 51) & (data_cwhsa["interval"] <= 25))
        | (
            ((data_cwhsa["byr"] == 52) | (data_cwhsa["byr"] == 53))
            & (data_cwhsa["interval"] <= 19)
        ),
        "eligible",
    ] = 1

    # create ethnicity dummy
    data_cwhsa["white"] = 1 - pd.get_dummies(data_cwhsa["race"], drop_first=True)

    # get the sample size across groups
    data_cwhsa = data_cwhsa.groupby(["byr", "white", "eligible"])["vnu1"].sum()

    # create eligibility dummy
    data_dmdc["eligible"] = 0
    data_dmdc.loc[
        (
            (data_dmdc["byr"] >= 44)
            & (data_dmdc["byr"] <= 50)
            & (data_dmdc["interval"] <= 39)
        )
        | ((data_dmdc["byr"] == 51) & (data_dmdc["interval"] <= 25))
        | (
            ((data_dmdc["byr"] == 52) | (data_dmdc["byr"] == 53))
            & (data_dmdc["interval"] <= 19)
        ),
        "eligible",
    ] = 1

    # create ethnicity dummy
    data_dmdc["white"] = 1 - pd.get_dummies(data_dmdc["race"], drop_first=True)

    # get sample size per group
    data_dmdc = data_dmdc.groupby(["byr", "white", "eligible"])["nsrvd"].sum()

    # merge the two data sets
    data_dmdc_cwsh = pd.merge(data_cwhsa, data_dmdc, on=["byr", "white", "eligible"])

    # calculate sample size for the sum of eligible and non-eligible per group and per data set
    nsrvd_all = (
        data_dmdc_cwsh.groupby(["white", "byr"])["nsrvd"]
        .sum()
        .to_frame()
        .rename(columns={"nsrvd": "nsrvd_all"})
    )
    vnu1_all = (
        data_dmdc_cwsh.groupby(["white", "byr"])["vnu1"]
        .sum()
        .to_frame()
        .rename(columns={"vnu1": "vnu1_all"})
    )
    data_dmdc_cwsh = data_dmdc_cwsh.join(
        pd.merge(nsrvd_all, vnu1_all, on=["byr", "white"])
    )

    # get probability of being a veteran conditional on eligibility status
    # times 100 because the DMDC data is across the whole population and
    # the CWSH is only a sample of one percent
    data_dmdc_cwsh["p_vet"] = data_dmdc_cwsh["nsrvd"] / (100 * data_dmdc_cwsh["vnu1"])
    # calculate prob of being a veteran in general
    data_dmdc_cwsh["p_vet_all"] = data_dmdc_cwsh["nsrvd_all"] / (
        100 * data_dmdc_cwsh["vnu1_all"]
    )
    # calculate the standard errors
    data_dmdc_cwsh["se_vet"] = (
        data_dmdc_cwsh["p_vet"] * (1 - data_dmdc_cwsh["p_vet"]) / data_dmdc_cwsh["vnu1"]
    ) ** 0.5
    data_dmdc_cwsh["se_vet_all"] = (
        data_dmdc_cwsh["p_vet_all"]
        * (1 - data_dmdc_cwsh["p_vet_all"])
        / data_dmdc_cwsh["vnu1_all"]
    ) ** 0.5

    table_2 = {}
    for dummy, ethnicity in enumerate(["white", "nonwhite"]):
        new_dummy = 1 - dummy

        # Initialize a temporary table
        dataset = ["SIPP (84)", "DMDC/CWHS"]
        cohort = np.arange(1951, 1954)
        statistic = ["Value", "Standard Error"]
        index_end = pd.MultiIndex.from_product(
            [dataset, cohort, statistic], names=["Data Set", "Cohort", "Statistic"]
        )
        index_beginning = pd.MultiIndex.from_product(
            [[dataset[0]], [1950], statistic], names=["Data Set", "Cohort", "Statistic"]
        )
        index = index_beginning.append(index_end)
        table_2_temp = pd.DataFrame(
            index=index,
            columns=[
                "Sample",
                "P(Veteran)",
                "P(Veteran|eligible)",
                "P(Veteran|ineligible)",
                "P(V|eligible) - P(V|ineligible)",
            ],
        )

        # fill the table with values created through the DMDC/CWHS data set
        table_2_temp.loc[
            ("DMDC/CWHS", slice(None), "Value"),
            ["Sample", "P(Veteran)", "P(Veteran|eligible)"],
        ] = data_dmdc_cwsh.loc[
            (slice(None), new_dummy, 1), ["vnu1_all", "p_vet_all", "p_vet"]
        ].values
        table_2_temp.loc[
            ("DMDC/CWHS", slice(None), "Standard Error"),
            ["P(Veteran)", "P(Veteran|eligible)"],
        ] = data_dmdc_cwsh.loc[
            (slice(None), new_dummy, 1), ["se_vet_all", "se_vet"]
        ].values
        table_2_temp.loc[
            ("DMDC/CWHS", slice(None), "Value"), "P(Veteran|ineligible)"
        ] = data_dmdc_cwsh.loc[(slice(None), new_dummy, 0), ["p_vet"]].values
        table_2_temp.loc[
            ("DMDC/CWHS", slice(None), "Standard Error"), "P(Veteran|ineligible)"
        ] = data_dmdc_cwsh.loc[(slice(None), new_dummy, 0), ["se_vet"]].values
        table_2_temp.loc[
            ("DMDC/CWHS", slice(None), "Value"), "P(V|eligible) - P(V|ineligible)"
        ] = (
            table_2_temp.loc[("DMDC/CWHS", slice(None), "Value"), "P(Veteran|eligible)"]
            - table_2_temp.loc[
                ("DMDC/CWHS", slice(None), "Value"), "P(Veteran|ineligible)"
            ]
        )
        table_2_temp.loc[
            ("DMDC/CWHS", slice(None), "Standard Error"),
            "P(V|eligible) - P(V|ineligible)",
        ] = (
            (
                table_2_temp.loc[
                    ("DMDC/CWHS", slice(None), "Standard Error"), "P(Veteran|eligible)"
                ]
                ** 2
                + table_2_temp.loc[
                    ("DMDC/CWHS", slice(None), "Standard Error"),
                    "P(Veteran|ineligible)",
                ]
                ** 2
            )
            ** 0.5
        )

        # create table 2
        table_2[ethnicity] = table_2_temp

    for dummy, ethnicity in enumerate(["white", "nonwhite"]):
        for year in np.arange(1950, 1954):
            # fill table 2 with values from the SIPP data set
            data_temp = data_sipp.loc[
                (data_sipp["u_brthyr"] >= year - 1)
                & (data_sipp["u_brthyr"] <= year + 1)
                & (data_sipp["nrace"] == dummy)
            ]
            # run WLS regression to get probabilitiy of being a veteran per group
            wls = smf.wls(
                formula="nvstat ~ 1", data=data_temp, weights=data_temp["fnlwgt_5"]
            ).fit()
            coefficient = wls.params
            standard_error = wls.bse
            # extract sample size and fill table 2
            table_2[ethnicity].loc[
                ("SIPP (84)", year, "Value"), "Sample"
            ] = data_sipp.loc[
                (data_sipp["u_brthyr"] == year) & (data_sipp["nrace"] == dummy)
            ].shape[
                0
            ]

            table_2[ethnicity].loc[
                ("SIPP (84)", year, slice(None)), "P(Veteran)"
            ] = coefficient.append(standard_error).values

            # get prob of being a veteran given eligibility
            data_temp = data_sipp.loc[
                (data_sipp["u_brthyr"] >= year - 1)
                & (data_sipp["u_brthyr"] <= year + 1)
                & (data_sipp["nrace"] == dummy)
                & (data_sipp["rsncode"] == 1)
            ]
            wls = smf.wls(
                formula="nvstat ~ 1", data=data_temp, weights=data_temp["fnlwgt_5"]
            ).fit()
            coefficient = wls.params
            standard_error = wls.bse
            table_2[ethnicity].loc[
                ("SIPP (84)", year, slice(None)), "P(Veteran|eligible)"
            ] = coefficient.append(standard_error).values

            # get prob of being veteran given not being eligible
            data_temp = data_sipp.loc[
                (data_sipp["u_brthyr"] >= year - 1)
                & (data_sipp["u_brthyr"] <= year + 1)
                & (data_sipp["nrace"] == dummy)
                & (data_sipp["rsncode"] != 1)
            ]
            wls = smf.wls(
                formula="nvstat ~ 1", data=data_temp, weights=data_temp["fnlwgt_5"]
            ).fit()
            coefficient = wls.params
            standard_error = wls.bse
            table_2[ethnicity].loc[
                ("SIPP (84)", year, slice(None)), "P(Veteran|ineligible)"
            ] = coefficient.append(standard_error).values

            # create last column for the SIPP data set in table 2
            table_2[ethnicity].loc[
                ("SIPP (84)", slice(None), "Value"), "P(V|eligible) - P(V|ineligible)"
            ] = (
                table_2[ethnicity].loc[
                    ("SIPP (84)", slice(None), "Value"), "P(Veteran|eligible)"
                ]
                - table_2[ethnicity].loc[
                    ("SIPP (84)", slice(None), "Value"), "P(Veteran|ineligible)"
                ]
            )
            table_2[ethnicity].loc[
                ("SIPP (84)", slice(None), "Standard Error"),
                "P(V|eligible) - P(V|ineligible)",
            ] = (
                (
                    table_2[ethnicity].loc[
                        ("SIPP (84)", slice(None), "Standard Error"),
                        "P(Veteran|eligible)",
                    ]
                    ** 2
                    + table_2[ethnicity].loc[
                        ("SIPP (84)", slice(None), "Standard Error"),
                        "P(Veteran|ineligible)",
                    ]
                    ** 2
                )
                ** 0.5
            )

    for ethnicity in ["white", "nonwhite"]:
        table_2[ethnicity] = table_2[ethnicity].astype(float).round(4)
        table_2[ethnicity] = table_2[ethnicity].fillna("")

    return table_2


# for the second to last column I get different standard errors as this difference
# directly transfers from table 2
def get_table3(data_cwhsa, data_cwhsb, data_dmdc, data_sipp, data_cwhsc_new):
    """
    Create Table 3 of the paper.
    For the second to last column I get different standard errors as those results
    are taken exactly from Table 2.

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

    Returns
    -------
    table_3 : dictionairy
        The dict holds the keys "white" and "nonwhite".
        Those are both pd.DataFrame's that contain the parts of Table 3
        for the respective ethnicity specified as key.


    """
    # create data frame for table 3
    cohort = np.arange(1950, 1953)
    year = np.arange(1981, 1985)
    statistic = ["Value", "Standard Error"]
    index = pd.MultiIndex.from_product(
        [cohort, year, statistic], names=["Cohort", "Year", "Statistic"]
    )
    draft_eligible = np.full(3, "Draft Eligibility Effects in Current $")
    not_draft_eligible = np.full(2, "")
    first_level = np.concatenate((draft_eligible, not_draft_eligible))
    second_level = np.array(
        [
            "FICA Earnings",
            "Adjusted FICA Earnings",
            "Total W-2 Earnings",
            "P(V|eligible) - P(V|ineligible)",
            "Service Effect in 1978 $",
        ]
    )
    columns = pd.MultiIndex.from_arrays(
        [first_level, second_level], names=["First Level", "Second Level"]
    )
    table_3 = {}
    table_3["white"] = pd.DataFrame(index=index, columns=columns)
    table_3["nonwhite"] = pd.DataFrame(index=index, columns=columns)

    # fill table 3 with results from table 1 and 2
    table_1 = get_table1(data_cwhsa, data_cwhsb)
    table_2 = get_table2(data_cwhsa, data_dmdc, data_sipp)
    for ethnicity in ["white", "nonwhite"]:
        table_3[ethnicity].loc[
            :, (slice(None), ["FICA Earnings", "Total W-2 Earnings"])
        ] = (
            table_1[ethnicity]
            .loc[(slice(81, 84), slice(None)), (slice(None), slice(50, 52))]
            .values.reshape((24, 2), order="F")
        )

        for number in year:
            table_3[ethnicity].loc[
                (slice(None), number, slice(None)),
                (slice(None), "P(V|eligible) - P(V|ineligible)"),
            ] = (
                table_2[ethnicity]
                .loc[
                    ("SIPP (84)", [1950, 1951, 1952], slice(None)),
                    "P(V|eligible) - P(V|ineligible)",
                ]
                .values
            )

    # fill table 3 with new values
    data = data_cwhsc_new
    data_cpi = pd.read_stata("data/cpi_angrist1990.dta")
    data = pd.merge(data, data_cpi, on="year")

    data["cpi"] = (data["cpi"] / data.loc[data["year"] == 78, "cpi"].mean()).round(3)
    data["cpi2"] = data["cpi"] ** 2
    data["smplsz"] = data["nj"] - data["nj0"]
    data = data.loc[(data["year"] >= 81) & (data["byr"] >= 50) & (data["byr"] <= 52)]

    # get variance
    data["var"] = 1 / data["iweight_old"] * data["smplsz"] * data["cpi2"]
    # create nominal earnings from the included real earnings in 1978 dollar terms
    data["nomearn"] = data["earnings"] * data["cpi"]
    # create eligibilty dummy
    data["eligible"] = 0
    data.loc[
        ((data["byr"] == 50) & (data["interval"] == 1))
        | ((data["byr"] == 51) & (data["interval"] <= 25))
        | (((data["byr"] == 52) | (data["byr"] == 53)) & (data["interval"] <= 19)),
        "eligible",
    ] = 1

    # create ethnicity dummy
    data["white"] = 1 - pd.get_dummies(data["race"], drop_first=True)

    # get the sample size by group
    sumwt = (
        data.groupby(["white", "byr", "year", "eligible", "type"])["smplsz"]
        .sum()
        .to_frame()
        .rename(columns={"smplsz": "sumwt"})
    )
    data = pd.merge(
        data, sumwt, how="outer", on=["white", "byr", "year", "eligible", "type"]
    )

    # get group variance
    data["var_cm"] = 1 / data["sumwt"] * data["var"]
    # get weighted average
    data = data.groupby(["white", "byr", "year", "eligible", "type"]).apply(
        lambda x: np.average(
            x[["var_cm", "nomearn", "earnings", "cpi"]], weights=x["smplsz"], axis=0
        )
    )
    data = pd.DataFrame(
        data.to_list(),
        columns=["var_cm", "nomearn", "earnings", "cpi"],
        index=data.index,
    )
    # only keep adjusted FICA data
    data = data.loc[(slice(None), slice(None), slice(None), slice(None), "ADJ"), :]
    data.reset_index("type", drop=True, inplace=True)

    # fill adjusted FICA earnings column
    for dummy, ethnicity in enumerate(["white", "nonwhite"]):
        new_dummy = 1 - dummy
        table_3[ethnicity].loc[
            (slice(None), slice(None), "Value"), (slice(None), "Adjusted FICA Earnings")
        ] = (
            data.loc[(new_dummy, slice(None), slice(None), 1), "nomearn"].values
            - data.loc[(new_dummy, slice(None), slice(None), 0), "nomearn"].values
        )

        table_3[ethnicity].loc[
            (slice(None), slice(None), "Standard Error"),
            (slice(None), "Adjusted FICA Earnings"),
        ] = (
            (
                data.loc[(new_dummy, slice(None), slice(None), 1), "var_cm"].values
                + data.loc[(new_dummy, slice(None), slice(None), 0), "var_cm"].values
            )
            ** 0.5
        )

    # fill the last column with the Wald estimate based on FICA earnings
    for dummy, ethnicity in enumerate(["white", "nonwhite"]):
        new_dummy = 1 - dummy
        for stat in statistic:
            table_3[ethnicity].loc[
                (slice(None), slice(None), stat),
                (slice(None), "Service Effect in 1978 $"),
            ] = table_3[ethnicity].loc[
                (slice(None), slice(None), stat),
                (slice(None), "Adjusted FICA Earnings"),
            ].values.flatten() / (
                table_3[ethnicity]
                .loc[
                    (slice(None), slice(None), "Value"),
                    (slice(None), "P(V|eligible) - P(V|ineligible)"),
                ]
                .values.flatten()
                * data.loc[(new_dummy, slice(None), slice(None), 0), "cpi"].values
            )

        table_3[ethnicity].loc[:, (slice(None), "P(V|eligible) - P(V|ineligible)")] = (
            table_3[ethnicity]
            .loc[:, (slice(None), "P(V|eligible) - P(V|ineligible)")]
            .astype(float)
            .round(3)
        )
        table_3[ethnicity].loc[
            (slice(None), slice(1982, 1984), slice(None)),
            (slice(None), "P(V|eligible) - P(V|ineligible)"),
        ] = ""
        table_3[ethnicity].loc[
            :,
            ~table_3[ethnicity].columns.isin([("", "P(V|eligible) - P(V|ineligible)")]),
        ] = (
            table_3[ethnicity]
            .loc[
                :,
                ~table_3[ethnicity].columns.isin(
                    [("", "P(V|eligible) - P(V|ineligible)")]
                ),
            ]
            .astype(float)
            .round(1)
        )

    return table_3


# my results are like in the stata code but the table in Angrist is a tiny bit different
def get_table4(data_cwhsc_new):
    """
    Create Table 4 of the paper.

    Parameters
    ----------
    data_cwhsc_new : pd.DataFrame
        CWSH data with real earnings of also adjusted FICA.

    Returns
    -------
    table_4 : dictionairy
        The dict holds the keys "white" and "nonwhite".
        Those are both pd.DataFrame's that contain the parts of Table 4
        for the respective ethnicity specified as key.

    """
    data = data_cwhsc_new
    data = data.loc[data["year"] >= 81].reset_index(drop=True)

    # create cohort and year dummies
    data = data.join(pd.get_dummies(data["year"], prefix="year"))
    data = data.join(pd.get_dummies(data["byr"], prefix="byr"))

    # get columns for probability of serving within cohort and
    # a given set of lottery numbers by cohort
    for birthyear in [50, 51, 52, 53]:
        data["ps_r" + str(birthyear)] = data["ps_r"] * (data["byr"] == birthyear)

    data["alpha1"] = 0
    data["alpha2"] = 0

    # get the coefficients from the first stage for the two models
    for race in [1, 2]:
        for source in ["TAXAB", "ADJ", "TOTAL"]:
            data_temp = data.loc[(data["race"] == race) & (data["type"] == source)]
            model1 = [
                "byr_51",
                "byr_52",
                "byr_53",
                "year_82",
                "year_83",
                "year_84",
                "ps_r",
            ]
            model2 = model1[:-1]
            model2.extend(["ps_r50", "ps_r51", "ps_r52", "ps_r53"])

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
            for cohort in [50, 51, 52, 53]:
                data.loc[
                    (data["race"] == race)
                    & (data["type"] == source)
                    & (data["byr"] == cohort),
                    "alpha2",
                ] = wls_model2.params["ps_r" + str(cohort)]

    # generate sample size column
    cohort_ethnicity = list(itertools.product(np.arange(50, 54), np.arange(1, 3)))
    sample = [351, 70, 16744, 5251, 17662, 5480, 17694, 5294]
    for (cohort, ethnicity), size in zip(cohort_ethnicity, sample):
        data.loc[(data["byr"] == cohort) & (data["race"] == ethnicity), "smpl"] = size

    # generate alpha squared times Variance of ps_r for the two models
    # as needed for the GLS tarnsformation on page 325
    data["term1"] = (
        data["alpha1"] ** 2 * data["ps_r"] * (1 - data["ps_r"]) * (1 / data["smpl"])
    )
    data["term2"] = (
        data["alpha2"] ** 2 * data["ps_r"] * (1 - data["ps_r"]) * (1 / data["smpl"])
    )

    data["intercept"] = 1
    data["wts"] = 1 / data["iweight_old"] ** 0.5

    # sort the dataframe
    for number, name in enumerate(["TAXAB", "ADJ", "TOTAL"]):
        data.loc[data["type"] == name, "tctr"] = number + 1

    data.sort_values(by=["byr", "tctr", "race", "interval", "year"], inplace=True)
    data.set_index(["byr", "tctr", "race", "interval", "year"], inplace=True, drop=True)

    # get transformed data for second stage regression
    X1_columns = [
        "intercept",
        "byr_51",
        "byr_52",
        "byr_53",
        "year_82",
        "year_83",
        "year_84",
        "ps_r",
    ]
    X2_columns = [
        "intercept",
        "byr_51",
        "byr_52",
        "byr_53",
        "year_82",
        "year_83",
        "year_84",
        "ps_r50",
        "ps_r51",
        "ps_r52",
        "ps_r53",
    ]
    Y = data["earnings"].values.reshape((int(5304 / 4), 4, 1))
    X1 = data[X1_columns].values.reshape((int(5304 / 4), 4, 8))
    X2 = data[X2_columns].values.reshape((int(5304 / 4), 4, 11))
    covmtrx = data[["ern81", "ern82", "ern83", "ern84"]].values.reshape(
        (int(5304 / 4), 4, 4)
    )
    term1 = data["term1"].values.reshape((int(5304 / 4), 4, 1))
    term2 = data["term2"].values.reshape((int(5304 / 4), 4, 1))
    wtvec = data["wts"].values.reshape((int(5304 / 4), 4, 1))

    # get the term in the squared brackets on page 325
    covmtrx1 = wtvec * covmtrx * np.transpose(wtvec, (0, 2, 1)) + term1
    covmtrx2 = wtvec * covmtrx * np.transpose(wtvec, (0, 2, 1)) + term2

    # get its inverse and decompose it
    final1 = np.linalg.cholesky(np.linalg.inv(covmtrx1))
    final2 = np.linalg.cholesky(np.linalg.inv(covmtrx2))

    # transform the data for model 1 and 2 by using the above matrices
    Y1 = np.matmul(np.transpose(final1, (0, 2, 1)), Y).reshape((5304, 1))
    X1 = np.matmul(np.transpose(final1, (0, 2, 1)), X1).reshape((5304, 8))
    data2 = pd.DataFrame(
        data=np.concatenate((Y1, X1), axis=1),
        index=data.index,
        columns=["earnings"] + X1_columns,
    )

    Y2 = np.matmul(np.transpose(final2, (0, 2, 1)), Y).reshape((5304, 1))
    X2 = np.matmul(np.transpose(final2, (0, 2, 1)), X2).reshape((5304, 11))
    data1 = pd.DataFrame(
        data=np.concatenate((Y2, X2), axis=1),
        index=data.index,
        columns=["earnings"] + X2_columns,
    )

    # Create empty table 4
    table_4 = {}
    statistic = ["Value", "Standard Error"]
    index_beginning = pd.MultiIndex.from_product(
        [["Model 1"], np.arange(1950, 1954), statistic],
        names=["Model", "Cohort", "Statistic"],
    )
    index_beginning = index_beginning.append(
        pd.MultiIndex.from_tuples([("Model 1", "Chi Squared", "")])
    )
    index_end = pd.MultiIndex.from_product([["Model 2"], ["1950-53"], statistic])
    index_end = index_end.append(
        pd.MultiIndex.from_tuples([("Model 2", "Chi Squared", "")])
    )
    index = index_beginning.append(index_end)
    columns = [
        "FICA Taxable Earnings",
        "Adjusted FICA Earnings",
        "Total W-2 Compensation",
    ]

    # for loop to run regressions for the two models and for the different earnings
    # and fill table 4
    for dummy, ethnicity in enumerate(["white", "nonwhite"]):
        table_4[ethnicity] = pd.DataFrame(index=index, columns=columns)
        new_dummy = dummy + 1

        for number, dataset in enumerate(columns):
            model1_result = smf.ols(
                formula="earnings ~ 0 +" + " + ".join(data1.columns[1:]),
                data=data1.loc[
                    (slice(None), number + 1, new_dummy, slice(None), slice(None)), :
                ],
            ).fit()
            table_4[ethnicity].loc[
                ("Model 1", slice(None), "Value"), dataset
            ] = model1_result.params[-4:].values
            table_4[ethnicity].loc[
                ("Model 1", slice(None), "Standard Error"), dataset
            ] = (model1_result.bse[-4:].values / model1_result.mse_resid ** 0.5)
            table_4[ethnicity].loc[
                ("Model 1", "Chi Squared", slice(None)), dataset
            ] = model1_result.ssr

            model2_result = smf.ols(
                formula="earnings ~ 0 +" + " + ".join(data2.columns[1:]),
                data=data2.loc[
                    (slice(None), number + 1, new_dummy, slice(None), slice(None)), :
                ],
            ).fit()
            table_4[ethnicity].loc[
                ("Model 2", slice(None), "Value"), dataset
            ] = model2_result.params[-1]
            table_4[ethnicity].loc[
                ("Model 2", slice(None), "Standard Error"), dataset
            ] = (model2_result.bse[-1] / model2_result.mse_resid ** 0.5)
            table_4[ethnicity].loc[
                ("Model 2", "Chi Squared", slice(None)), dataset
            ] = model2_result.ssr

        table_4[ethnicity] = table_4[ethnicity].astype(float).round(1)

    return table_4
