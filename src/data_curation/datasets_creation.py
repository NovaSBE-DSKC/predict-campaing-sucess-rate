'''
Create training and test dataset
'''

import settings
from src.data_curation.clean import clean
from src.data_curation.clean_model import clean_model
from dskc import dskc_clean

import pandas as pd
import os

def save_data(train,
              test,
              dataset_processed_path=None):

  if dataset_processed_path is None:
    train_path = settings.DATASET_TRAIN_PATH
    test_path = settings.DATASET_TEST_PATH
  else:
    train_path = os.path.join(dataset_processed_path,"train.csv")
    test_path = os.path.join(dataset_processed_path, "test.csv")

  print("Saving...", end=" ")
  train.to_csv(train_path, index=False)
  test.to_csv(test_path, index=False)
  print("done")


def get_train_test(projects_path, pledges_path, rewards_path):
  # read dataframe
  df = pd.read_csv(projects_path, index_col=None)
  df = clean(df)

  # divide into train and test
  train, test = dskc_clean.divide_in_train_test(df, "FINANCED", shuffle=False)
  
  # clean data
  train = clean_model(train, pledges_path, rewards_path, normalize=True)
  test = clean_model(test, pledges_path, rewards_path, load_normalization=True,normalize=True)

  return train, test


def create_train_test_dataset(projects_path=settings.DATASET_PROJECTS_PATH,
                              pledges_path=settings.DATASET_PLEDGES_PATH,
                              rewards_path=settings.DATASET_REWARDS_PATH,
                              dataset_processed_path=None,
                              save=True,
                              return_data=False):

  train, test = get_train_test(projects_path, pledges_path, rewards_path)

  if save:
    save_data(train, test, dataset_processed_path)

  if return_data:
    return train, test


if __name__ == '__main__':
  create_train_test_dataset()
