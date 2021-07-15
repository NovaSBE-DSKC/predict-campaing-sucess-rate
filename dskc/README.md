# dskc 

A library to automate tasks on a data science project pipeline.

### Read the data with `pandas`

```python
import pandas as pd
df = pd.read_csv("dataset.csv")
```

# Clean


```python
from dskc import dskc_clean
```


## One hot encode

```python
dskc_clean.one_hot_encode(df,"Category")
```

## Normalize data

```python
dskc_clean.normalize_data(df)
```

### Change data type

```python
# to integer
dskc_clean.column_to_int(dataframe, column_name)

# to date
dskc_clean.column_to_date(dataframe, column_name, format="%Y-%m-%d")

# to boolean
dskc_clean.column_to_bolean(dataframe, column_name)

# to binary
dskc_clean.column_to_binary(dataframe, column_name, target_true=True,false_value=False)

```




### Divide dataset into train and test

```python
train, test = dskc_clean.divide_in_train_test(df, 
                                              target="target_column", 
                                              target_true=True, 
                                              train_percentage=0.8)
```


#  Exploration

```python
from dskc import dskc_exploration
```

#### Data dictionary

```python
dskc_exploration.data_dictionary(df, filename="DataDictionary.csv", 
				                name="My dataset name", 
				                description="My dataset description")
```


### Summary

```python
dskc_exploration.summary(df)
```

### Basic exploration

```python
dskc_exploration.basic_exploration(df)
```



# Graphs

```python
from dskc import dskc_graphs

```
### All graphs 
```python
dskc_graphs.all_graphs(pd_dataframe, 
                       target='target_column',
                       target_true=TARGET_SUCCESS_VALUE)
```



### Numbers graphs:

```python
dskc_graphs.number_col(pd_dataframe, column_name,
                       target='target_column',
                       target_true=1)
```

*  histogram
* density plot 
*  histogram (without outliers)
* density plot (without outliers)


### Categoricals graphs:

```python
dskc_graphs.category_col(pd_dataframe, column_name,
	                     target='target_column',
	                     target_true=1)
```

* bars graph
* bars graphs with success proportion (if target)

### Boolean graphs:

```python
dskc_graphs.boolean_col(pd_dataframe, column_name,
                        target='target_column',
                        target_true=1)
```

* bars graph
* bars graphs with success proportion (if target)

### Text graphs:


```python
dskc_graphs.text_col(pd_dataframe, column_name,
                     target='target_column',
                     target_true=1)
```

* wordcloud
* top 15 words
* bars graphs of  success proportion for top 15 words (if target)

### Date graphs:

```python
dskc_graphs.date_col(pd_dataframe, column_name,
                     target='target_column',
                     target_true=1)
```


# Modeling

```python
from dskc import dskc_modeling

```

### Get x and y from dataframe, select the index that divides x from y 

```python
dskc_modeling.get_x_y(train_df, idx_divider=-2)

```
