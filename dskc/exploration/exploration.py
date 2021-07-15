from dskc.exploration.visualization import show_exploration
import pandas as pd


def summary(df, dataframe=True):
  '''

  :param df: dataframe
  :return: table of:
   column name
   type of object
   number of distinct values
   unique values (showsa a maximum of 3 unique values)
   missing values
  '''

  data_types = df.dtypes
  applied = df.apply(lambda x: [x.unique()])
  columns = df.columns
  missing_values = df.isna().mean().round(4) * 100

  header = ["Column",
            "Type",
            "Distinct values",
            "Values",
            "% Missing"]

  matrix = [header, ]

  max_var_length = 30

  # for each column
  for i in range(len(columns)):

    # build example values
    distinct = applied[i][0]
    len_applied = len(distinct)

    j = 0
    sum_text = 0
    example_unique_values = []
    while j < len_applied:
      sum_text += len(str(distinct[j]))
      if sum_text > max_var_length:
        example_unique_values.append("...")
        break
      example_unique_values.append(distinct[j])
      j += 1

    # build row
    row = [columns[i],
           str(data_types[i]),
           len_applied,
           example_unique_values,
           missing_values[i]]

    matrix.append(row)

  # return with dataframe format
  if dataframe:
    return pd.DataFrame(matrix[1:],columns=matrix[0])

  return matrix


def basic_exploration(df, histograms=[]):
  '''

  :param df: dataframe
  :return: shows a basic exploration of the dataframe
  '''

  pd.set_option('display.max_columns', None)
  pd.set_option('display.max_rows', None)

  data_head = df.head()
  columns = summary(df,dataframe=False)
  n_samples = df.shape[0]

  corr_pearson = df.corr(method='pearson')

  show_exploration(df, data_head, columns, n_samples, corr_pearson, histograms)
