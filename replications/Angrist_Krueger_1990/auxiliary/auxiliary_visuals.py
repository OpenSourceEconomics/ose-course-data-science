"""Function to create the shades of grey Table 1 and function to create significance stars."""
import numpy as np
import pandas as pd


def background_negative_green(val):
    """
    Change the background color of a cell in DataFrame according to its value.

    Parameters
    ----------
    val : float
        single cell value in a pandas DataFrame.

    Returns
    -------
    str
        return background color for the cell of pandas DataFrame.

    """
    if val == "":
        color = "white"
    elif val < -200:
        color = "#009900"
    elif -200 <= val < -150:
        color = "#00cc00"
    elif -150 <= val < -100:
        color = "#80ff80"
    elif -100 <= val < -50:
        color = "#b3ffb3"
    elif -50 <= val < 0:
        color = "#e6ffe6"
    else:
        color = "white"

    return f"background-color: {color}"


def p_value_star(data, rows, columns):
    """
    Add a star to values that are statistically significant to the 5 percent level.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame for which the stars should be added.
    rows : tuple
        The row index using slices.
    columns : tuple
        The column index using slices.

    Returns
    -------
    data : pd.DataFrame
        Returns the original DataFrame with significance stars.

    """
    if isinstance(data.loc[rows, columns], pd.Series):
        data_temp = data.loc[rows, columns].to_frame()
        for index in np.arange(0, data_temp.shape[0], 2):
            if abs(data_temp.iloc[index] / data_temp.iloc[index + 1])[0] > 1.96:
                data_temp.iloc[index] = str(data_temp.iloc[index][0]) + "*"
            else:
                pass
    else:
        data_temp = data.loc[rows, columns]

        for index in np.arange(0, data_temp.shape[0], 2):
            for column in np.arange(0, data_temp.shape[1]):
                if abs(data_temp.iloc[index, column] / data_temp.iloc[index + 1, column]) > 1.96:
                    data_temp.iloc[index, column] = str(data_temp.iloc[index, column]) + "*"
                else:
                    pass

    data.loc[rows, columns] = data_temp

    return data
