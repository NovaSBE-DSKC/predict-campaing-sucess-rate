from src.data_curation import pre_processing
from dskc import dskc_clean
from src.data_curation.pre_processing.settings import REWARD_SLOTS
import warnings

import settings
import json

def _drop_columns(df,mantain_id):
    columns_to_exclude = [
        # dates
        'START',
        'START_YEAR',
        'END',
        'END_YEAR',
        # ids
        'URL',
        'UID_Pledges',
        'UID_Projects',
        # dates
        'PAYDATE',
        'PAYDATE_YEAR',
        'PAYDATE_MONTH',
        'PAYDATE_MONTH_sin',
        'PAYDATE_MONTH_cos',
        'PAYDATE_DAY',
        'PAYDATE_DAY_sin',
        'PAYDATE_DAY_cos',
        'PAYDATE_WEEKDAY',
        'PAYDATE_WEEKDAY_sin',
        'PAYDATE_WEEKDAY_cos',
        'PAYMETHOD',
        # pledge
        'AMOUNT',
        'UNCOND',
        'ANONYMOUS',
        'COMMENT',
        'COMMENT_LENGTH',
        'CITY',
        'COUNTRY',
        # text
        'TITLE',
        'PRJ_SUMMARY',
        "title_prj_summary"]

    if not mantain_id:
        columns_to_exclude.append("PID")

    df.drop(columns_to_exclude, axis=1, inplace=True)


    # unnamed drop
    dskc_clean.drop_unnamed(df)



def add_categories(df):
    # project summary
    dskc_clean.categories_from_word_series(df, "PRJ_SUMMARY", categories=9,
                                           stop_words=["projecto",
                                                       "apoio",
                                                       "ajuda",
                                                       "todos",
                                                       "projeto",
                                                       "objectivo",
                                                       "campanha",
                                                       "sobre",
                                                       "fazer",
                                                       "pretende",
                                                       "através",
                                                       "onde",
                                                       "forma",
                                                       "pessoas",
                                                       "ajudar",
                                                       "angariar",
                                                       "criar",
                                                       "fundos"])

    df = dskc_clean.one_hot_encode(df, "CAT_PRJ_SUMMARY")

    # title
    dskc_clean.categories_from_word_series(df, "TITLE", categories=10,
                                           stop_words=["novo",
                                                       "vamos",
                                                       "projeto",
                                                       "projecto",
                                                       "gravação",
                                                       "todos"])

    df = dskc_clean.one_hot_encode(df, "CAT_TITLE")

    return df



def save_features(df):
  features_list = list(df.columns)

  with open(settings.FEATURES_LIST_PATH, 'w') as f:
    json.dump(features_list, f)



def clean_model(df,
                pledges_path=settings.DATASET_PLEDGES_PATH,
                rewards_path=settings.DATASET_REWARDS_PATH,
                normalize=True,
                mantain_id=False,
                load_normalization=False):

    # clear python warning
    warnings.filterwarnings("ignore")

    # Remove duplicates
    pre_processing.unique_projects(df)

    # financed to binary
    dskc_clean.column_to_binary(df, "FINANCED", true_value="COMPLETED", false_value="NOT FINANCED")


    # drop columns
    df.drop([
        'LOCATION',
        'VIDEO_URL',
    ], axis=1, inplace=True)

    # user n projects
    df['USER_N_PROJECTS'] = 0

    # user n projects
    df['USER_N_SUCCESS_PROJECTS'] = 0

    # adding categories
    #print("Adding categories... ", end="")
    #df = add_categories(df)
    #print("done")

    # set sentiment analysis
    #print("Set sentiment analysis... ", end="")
    #dskc_clean.set_sentiment(df, "TITLE")
    #dskc_clean.set_sentiment(df, "PRJ_SUMMARY")
    #print("done")



    # user projects
    print("Calculating user projects... ", end="")
    df = pre_processing.user_projects(df)
    print("done")

    # merge with rewards
    print("Merging rewards... ", end="")
    pre_processing.rewards_merge(df,rewards_path)
    print("done")

    # merge with pledges
    print("Merging pledges... ", end="")
    df = pre_processing.pledges_merge(df, pledges_path)
    print("done")

    # drop projects with days == 0
    df.drop(df[df['DAYS'] == 0].index, inplace=True)

    # fill all days
    print("Filling days... ", end="")
    df = pre_processing.fill_days(df)
    print("done")

    # drop columns
    _drop_columns(df,mantain_id)

    # set percentages
    df['PERCENTAGE_RAISED'] = df['RAISED'] / df['TARGET']
    df["PERCENTAGE_TARGET_SELF_FUNDED"] = df['AMOUNT_SELF_FUNDED'] / df['TARGET']
    df['PERCENTAGE_DAYS_ELAPSED'] = df['DAYS_ELAPSED'] / df['DAYS']

    # estimate views along time
    df["VIEWS"] = df["VIEWS"] * df["PERCENTAGE_DAYS_ELAPSED"]

    # estimate comments along time
    df["COMMENTS"] = df["COMMENTS"] * df["PERCENTAGE_DAYS_ELAPSED"]

    # change indexes
    df = dskc_clean.change_index(df, "FINANCED", -1)
    df = dskc_clean.change_index_next_to(df, "PERCENTAGE_RAISED", "RAISED")
    df = dskc_clean.change_index_next_to(df, "DAYS_ELAPSED", "DAYS")
    df = dskc_clean.change_index_next_to(df, "PERCENTAGE_DAYS_ELAPSED", "DAYS_ELAPSED")
    df = dskc_clean.change_index_next_to(df, "AMOUNT_SELF_FUNDED", "PERCENTAGE_RAISED")
    df = dskc_clean.change_index_next_to(df, "PERCENTAGE_TARGET_SELF_FUNDED", "AMOUNT_SELF_FUNDED")
    df = dskc_clean.change_index_next_to(df, "BACKERS", "PERCENTAGE_RAISED")

    # rename columns
    dskc_clean.clean_columns_names(df)

    # remove nan samples
    df.dropna(inplace=True)

    if normalize:
            
        # normalize data
        df = dskc_clean.normalize_data(df,
                                     exclude=["percentage_days_elapsed", "percentage_raised"],
                                     filepath=settings.NORMALIZATION_MODEL_PATH,
                                     save=not load_normalization,
                                     load=load_normalization)

    # save feature list
    save_features(df)

    return df



