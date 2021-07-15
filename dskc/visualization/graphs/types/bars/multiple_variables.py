import matplotlib.pyplot as plt

from dskc._settings import colors
from dskc.visualization.graphs.types import util
import numpy as np


def bars_mean_y_grouped_by(df,
                           column_y,
                           column_x,
                           title="",
                           xlabel="",
                           ylabel="",
                           horizontal=False):

  data = df.groupby(column_x).mean()[column_y]

  x_values = data.keys().to_numpy()
  y_values = data.to_numpy()

  # sort
  y_values, x_values = zip(*sorted(zip(y_values, x_values)))

  # bar graph
  index = range(len(x_values))
  if horizontal:
    plt.barh(x_values, y_values, color=colors.FIRST_COLOR)
    plt.yticks(index, x_values)
  else:
    plt.bar(x_values, y_values, color=colors.FIRST_COLOR)
    plt.xticks(index, x_values)

  # layout
  plt.tight_layout()

  # titles
  if horizontal:
    util.set_titles(title, ylabel, xlabel)
  else:
    util.set_titles(title, xlabel, ylabel)

  plt.show()


def bars_grouped(data1, data2, title="", xlabels=[], graph_labels=[], xtick_vertical=False, sort_labels=True):
  if sort_labels:
    data1 = data1.sort_index()
    data2 = data2.sort_index()

  data1 = data1.value_counts()
  data2 = data2.value_counts()

  #reorder data 2 to use same keys
  data2 = data2.reindex(data1.keys().to_numpy())

  N = len(data1)
  ind = np.arange(N)  # the x locations for the groups
  width = 0.35  # the width of the bars

  fig, ax = plt.subplots()

  # types of bars
  p1 = ax.bar(ind, data1, width, color=colors.FIRST_COLOR)
  p2 = ax.bar(ind + width, data2, width, color=colors.SECOND_COLOR)

  # set titles
  if not xlabels:
    xlabels = data1.keys().to_numpy()

  ax.set_title(title)
  ax.set_xticks(ind + width / 2)
  ax.set_xticklabels(xlabels)

  if xtick_vertical:
    for ax in fig.axes:
      plt.sca(ax)
      plt.xticks(rotation=90)

  ax.legend((p1[0], p2[0]), graph_labels)
  ax.autoscale_view()

  plt.show()
