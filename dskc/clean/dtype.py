import pandas as pd


def column_to_int(df, column):
    values = []
    for v in df[column]:
        values.append(int(v))

    df[column] = values


def column_to_date(df, column, format="%Y-%m-%d"):
    try:
        df[column] = pd.to_datetime(df[column])
    except:
        df[column] = pd.to_datetime(df[column], format=format)


def column_to_boolean(df, column):
    values = []
    for v in df[column]:
        values.append(bool(v))

    df[column] = values


def column_to_binary(df, column, true_value=True, false_value=False):
    values = []
    for value in df[column]:
        if value == true_value:
            values.append(1)
        elif value == false_value:
            values.append(0)
        else:
            values.append(value)

    df[column] = values
