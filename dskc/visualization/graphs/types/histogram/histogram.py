import matplotlib.pyplot as plt
import numpy as np

from dskc._settings import colors
from dskc.stats import dskc_stats
from dskc.visualization.graphs.types.histogram import histogram_util
from dskc.visualization.graphs.types.util import set_titles


def histogram(series,
              title="",
              xlabel="",
              ylabel="",
              save=False,
              bins=15,
              range=None,
              no_outliers=False,
              percentage_on_top=False,
              value_on_top=False,
              xticks=None):
  # get data type
  dtype = str(series.dtype)

  # continue if not number
  if not (dtype.find("int") >= 0 or dtype.find("float") >= 0):
    return

  # data
  data = series.to_numpy()

  # remove outliers
  if no_outliers:
    data = dskc_stats.reject_outliers_percentile(data)

  # mu and sigma calc
  mean, std = dskc_stats.mean_std(data)

  # min and max calc
  min_value, max_value = dskc_stats.min_max(data)

  # set graph title
  graph_title = title
  graph_title += "\n\n mean = {0:.2f}     ".format(mean)
  graph_title += "min = {0:.2f}\n     ".format(min_value)
  graph_title += "std = {0:.2f}     ".format(std)
  graph_title += "max = {0:.2f}".format(max_value)

  ind = np.arange(len(data))  # the x locations for the groups

  fig, ax = plt.subplots()
  rects = ax.hist(data, bins=bins, color=colors.SECOND_COLOR)

  # sum data
  sum_data = rects[0].sum()

  # set percentage on top of bar
  histogram_util.autolabel(ax, rects, bins, percentage=percentage_on_top, value=value_on_top, sum_data=sum_data)

  # titles
  set_titles(graph_title, xlabel, ylabel, axis=ax)

  # set ticks
  if not xticks:
    xticks = series.keys()

  # save
  if save:
    plt.savefig("graph_hist_{}.png".format(title))

  # show
  plt.tight_layout()
  plt.show()
