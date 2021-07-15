import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def matshow(corr):
  '''
  used for pearson correlation graph
  :param corr:
  :return:
  '''

  # Generate a mask for the upper triangle
  mask = np.zeros_like(corr, dtype=np.bool)
  mask[np.triu_indices_from(mask)] = False

  # Set up the matplotlib figure
  f, ax = plt.subplots(figsize=(11, 9))

  # Generate a custom diverging colormap
  cmap = sns.diverging_palette(220, 10, as_cmap=True)

  # Draw the heatmap with the mask and correct aspect ratio
  sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1.0, vmin=-1, center=0,
              square=True, linewidths=.5, cbar_kws={"shrink": .5})

  plt.show()
