
from sklearn.model_selection import RandomizedSearchCV,GridSearchCV
from xgboost import XGBRegressor,XGBClassifier

from src.modeling import util
from src.modeling.models.timer import Timer
from src.modeling.models.xgboost.model import save_model

import multiprocessing
import numpy as np

def find_best_model():
    
    # set number of jobs given the n cpus
    n_cpus = multiprocessing.cpu_count()
    n_jobs = max(1,int(n_cpus/3)) 
    
    # set model
    model = XGBClassifier(random_state=0)
    
    
    # set hyper parameters
    param_dist = {
        'learning_rate':  [0.1, 0.01],
        'n_estimators': [300, 500, 1000],
        'learning_rate':  [6, 10],
    }
    
    # set ramdomized searc1
    n_iter = 1
    model = RandomizedSearchCV(model,
                             n_jobs=n_jobs,
                             param_distributions=param_dist, 
                             n_iter=n_iter,
                             random_state=0,
                             verbose=1)


    return model


def train(search=True):
    # read data
    x_train, y_train, feature_names = util.read_train_data()
    
    #todo correct
    x_train[np.isinf(x_train)] = 1
    y_train[np.isinf(y_train)] = 1
    
    np.nan_to_num(x_train)
    np.nan_to_num(y_train)
    
    
    x_train = x_train.astype(np.float32)
    y_train = y_train.astype(np.float32)
    
    # set model
    if search:
        model = find_best_model()
    else:
        model = XGBRegressor()

    # train
    timer = Timer()
    model.fit(x_train, y_train)
    timer.end()

    # save
    save_model(model)

    return model
