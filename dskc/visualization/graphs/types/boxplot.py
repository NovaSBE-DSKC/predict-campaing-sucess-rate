import pandas as pd
from mizani.formatters import custom_format
from plotnine import *
from matplotlib import pyplot as plt

from dskc._settings import colors
from dskc._util.string import get_display_text


def _filter_aux(aux, filter_col, filterby):
    try:
        if filter_col is None:
            f_aux = aux.iloc[:, 2]
        else:
            f_aux = aux[filter_col]

        aux = aux.loc[~f_aux.isin(filterby)]

    except:
        print("Error: couldn't filter data")

    return aux


def _get_grouped_aux(df, x_col, fill_col, agg_col, agg_func, filter_col, filterby):
    try:
        aux = df.groupby([x_col, fill_col], sort=True).agg(
            aux_agg=pd.NamedAgg(column=agg_col, aggfunc=agg_func)
        ).reset_index()

        aux_str = "aux_agg"
        aux[x_col] = aux[x_col].astype(str)
        aux[fill_col] = aux[fill_col].astype(str)

    except:
        print("Couldn't group by the dataframe, is {0:s} a valid aggfunc?".format(agg_func))
        raise

    aux = _filter_aux(aux, filter_col, filterby)

    return aux, aux_str


def box_plot(df, x_col, fill_col, agg_col, agg_func='count',
             filter_col=None, filterby=[""], no_outliers=False,
             title=None, ylabel=None, grouped=True, flip=True, dots=True):
    '''
    :param df: dataframe,x_col: variable  located on x axis,fill_col: variable for coloring the dots,agg_col: name of the column to which the aggregation function is going to perform
    :optional agg_fun: for example: sum,min,mean,median,max,etc. filter_col: after groupying filtering option,filterby: list of characters to be filtered out (located in filter column),outliers,title
    :return: ggplot graphs of univariate analysis
    :type: boxplot
    :usage: after cleaning dataframe
    '''

    # set display texts

    fill_label = get_display_text(fill_col)

    if grouped:
        aux, aux_str = _get_grouped_aux(df, x_col, fill_col, agg_col, agg_func, filter_col, filterby)
    else:
        aux = df
        aux_str = agg_col

    # sort x labels
    aux = aux.sort_values(by=[x_col])

    xcol_list = aux.astype(str)[x_col].unique().tolist()

    # graph creation
    graph = (ggplot(aux)
             + geom_boxplot(aes(x=x_col, y=aux_str))
             + theme_bw()
             + theme(
                axis_line_x=element_line(color='gray'),
                axis_line_y=element_line(color='gray'),
                line=element_line(color='white')
            )
             + scale_fill_manual(values=colors.OFICIAL_COLORS, name=fill_label)
             + scale_x_discrete(limits=xcol_list)
             + scale_y_continuous(labels=custom_format('{:,.0f}'))
             )

    # dots
    if dots:
        graph += geom_jitter(aes(x=x_col, y=aux_str, fill=fill_col))

    # no outliers
    aux_describe = aux[aux_str].describe().loc
    if no_outliers:
        graph += ylim(aux_describe["min"], aux_describe["75%"])

    # title
    if title != None:
        graph += ggtitle("Box plot:" + str(title))

    # flip
    if flip:
        graph += coord_flip()

    # set y label
    if not ylabel:
        ylabel = get_display_text(agg_col)
    graph += ylab(ylabel)

    # show
    graph.draw()
    plt.show()
