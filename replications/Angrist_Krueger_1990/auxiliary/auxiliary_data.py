import pandas as pd


def process_data(data_name):
    if data_name == "cwhsa":
        data = pd.read_stata("data/cwhsa.dta").drop(columns=["vnms1", "ltax", "xltax", "ctr1"])
        data.columns = [
            "birth year",
            "ethnicity",
            "lottery interval",
            "earnings",
            "earnings variance",
            "sample size",
            "fraction zero earnings",
            "year",
        ]
        data.set_index(
            ["ethnicity", "birth year", "year", "lottery interval"], inplace=True, drop=True,
        )
    elif data_name == "cwhsb":
        data = pd.read_stata("data/cwhsb.dta").drop(columns=["vnms1", "ltax", "xltax", "ctr1"])
        data.columns = [
            "birth year",
            "ethnicity",
            "lottery interval",
            "earnings",
            "earnings variance",
            "sample size",
            "fraction zero earnings",
            "year",
            "data source",
        ]
        data.set_index(
            ["data source", "ethnicity", "birth year", "year", "lottery interval"],
            inplace=True,
            drop=True,
        )
    elif data_name == "cwhsc_new":
        data = pd.read_stata("data/cwhsc_new.dta")[
            ["byr", "race", "year", "type", "interval", "earnings", "ps_r"]
        ]
        data.columns = [
            "birth year",
            "ethnicity",
            "year",
            "data source",
            "lottery interval",
            "earnings",
            "probability of serving",
        ]
        data.set_index(
            ["data source", "ethnicity", "birth year", "year", "lottery interval"],
            inplace=True,
            drop=True,
        )

    return data
