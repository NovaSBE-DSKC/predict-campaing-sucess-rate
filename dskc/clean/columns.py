def clean_columns_names(df, prefix=""):
    '''
    Modifications inplace

    :param df:
    :return:
    '''
    old_new_dict = {}

    for col in df.columns:
        new_value = col.strip().lstrip().replace(" ", "_").lower()
        old_new_dict[col] = prefix + new_value

    df.rename(columns=old_new_dict, inplace=True)


def change_index(df, column, index):
    '''
    :param df:
    :param column:
    :param index:
    :return:
    '''
    re_idx = []
    if index < 0:
        index = len(df) + 1 - index

    index = index + 1

    for col in df.columns:
        if col == column:
            continue

        re_idx.append(col)

    re_idx.insert(index, column)

    df = df[re_idx]

    return df


def change_index_next_to(df, column_name, next_to_column):
    # search for the column
    for i, column in enumerate(df.columns):
        if column == next_to_column:
            # insert column
            return change_index(df, column_name, i)


def insert_next_to(df, new_column, left_column, data):
    # search for the column
    for i, column in enumerate(df.columns):
        if column == left_column:
            # insert column
            df.insert(i + 1, new_column, data)
            return

    # add to the end if not found the column
    df[new_column] = data


def drop_unnamed(df):
    delete_columns = []

    for col in df.columns:
        if col.lower().startswith("unnamed"):
            delete_columns.append(col)

    df.drop(delete_columns, axis=1, inplace=True)
