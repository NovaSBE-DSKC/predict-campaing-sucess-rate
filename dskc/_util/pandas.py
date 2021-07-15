def get_series_condition(df, column, condition):
    if condition is None:
        return df[column]
    else:
        return df[condition][column]


def df_to_list(df):
    '''
    Generates a dictionary with the column number and its label
    Returns dataframe as a numpy array and the dictionary described above
    #input: dataframe
    #return: numpy array, columns dictionary
    '''
    header = df.columns
    my_list = df.to_numpy().tolist()

    return header, my_list

def df_to_list_w_column_idx(df):
    columns = df.columns
    c_idx = {}
    for i, col in enumerate(columns):
        c_idx[col] = i

    data = df.to_numpy().tolist()

    return data, c_idx, columns


