from dskc import dskc_clean
from dskc import dskc_util
from src.data_curation import pre_processing

import settings
import os

PROJECTS_N_TOPICS = 6

def get_stop_words():
    from dskc import get_root_path

    # read from file
    file = os.path.join(get_root_path(), "src","data_curation","datasets","rewards","stop_words.txt")
    with open(file, "r") as f:
        return f.read().splitlines()




def clean(df):
    # FINANCED (STATUS)
    df = df.rename(columns={"STATUS": "FINANCED"})

    # CHANNEL
    dskc_clean.replace_values(df, "CHANNEL", " ", None)
    dskc_clean.if_contains_to_binary(df, "CHANNEL")

    # START
    dskc_clean.to_timestamp(df,"START",format="%Y-%m-%d")
    dskc_clean.add_dates(df, "START")

    # END
    dskc_clean.to_timestamp(df, "END", format="%Y-%m-%d")
    dskc_clean.add_dates(df, "END")

    # DAYS, diff of dates START and END
    days = dskc_clean.days_diff_columns(df, "START", "END", timestamp=True)
    dskc_clean.insert_next_to(df, "DAYS", "END_WEEKDAY", days)

    # IMAGES
    dskc_clean.replace_values(df, "IMAGES", " ", 0)

    # FACEBOOK
    dskc_clean.replace_values(df, "FACEBOOK", " ", None)
    dskc_clean.if_contains_to_binary(df, "FACEBOOK")

    # TITLE_LENGTH
    data = dskc_clean.get_str_length(df, "TITLE")
    dskc_clean.insert_next_to(df, "TITLE_LENGTH", "TITLE", data)

    # cat one hot encoded
    df = dskc_clean.one_hot_encode(df, "CAT")

    # Working the Location
    print("Calculating countries... ", end="")
    df = pre_processing.set_countries(df)
    print("done")

    # topic modeling
    df["title_prj_summary"] = df["TITLE"] + " " + df["PRJ_SUMMARY"].fillna("")

    print("Calculating topics... ", end="")
    timer = dskc_util.Timer()
    dskc_clean.topic_modeling(df,
                              "title_prj_summary",
                              n_components = PROJECTS_N_TOPICS,
                              stop_words=get_stop_words(),
                              path=settings.LDA_TOPICS_MODEL_PATH,
                              save=True,
                              visualize=False,
                              dominant_topic=False,
                             )


    timer.end(prefix="done in ")



    return df
