from src.modeling import util
import numpy as np
from dskc import dskc_modeling


def test(model):
    x_test, y_test, _ = util.read_test_data()

    # predict
    y_pred = model.predict(x_test)

    # clean
    y_pred = np.asarray([x[0] for x in y_pred])

    # evaluate
    report = dskc_modeling.EvaluationReport(y_test, y_pred, name="Neural Network")

    return report

def predict(model,data):
    data = np.array(data,ndmin=2)
    y_pred = model.predict(data)    
    value = y_pred[0][0]
    return value
