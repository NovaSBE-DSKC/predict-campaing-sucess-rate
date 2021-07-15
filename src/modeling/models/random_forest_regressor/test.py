from src.modeling import util
from dskc import dskc_modeling

def test(model):
    # read data
    x_test, y_test, _ = util.read_test_data()

    # predict
    y_pred = model.predict(x_test)

    # evaluate
    report = dskc_modeling.EvaluationReport(y_test, y_pred,name="Random Forest Regressor",to_binary=True)

    return report