from operator import itemgetter

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from . import regressions


def create_table_qob(results, outcome_variables=None):

    table = """
    <table>
        <thead>
            <tr>
                <th>Outcome variable</th>
                <th>Birth cohort</th>
                <th>Mean</th>
                <th colspan="3">Quarter-of-birth effect</th>
                <th>F-test</th>
            </tr>
            <tr>
                <th></th><th></th><th></th>
                <th>I</th>
                <th>II</th>
                <th>III</th>
                <th>[P-value]</th>
            </tr>
        </thead>
        <tbody>
    """

    if outcome_variables:
        for out_var, rslt in zip(outcome_variables, results):
            table += create_table_row_qob(out_var, rslt["cohort"], rslt["mean"], rslt["ols"])

    else:
        for rslt in results:
            table += create_table_row_qob(rslt["var"], rslt["cohort"], rslt["mean"], rslt["ols"])

    table += """
        </tbody>
    </table>
    """

    return table


def create_table_row_qob(outcome_variable, cohort, mean, ols):

    table_row = f"""
    <tr>
        <td>{outcome_variable}</td>
        <td>{cohort}</td>
        <td>{mean:5.2f}</td>
        <td>{ols.params['DUMMY_QOB_1']:6.3f}</td>
        <td>{ols.params['DUMMY_QOB_2']:6.3f}</td>
        <td>{ols.params['DUMMY_QOB_3']:6.3f}</td>
        <td>{ols.fvalue:6.1f}</td>
    </tr>
    <tr>
        <td></td><td></td><td></td>
        <td>({ols.bse['DUMMY_QOB_1']:5.3f})</td>
        <td>({ols.bse['DUMMY_QOB_2']:5.3f})</td>
        <td>({ols.bse['DUMMY_QOB_3']:5.3f})</td>
        <td>[{ols.f_pvalue:6.4f}]</td>
    </tr>
    """
    return table_row


def create_table_wald_estimates(title, results):

    table = f"""
    <table>
        <thead>
            <tr>
                <th colspan="4">
                    {title}
                </th>
            </tr>
            <tr>
                <th></th>
                <th>(1)<br>Born<br>in 1st quarter<br>of year</th>
                <th>(2)<br>Born in 2nd,<br>3rd, or 4th<br>quarter of year</th>
                <th>(3)<br>Difference<br>(std.error)<br>(1) - (2)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>ln (wkly. wage)</td>
                <td>{results['wage_1st']:6.4f}</td>
                <td>{results['wage_other']:6.4f}</td>
                <td>{results['wage_diff']:6.5f}</td>
            </tr>
            <tr>
                <td></td><td></td><td></td>
                <td>({results['wage_err']:6.5f})</td>
            </tr>
            <tr>
                <td>Education</td>
                <td>{results['educ_1st']:6.4f}</td>
                <td>{results['educ_other']:6.4f}</td>
                <td>{results['educ_diff']:6.5f}</td>
            </tr>
            <tr>
                <td></td><td></td><td></td>
                <td>({results['educ_err']:6.5f})</td>
            </tr>
            <tr>
                <td>Wald est. of return to education</td>
                <td></td><td></td>
                <td>{results['wald_est']:6.5f}</td>
            </tr>
            <tr>
                <td></td><td></td><td></td>
                <td>({results['wald_err']:6.5f})</td>
            </tr>
            <tr>
                <td>OLS return to education</td>
                <td></td><td></td>
                <td>{results['ols_est']:6.5f}</td>
            </tr>
            <tr>
                <td></td><td></td><td></td>
                <td>({results['ols_err']:6.5f})</td>
            </tr>
        </tbody>
    </table>
    """

    return table


def create_table_4_5_6(results):

    table = """
    <table>
        <thead>
            <tr>
                <th></th>
    """
    table += "\n".join([f"<th>({i})</th>" for i in range(1, 9)])
    table += """
            </tr>
            <tr>
                <th>Independent variable</th>
    """
    table += "\n".join([f"<th>{method}</th>" for method in ["OLS", "TSLS"] * 4])
    table += """
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Years of education</td>
    """
    table += "\n".join([f'<td>{rslt.params["EDUC"]:5.4f}</td>' for rslt in results])
    table += """
            </tr>
            <tr>
                <td></td>
    """
    table += "\n".join([f'<td>({rslt.bse["EDUC"]:5.4f})</td>' for rslt in results])

    table += """
            </tr>
            <tr>
                <td>Race (1 = black)</td>
    """
    table += "\n".join(
        [
            f'<td>{rslt.params["RACE"]:6.4f}</td>' if "RACE" in rslt.params else "<td>-</td>"
            for rslt in results
        ]
    )
    table += """
            </tr>
            <tr>
                <td></td>
    """
    table += "\n".join(
        [
            f'<td>({rslt.bse["RACE"]:6.4f})</td>' if "RACE" in rslt.bse else "<td></td>"
            for rslt in results
        ]
    )
    table += """
            </tr>
            <tr>
                <td>SMSA (1 = center city)</td>
    """
    table += "\n".join(
        [
            f'<td>{rslt.params["SMSA"]:6.4f}</td>' if "SMSA" in rslt.params else "<td>-</td>"
            for rslt in results
        ]
    )
    table += """
            </tr>
            <tr>
                <td></td>
    """
    table += "\n".join(
        [
            f'<td>({rslt.bse["SMSA"]:6.4f})</td>' if "SMSA" in rslt.bse else "<td></td>"
            for rslt in results
        ]
    )
    table += """
            </tr>
            <tr>
                <td>Married (1 = married)</td>
    """
    table += "\n".join(
        [
            f'<td>{rslt.params["MARRIED"]:6.4f}</td>' if "MARRIED" in rslt.params else "<td>-</td>"
            for rslt in results
        ]
    )
    table += """
            </tr>
            <tr>
                <td></td>
    """
    table += "\n".join(
        [
            f'<td>({rslt.bse["MARRIED"]:6.4f})</td>' if "MARRIED" in rslt.bse else "<td></td>"
            for rslt in results
        ]
    )
    table += """
            </tr>
            <tr>
                <td>9 Year-of-birth dummies</td>
    """
    table += "\n".join(["<td>Yes</td>"] * 8)
    table += """
            </tr>
            <tr>
                <td>8 Region-of-residence dummies</td>
    """
    table += "\n".join(["<td>No</td>"] * 4 + ["<td>Yes</td>"] * 4)
    table += """
            </tr>
            <tr>
                <td>Age</td>
    """
    table += "\n".join(
        [
            f'<td>{rslt.params["AGEQ"]:6.4f}</td>' if "AGEQ" in rslt.params else "<td>-</td>"
            for rslt in results
        ]
    )
    table += """
            </tr>
            <tr>
                <td></td>
    """
    table += "\n".join(
        [
            f'<td>({rslt.bse["AGEQ"]:6.4f})</td>' if "AGEQ" in rslt.bse else "<td></td>"
            for rslt in results
        ]
    )
    table += """
            </tr>
            <tr>
                <td>Age Squared</td>
    """
    table += "\n".join(
        [
            f'<td>{rslt.params["AGESQ"]:6.4f}</td>' if "AGESQ" in rslt.params else "<td>-</td>"
            for rslt in results
        ]
    )
    table += """
            </tr>
            <tr>
                <td></td>
    """
    table += "\n".join(
        [
            f'<td>({rslt.bse["AGESQ"]:6.4f})</td>' if "AGESQ" in rslt.bse else "<td></td>"
            for rslt in results
        ]
    )
    table += """
            </tr>
        </tbody>
    </table>
    """

    return table


def create_table_7_8(results, race=True):

    table = """
    <table>
        <thead>
            <tr>
                <th></th>
    """
    table += "\n".join([f"<th>({i})</th>" for i in range(1, 9)])
    table += """
            </tr>
            <tr>
                <th>Independent variable</th>
    """
    table += "\n".join([f"<th>{method}</th>" for method in ["OLS", "TSLS"] * 4])
    table += """
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Years of education</td>
    """
    table += "\n".join([f'<td>{rslt.params["EDUC"]:5.4f}</td>' for rslt in results])
    table += """
            </tr>
            <tr>
                <td></td>
    """
    table += "\n".join([f'<td>({rslt.bse["EDUC"]:5.4f})</td>' for rslt in results])
    if race:
        table += """
                </tr>
                <tr>
                    <td>Race (1 = black)</td>
        """
        table += "\n".join(
            [
                f'<td>{rslt.params["RACE"]:6.4f}</td>' if "RACE" in rslt.params else "<td>-</td>"
                for rslt in results
            ]
        )
        table += """
                </tr>
                <tr>
                    <td></td>
        """
        table += "\n".join(
            [
                f'<td>({rslt.bse["RACE"]:6.4f})</td>' if "RACE" in rslt.bse else "<td></td>"
                for rslt in results
            ]
        )
    table += """
            </tr>
            <tr>
                <td>SMSA (1 = center city)</td>
    """
    table += "\n".join(
        [
            f'<td>{rslt.params["SMSA"]:6.4f}</td>' if "SMSA" in rslt.params else "<td>-</td>"
            for rslt in results
        ]
    )
    table += """
            </tr>
            <tr>
                <td></td>
    """
    table += "\n".join(
        [
            f'<td>({rslt.bse["SMSA"]:6.4f})</td>' if "SMSA" in rslt.bse else "<td></td>"
            for rslt in results
        ]
    )
    table += """
            </tr>
            <tr>
                <td>Married (1 = married)</td>
    """
    table += "\n".join(
        [
            f'<td>{rslt.params["MARRIED"]:6.4f}</td>' if "MARRIED" in rslt.params else "<td>-</td>"
            for rslt in results
        ]
    )
    table += """
            </tr>
            <tr>
                <td></td>
    """
    table += "\n".join(
        [
            f'<td>({rslt.bse["MARRIED"]:6.4f})</td>' if "MARRIED" in rslt.bse else "<td></td>"
            for rslt in results
        ]
    )
    table += """
            </tr>
            <tr>
                <td>9 Year-of-birth dummies</td>
    """
    table += "\n".join(["<td>Yes</td>"] * 8)
    table += """
            </tr>
            <tr>
                <td>8 Region-of-residence dummies</td>
    """
    table += "\n".join(["<td>No</td>"] * 4 + ["<td>Yes</td>"] * 4)
    if race:
        table += """
            </tr>
            <tr>
                <td>50 State-of-birth dummies</td>
            """
    else:
        table += """
            </tr>
            <tr>
                <td>49 State-of-birth dummies</td>
            """
    table += "\n".join(["<td>Yes</td>"] * 8)
    table += """
            </tr>
            <tr>
                <td>Age</td>
    """
    table += "\n".join(
        [
            f'<td>{rslt.params["AGEQ"]:6.4f}</td>' if "AGEQ" in rslt.params else "<td>-</td>"
            for rslt in results
        ]
    )
    table += """
            </tr>
            <tr>
                <td></td>
    """
    table += "\n".join(
        [
            f'<td>({rslt.bse["AGEQ"]:6.4f})</td>' if "AGEQ" in rslt.bse else "<td></td>"
            for rslt in results
        ]
    )
    table += """
            </tr>
            <tr>
                <td>Age Squared</td>
    """
    table += "\n".join(
        [
            f'<td>{rslt.params["AGESQ"]:6.4f}</td>' if "AGESQ" in rslt.params else "<td>-</td>"
            for rslt in results
        ]
    )
    table += """
            </tr>
            <tr>
                <td></td>
    """
    table += "\n".join(
        [
            f'<td>({rslt.bse["AGESQ"]:6.4f})</td>' if "AGESQ" in rslt.bse else "<td></td>"
            for rslt in results
        ]
    )
    table += """
            </tr>
        </tbody>
    </table>
    """

    return table


def create_table_mstly_hrmlss_ecnmtrcs_4_6_2(tsls, liml, f_test):

    table = """
    <table>
        <thead>
            <tr>
                <th></th>
                <th>(1)</th>
                <th>(2)</th>
                <th>(3)</th>
                <th>(4)</th>
                <th>(5)</th>
                <th>(6)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>2SLS</td>
    """
    table += "\n".join([f'<td>{rslt.params["EDUC"]:5.4f}</td>' for rslt in tsls])
    table += """
            </tr>
            <tr>
                <td></td>
    """
    table += "\n".join([f'<td>({rslt.bse["EDUC"]:5.4f})</td>' for rslt in tsls])
    table += """
            </tr>
            <tr>
                <td>LIML</td>
    """
    table += "\n".join([f'<td>{rslt.params["EDUC"]:5.4f}</td>' for rslt in liml])
    table += """
            </tr>
            <tr>
                <td></td>
    """
    table += "\n".join([f'<td>({rslt.std_errors["EDUC"]:5.4f})</td>' for rslt in liml])
    table += """
            </tr>
            <tr>
                <td>F-statistic\n(excluded instruments)</td>
    """
    table += "\n".join(
        [f"<td>{f.fvalue[0][0]:5.4f}</td>" if f is not None else "<td></td>" for f in f_test]
    )
    table += """
            </tr>
            <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
            <tr>
                <td>Controls</td>
                <td></td><td></td><td></td><td></td><td></td><td></td>
            </tr>
            <tr>
                <td>Year of birth</td>
                <td>x</td><td>x</td><td>x</td><td>x</td><td>x</td><td>x</td>
            </tr>
            <tr>
                <td>State of birth</td>
                <td></td><td></td><td></td><td></td><td>x</td><td>x</td>
            </tr>
            <tr>
                <td>Age, age squared</td>
                <td></td><td>x</td><td></td><td>x</td><td></td><td>x</td>
            </tr>
            <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
            <tr>
                <td>Excluded instruments</td>
                <td></td><td></td><td></td><td></td><td></td>
            </tr>
            <tr>
                <td>Quarter-of-birth dummies</td>
                <td>x</td><td>x</td><td></td><td></td><td></td><td></td>
            </tr>
            <tr>
                <td>Quarter of birth * year of birth</td>
                <td></td><td></td><td>x</td><td>x</td><td>x</td><td>x</td>
            </tr>
            <tr>
                <td>Quarter of birth * year of birth</td>
                <td></td><td></td><td></td><td></td><td>x</td><td>x</td>
            </tr>
            <tr>
                <td>Number of Excluded instruments</td>
                <td>3</td><td>2</td><td>30</td><td>28</td><td>180</td><td>178</td>
            </tr>
        </tbody>
    </table>
    """

    return table


def create_weak_instruments_table_1(results, f_test, partial_rsquared):

    table = """
    <table>
        <thead>
            <tr>
                <th></th>
                <th>(1)</th>
                <th>(2)</th>
                <th>(3)</th>
                <th>(4)</th>
                <th>(5)</th>
                <th>(6)</th>
            </tr>
            <tr>
                <th></th>
                <th>OLS</th>
                <th>IV</th>
                <th>OLS</th>
                <th>IV</th>
                <th>OLS</th>
                <th>IV</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Coefficient</td>
    """
    table += "\n".join([f'<td>{rslt.params["EDUC"]:5.4f}</td>' for rslt in results])
    table += """
            </tr>
            <tr>
                <td></td>
    """
    table += "\n".join([f'<td>({rslt.bse["EDUC"]:5.4f})</td>' for rslt in results])
    table += """
            </tr>
            <tr>
                <td>F(excluded instruments)</td>
    """
    table += "\n".join(
        [f"<td>{f.fvalue[0][0]:5.4f}</td>" if f is not None else "<td></td>" for f in f_test]
    )
    table += """
            </tr>
            <tr>
                <td>Parital R squared (excluded instruments, x100)</td>
    """
    table += "\n".join(
        [
            f"<td>{r_sq * 100:5.4f}</td>" if r_sq is not None else "<td></td>"
            for r_sq in partial_rsquared
        ]
    )
    table += """
            </tr>
            <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
            <tr>
                <td>Age Control Variables</td>
                <td></td><td></td><td></td><td></td><td></td><td></td>
            </tr>
            <tr>
                <td>Age, age squared</td>
                <td>x</td><td>x</td><td></td><td></td><td>x</td><td>x</td>
            </tr>
            <tr>
                <td>9 Year of birth dummies</td>
                <td></td><td></td><td>x</td><td>x</td><td>x</td><td>x</td>
            </tr>
            <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
            <tr>
                <td>Excluded instruments</td>
                <td></td><td></td><td></td><td></td><td></td><td></td>
            </tr>
            <tr>
                <td>Quarter-of-birth dummies</td>
                <td></td><td>x</td><td></td><td>x</td><td></td><td>x</td>
            </tr>
            <tr>
                <td>Quarter of birth * year of birth</td>
                <td></td><td></td><td></td><td></td><td>x</td><td>x</td>
            </tr>
            <tr>
                <td>Number of Excluded instruments</td>
                <td></td><td>3</td><td></td><td>30</td><td></td><td>28</td>
            </tr>
        </tbody>
    </table>
    """

    return table


def create_weak_instruments_table_2(results, f_test, partial_rsquared):

    table = """
    <table>
        <thead>
            <tr>
                <th></th>
                <th>(1)</th>
                <th>(2)</th>
                <th>(3)</th>
                <th>(4)</th>
            </tr>
            <tr>
                <th></th>
                <th>OLS</th>
                <th>IV</th>
                <th>OLS</th>
                <th>IV</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Coefficient</td>
    """
    table += "\n".join([f'<td>{rslt.params["EDUC"]:5.4f}</td>' for rslt in results])
    table += """
            </tr>
            <tr>
                <td></td>
    """
    table += "\n".join([f'<td>({rslt.bse["EDUC"]:5.4f})</td>' for rslt in results])
    table += """
            </tr>
            <tr>
                <td>F(excluded instruments)</td>
    """
    table += "\n".join(
        [f"<td>{f.fvalue[0][0]:5.4f}</td>" if f is not None else "<td></td>" for f in f_test]
    )
    table += """
            </tr>
            <tr>
                <td>Parital R squared (excluded instruments, x100)</td>
    """
    table += "\n".join(
        [
            f"<td>{r_sq * 100:5.4f}</td>" if r_sq is not None else "<td></td>"
            for r_sq in partial_rsquared
        ]
    )
    table += """
            </tr>
            <tr>
                <td>Age Control Variables</td>
                <td></td><td></td><td></td><td></td>
            </tr>
            <tr>
                <td>Age, age squared</td>
                <td></td><td></td><td>x</td><td>x</td>
            </tr>
            <tr>
                <td>9 Year of birth dummies</td>
                <td>x</td><td>x</td><td>x</td><td>x</td>
            </tr>
            <tr><td></td><td></td><td></td><td></td><td></td></tr>
            <tr>
                <td>Excluded instruments</td>
                <td></td><td></td><td></td><td></td>
            </tr>
            <tr>
                <td>Quarter-of-birth dummies</td>
                <td></td><td>x</td><td></td><td>x</td>
            </tr>
            <tr>
                <td>Quarter of birth * year of birth</td>
                <td></td><td>x</td><td></td><td>x</td>
            </tr>
            <tr>
                <td>Quarter of birth * state of birth</td>
                <td></td><td>x</td><td></td><td>x</td>
            </tr>
            <tr>
                <td>Number of Excluded instruments</td>
                <td></td><td>180</td><td></td><td>178</td>
            </tr>
        </tbody>
    </table>
    """
    return table
