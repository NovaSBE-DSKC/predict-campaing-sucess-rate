import pandas as pd


def cols_with_missing(df):
  cols_with_missing = [col for col in df.columns
                       if df[col].isnull().any()]
  return cols_with_missing


def object_columns(df):
  series = ((df.dtypes == 'object') | (df.dtypes == 'bool') & (df.dtypes != 'datetime64[ns]'))
  return list(series[series].index)


def num_columns(df):
  series = ((df.dtypes != 'object') & (df.dtypes != 'bool') & (df.dtypes != 'datetime64[ns]'))
  return list(series[series].index)


def date_columns(df):
  series = (df.dtypes == 'datetime64[ns]')
  return list(series[series].index)


def _object_table(df, columns):
  data = {'Column Name': [],
          'Count': [],
          'Top': [],
          'Freq': [],
          '% Missing': []
          }

  for col in columns:
    describe = df[col].describe()

    data["Column Name"].append(col)
    data["Count"].append(describe[0])
    data["Top"].append(describe[2])
    data["Freq"].append(describe[3])
    data["% Missing"].append((df[col].isnull().sum() / df.shape[0] * 100))

  return pd.DataFrame(data)


def _number_table(df, columns):
  data = {'Column Name': [],
          'Mean': [],
          'Standard Deviation': [],
          'Minimum': [],
          '25%': [],
          '50%': [],
          '75%': [],
          'Maximum': [],
          '% Missing': []
          }

  for col in columns:
    describe = df[col].describe()

    data["Mean"].append(describe[1])
    data["Standard Deviation"].append(describe[2])
    data["Minimum"].append(describe[3])
    data["25%"].append(describe[4])
    data["50%"].append(describe[5])
    data["75%"].append(describe[6])
    data["Maximum"].append(describe[7])
    data["Column Name"].append(col)
    data["% Missing"].append((df[col].isnull().sum() / df.shape[0] * 100))

  return pd.DataFrame(data)


def _dates_table(df, columns):
  data = {'Column Name': [],
          'Count': [],
          'Unique': [],
          'Top': [],
          'Freq': [],
          'First': [],
          'Last': [],
          '% Missing': []}

  for col in columns:
    describe = df[col].describe()

    data["Count"].append(describe[0])
    data["Unique"].append(describe[1])
    data["Top"].append(describe[2])
    data["Freq"].append(describe[3])
    data["First"].append(describe[4])
    data["Last"].append(describe[5])
    data["Column Name"].append(col)
    data["% Missing"].append((df[col].isnull().sum() / df.shape[0] * 100))

  return pd.DataFrame(data)


def summary_statistics_tables(df, only_missing=False):

  if only_missing:
    missing_cols = cols_with_missing(df)
    df = df[missing_cols]

  objects = object_columns(df)
  numbers = num_columns(df)
  dates = date_columns(df)

  object_data = number_data = date_data = []

  if objects:
    object_data = _object_table(df, objects)

  if numbers:
    number_data = _number_table(df, numbers)

  if dates:
    date_data = _dates_table(df, dates)

  return object_data, number_data, date_data
