from dskc import dskc_modeling
from dskc import dskc_graphs

from src.modeling import util

import numpy as np
import pickle
import settings

def load_scaler():
    file = settings.MODEL_PATH + 'normalization'
    min_max_scaler = pickle.load(open(file, 'rb'))
    return min_max_scaler

def _data_with_percentage_days(report,column):

    min_max_scaler=load_scaler()
    y_pred = report.y_pred_true

    # get x an y for test 
    x_test, y_test, feature_names = util.read_test_data()
    col_idx = {f:i for i,f in enumerate(feature_names)}

    # list of [percentage_elapsed_days, y_test, y_pred]
    data = []
    for i in range(len(x_test)):
        
        if column=="days_elapsed":
            array = [np.append(x_test[i],0)]
            value = min_max_scaler.inverse_transform(array)
            
            days = value[0][col_idx["days"]]
            days_elapsed= value[0][col_idx["days_elapsed"]]
            
            value = days-days_elapsed
            
        elif column=="backers":
            array = [np.append(x_test[i],0)]
            value = min_max_scaler.inverse_transform(array)
            value = value[0][col_idx["backers"]]
        
        else:
            value = x_test[i][col_idx[column]]*100
            
        data.append([value,y_test[i],y_pred[i]])
   
    # sort by percentage days elapsed
    data.sort(key=lambda x:x[0])
    return data

def _get_report(technique):
    # set model
    model = technique.load_model()

    # predict
    report = technique.test(model)
    
    return report

def _get_x_y_report(data, jump=0.01,max_pos=None):
    if max_pos==None:
        max_pos=1
    
    x = []
    y = []
    
    # build x and y for graph
    idx = 0
    x_pos = 0
    while data[idx][0]<x_pos-jump/2:
        idx+=1
        
    while x_pos < max_pos:
        y_data = []
        
        
        # get all the data between [current_jump-jump/2, current_jump+jump/2[
        while idx<len(data) and data[idx][0] >= x_pos-jump/2 and data[idx][0] < x_pos+jump/2:
            y_data.append(data[idx])
            idx+=1

        if y_data:
            
            y_true_values = np.asarray(list(map(lambda t:t[1],y_data)))
            y_pred_values = np.asarray(list(map(lambda t:t[2],y_data)))

            report = dskc_modeling.EvaluationReport(y_true_values, y_pred_values)

            x.append(x_pos)
            y.append(report)
        
        x_pos += jump
        
    return x,y
 
    
def error_by_time(technique,column,jump=0.01,max_pos=1):
    """
    @param technique: python module of the technique model trained
    """
    
    report = _get_report(technique)
    data = _data_with_percentage_days(report,column)
        
    x, y = _get_x_y_report(data, jump=jump,max_pos=max_pos)
 
    
    y = list(map(lambda x:x.mse,y))

    if column=="days_elapsed":
        column="Days to End"
        
    # display line graph
    dskc_graphs.line(x, y, 
                     xlabel=" ".join(column.split("_")).title(),
                     ylabel="Mean Squared Error",
                     title="Mean Squared Error along time")
    

def value_by_time(technique,column, jump=0.01,max_pos=1):
    """
    @param technique: python module of the technique model trained
    """

    report = _get_report(technique)
    data = _data_with_percentage_days(report,column)
    
    pos_data = list(filter(lambda x:x[1]==1,data))
    neg_data = list(filter(lambda x:x[1]==0,data))
    
    
    # financed
    x_pos, y_pos = _get_x_y_report(pos_data, jump=jump,max_pos=max_pos)
    y_pos = list(map(lambda x:sum(x.y_pred_true)/len(x.y_pred_true),y_pos))
    
    # non financed
    x_neg, y_neg = _get_x_y_report(neg_data, jump=jump,max_pos=max_pos)
    y_neg = list(map(lambda x:sum(x.y_pred_true)/len(x.y_pred_true),y_neg))
    
    # display line graph
    if column=="days_elapsed":
        column="Days to End"
        
    dskc_graphs.line([x_pos,x_neg], [y_pos, y_neg],multiple=True,legend=["Financed","Non Financed"],
                     xlabel=" ".join(column.split("_")).title(),
                     ylabel="Prediction",
                     title="Prediction by financed/non financed")

    
def by_variable(technique,column,jump=0.01,max_pos=1):
    error_by_time(technique,column,jump,max_pos)
    print("\n")
    value_by_time(technique,column,jump,max_pos)