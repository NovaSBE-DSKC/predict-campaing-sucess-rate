from src.modeling import util
from dskc import dskc_modeling
import numpy as np


def test(model):
    # read data
    x_test, y_test, _ = util.read_test_data()

    # predict
    y_pred = model.predict(x_test)

    # clean
    array = []
    for x in y_pred:

        if x < 0:
            array.append(0)
        elif x > 1:
            array.append(1)
        else:
            array.append(x)

    y_pred = np.asarray(array)

    # evaluate
    report = dskc_modeling.EvaluationReport(y_test, y_pred, name="Bayesian Ridge")

    return report
