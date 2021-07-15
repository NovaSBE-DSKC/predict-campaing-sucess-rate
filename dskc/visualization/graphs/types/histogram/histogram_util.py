def autolabel(ax, heights, bins, horizontal=False, sum_data=1, percentage=False, value=False):
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

  initial_width = heights[1][0]
  width = abs(heights[1][1] - initial_width)

  for i, height in enumerate(heights[0]):
    text = ''
    if percentage:
      percentage_value = height / sum_data * 100
      if bins > 10:
        text = '{0:.0f}%'.format(percentage_value)
      else:
        text = '{0:.1f}%'.format(percentage_value)

    if value:
      temp = '%d' % int(height)
      if percentage:
        text += "\n({})".format(temp)
      else:
        text = temp

    x = (i) * width + width / 2 + initial_width
    y = 1.05 * height

    ax.text(x, y,
            text,
            ha='center', va='bottom')

  # ser margins
  ax.margins(0.0, 0.25)
