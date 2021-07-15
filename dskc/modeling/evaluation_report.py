import itertools

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pandas.api.types import CategoricalDtype
from plotnine import *

from sklearn.metrics import mean_squared_error, recall_score, f1_score, precision_score, log_loss, accuracy_score, \
    confusion_matrix, classification_report, r2_score, roc_curve,auc

from dskc.visualization import graphs
from dskc.visualization import terminal
from dskc._settings import colors
def summary_class_metrics(y,y_pred):
    return pd.DataFrame({'Accuracy':accuracy_score(y,y_pred),
                        'Precision':precision_score(y,y_pred),
                        'Recall':recall_score(y,y_pred),
                        'F1 score':f1_score(y,y_pred)},index=['Performance metrics'])


def evaluate(model, features, labels,model_name="",regressor=False):
    predictions = model.predict(features)
    
    if regressor:
        metric = mean_squared_error(predictions, labels)
        perf_metric='MSE'
        
    else:
        metric = accuracy_score(predictions, labels)
        perf_metric='Accuracy'  
    pars = model.get_params()
    print('{} model performance'.format(model_name.title()))
    print('{} = {:0.2f}%.'.format(perf_metric,metric*100))
    
    return metric,predictions,pd.DataFrame(zip(pars.keys(),pars.values()),columns=['Hyperparameter','Value'])


def df_conf_matrix(y,y_pred):
    #sklearn method
    conf_matrix = confusion_matrix(y,y_pred)
    #dskc works with numpy
    pd.Series(y_pred).value_counts()
    #confussion matrix to pandas df
    cf_mat=pd.DataFrame(conf_matrix) 
    #adding total of actual classes
    cf_mat_1=pd.concat([cf_mat,pd.Series(y,name='Target').value_counts()],axis=1)
    #adding total of predicted classes
    negative=cf_mat_1[0].sum()
    postive=cf_mat_1[1].sum()
    total=cf_mat_1['Target'].sum()
    last_row=pd.DataFrame({0:negative,
                 1:postive,
                 'Target':total},
                index=['Target'])
    #concatenate last row
    pandas_conf_matrix=pd.concat([cf_mat_1,last_row],sort=False)
    #enhancing labels
    return pandas_conf_matrix.rename_axis("Predicted Class",axis="columns").rename_axis("Actual Class",axis="rows")


def pd_roc(y,y_pred):
    fpr, tpr, thresholds = roc_curve(y,y_pred, pos_label=1)
    # Transform the output into a pandas DataFrame
    ROC_dataframe=pd.concat([pd.Series(fpr),
               pd.Series(tpr),
               pd.Series(thresholds)],sort=False,axis=1).rename(columns={0:'FPR',
                                                                         1:'TPR',
                                                                         2:'thresholds'})
    # Calculate the area under the ROC curve
    AUC=auc(fpr,tpr)
    return ROC_dataframe,AUC


def to_cat(roc_df,y_pred):
    """
    :usage:  random forest regressor for binary classification
    :aim: converts y predicted into binary categories
    :returns: pandas series
    :input: roc df from roc function
    """
    
    #filtering the threshold with higheest tpr
    trshd = roc_df.loc[roc_df['TPR']==max(roc_df['TPR'])]['thresholds'].iloc[0]
    
    #generating binario variable
    y_pred = pd.Series(y_pred,name="y_pred").map(lambda x:1 if x>=trshd else 0)
    
    return y_pred,trshd
    

def roc_plot(df,auc):
    graph = (ggplot(df)         # defining what data to use
     + aes(x='FPR',y='TPR')    # defining what variable to use ,fill='thresholds'
     + geom_point(color = colors.OFICIAL_COLORS[1],size=.1) # defining the type of plot to use + stat_smooth(color = "darkorange", se = False)
     + geom_abline(slope=1, intercept=0,linetype = "dashed",color=colors.OFICIAL_COLORS[3])
     + ggtitle("Reciever Operating Characteristic curve")
     + geom_label(
        label="AUC ="+str(round(auc,2)), 
        x=.35,
        y=.55 
      )
     + ylab("True Positive Rate (TPR)")
     + xlab("False Positive Rate (FPR)")
     + theme_bw()
     + theme(
                axis_line_x=element_line(color='gray'),
                axis_line_y=element_line(color='gray'),
                line=element_line(color='white')
            )       

    )
    # show
    graph.draw()
    plt.show()

class EvaluationReport():

    def __init__(self, y_test, y_pred, to_binary=True, name=""):
        y_pred = y_pred.astype(np.float64)

        self.name = name
        self.to_binary = to_binary
        self.y_pred_true = y_pred

        if self.to_binary:
            # Converting predictions to label
            y_pred = [round(x) for x in y_pred]

        self.y_test = y_test
        self.y_pred = y_pred

        self._set_performance_metrics()
        self._set_error_metrics()

    def _set_performance_metrics(self):
        self.accuracy = accuracy_score(self.y_test, self.y_pred) * 100
        self.precision = precision_score(self.y_test, self.y_pred) * 100
        self.recall = recall_score(self.y_test, self.y_pred) * 100
        self.f1 = f1_score(self.y_test, self.y_pred) * 100

    def _set_error_metrics(self):
        self.mse = mean_squared_error(self.y_test, self.y_pred_true)
        if len(set(self.y_test))>1:
            self.cross_entropy = log_loss(self.y_test, self.y_pred_true)
        self.r2 = r2_score(self.y_test, self.y_pred_true)

    def display_performance_errors(self):
        terminal.markdown_h3("Performance Metrics and Errors")
        print()
        terminal.markdown_table([self.table_header(), self.table_row()])

    def display_classification_report(self):
        print("\n")
        terminal.markdown_h3("Classification Report")
        print()
        print(classification_report(self.y_test, self.y_pred))
        print("\n\n")

    def display_predictions(self):
        terminal.markdown_h3("Predictions")
        print()
        series = pd.Series(self.y_pred_true)
        graphs.histogram(series, title="Predicted Values Histogram", percentage_on_top=True)
        print("\n\n")

    def display_prediction_success(self):
        terminal.markdown_h3("Predictions Accuracy")
        print()

        data = {}
        data["True"] = [x for x in self.y_test]
        data["Pred."] = self.y_pred

        correct = []
        for i in range(len(self.y_test)):
            correct.append(self.y_test[i] == self.y_pred[i])

        data["Correct"] = correct

        df = pd.DataFrame(data=data)

        graphs.bars_target_proportion(df, "Pred.", target="Correct", hline=False, sort_labels=True,
                                      value_on_top=True)

    def display(self):

        self.display_performance_errors()
        self.display_classification_report()
        self.display_predictions()
        self.display_prediction_success()

    def plot_confusion_matrix(self, y_true, y_pred, class_names):
        cf = confusion_matrix(y_true, y_pred)

        plt.imshow(cf, cmap=plt.cm.Blues)

        plt.title("Confusion Matrix")

        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')

        tick_marks = np.arange(len(class_names))

        plt.xticks(tick_marks, class_names)
        plt.yticks(tick_marks, class_names)

        thresh = cf.max() / 2.

        for i, j in itertools.product(range(cf.shape[0]), range(cf.shape[1])):
            plt.text(j, i, cf[i, j], horizontalalignment='center', color='white' if cf[i, j] > thresh else 'black')

        plt.colorbar()

    def table_row(self):
        return [self.name,
                round(self.accuracy, 2),
                round(self.precision, 2),
                round(self.recall, 2),
                round(self.f1, 2),
                round(self.mse, 3),
                round(self.cross_entropy, 3),
                round(self.r2, 3),
                ]

    def table_header(self):
        return ["Algorithm",
                "Accuracy",
                "Precision",
                "Recall",
                "F1",
                "Mean Squared Error",
                "Cross-Entropy",
                "R^2"]
    
