def delete_row_column_is_nan(df, column):
  '''

  :param df: pandas dataframe
  :param column: column name
  :return: dataframe without nan types
  '''
  
  df = df.dropna(subset=[column])
  return df
