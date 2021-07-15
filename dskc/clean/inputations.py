from dskc._util.pandas import df_to_list_w_column_idx
import pandas as pd
import numpy as np
import math

def _linear_inputation(data,c_idx,column,date_column,start_idx,end_idx):
    
    start_row=data[start_idx]
    end_row=data[end_idx]
    
    # start sample 
    start_time = start_row[c_idx[date_column]]
    start_value = start_row[c_idx[column]]
    
    # end sample
    end_time = end_row[c_idx[date_column]]
    end_value = end_row[c_idx[column]]
    
    # diffs
    diff_values = end_value - start_value
    diff_time = (end_time - start_time).days
    
    # for each sample in the middle of start and end indexes
    for j in range(start_idx + 1, end_idx):
        time_passed = (data[j][c_idx[date_column]] - start_time).seconds
        if diff_time == 0:
            percentage_time_passed = 0
        else:
            percentage_time_passed = time_passed / diff_time

        # set value
        data[j][c_idx[column]] = start_value + diff_values * percentage_time_passed

    return data
    
def grouped_inputation_mean_by_date(df, column, group_by, date):
    data, c_idx, columns = df_to_list_w_column_idx(df)

    i = 0
    # iterate over patients, each cylce is all medical appintsments of a patient
    while i < len(data):
        
        patient_id = data[i][c_idx["id"]]
        
        # skip first misisng values
        while i < len(data) and patient_id == data[i][c_idx["id"]] and not data[i][c_idx[column]]:
            i+=1
            
        # real value
        start_idx=i 
        missing_founded = False

        # For each medical appointent of the patient
        while i < len(data) and patient_id == data[i][c_idx["id"]]:

            # found missing value
            if math.isnan(data[i][c_idx[column]]):
                missing_founded = True

            else:  # real value
                
                if missing_founded: # we had previous missing value
                    end_idx = i
                    data = _linear_inputation(data,c_idx,column,date,start_idx,end_idx)    
                
                start_idx = i
                missing_founded = False

            i += 1
    

    return pd.DataFrame(data, columns=columns)


def bfill_if(df,column,grouped_by,value):
    data, c_idx, columns = df_to_list_w_column_idx(df)

    i = 0
    # iterate over ids
    while i < len(data):
        
        patient_id = data[i][c_idx[grouped_by]]
        
        
        # real value
        start_idx = i 
        missing_founded = False

        # For each sample of the id
        while i < len(data) and patient_id == data[i][c_idx[grouped_by]]:
            
            sample_value = data[i][c_idx[column]]
            
            # found missing value
            if math.isnan(sample_value):
                
                # set start index
                if not missing_founded:
                    start_idx = i
                    
                missing_founded = True

            else:  # real value
                
                # check condition to do backward fill
                if missing_founded and value == sample_value: # we had previous missing value
                    end_idx = i
                    
                    # backward fill
                    for j in range(start_idx,end_idx):
                        data[j][c_idx[column]]=sample_value
                
                
                missing_founded = False

            i += 1
    

    return pd.DataFrame(data, columns=columns)