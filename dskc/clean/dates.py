from datetime import datetime
import math

from pandas._libs.tslibs.nattype import NaTType
from pandas._libs.tslibs.timestamps import Timestamp

from dskc.clean import set_cyclical_features
from dskc.clean.columns import insert_next_to


def days_diff_columns(df, column_start, column_stop, date_format="%d-%m-%Y", timestamp=False):
    values = []

    # for each row
    for i, start_date in enumerate(df[column_start]):

        # convert if needed to another object type
        date_type = type(start_date)
        # timestamp number
        if date_type == float:
            start_date = datetime.fromtimestamp(start_date)
            end_date = datetime.fromtimestamp(df[column_stop][i])

        # string
        elif date_type == str:
            start_date = datetime.strptime(start_date, date_format)
            end_date = datetime.strptime(df[column_stop][i], date_format)
        else:
            end_date = df[column_stop][i]

        # subtract dates
        diff_date = end_date - start_date

        # add date
        values.append(diff_date.days)

    return values


def to_timestamp(df, column, format="%d-%m-%Y"):
    '''

    :param df:
    :param column:
    :param format: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
    :return:
    '''
    values = []

    for v in df[column]:
        if not v:
            values.append(None)
            continue

        temp = datetime.strptime(v, format)
        values.append(temp.timestamp())

    df[column] = values

    return df


def _map_timestamps(series, f):
    '''
    Applies a function to each element of the series.
    The elements are filtered given the object type.

    :param series: pandas series
    :param f: lambda funtion
    :return: lambda function of each vale
    '''
    values = []

    for v in series:
        value_type = type(v)
        if not v or (type(v) is float and math.isnan(v)) or value_type == NaTType:
            values.append(None)
            continue

        if value_type == Timestamp:
            datetime_object = v
        else:
            datetime_object = datetime.fromtimestamp(v)

        values.append(f(datetime_object))

    return values


def get_year(series):
    '''

    :param series: pandas series
    :return: array of years
    '''
    values = _map_timestamps(series, lambda x: int(x.year))
    return values


def get_month(series):
    '''

    :param series: pandas series
    :return: array of months
    '''

    values = _map_timestamps(series, lambda x: int(x.month))
    return values


def get_day(series):
    '''

    :param series: pandas series
    :return: array of days
    '''

    values = _map_timestamps(series, lambda x: int(x.day))
    return values


def get_weekday(series):
    '''

    :param series: pandas series
    :return: array of weekdays
    '''

    values = _map_timestamps(series, lambda x: int(x.weekday()))
    return values


def add_dates(df, column, year=True, month=True, day=True, weekday=True):
    '''

    :param df: pandas dataframe
    :param column: column name of timestamp column
    :param year: if column with years is to be added
    :param month: if column with months is to be added
    :param day: if column with days is to be added
    :param weekday: if column with weekdays is to be added
    :return:
    '''
    series = df[column]

    if weekday:
        column_name = column + "_WEEKDAY"
        insert_next_to(df, column_name, column, get_weekday(series))
        set_cyclical_features(df, column_name, cycle=7)

    if day:
        column_name = column + "_DAY"
        insert_next_to(df, column_name, column, get_day(series))
        set_cyclical_features(df, column_name, cycle=31)

    if month:
        column_name = column + "_MONTH"
        insert_next_to(df, column_name, column, get_month(series))
        set_cyclical_features(df, column_name, cycle=12)

    if year:
        insert_next_to(df, column + "_YEAR", column, get_year(series))
