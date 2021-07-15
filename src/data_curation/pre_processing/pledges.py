import settings
import pandas as pd

from dskc._util import df_to_list_w_column_idx
from src.data_curation.datasets import pledges_clean
import numpy as np



def pledges_merge(df,pledges_path):
    df_pledges = pd.read_csv(pledges_path,index_col=None)
    df_pledges = pledges_clean(df_pledges)

    df = pd.merge(df, df_pledges,
                  suffixes=('_Projects', '_Pledges'),
                  left_on='PID',
                  right_on='PID',
                  how='left',
                  validate="1:m")

    df.sort_values(by=['PID', 'PAYDATE'], inplace=True)

    return feature_creation(df)


def _set_rewards(data, c_idx, rewards, amount, index, last_is_same_prj):
    # for each reward
    for i, r in enumerate(rewards):
        if amount >= r:

            # can be the next reward
            if i + 1 < len(rewards) and amount >= rewards[i + 1]:
                continue

            # add reward
            if last_is_same_prj:
                n_pledges = data[index - 1][c_idx["REWARD_SLOT_{}_N_PLEDGES".format(i + 1)]] + 1
            else:
                n_pledges = 1

            # set reward
            data[index][c_idx["REWARD_SLOT_{}_N_PLEDGES".format(i + 1)]] = n_pledges
            break


def _set_percentage_self_funded(data, c_idx, index, last_is_same_prj):
    # if pledge has same UID that project
    if data[index][c_idx["UID_Projects"]] == data[index][c_idx["UID_Pledges"]]:
        amount_self_funded = 0

        # sum the last self funded
        if last_is_same_prj:
            amount_self_funded += data[index - 1][c_idx["AMOUNT_SELF_FUNDED"]]

        amount_self_funded += data[index][c_idx["AMOUNT"]]

        # set amount
        data[index][c_idx["AMOUNT_SELF_FUNDED"]] = amount_self_funded


def feature_creation(df):
    # set new features default
    df['RAISED'] = 0
    df["BACKERS"] = 0
    df['DAYS_ELAPSED'] = 0
    df["AMOUNT_SELF_FUNDED"] = 0

    data, c_idx, columns = df_to_list_w_column_idx(df)

    rewards = []
    n_backers = 0
    raised = 0

    # for each pledge
    for i in range(len(data)):
        amount = data[i][c_idx['AMOUNT']]

        # project without pledges
        if np.isnan(amount):
            continue

        if i == 0 or data[i][c_idx['PID']] != data[i - 1][c_idx['PID']]:  # new project

            # set rewards
            rewards = []
            n_rewards = data[i][c_idx["N_REWARDS"]]

            for j in range(n_rewards):
                rewards.append(data[i][c_idx["REWARD_SLOT_{}_AMOUNT".format(j + 1)]])

            raised = amount
            n_backers = 1

            last_is_same_prj = False

        else:
            raised += amount
            n_backers += 1

            last_is_same_prj = True

        _set_percentage_self_funded(data, c_idx, i, last_is_same_prj)
        #_set_rewards(data, c_idx, rewards, amount, i, last_is_same_prj)

        # set calculated variables
        data[i][c_idx["BACKERS"]] = n_backers
        data[i][c_idx['RAISED']] = raised

        days = int((data[i][c_idx['PAYDATE']] - data[i][c_idx['START']]) / 86400)  # divide all seconds in a day
        data[i][c_idx['DAYS_ELAPSED']] = days

    return pd.DataFrame(data, columns=columns)
