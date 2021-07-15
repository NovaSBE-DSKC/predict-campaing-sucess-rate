from sklearn.linear_model import LinearRegression

from src.modeling import util
from src.modeling.models.linear_regression.model import save_model
from src.modeling.models.timer import Timer


def train():
    # read data
    x_train, y_train, feature_names = util.read_train_data()

    # model
    model = LinearRegression()

    # train
    timer = Timer()
    model.fit(x_train, y_train)
    timer.end()

    # save
    save_model(model)

    return model
