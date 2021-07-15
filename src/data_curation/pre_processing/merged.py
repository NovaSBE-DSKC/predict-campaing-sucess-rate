import pandas as pd

from dskc._util import df_to_list_w_column_idx
from src.data_curation.pre_processing.settings import REWARD_SLOTS


def _clear_row(row, c_idx):
    row[c_idx["RAISED"]] = 0
    row[c_idx["BACKERS"]] = 0
    row[c_idx["COMMENTS"]] = 0
    row[c_idx["VIEWS"]] = 0
    row[c_idx["AMOUNT_SELF_FUNDED"]] = 0

    #for i in range(REWARD_SLOTS):
    #    row[c_idx["REWARD_SLOT_{}_N_PLEDGES".format(i + 1)]] = 0


def fill_from_to(start_day, end_day, new_data, sample, c_idx):
    row = sample.copy()

    if start_day == 0:
        # clear row to have 0 values on raised ...
        _clear_row(row, c_idx)

    # change elapsed days from start day to end
    for i in range(start_day, end_day):
        new_sample = row.copy()
        new_sample[c_idx["DAYS_ELAPSED"]] = i

        new_data.append(new_sample)

    return new_data


def _fill_project(data, c_idx, new_data, i):
    # first pledge
    current_plg = data[i]

    # get project fixed variables
    pid = current_plg[c_idx["PID"]]

    i += 1
    # get pledges from project
    project_pledges = [current_plg]
    while i < len(data) and pid == data[i][c_idx["PID"]]:
        if project_pledges[-1][c_idx["DAYS_ELAPSED"]] == data[i][c_idx["DAYS_ELAPSED"]]:
            project_pledges[-1] = data[i]
        else:
            project_pledges.append(data[i])

        i += 1

    n_days = current_plg[c_idx["DAYS"]]
    # current_plg_days = current_plg[c_idx["DAYS_ELAPSED"]]

    # fill past until the first pledge
    # if current_plg_days > 0:
    #    i, new_data = fill_from_to(0, current_plg_days, new_data, current_plg, c_idx, i)

    start_day = 0
    for current_plg in project_pledges:
        days_elapsed = current_plg[c_idx["DAYS_ELAPSED"]]

        # fill from [current pledge,next pledge[
        new_data = fill_from_to(start_day,
                                days_elapsed,
                                new_data,
                                current_plg,
                                c_idx)

        start_day = days_elapsed

    # fill to the end
    new_data = fill_from_to(project_pledges[-1][c_idx["DAYS_ELAPSED"]], n_days, new_data, current_plg, c_idx)

    return i, new_data


def fill_days(df):
    # dataframe to lists
    data, c_idx, columns = df_to_list_w_column_idx(df)

    new_data = []

    i = 0
    # for each project
    while i < len(data):
        i, new_data = _fill_project(data, c_idx, new_data, i)

    return pd.DataFrame(new_data, columns=columns)
