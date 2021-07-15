from keras.layers import Dropout
from keras.layers import Dense
from keras.models import Sequential
from keras.models import load_model as keras_load_model
from keras.utils.vis_utils import plot_model
import settings

FILENAME = settings.MODEL_PATH + "model"
EXTENSION = ".h5"


def set_layers(model, neurons, inpt_size, outpt_size):
    # perceptron
    if len(neurons) == 0:
        model.add(Dense(outpt_size, activation='sigmoid', input_dim=inpt_size))
        return

    # hidden layer
    for i, neuron in enumerate(neurons):
        if i == 0:
            # first layer
            model.add(Dense(neuron, input_dim=inpt_size, activation='relu'))
        else:
            model.add(Dropout(0.3))
            model.add(Dense(neuron, activation='relu'))

    # output layer
    model.add(Dense(outpt_size, activation='sigmoid'))


def get_model(inpt_size, outpt_size, neurons=[10], optimizer="adadelta"):
    # init
    model = Sequential()

    set_layers(model, neurons, inpt_size, outpt_size)

    # train
    # loss: mean_squared_error, binary_crossentropy
    # optimizers: sgd, adam, adadelta
    model.compile(loss='mean_squared_error',
                  optimizer=optimizer,
                  metrics=['accuracy'])

    return model


def save_model(model, sufix=""):
    filename = FILENAME + sufix + EXTENSION
    print("saving model... ", end="")
    model.save(filename)
    print("done")
    print("Saved as {}".format(filename))


def load_model(sufix=""):
    return keras_load_model(FILENAME + sufix + EXTENSION)


def display_model(model):
    plot_model(model, to_file=FILENAME + '_neural_net.png', show_shapes=True, show_layer_names=True)
