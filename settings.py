from dskc import get_root_path

ROOT_PATH = get_root_path()
DATASET_FOLDER_PATH = "/home/ppl/Documents/dataset/"

# raw
DATASET_RAW_PATH = DATASET_FOLDER_PATH + 'raw/'

DATASET_PATH = "{}{}".format(DATASET_RAW_PATH, "data-set.xlsx")

DATASET_PROJECTS_PATH = "{}{}".format(DATASET_RAW_PATH, "projects.csv")
DATASET_PLEDGES_PATH = "{}{}".format(DATASET_RAW_PATH, "pledges.csv")
DATASET_REWARDS_PATH = "{}{}".format(DATASET_RAW_PATH, "rewards.csv")
DATASET_REWARDS_PROCESSED_PATH = "{}{}".format(DATASET_RAW_PATH, "rewards-processed.csv")

# dataset processed
DATASET_PROCESSED_PATH = DATASET_FOLDER_PATH + "processed/"

DATASET_TRAIN_PATH = "{}{}".format(DATASET_PROCESSED_PATH, "train.csv")
DATASET_TEST_PATH = "{}{}".format(DATASET_PROCESSED_PATH, "test.csv")

# model
MODEL_PATH = ROOT_PATH + "/model/"

# models used on pre processing
ML_MODEL_PATH = MODEL_PATH + 'model.h5'
NORMALIZATION_MODEL_PATH = MODEL_PATH + 'normalization.sav'
LDA_TOPICS_MODEL_PATH = MODEL_PATH + "lda-projects-topics.sav"
COUNTRIES_LIST_PATH = MODEL_PATH + "countries-list.json"
FEATURES_LIST_PATH = MODEL_PATH + "features-list.json"
