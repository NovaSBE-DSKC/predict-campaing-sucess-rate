from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV

from src.modeling import util
from src.modeling.models.random_forest_regressor.model import save_model
from src.modeling.models.timer import Timer

import numpy as np
import multiprocessing

def _get_param_dist():
     
    # Number of trees in random forest
    n_estimators = [int(x) for x in np.linspace(start=20, stop=2000, num=10)]

    # Number of features to consider at every split
    max_features = ['auto', 'sqrt']

    # Maximum number of levels in tree
    max_depth = [int(x) for x in np.linspace(10, 110, num=11)]
    max_depth.append(None)

    # Minimum number of samples required to split a node
    min_samples_split = [2, 5, 10]

    # Minimum number of samples required at each leaf node
    min_samples_leaf = [1, 2, 4]

    # Method of selecting samples for training each tree
    bootstrap = [True, False]

    # Create the random grid
    param_tuning = {
        'n_estimators': n_estimators,
        'max_features': max_features,
        'max_depth': max_depth,
        'min_samples_split': min_samples_split,
        'min_samples_leaf': min_samples_leaf,
        'bootstrap': bootstrap
    }

    return param_tuning

def find_best_model():
    
    # set number of jobs goven the n cpus
    n_cpus = multiprocessing.cpu_count()
    n_jobs = max(1,int(n_cpus/3)) 
    
    # set model
    model=RandomForestRegressor(random_state=0)
    
    # set hyperparameters
    param_dist = _get_param_dist()
    
    # set ramdomized search
    n_iter = 1
    model = RandomizedSearchCV(model,
                               n_jobs=n_jobs, 
                               param_distributions=param_dist, 
                               verbose=1,
                               n_iter=n_iter)

    return model


def train(search=True):
    # read data
    x_train, y_train, feature_names = util.read_train_data()

    # model
    if search:
        model=find_best_model()
    else:
        model = RandomForestRegressor()

    # train
    timer = Timer()
    model.fit(x_train, y_train)
    timer.end()

    if search:
        print("\nBest parameters:\n")
        for param in model.best_params_:
            print("{}: {}".format(param,model.best_params_[param]))
        print()

    # save
    save_model(model)

    return model
