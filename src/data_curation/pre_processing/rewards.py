import settings
import pandas as pd

from dskc._util import df_to_list_w_column_idx
from src.data_curation.datasets import rewards_clean
from src.data_curation.pre_processing.settings import REWARD_SLOTS
from src.data_curation.datasets.rewards.clean import REWARDS_N_TOPICS

def rewards_merge(df,rewards_path):
    df_rewards = pd.read_csv(rewards_path,index_col=None)
    df_rewards = rewards_clean(df_rewards)


    # initialize reward slots
    df["N_REWARDS"] = 0
    for i in range(REWARD_SLOTS):
        df["REWARD_SLOT_{}_AMOUNT".format(i + 1)] = 0
        #df["REWARD_SLOT_{}_N_PLEDGES".format(i + 1)] = 0

        #df["REWARD_SLOT_{}_DOMINANT_TOPIC".format(i + 1)] = 0
        #df["REWARD_SLOT_{}_PROB_DOMINANT_TOPIC".format(i + 1)] = 0

        #for j in range(REWARDS_N_TOPICS):
        #    df["REWARD_SLOT_{}_TOPIC_{}".format(i+1,j + 1)] = 0

    # for each row
    for i in range(df.shape[0]):

        # get projects rewards sorted by amount
        project_rewards = df_rewards[df_rewards["PID"] == df["PID"][i]]
        project_rewards, c_idx, columns = df_to_list_w_column_idx(project_rewards)
        project_rewards.sort(key=lambda x: x[c_idx["AMOUNT"]])

        # for each reward
        for j, row_reward in enumerate(project_rewards):
            if j + 1 > REWARD_SLOTS:
                break

            df["REWARD_SLOT_{}_AMOUNT".format(j + 1)][i] = row_reward[c_idx["AMOUNT"]]

            # add topics
            #df["REWARD_SLOT_{}_DOMINANT_TOPIC".format(j + 1)][i] = row_reward[c_idx["title_description_dominant_topic"]]
            #df["REWARD_SLOT_{}_PROB_DOMINANT_TOPIC".format(j + 1)][i] = row_reward[c_idx["title_description_prob_dominant_topic"]]

            #for k in range(1,REWARDS_N_TOPICS+1):
            #    df["REWARD_SLOT_{}_TOPIC_{}".format(j+1,k)] =  row_reward[c_idx["title_description_topic_{}".format(k)]]

        df["N_REWARDS"][i] = min(len(project_rewards), REWARD_SLOTS)
