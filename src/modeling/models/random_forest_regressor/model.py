import pickle

import settings

FILENAME = settings.MODEL_PATH + 'random_forest_regressor.sav'


def save_model(model):
    print("saving model... ", end="")
    pickle.dump(model, open(FILENAME, 'wb'))
    print("done")


def load_model():
    loaded_model = pickle.load(open(FILENAME, 'rb'))
    return loaded_model
