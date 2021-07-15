
import pandas as pd

from dskc._util import df_to_list_w_column_idx


def unique_projects(df):
    """
    Meant to be used on the raw projects dataset
    :param df: raw projects' dataset
    :return: projects' dataset without duplicates and clean
    """

    df.drop_duplicates(inplace=True)
    ids = df.PID

    df[ids.isin(ids[ids.duplicated()])].sort_values(by=['PID'])
    df.drop_duplicates(subset='PID', keep="first", inplace=True)
    df.reset_index(drop=True, inplace=True)


def user_projects(df):
    data, c_idx, columns = df_to_list_w_column_idx(df)
    
    # for each project
    for i in range(len(data)):
        # get projects by the same user until now # todo improve efficiency
        same_user_projects = list(filter(lambda x: x[c_idx["UID"]] == data[i][c_idx["UID"]], data[:i]))

        # set number of user projects
        data[i][c_idx["USER_N_PROJECTS"]] = len(same_user_projects)

        # set number of user success projects
        financed_projects=list(filter(lambda x: x[c_idx["FINANCED"]] == 1, same_user_projects))
        data[i][c_idx["USER_N_SUCCESS_PROJECTS"]] = len(financed_projects)

    df = pd.DataFrame(data, columns=columns)
    return df
