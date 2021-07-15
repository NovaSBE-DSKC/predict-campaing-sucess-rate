import pandas as pd
import settings
from dskc import dskc_modeling


def _read_x_y(path, target):
    # read data
    data = pd.read_csv(path,index_col=False)

    # get x and y
    x, y = dskc_modeling.get_x_y(data, target=target)

    # get feature names
    feature_names = x.columns

    return x.values, y.values, feature_names


def read_train_data(target="financed", path=settings.DATASET_TRAIN_PATH):
    return _read_x_y(path, target=target)


def read_test_data(target="financed",path=settings.DATASET_TEST_PATH):
    return _read_x_y(path, target=target)
