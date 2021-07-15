MIN = 0.05
MAX = 0.95


def no_correlation_lables(df):
  labels = df.columns.values
  values = df.to_numpy()

  mins = []

  # for each row
  for i, row in enumerate(values):
    is_min = True

    # for each value
    for j, value in enumerate(row):

      # ignore diagonal
      if i == j:
        continue

      is_min = abs(value) <= MIN and is_min

    if is_min:
      mins.append(labels[i])

  return mins
