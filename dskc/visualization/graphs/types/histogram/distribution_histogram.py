from dskc._settings import colors
from plotnine import *
from mizani.formatters import percent_format
from matplotlib import pyplot as plt


def density_plot(df_original, variable, target=False, no_outliers=False, title=None, mean=True, mode=True, q1=True, q3=True):
    '''
    :param df: dataframe, variable: column to plot, target: object variable for split graph
    :return: ggplot graphs of univariate analysis
    by dtype: histogram, frequency, unique categories,
    :usage: after cleaning dataframe
    :target: is a string with the name of the categorical variable selected as target variable
    '''
    # target as str
    df = df_original.copy()
    df[target] = df[target].apply(str)
    
    x_label = variable.lower().replace("_", " ").title()
    graph = (ggplot(df) + aes(x=variable, y='..scaled..', fill=target))

    # target
    if target == False:
        graph += geom_density(fill=colors.FIRST_COLOR)

    else:
        fill_label = target.lower().replace("_", " ").title()
        graph += geom_density(alpha=.5)
        graph += scale_fill_manual(values=[colors.FIRST_COLOR, colors.SECOND_COLOR],
                                   name=fill_label)

    graph += (theme_bw()
              + theme(
                axis_line_x=element_line(color='gray'),
                axis_line_y=element_line(color='gray'),
                line=element_line(color='white')
            )
              )
    # labels
    graph += xlab(x_label) + ylab("Density")
    graph += scale_y_continuous(labels=percent_format())  # custom_format('{:.2f} USD')

    line_args = {
        "color": colors.THIRD_COLOR,
        "size": .5
    }

    var_describe = df[variable].describe()

    if mean:
        graph += geom_vline(xintercept=var_describe.loc["mean"],
                            linetype="dashed", **line_args
                            )

    if mode:
        graph += geom_vline(xintercept=var_describe.loc["50%"],
                            linetype="solid",
                            **line_args)

    if q1:
        graph += geom_vline(xintercept=var_describe.loc["25%"],
                            linetype="solid",
                            **line_args)

    if q3:
        graph += geom_vline(xintercept=var_describe.loc["75%"],
                            linetype="solid",
                            **line_args)

    # title
    if not title is None:
        graph += ggtitle(str(title))

    # no outliers
    if no_outliers:
        max_75 = df[variable].describe().loc['75%']
        min_25 = df[variable].describe().loc['25%']
        graph += xlim(min_25, max_75)

    # show
    graph.draw()
    plt.show()
