
def df_column_map(df, column, function):
  values = []

  for v in df[column]:
    values.append(function(v))

  return values
