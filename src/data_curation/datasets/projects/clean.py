'''
Cleanning data algorithms
'''
import settings
from src.data_curation.datasets.projects import pre_processing
from dskc import dskc_clean
import pandas as pd

 

def remove_uncond_channels(df):
    channels_uncond = ["PPL Causas",
                       "WACT"
                       "Fundão Funding",
                       "Tempos Brilhantes",
                       "Terra dos Sonhos",
                       "Maratona da Saúde",
                       "IES-SBS",
                       "Fundação EDP",
                       "Giving Tuesday"]

    df['CHANNEL'].replace(channels_uncond, " ", regex=True, inplace=True)
    return df

def pledges_processing(df):
  df_pledges = pd.read_excel(settings.DATASET_PATH, sheet_name="PLEDGES")

  # PERCENTAGE SELF FUNDED
  amount_raised, percentage_self_funded = pre_processing.get_raised_and_percentage_self_funded(df, df_pledges)
  dskc_clean.insert_next_to(df, "AMOUNT_SELF_FUNDED", "PERCENTAGE_RAISED", amount_raised)
  dskc_clean.insert_next_to(df, "PERCENTAGE_TARGET_SELF_FUNDED", "AMOUNT_SELF_FUNDED", percentage_self_funded)


def clean(df,pledges=True):

    # FINANCED (STATUS)
    df = df.rename(columns={"STATUS": "FINANCED"})

    # CHANNEL
    df = remove_uncond_channels(df)
    dskc_clean.replace_values(df, "CHANNEL", " ", None)
    dskc_clean.if_contains_to_binary(df, "CHANNEL")

    # START
    dskc_clean.add_dates(df, "START")

    # END
    dskc_clean.add_dates(df, "END")

    # DAYS, diff of dates START and END
    days = dskc_clean.days_diff_columns(df, "START", "END", timestamp=True)
    dskc_clean.insert_next_to(df, "DAYS", "END_WEEKDAY", days)

    # PERCENTAGE_RAISED
    percentage_raised = pre_processing.get_percentage_raised(df)
    dskc_clean.insert_next_to(df, "PERCENTAGE_RAISED", "RAISED", percentage_raised)

    # IMAGES
    dskc_clean.replace_values(df, "IMAGES", " ", 0)

    # FACEBOOK
    dskc_clean.replace_values(df, "FACEBOOK", " ", None)
    dskc_clean.if_contains_to_binary(df, "FACEBOOK")

    # TITLE_LENGTH
    data = dskc_clean.get_str_length(df, "TITLE")
    dskc_clean.insert_next_to(df, "TITLE_LENGTH", "TITLE", data)
    
    

    # SET DF PLEDGES
    if pledges:
        pledges_processing(df)

    # COUNTRY
    # countries = pre_processing.get_countries(df, "LOCATION")
    # df["COUNTRY"] = countries

    # DROP drop columns
    df = df.drop(columns=["URL", "PID", "UID"])

    return df


