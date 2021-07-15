'''
Cleanning data algorithms
'''
import settings
from src.data_curation.datasets.pledges import pre_processing
from dskc import dskc_clean

import pandas as pd


def projects_merge(df):
    df_projects = pd.read_excel(settings.DATASET_PATH, sheet_name="PROJECTS")
    channel = pre_processing.get_channel(df, df_projects)
    df["CHANNEL"] = channel


def clean(df, merge_projects=False):
    # remove columns
    df = df.drop(columns=["IID"])

    # paydate
    dskc_clean.replace_values(df, "PAYDATE", " ", None)
    df = dskc_clean.delete_row_column_is_nan(df, "PAYDATE")

    # add dates
    dskc_clean.to_timestamp(df, "PAYDATE",format="%Y-%m-%d %H:%M:%S")
    dskc_clean.add_dates(df, "PAYDATE")

    # paymethod
    dskc_clean.replace_values(df, "PAYMETHOD", " ", None)

    # anonymous
    dskc_clean.replace_values(df, "ANONYMOUS", " ", 1)
    dskc_clean.column_to_int(df, "ANONYMOUS")

    # comment
    dskc_clean.replace_values(df, "COMMENT", " ", None)
    dskc_clean.replace_nan(df, "COMMENT", None)

    # comment_length
    data = dskc_clean.get_str_length(df, "COMMENT")
    dskc_clean.insert_next_to(df, "COMMENT_LENGTH", "COMMENT", data)

    # city
    dskc_clean.replace_values(df, "CITY", " ", None)
    dskc_clean.replace_nan(df, "CITY", None)

    # country
    dskc_clean.replace_nan(df, "COUNTRY", None)
    dskc_clean.replace_values(df, "COUNTRY", " ", None)

    if merge_projects:
        projects_merge(df)

    return df



