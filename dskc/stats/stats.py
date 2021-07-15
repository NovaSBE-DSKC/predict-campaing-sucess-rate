import numpy as np


def mean_std(data):
  mean = sum(data) / len(data)
  std = np.std(data)

  return mean, std


def min_max(data):
  min_value = min(data)
  max_value = max(data)

  return min_value, max_value


def show_stats_number(data):
  mean, std = mean_std(data)
  print("Mean: {}".format(mean))
  print("Standard Deviation: {}".format(std))

  min_value, max_value = min_max(data)
  print("Min: {}".format(min_value))
  print("Max: {}".format(max_value))


def show_stats(df, label):
  data = df[label]
  dtype = str(data.dtype)

  if dtype.find("int") >= 0 or dtype.find("float") >= 0:
    show_stats_number(data)
  else:
    pass
    # show_stats_categories(data)


def reject_outliers(data, m=2):
  '''

  :param data: numpy array
  :param m: std multiplier
  :return: data with no outliers based on std
  '''
  return data[abs(data - np.mean(data)) < m * np.std(data)]


def reject_outliers_percentile(data,index=False):
    '''
    :param data: numpy array
    :return: data with no outliers, values are between 25% and 75% percentiles
    '''
    
    len_data=len(data)
    data=np.sort(data)
    return data[int(len_data*0.25):int(len_data*0.75)]
    
    
    p25 = np.percentile(data, 25)
    p75 = np.percentile(data, 75)

    data = data[(data >= p25) & (data <= p75)]
    return data
