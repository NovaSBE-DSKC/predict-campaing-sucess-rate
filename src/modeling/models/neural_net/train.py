'''
Trainning algorithms
'''

from src.modeling import util
from src.modeling.models.neural_net import visualization
from src.modeling.models.neural_net.model import get_model,save_model,display_model
from src.modeling.models.timer import Timer
import settings

def train(neurons=[10],
          epochs=50,
          retrain=None,
          optimizer="adadelta",
          train_path=settings.DATASET_TRAIN_PATH,
          test_path=settings.DATASET_TEST_PATH):

    # read data
    print(train_path)
    x_train, y_train, feature_names = util.read_train_data(path=train_path)
    x_test, y_test, feature_names = util.read_test_data(path=test_path)

    # get model
    if retrain is None:
        # get model
        input_size = x_train.shape[1]

        if len(y_train.shape) == 1:
            output_size = 1
        else:
            output_size = y_train.shape[1]

        model = get_model(input_size, output_size, neurons=neurons, optimizer=optimizer)
    else:
        model = retrain

    # train
    timer = Timer()
    history = model.fit(x_train, y_train,
                        validation_data=(x_test, y_test),
                        epochs=epochs,
                        batch_size=12)
    timer.end()
    # graphs
    #visualization.accuracy__graph(history.history)
    #visualization.model_loss_graph(history.history)

    # save model
    save_model(model)

    return model


if __name__ == '__main__':
    train()
