import matplotlib.pyplot as plt

from dskc.visualization.graphs.types.util import set_titles
from dskc._util.pandas import df_to_list_w_column_idx
from dskc.stats import stats
from dskc._settings import colors

import numpy as np

def line(x, y,
         multiple=False,
         title="",
         xlabel="",
         ylabel="",
         legend=None,
         xrange=False,
         loc_legend="upper left",
         hline=None):
    '''
    Plot a line graph
    :param x: x data
    :param y: y data
    :return:
    '''
    if multiple:
        for i in range(len(y)):
            plt.plot(x[i],y[i],label=legend[i], color=colors.OFICIAL_COLORS[i])
    else:
        plt.plot(x, y, color=colors.FIRST_COLOR)
    
    
    if legend:
        plt.legend()
    
    if xrange:
        plt.xlim(xrange) 
        
    if hline != None:
        plt.axhline(y=hline, color='black', linestyle='--')

    
    set_titles(title,xlabel,ylabel)
    plt.tight_layout()
    
    plt.show()



def slope(p1, p2):
    x1,y1=p1
    x2,y2=p2
    m = (y2-y1)/(x2-x1)
    return m


def derivative_line(x,y,xlabel="",ylabel="",title="",xrange=False):
    slopes_y = []
    for i in range(len(x)):
        if i==0:
            slopes_y.append(0)
            continue
            
        p1 = (x[i-1],y[i-1])
        p2 = (x[i],y[i])
        s = slope(p1, p2)
        slopes_y.append(s)
    
    
    # display slopes 
    line(x, slopes_y, 
         xlabel=xlabel,
         ylabel=ylabel,
         title=title,
         hline=0,
         xrange=xrange)

def target_by_value(df, column, target, 
                    group_column=False,
                    no_outliers=False,
                    jump=False, 
                    xlabel=False, 
                    ylabel=False, 
                    title=False,
                    xrange=False):

    # get data
    data,c_idx,_ = df_to_list_w_column_idx(df)
    
    # sort by column
    data.sort(key=lambda x:x[c_idx[column]])
    
    if no_outliers:
        p25 = data[int(len(data)*0.25)][c_idx[column]]
        p75 = data[int(len(data)*0.75)][c_idx[column]]
        data = list(filter(lambda x: (x[c_idx[column]] >= p25) and (x[c_idx[column]] <= p75), data))
    
    # init graph variables
    x = []
    y = []
    
    # temp variables
    ys = []
    temp_value = data[0][c_idx[column]]
    last_group = None
    same_value = False
    
    # for each sample
    for i in range(len(data)):
        
        value = data[i][c_idx[column]]
        group = data[i][c_idx[group_column]]
        target_value = data[i][c_idx[target]]
        same_value = value >= temp_value-jump and value <= temp_value+jump

        if group == last_group and same_value:
            continue
        
        if same_value:
            ys.append(target_value)
        else:
            mean = sum(ys)/len(ys)
            x.append(value)
            y.append(mean)
            
            ys = [target_value]
            temp_value = value
            
        last_group = group
    
    
    
    # figure lengends
    if not xlabel:
        xlabel = column.capitalize()
        
    if not ylabel:
        ylabel = "Pecentage of {}".format(target)
    
    if not title:
        title = "Percentage of {} along {}".format(target, column)
        
    
    # display line graph
    line(x, y, 
         xlabel=xlabel,
         ylabel=ylabel,
         title=title,
         xrange=xrange)

    # derivative
    print("\n")
    ylabel = "Derivative of "+ylabel
    title = "Derivative of "+title
    derivative_line(x,y,xlabel=xlabel,ylabel=ylabel,title=title,xrange=xrange)
    