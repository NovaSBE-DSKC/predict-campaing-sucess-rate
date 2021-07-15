from dskc.visualization.graphs.types.bars import bars_util

def bars(data,
         sort_labels=False,
         horizontal=False,
         max_values=None,
         bins=False,
         percentage_on_top=True,
         value_on_top=False,
         data_processed=False,
         title="",
         xlabel="",
         xticks=False,
         xticks_rotation_horizontal=False,
         flip=False,
         ylabel="Ocurrences"):
  '''
  Bars graph, horizontal or vertical
  :param series:
  :param sort_labels:
  :param horizontal:
  :param bins:
  :param percentage_on_top: true by default
  :param title:
  :param xlabel:
  :param xticks:
  :param xticks_rotation_horizontal:
  :param ylabel:
  :return: bars graph
  '''

  # values count
  if not data_processed:
      data = data.value_counts()

  bars_util.bars(data,
                 sort_labels=sort_labels,
                 horizontal=horizontal,
                 max_values=max_values,
                 bins=bins,
                 percentage_on_top=percentage_on_top,
                 value_on_top=value_on_top,
                 title=title,
                 xlabel=xlabel,
                 xticks=xticks,
                 flip=flip,
                 xticks_rotation_horizontal=xticks_rotation_horizontal,
                 ylabel=ylabel)
