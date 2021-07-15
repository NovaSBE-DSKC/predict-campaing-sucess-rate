import matplotlib.pyplot as plt

import numpy as np

from dskc._settings import colors
from dskc.visualization.graphs.types.util import set_titles


def autolabel(ax, rects, bins, horizontal=False,
              sum_data=1,
              percentage=False,
              value=True,
              flip=False):
    """
    Attach a text label above each bar displaying its height

    :param data:
    :param ax:
    :param horizontal:
    :param percentage: percentage on top
    :param value: bar value on top
    :return:
    """
    if not percentage and not value:
        return

    for i, rect in enumerate(rects):
        height = rect.get_height()

        text = ''
        if percentage:
            if bins > 10:
                text = '{0:.0f}%'.format(int(height) / sum_data * 100)
            else:
                text = '{0:.1f}%'.format(int(height) / sum_data * 100)
        if value:
            temp = '%d' % int(height)
            if percentage:
                text += "\n({})".format(temp)
            else:
                text = temp

        x = rect.get_x() + rect.get_width() / 2.

        if flip:
            if i == 0:
                y = 1.07 * height
                flip_size = y - height
            else:
                y = height + flip_size
        else:
            y = 1.05 * height

        ax.text(x, y,
                text,
                ha='center', va='bottom')

    # ser margins
    ax.margins(0.0, 0.25)


def set_xticks(xticks, xticks_rotation_horizontal):
    '''
    Set x axis names and rotation
    :param xticks:
    :param xticks_rotation_horizontal:
    :return:
    '''

    # x rotation
    if xticks_rotation_horizontal:
        xticks_rotation = 'horizontal'
    else:
        xticks_rotation = 'vertical'

    # set
    plt.xticks(np.arange(len(xticks)), xticks, rotation=xticks_rotation)


def set_settings(data, ax, rects, bins, horizontal, percentage_on_top, value_on_top, sum_data, title, xlabel, ylabel,
                 xticks, xticks_rotation_horizontal, flip):
    # set percentage on top of bar
    autolabel(ax, rects, bins, horizontal=horizontal,
              percentage=percentage_on_top, sum_data=sum_data,
              value=value_on_top, flip=flip)

    # titles
    set_titles(title, xlabel, ylabel, axis=ax)

    # set ticks
    if not xticks:
        xticks = data.keys()

    if flip:
        plt.gca().invert_yaxis()
        ax.xaxis.tick_top()

    set_xticks(xticks, xticks_rotation_horizontal)


def bars(data,
         sort_labels=False,
         horizontal=False,
         max_values=None,
         bins=False,
         percentage_on_top=False,
         value_on_top=False,
         title="",
         xlabel="",
         xticks=False,
         xticks_rotation_horizontal=False,
         ylabel="",
         flip=False,
         hline=False):
    # sort labels
    if sort_labels:
        data = data.sort_index()

    sum_data = sum(data)

    # select bins
    if max_values:
        data = data[:max_values]

    # re eindex
    data_index = data.index
    if str(data_index.dtype).find("int") >= 0:
        if len(data_index) == 2:
            if data_index[0] == 0 and data_index[1] == 1:
                data = data.rename(index={0: "False", 1: "True"})
            if data_index[0] == 1 and data_index[1] == 0:
                data = data.rename(index={0: "True", 1: "False"})

    # select type of graph
    ind = np.arange(len(data))  # the x locations for the groups
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects = ax.bar(ind, data.to_numpy(), width)

    if horizontal:
        ax = data.plot(kind='barh', color=colors.FIRST_COLOR)
    else:
        ax = data.plot(kind='bar', color=colors.FIRST_COLOR)

    # set settings
    set_settings(data, ax, rects, bins, horizontal,
                 percentage_on_top,
                 value_on_top,
                 sum_data,
                 title,
                 xlabel,
                 ylabel,
                 xticks,
                 xticks_rotation_horizontal,
                 flip)

    # horizontal line
    if hline:
        plt.axhline(y=0.5, color='black', linestyle='--')

    # show
    plt.tight_layout()
    plt.show()
