'''
Cleanning data algorithms
'''

from dskc import dskc_clean
from dskc import dskc_util
import settings

REWARDS_N_TOPICS = 5

def get_stop_words():
    from dskc import get_root_path
    
    # read from file
    file ="{}/src/data_curation/datasets/rewards/stop_words.txt".format(get_root_path())
    with open(file, "r") as f:
        return f.read().splitlines()
    
    
def clean(df):
    # drop columns
    df.drop([
        'REWARD_ID',
    ], axis=1, inplace=True)

    # rename PROJECT ID
    df = df.rename(columns={"PROJECT_ID": "PID"})

    # topic modeling
    df["title_description"] = df["TITLE"].fillna("") + " " + df["DESCRIPTION"].fillna("")
    
    """
    print("Rewards calc topics... ",end="")
    timer= dskc_util.Timer()
    lda_file = "{}lda-rewards-{}.sav".format(settings.MODEL_PATH,REWARDS_N_TOPICS)
    dskc_clean.topic_modeling(df,"title_description",
                              n_components=REWARDS_N_TOPICS,
                              path=lda_file,
                              stop_words=get_stop_words())
    timer.end(prefix="done in ")
    """
    return df

