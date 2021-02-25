from collections import OrderedDict
from unittest import mock

import numpy as np
import pandas as pd
import patsy
import statsmodels.formula.api as smf
from linearmodels.iv.model import IV2SLS
from linearmodels.iv.model import IVLIML
from statsmodels.regression.linear_model import OLS

from . import data_helper as dhlp
from .data_helper import get_age_control_names
from .data_helper import get_constant_name
from .data_helper import get_education_name
from .data_helper import get_further_exogenous_regressors
from .data_helper import get_log_weekly_wage_name
from .data_helper import get_qob_state_of_birth_interaction_names
from .data_helper import get_qob_yob_interaction_names
from .data_helper import get_quarter_of_birth_dummy_names
from .data_helper import get_region_of_residence_dummies
from .data_helper import get_state_of_birth_dummy_names
from .data_helper import get_year_of_birth_dummy_names


def get_regression_results_educational_variables(educ_vars, cohorts):

    results = []

    for ev in educ_vars:
        for chrt_name, chrt in cohorts:
            results.append(
                {
                    "var": ev,
                    "cohort": chrt_name,
                    "mean": chrt[ev].mean(),
                    "ols": smf.ols(
                        formula=f"DTRND_{ev} ~ DUMMY_QOB_1 + DUMMY_QOB_2 + DUMMY_QOB_3", data=chrt
                    ).fit(),
                }
            )

    return results


def get_results_table_wald_estimates(df):

    wage_1st = df.loc[df["QOB"] == 1]["LWKLYWGE"].mean()
    wage_other = df.loc[df["QOB"] != 1]["LWKLYWGE"].mean()
    wage_diff = wage_1st - wage_other
    wage_err = np.sqrt(
        np.power(df.loc[df["QOB"] == 1]["LWKLYWGE"].sem(), 2)
        + np.power(df.loc[df["QOB"] != 1]["LWKLYWGE"].sem(), 2)
    )

    educ_1st = df.loc[df["QOB"] == 1]["EDUC"].mean()
    educ_other = df.loc[df["QOB"] != 1]["EDUC"].mean()
    educ_diff = educ_1st - educ_other
    educ_err = np.sqrt(
        np.power(df.loc[df["QOB"] == 1]["EDUC"].sem(), 2)
        + np.power(df.loc[df["QOB"] != 1]["EDUC"].sem(), 2)
    )

    # wald return to education
    df["EDUC_pred"] = smf.ols(formula="EDUC ~ DUMMY_QOB_1", data=df).fit().predict()
    wald_rslt = smf.ols(formula="LWKLYWGE ~ EDUC_pred", data=df).fit()

    # ols return to education
    ols_rslt = smf.ols(formula="LWKLYWGE ~ EDUC", data=df).fit()

    return {
        "wage_1st": wage_1st,
        "wage_other": wage_other,
        "wage_diff": wage_diff,
        "wage_err": wage_err,
        "educ_1st": educ_1st,
        "educ_other": educ_other,
        "educ_diff": educ_diff,
        "educ_err": educ_err,
        "wald_est": wald_rslt.params["EDUC_pred"],
        "wald_err": wald_rslt.bse["EDUC_pred"],
        "ols_est": ols_rslt.params["EDUC"],
        "ols_err": ols_rslt.bse["EDUC"],
    }


def get_regression_results_ols_tsls(df, state_of_birth_dummies=False, race=True):

    # add dummies for quarter and year of birth
    df = dhlp.add_quarter_of_birth_dummies(df)
    df = dhlp.add_year_of_birth_dummies(df)

    if state_of_birth_dummies:
        df = dhlp.add_state_of_birth_dummies(df)
        state_lst = set(df["STATE"])
        state_lst.remove(1)

    # add AGESQ age squared
    df["AGESQ"] = df["AGEQ"].pow(2)

    # regression (1) OLS
    formula_1 = "LWKLYWGE ~ EDUC + "
    formula_1 += " + ".join([f"DUMMY_YOB_{i}" for i in range(0, 9)])

    if state_of_birth_dummies:
        formula_1 += " + "
        formula_1 += " + ".join([f"DUMMY_STATE_{i}" for i in state_lst])

    ols_1 = smf.ols(formula=formula_1, data=df).fit()

    # regression (2) TSLS
    formula_1st_stage_2 = "EDUC ~ "
    formula_1st_stage_2 += " + ".join([f"DUMMY_YOB_{i}" for i in range(0, 9)])
    formula_1st_stage_2 += " + "
    formula_1st_stage_2 += " + ".join(
        [f"DUMMY_YOB_{i} : DUMMY_QOB_{j}" for j in range(1, 4) for i in range(0, 10)]
    )

    if state_of_birth_dummies:
        formula_1st_stage_2 += " + "
        formula_1st_stage_2 += " + ".join([f"DUMMY_STATE_{i}" for i in state_lst])
        formula_1st_stage_2 += " + "
        formula_1st_stage_2 += " + ".join(
            [f"DUMMY_STATE_{i} : DUMMY_QOB_{j}" for j in range(1, 4) for i in state_lst]
        )

    df["EDUC_pred_2"] = smf.ols(formula=formula_1st_stage_2, data=df).fit().predict()

    formula_2nd_stage_2 = "LWKLYWGE ~ EDUC_pred_2 +"
    formula_2nd_stage_2 += " + ".join([f"DUMMY_YOB_{i}" for i in range(0, 9)])

    if state_of_birth_dummies:
        formula_2nd_stage_2 += " + "
        formula_2nd_stage_2 += " + ".join([f"DUMMY_STATE_{i}" for i in state_lst])

    tsls_2 = smf.ols(formula=formula_2nd_stage_2, data=df).fit()

    # regression (3) OLS
    formula_3 = "LWKLYWGE ~ EDUC + AGEQ + AGESQ + "
    formula_3 += " + ".join([f"DUMMY_YOB_{i}" for i in range(0, 9)])

    if state_of_birth_dummies:
        formula_3 += " + "
        formula_3 += " + ".join([f"DUMMY_STATE_{i}" for i in state_lst])

    ols_3 = smf.ols(formula=formula_3, data=df).fit()

    # regression (4) TSLS
    formula_1st_stage_4 = "EDUC ~ AGEQ + AGESQ + "
    formula_1st_stage_4 += " + ".join([f"DUMMY_YOB_{i}" for i in range(0, 9)])
    formula_1st_stage_4 += " + "
    formula_1st_stage_4 += " + ".join(
        [f"DUMMY_YOB_{i} : DUMMY_QOB_{j}" for j in range(1, 4) for i in range(0, 10)]
    )

    if state_of_birth_dummies:
        formula_1st_stage_4 += " + "
        formula_1st_stage_4 += " + ".join([f"DUMMY_STATE_{i}" for i in state_lst])
        formula_1st_stage_4 += " + "
        formula_1st_stage_4 += " + ".join(
            [f"DUMMY_STATE_{i} : DUMMY_QOB_{j}" for j in range(1, 4) for i in state_lst]
        )

    df["EDUC_pred_4"] = smf.ols(formula=formula_1st_stage_4, data=df).fit().predict()

    formula_2nd_stage_4 = "LWKLYWGE ~ EDUC_pred_4 + AGEQ + AGESQ + "
    formula_2nd_stage_4 += " + ".join([f"DUMMY_YOB_{i}" for i in range(0, 9)])

    if state_of_birth_dummies:
        formula_2nd_stage_4 += " + "
        formula_2nd_stage_4 += " + ".join([f"DUMMY_STATE_{i}" for i in state_lst])

    tsls_4 = smf.ols(formula=formula_2nd_stage_4, data=df).fit()

    # regression (5) OLS
    formula_5 = "LWKLYWGE ~ EDUC + MARRIED + SMSA + NEWENG + MIDATL + "
    formula_5 += "ENOCENT + WNOCENT + SOATL + ESOCENT + WSOCENT + MT + "
    formula_5 += " + ".join([f"DUMMY_YOB_{i}" for i in range(0, 9)])

    if race:
        formula_5 += " + RACE"

    if state_of_birth_dummies:
        formula_5 += " + "
        formula_5 += " + ".join([f"DUMMY_STATE_{i}" for i in state_lst])

    ols_5 = smf.ols(formula=formula_5, data=df).fit()

    # regression (6) TSLS
    formula_1st_stage_6 = "EDUC ~ MARRIED + SMSA + NEWENG + MIDATL + "
    formula_1st_stage_6 += "ENOCENT + WNOCENT + SOATL + ESOCENT + WSOCENT + MT + "
    formula_1st_stage_6 += " + ".join([f"DUMMY_YOB_{i}" for i in range(0, 9)])
    formula_1st_stage_6 += " + "
    formula_1st_stage_6 += " + ".join(
        [f"DUMMY_YOB_{i} : DUMMY_QOB_{j}" for j in range(1, 4) for i in range(0, 10)]
    )

    if race:
        formula_1st_stage_6 += " + RACE"

    if state_of_birth_dummies:
        formula_1st_stage_6 += " + "
        formula_1st_stage_6 += " + ".join([f"DUMMY_STATE_{i}" for i in state_lst])
        formula_1st_stage_6 += " + "
        formula_1st_stage_6 += " + ".join(
            [f"DUMMY_STATE_{i} : DUMMY_QOB_{j}" for j in range(1, 4) for i in state_lst]
        )

    df["EDUC_pred_6"] = smf.ols(formula=formula_1st_stage_6, data=df).fit().predict()

    formula_2nd_stage_6 = "LWKLYWGE ~ EDUC_pred_6 + MARRIED + SMSA + NEWENG + MIDATL + "
    formula_2nd_stage_6 += "ENOCENT + WNOCENT + SOATL + ESOCENT + WSOCENT + MT + "
    formula_2nd_stage_6 += " + ".join([f"DUMMY_YOB_{i}" for i in range(0, 9)])

    if race:
        formula_2nd_stage_6 += " + RACE"

    if state_of_birth_dummies:
        formula_2nd_stage_6 += " + "
        formula_2nd_stage_6 += " + ".join([f"DUMMY_STATE_{i}" for i in state_lst])

    tsls_6 = smf.ols(formula=formula_2nd_stage_6, data=df).fit()

    # regression (7) OLS
    formula_7 = "LWKLYWGE ~ EDUC + AGEQ + AGESQ + MARRIED + SMSA + NEWENG + MIDATL + "
    formula_7 += "ENOCENT + WNOCENT + SOATL + ESOCENT + WSOCENT + MT + "
    formula_7 += " + ".join([f"DUMMY_YOB_{i}" for i in range(0, 9)])

    if race:
        formula_7 += " + RACE"

    if state_of_birth_dummies:
        formula_7 += " + "
        formula_7 += " + ".join([f"DUMMY_STATE_{i}" for i in state_lst])

    ols_7 = smf.ols(formula=formula_7, data=df).fit()

    # regression (8) TSLS
    formula_1st_stage_8 = "EDUC ~ AGEQ + AGESQ + MARRIED + SMSA + NEWENG + MIDATL + "
    formula_1st_stage_8 += "ENOCENT + WNOCENT + SOATL + ESOCENT + WSOCENT + MT + "
    formula_1st_stage_8 += " + ".join([f"DUMMY_YOB_{i}" for i in range(0, 9)])
    formula_1st_stage_8 += " + "
    formula_1st_stage_8 += " + ".join(
        [f"DUMMY_YOB_{i} : DUMMY_QOB_{j}" for j in range(1, 4) for i in range(0, 10)]
    )

    if race:
        formula_1st_stage_8 += " + RACE"

    if state_of_birth_dummies:
        formula_1st_stage_8 += " + "
        formula_1st_stage_8 += " + ".join([f"DUMMY_STATE_{i}" for i in state_lst])
        formula_1st_stage_8 += " + "
        formula_1st_stage_8 += " + ".join(
            [f"DUMMY_STATE_{i} : DUMMY_QOB_{j}" for j in range(1, 4) for i in state_lst]
        )

    df["EDUC_pred_8"] = smf.ols(formula=formula_1st_stage_8, data=df).fit().predict()

    formula_2nd_stage_8 = (
        "LWKLYWGE ~ EDUC_pred_8 + AGEQ + AGESQ + MARRIED + SMSA + NEWENG + MIDATL + "
    )
    formula_2nd_stage_8 += "ENOCENT + WNOCENT + SOATL + ESOCENT + WSOCENT + MT + "
    formula_2nd_stage_8 += " + ".join([f"DUMMY_YOB_{i}" for i in range(0, 9)])

    if race:
        formula_2nd_stage_8 += " + RACE"

    if state_of_birth_dummies:
        formula_2nd_stage_8 += " + "
        formula_2nd_stage_8 += " + ".join([f"DUMMY_STATE_{i}" for i in set(df["STATE"])])

    tsls_8 = smf.ols(formula=formula_2nd_stage_8, data=df).fit()

    return OrderedDict(
        [
            ("ols_1", ols_1),
            ("tsls_2", tsls_2),
            ("ols_3", ols_3),
            ("tsls_4", tsls_4),
            ("ols_5", ols_5),
            ("tsls_6", tsls_6),
            ("ols_7", ols_7),
            ("tsls_8", tsls_8),
        ]
    )


class SmallRegressionResult:
    def __init__(self, regressionResult):

        self.params = regressionResult.params
        self.bse = regressionResult.bse if hasattr(regressionResult, "bse") else None
        self.std_errors = (
            regressionResult.std_errors if hasattr(regressionResult, "std_errors") else None
        )


# wrapper for the IV2SLS method
def IV2SLS_wrapper(dependent, exog, endog, instruments, small_rslt=False):
    """
    If small_rslt is True, the method return a smaller version of the regression result
    using the SmallRegressionResult class.
    """
    # try to run the IV2SLS method without mocking the validation
    try:
        if small_rslt:
            rslt = SmallRegressionResult(IV2SLS(dependent, exog, endog, instruments).fit())
        else:
            rslt = IV2SLS(dependent, exog, endog, instruments).fit()
    except ValueError as e:
        print(str(e))

        # run the IV2LS method while mocking the validation
        with mock.patch("linearmodels.iv.model._IVModelBase._validate_inputs"):
            if small_rslt:
                rslt = SmallRegressionResult(IV2SLS(dependent, exog, endog, instruments).fit())
            else:
                rslt = IV2SLS(dependent, exog, endog, instruments).fit()

    return rslt


def IV2SLS_using_ols(dependent, exog, endog, instruments, small_rslt=False):
    """
    If small_rslt is True, the method return a smaller version of the regression result
    using the SmallRegressionResult class.


    The IV2SLS method of the linearmodels module run a simple OLS regression,
    if only inputs for dependent and exog are provided.
    To provide a uniform interface this procedure is also implemented for this method.
    """
    # run tsls regression if all required variables are passed, otherwise run ols
    if endog is not None and instruments is not None:
        # predict the endog, using the results from first stage
        endog_pred = pd.Series(
            data=OLS(endog=endog, exog=pd.concat((exog, instruments), axis=1)).fit().predict(),
            name=f"{endog.columns[0]}",
        )
        # run the second stage, effect of the predicted endog on dependent controlling for exog
        if small_rslt:
            rslt = SmallRegressionResult(
                OLS(endog=dependent, exog=pd.concat((exog, endog_pred), axis=1)).fit()
            )
        else:
            rslt = OLS(endog=dependent, exog=pd.concat((exog, endog_pred), axis=1)).fit()

    else:
        if small_rslt:
            rslt = SmallRegressionResult(OLS(endog=dependent, exog=exog).fit())
        else:
            rslt = OLS(endog=dependent, exog=exog).fit()

    return rslt


def IVLIML_wrapper(dependent, exog, endog, instruments, small_rslt=False):

    try:
        if small_rslt:
            rslt = SmallRegressionResult(IVLIML(dependent, exog, endog, instruments).fit())
        else:
            rslt = IVLIML(dependent, exog, endog, instruments).fit()
    except ValueError as e:
        print(str(e))

        with mock.patch("linearmodels.iv.model._IVModelBase._validate_inputs"):
            if small_rslt:
                rslt = SmallRegressionResult(IVLIML(dependent, exog, endog, instruments).fit())
            else:
                rslt = IVLIML(dependent, exog, endog, instruments)

    return rslt


def run_specification_iv2sls(df, specification, small_rslt=True):

    dependent, exog, endog, instruments = specification

    results = []

    for dpnd, exg, endg, instr in zip(dependent, exog, endog, instruments):

        if endg and instr:
            try:
                rslt = IV2SLS_using_ols(df[dpnd], df[exg], df[endg], df[instr], small_rslt)
            except MemoryError as e:
                print(str(e))
                break
        else:
            try:
                rslt = IV2SLS_using_ols(df[dpnd], df[exg], None, None, small_rslt)
            except MemoryError as e:
                print(str(e))
                break

        results += [rslt]

    return results


def run_specification_ivliml(df, specification, small_rslt=True):

    dependent, exog, endog, instruments = specification

    results = []

    for dpnd, exg, endg, instr in zip(dependent, exog, endog, instruments):

        if endg and instr:
            try:
                rslt = IVLIML_wrapper(df[dpnd], df[exg], df[endg], df[instr], small_rslt)
            except MemoryError as e:
                print(str(e))
                break
        else:
            rslt = None

        results += [rslt]

    return results


def f_test_excluded_instruments(df, specification):

    _, exog, endog, instruments = specification

    results = []

    for exg, endg, instr in zip(exog, endog, instruments):

        if endg:
            try:
                rslt = smf.ols(
                    formula=endg[0] + " ~ - 1 + " + " + ".join(exg + instr), data=df
                ).fit()
            except MemoryError as e:
                print(str(e))
                break

            restriction = np.zeros(shape=(len(instr), len(exg) + len(instr)))
            for i in range(len(instr)):
                restriction[i, -i - 1] = 1

            results += [rslt.f_test(restriction)]

        else:
            results += [None]

    return results


def partial_r_squared_excluded_instruments(df, specification):

    _, exog, endog, instruments = specification

    results = []

    for exg, endg, instr in zip(exog, endog, instruments):

        if endg:

            try:
                rslt = smf.ols(
                    formula=endg[0] + " ~ - 1 +" + " + ".join(exg + instr), data=df
                ).fit()
            except MemoryError as e:
                print(str(e))
                break

            try:
                rslt_excl_instr = smf.ols(
                    formula=endg[0] + " ~ - 1 + " + " + ".join(exg), data=df
                ).fit()
            except MemoryError as e:
                print(str(e))
                break

            partial_r_squared = (
                rslt_excl_instr.resid.pow(2).sum() - rslt.resid.pow(2).sum()
            ) / rslt_excl_instr.resid.pow(2).sum()

            results += [partial_r_squared]

        else:
            results += [None]

    return results


#####
# SPECIFICATIONS
#####


def get_specification_table_4_5_6():

    dependent, exog, endog, instruments = [], [], [], []

    # regression (1)
    dependent.append(get_log_weekly_wage_name())
    exog.append(get_constant_name() + get_education_name() + get_year_of_birth_dummy_names())
    endog.append(None)
    instruments.append(None)
    # regression (2)
    dependent.append(get_log_weekly_wage_name())
    exog.append(get_constant_name() + get_year_of_birth_dummy_names())
    endog.append(get_education_name())
    instruments.append(get_qob_yob_interaction_names())
    # regression (3)
    dependent.append(get_log_weekly_wage_name())
    exog.append(
        get_constant_name()
        + get_education_name()
        + get_year_of_birth_dummy_names()
        + get_age_control_names()
    )
    endog.append(None)
    instruments.append(None)
    # regression (4)
    dependent.append(get_log_weekly_wage_name())
    exog.append(get_constant_name() + get_year_of_birth_dummy_names() + get_age_control_names())
    endog.append(get_education_name())
    instruments.append(get_qob_yob_interaction_names())
    # regression (5)
    dependent.append(get_log_weekly_wage_name())
    exog.append(
        get_constant_name()
        + get_education_name()
        + get_year_of_birth_dummy_names()
        + get_region_of_residence_dummies()
        + get_further_exogenous_regressors()
    )
    endog.append(None)
    instruments.append(None)
    # regression (6)
    dependent.append(get_log_weekly_wage_name())
    exog.append(
        get_constant_name()
        + get_year_of_birth_dummy_names()
        + get_region_of_residence_dummies()
        + get_further_exogenous_regressors()
    )
    endog.append(get_education_name())
    instruments.append(get_qob_yob_interaction_names())
    # regression (7)
    dependent.append(get_log_weekly_wage_name())
    exog.append(
        get_constant_name()
        + get_education_name()
        + get_year_of_birth_dummy_names()
        + get_region_of_residence_dummies()
        + get_further_exogenous_regressors()
        + get_age_control_names()
    )
    endog.append(None)
    instruments.append(None)
    # regression (8)
    dependent.append(get_log_weekly_wage_name())
    exog.append(
        get_constant_name()
        + get_year_of_birth_dummy_names()
        + get_region_of_residence_dummies()
        + get_further_exogenous_regressors()
        + get_age_control_names()
    )
    endog.append(get_education_name())
    instruments.append(get_qob_yob_interaction_names())

    return dependent, exog, endog, instruments


def get_specification_table_7_8(state_list, race=True):

    dependent, exog, endog, instruments = [], [], [], []

    # regression (1)
    dependent.append(get_log_weekly_wage_name())
    exog.append(
        get_constant_name()
        + get_education_name()
        + get_year_of_birth_dummy_names()
        + get_state_of_birth_dummy_names(state_list)
    )
    endog.append(None)
    instruments.append(None)
    # regression (2)
    dependent.append(get_log_weekly_wage_name())
    exog.append(
        get_constant_name()
        + get_year_of_birth_dummy_names()
        + get_state_of_birth_dummy_names(state_list)
    )
    endog.append(get_education_name())
    instruments.append(
        get_qob_yob_interaction_names() + get_qob_state_of_birth_interaction_names(state_list)
    )
    # regression (3)
    dependent.append(get_log_weekly_wage_name())
    exog.append(
        get_constant_name()
        + get_education_name()
        + get_year_of_birth_dummy_names()
        + get_age_control_names()
        + get_state_of_birth_dummy_names(state_list)
    )
    endog.append(None)
    instruments.append(None)
    # regression (4)
    dependent.append(get_log_weekly_wage_name())
    exog.append(
        get_constant_name()
        + get_year_of_birth_dummy_names()
        + get_age_control_names()
        + get_state_of_birth_dummy_names(state_list)
    )
    endog.append(get_education_name())
    instruments.append(
        get_qob_yob_interaction_names() + get_qob_state_of_birth_interaction_names(state_list)
    )
    # regression (5)
    dependent.append(get_log_weekly_wage_name())
    exog.append(
        get_constant_name()
        + get_education_name()
        + get_year_of_birth_dummy_names()
        + get_region_of_residence_dummies()
        + get_further_exogenous_regressors(race=race)
        + get_state_of_birth_dummy_names(state_list)
    )
    endog.append(None)
    instruments.append(None)
    # regression (6)
    dependent.append(get_log_weekly_wage_name())
    exog.append(
        get_constant_name()
        + get_year_of_birth_dummy_names()
        + get_region_of_residence_dummies()
        + get_further_exogenous_regressors(race=race)
        + get_state_of_birth_dummy_names(state_list)
    )
    endog.append(get_education_name())
    instruments.append(
        get_qob_yob_interaction_names() + get_qob_state_of_birth_interaction_names(state_list)
    )
    # regression (7)
    dependent.append(get_log_weekly_wage_name())
    exog.append(
        get_constant_name()
        + get_education_name()
        + get_year_of_birth_dummy_names()
        + get_region_of_residence_dummies()
        + get_further_exogenous_regressors(race=race)
        + get_age_control_names()
        + get_state_of_birth_dummy_names(state_list)
    )
    endog.append(None)
    instruments.append(None)
    # regression (8)
    dependent.append(get_log_weekly_wage_name())
    exog.append(
        get_constant_name()
        + get_year_of_birth_dummy_names()
        + get_region_of_residence_dummies()
        + get_further_exogenous_regressors(race=race)
        + get_age_control_names()
        + get_state_of_birth_dummy_names(state_list)
    )
    endog.append(get_education_name())
    instruments.append(
        get_qob_yob_interaction_names() + get_qob_state_of_birth_interaction_names(state_list)
    )

    return dependent, exog, endog, instruments


def get_specification_weak_instruments_table_1():

    dependent, exog, endog, instruments = [], [], [], []

    # regression (1)
    dependent.append(get_log_weekly_wage_name())
    exog.append(
        get_constant_name()
        + get_education_name()
        + get_age_control_names()
        + get_further_exogenous_regressors()
        + get_region_of_residence_dummies()
    )
    endog.append(None)
    instruments.append(None)
    # regression (2)
    dependent.append(get_log_weekly_wage_name())
    exog.append(
        get_constant_name()
        + get_age_control_names()
        + get_further_exogenous_regressors()
        + get_region_of_residence_dummies()
    )
    endog.append(get_education_name())
    instruments.append(get_quarter_of_birth_dummy_names())
    # regression (3)
    dependent.append(get_log_weekly_wage_name())
    exog.append(
        get_constant_name()
        + get_education_name()
        + get_year_of_birth_dummy_names()
        + get_further_exogenous_regressors()
        + get_region_of_residence_dummies()
    )
    endog.append(None)
    instruments.append(None)
    # regression (4)
    dependent.append(get_log_weekly_wage_name())
    exog.append(
        get_constant_name()
        + get_year_of_birth_dummy_names()
        + get_further_exogenous_regressors()
        + get_region_of_residence_dummies()
    )
    endog.append(get_education_name())
    instruments.append(get_quarter_of_birth_dummy_names() + get_qob_yob_interaction_names())
    # regression (5)
    dependent.append(get_log_weekly_wage_name())
    exog.append(
        get_constant_name()
        + get_education_name()
        + get_year_of_birth_dummy_names()
        + get_age_control_names()
        + get_further_exogenous_regressors()
        + get_region_of_residence_dummies()
    )
    endog.append(None)
    instruments.append(None)
    # regression (6)
    dependent.append(get_log_weekly_wage_name())
    exog.append(
        get_constant_name()
        + get_year_of_birth_dummy_names()
        + get_age_control_names()
        + get_further_exogenous_regressors()
        + get_region_of_residence_dummies()
    )
    endog.append(get_education_name())
    instruments.append(get_quarter_of_birth_dummy_names() + get_qob_yob_interaction_names())

    return dependent, exog, endog, instruments


def get_specification_weak_instruments_table_2(state_list):

    dependent, exog, endog, instruments = [], [], [], []

    # regression (1)
    dependent.append(get_log_weekly_wage_name())
    exog.append(
        get_constant_name()
        + get_education_name()
        + get_year_of_birth_dummy_names()
        + get_further_exogenous_regressors()
        + get_region_of_residence_dummies()
        + get_state_of_birth_dummy_names(state_list)
    )
    endog.append(None)
    instruments.append(None)
    # regression (2)
    dependent.append(get_log_weekly_wage_name())
    exog.append(
        get_constant_name()
        + get_year_of_birth_dummy_names()
        + get_further_exogenous_regressors()
        + get_region_of_residence_dummies()
        + get_state_of_birth_dummy_names(state_list)
    )
    endog.append(get_education_name())
    instruments.append(
        get_quarter_of_birth_dummy_names()
        + get_qob_yob_interaction_names()
        + get_qob_state_of_birth_interaction_names(state_list)
    )
    # regression (3)
    dependent.append(get_log_weekly_wage_name())
    exog.append(
        get_constant_name()
        + get_education_name()
        + get_age_control_names()
        + get_year_of_birth_dummy_names()
        + get_further_exogenous_regressors()
        + get_region_of_residence_dummies()
        + get_state_of_birth_dummy_names(state_list)
    )
    endog.append(None)
    instruments.append(None)
    # regression (4)
    dependent.append(get_log_weekly_wage_name())
    exog.append(
        get_constant_name()
        + get_age_control_names()
        + get_year_of_birth_dummy_names()
        + get_further_exogenous_regressors()
        + get_region_of_residence_dummies()
        + get_state_of_birth_dummy_names(state_list)
    )
    endog.append(get_education_name())
    instruments.append(
        get_quarter_of_birth_dummy_names()
        + get_qob_yob_interaction_names()
        + get_qob_state_of_birth_interaction_names(state_list)
    )

    return dependent, exog, endog, instruments


def get_specification_mstly_hrmlss_ecnmtrcs_table_4_6_2(state_list):

    dependent, exog, endog, instruments = [], [], [], []

    # regression (1)
    dependent.append(get_log_weekly_wage_name())
    exog.append(get_constant_name() + get_year_of_birth_dummy_names())
    endog.append(get_education_name())
    instruments.append(get_quarter_of_birth_dummy_names())
    # regression (2)
    dependent.append(get_log_weekly_wage_name())
    exog.append(get_constant_name() + get_year_of_birth_dummy_names() + get_age_control_names())
    endog.append(get_education_name())
    instruments.append(get_quarter_of_birth_dummy_names())
    # regression (3)
    dependent.append(get_log_weekly_wage_name())
    exog.append(get_constant_name() + get_year_of_birth_dummy_names())
    endog.append(get_education_name())
    instruments.append(get_qob_yob_interaction_names())
    # regression (4)
    dependent.append(get_log_weekly_wage_name())
    exog.append(get_constant_name() + get_year_of_birth_dummy_names() + get_age_control_names())
    endog.append(get_education_name())
    instruments.append(get_qob_yob_interaction_names())
    # regression (5)
    dependent.append(get_log_weekly_wage_name())
    exog.append(
        get_constant_name()
        + get_year_of_birth_dummy_names()
        + get_state_of_birth_dummy_names(state_list)
    )
    endog.append(get_education_name())
    instruments.append(
        get_qob_yob_interaction_names() + get_qob_state_of_birth_interaction_names(state_list)
    )
    # regression (6)
    dependent.append(get_log_weekly_wage_name())
    exog.append(
        get_constant_name()
        + get_year_of_birth_dummy_names()
        + get_state_of_birth_dummy_names(state_list)
        + get_age_control_names()
    )
    endog.append(get_education_name())
    instruments.append(
        get_qob_yob_interaction_names() + get_qob_state_of_birth_interaction_names(state_list)
    )

    return dependent, exog, endog, instruments
