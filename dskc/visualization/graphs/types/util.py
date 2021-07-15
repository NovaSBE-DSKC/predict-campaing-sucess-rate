import matplotlib.pyplot as plt


def set_titles(title="", xlabel="", ylabel="", axis=None):
  if axis is None:
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
  else:
    axis.set_title(title)
    axis.set_xlabel(xlabel)
    axis.set_ylabel(ylabel)
