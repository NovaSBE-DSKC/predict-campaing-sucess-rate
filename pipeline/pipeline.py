from src.data_curation import datasets_creation
from src.modeling.models import nnet
from pipeline import util
import pickle
import settings
import os

MODEL = None
NORMALIZATION_MODEL = None
LDA_MODEL = None


def _setup_models():
  global NORMALIZATION_MODEL
  global LDA_MODEL
  global MODEL

  try:
    NORMALIZATION_MODEL = pickle.load(open(settings.NORMALIZATION_MODEL_PATH, 'rb'))
    print("Loaded normalization model: "+util.md5(settings.NORMALIZATION_MODEL_PATH))

    LDA_MODEL = pickle.load(open(settings.LDA_TOPICS_MODEL_PATH, 'rb'))
    print("Loaded lda model: " + util.md5(settings.LDA_TOPICS_MODEL_PATH))

    MODEL = nnet.load_model()
    print("Loaded neural network model: " + util.md5(settings.ML_MODEL_PATH))

  except:
    print("error loading models")
    pass


def train(projects_path, pledges_path, rewards_path, dataset_processed_path=settings.DATASET_PROCESSED_PATH):
  train, test = datasets_creation.create_train_test_dataset(projects_path=projects_path,
                                                            pledges_path=pledges_path,
                                                            rewards_path=rewards_path,
                                                            dataset_processed_path=dataset_processed_path,
                                                            save=True,
                                                            return_data=True)

  train_path = os.path.join(dataset_processed_path,"train.csv")
  test_path = os.path.join(dataset_processed_path,"test.csv")

  nnet.train(neurons=[3],
             epochs=20,
             retrain=None,
             optimizer="adadelta",
             train_path=train_path,
             test_path=test_path)

  _setup_models()


def predict(data):
  data_transform = util.transform_data(data, NORMALIZATION_MODEL, LDA_MODEL)
  value = nnet.predict(MODEL, data_transform)
  
  
  # project raised 
  if data["raised"] >= data["target"]:
    value = 1.00
    
  # min prediction
  elif value < 0.01:
    value = 0.01
  
  # project raised
  elif data["raised"] < data["target"] and value > 0.99:
    value = 0.99


  value = "{:.1f}".format(value*100)

  return value




_setup_models()

