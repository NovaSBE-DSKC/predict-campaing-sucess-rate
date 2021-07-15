from src.modeling import util
from src.modeling.models.neural_net import visualization, get_model, display_model, save_model

import pickle

HISTORYS_FILE = "historys_nn.sav"


def _test_model(neurons, x_train,y_train,x_test,y_test,epochs=10,):
    # get model
    input_size = x_train.shape[1]

    if len(y_train.shape) == 1:
        output_size = 1
    else:
        output_size = y_train.shape[1]

    model = get_model(input_size, output_size, neurons=neurons)
    display_model(model)

    # train
    history = model.fit(x_train, y_train,
                        validation_data=(x_test, y_test),
                        epochs=epochs,
                        batch_size=12,
                        verbose=0)

    return model, neurons, history.history


def test_models(init, final, sep=1, epochs=10):
    # read data
    x_train, y_train, _ = util.read_train_data()
    x_test, y_test, _ = util.read_test_data()

    historys = []
    for i in range(init, final + 1, sep):
        print("\nNeurons {} - start".format(i))

        model, neurons, history = _test_model([i], epochs, x_train, y_train,x_test, y_test)
        historys.append((neurons, history))

        save_model(model, sufix="_" + str(i))

        print("Neurons {} - done".format(i))

    pickle.dump(historys, open(HISTORYS_FILE, 'wb'))


def display_models_exploration():
    historys = pickle.load(open(HISTORYS_FILE, 'rb'))

    # graphs
    visualization.accuracy_graphs(historys)
    visualization.loss_graphs(historys)
    visualization.metrics_table(historys)


if __name__ == '__main__':
    test_models(1, 15, epochs=200)
