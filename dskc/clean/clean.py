import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import TimeSeriesSplit, train_test_split
from IPython.display import clear_output
from sklearn.model_selection import train_test_split

from dskc.clean.columns import clean_columns_names, insert_next_to

import pickle

def replace_values(df, column, to_replace, value):
    '''

    :param df:
    :param column:
    :param to_replace:
    :param value:
    :return:
    '''

    values = []

    for v in df[column]:
        if v == to_replace:
            values.append(value)
        else:
            values.append(v)

    df[column] = values


def if_contains_to_binary(df, column):
    values = []
    for value in df[column]:
        if value != None and value != "":
            values.append(1)
        else:
            values.append(0)

    df[column] = values


def one_hot_encode(df, column):
    '''

    :param df: dataframe
    :param column: column name
    :return:
    '''
    # create one hot encoding dataframe
    one_hot = pd.get_dummies(df[column])

    # change colum names
    clean_columns_names(one_hot, prefix=column + "_")

    # drop column
    df = df.drop(column, axis=1)

    # Join the encoded df
    df = df.join(one_hot)

    return df


def replace_nan(df, column, value):
    df = df.replace({pd.np.nan: None})  # todo remove
    return df


def backtest(df, target_var, group_var, min_group_len=5):
    '''
    :param df:
    :param target_var:
    :param group_var:
    :return: X_train,X_test,y_train,y_test
    '''

    # Generating the time series split object from sciki-learn
    tscv = TimeSeriesSplit(n_splits=min_group_len)

    # Counter for the number of groups
    first = True

    # Selecting groups with at least the min time meassurements
    groups = list(df[group_var].value_counts().loc[df[group_var].value_counts().values > min_group_len].index)

    # Generating the split among groups with bigger length than the min
    # tscv allows for k-fold (code uses only the last k)
    for i, group in enumerate(groups):
        aux = df.loc[df[group_var] == group].reset_index()
        y = aux[target_var]
        X = aux.drop(target_var, axis=1)
        clear_output(wait=True)
        print('Group ID: ', group, ' current group percentage: ', round((i / len(groups)) * 100, 2), '%')

        # Generating the dataframe to return
        for train_index, test_index in tscv.split(X):
            X_train, X_test = X.loc[train_index], X.loc[test_index]
            y_train, y_test = y.loc[train_index], y.loc[test_index]
            if first:
                first = False
                X_train_all = X_train
                X_test_all = X_test
                y_train_all = y_train
                y_test_all = y_test
            else:
                X_train_all = pd.concat([X_train_all, X_train])
                X_test_all = pd.concat([X_test_all, X_test])
                y_train_all = pd.concat([y_train_all, y_train])
                y_test_all = pd.concat([y_test_all, y_test])

    return X_train_all, X_test_all, y_train_all, y_test_all


    
    

def divide_in_train_test(df, target_name=None,group_id=None, target=True, train_percentage=0.8, shuffle=True,groups=False,verbose=True):
    '''
    :param df: dataframe with na's and categorical variables
    :param target_name: target column name
    :param group_id: grouping id column name
    :param target: boolean to indicate if target_name will be provided
    :param train_percentage: percentage of dataset division between train and test
    :param suffle: sklearn parameter for shuffle dataframe before split
    :param groups: boolean to indicate f group_id will be provided
    :return: two dataframes for train and validation
    '''

    # split in train test
    if groups:
        #Converts the id variable into an integer
        df[group_id] = df[group_id].map(lambda x: int(x))
        #Generates unique values split
        unique_ids = df[group_id].unique()
        train_ids, test_ids = train_test_split(unique_ids,
                                            train_size=train_percentage,
                                            random_state=0,
                                            shuffle=shuffle)
        #Generating train and test datasets
        train = pd.merge(df,pd.Series(train_ids,name=group_id),left_on=group_id,right_on=group_id,how='right',validate="m:1")
        test = pd.merge(df,pd.Series(test_ids,name=group_id),left_on=group_id,right_on=group_id,how='right',validate="m:1")
        if verbose:
            print("The number of unique {}'s in the train data: {}".format(group_id,train_ids.shape[0]))
            print("The number of unique {}'s in the test data: {}".format(group_id,test_ids.shape[0]))
            print("-------------------------------------------------")

    
    elif target:
        x_train, x_test, y_train, y_test = train_test_split(df.drop(columns=[target_name]),
                                                        df[target_name],
                                                        train_size=train_percentage,
                                                        random_state=0,
                                                        shuffle=shuffle)
        # concat
        train = pd.concat([x_train, y_train], axis=1)
        test = pd.concat([x_test, y_test], axis=1)
        
        
    else:
        train,test = train_test_split(df,
                                            train_size=train_percentage,
                                            random_state=0,
                                            shuffle=shuffle)
    if verbose:
        print("Train is a dataframe of: {} rows and {} columns".format(train.shape[0],train.shape[1]))
        print("Test is a dataframe of: {} rows and {} columns".format(test.shape[0],train.shape[1]))
        

    return train, test


def normalize_data(df_original,exclude=[],filename=None,load=False):
    
    
    columns = list(df_original.columns)
         
    x = df_original.values  # returns a numpy array
    
    if load:
        min_max_scaler = pickle.load(open(filename, 'rb'))
    else:
        min_max_scaler = preprocessing.MinMaxScaler()
        min_max_scaler.fit(x)  # todo save min_max_scaller to pickle for production

        if filename != None:
            pickle.dump(min_max_scaler, open(filename, 'wb'))

    x_scaled = min_max_scaler.transform(x)
        
    df = pd.DataFrame(x_scaled, columns=columns)
    
    for col in exclude:
        df[col]=df_original[col]
    
    return df


def set_cyclical_features(df, column, cycle=None):
    """
    Set two new columns with the sin and cos of this cycle variable

    :param df: pandas dataframe
    :param column: column name
    :param cycle: number of values of a cycle, when None calculated automatic by (max value - min value + 1)
    :return:
    """
    if not cycle:
        cycle = df[column].max() - df[column].min() + 1

    alpha = 2 * np.pi * df[column] / cycle

    insert_next_to(df, column + '_cos', column, np.cos(alpha))
    insert_next_to(df, column + '_sin', column, np.sin(alpha))
