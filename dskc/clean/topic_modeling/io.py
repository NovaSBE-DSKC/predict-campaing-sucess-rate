import pickle




def save_model(model,path):
    print("saving model... ", end="")
    pickle.dump(model, open(path, 'wb'))


def load_model(path):
    try:
        return pickle.load(open(path, 'rb'))
    except:
        return None
