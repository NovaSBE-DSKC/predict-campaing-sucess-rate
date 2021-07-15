'''
Data audit and exploration (descriptive statistics of the data)
'''
import pandas as pd

import settings
from src.data_curation.datasets import clean
from dskc import dskc_exploration



def pipeline():
  df = pd.read_excel(settings.DATASET_PATH, sheet_name="PLEDGES")

  # clean data
  df = clean(df)

  # basic exploration visualization
  dskc_exploration.basic_exploration(df)


if __name__ == '__main__':
  pipeline()
