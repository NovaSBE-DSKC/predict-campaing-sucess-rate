from dskc._util.string import get_display_text
from dskc.visualization import graphs as dskc_graphs
from dskc.visualization.graphs.types.correlation import variable_correlation_heatmap
from . import util
from matplotlib import pyplot as plt


def _correlation(df, name, section_number, sub_section, display_name):
    sub_section = util.header(section_number, sub_section, "{} Correlation".format(display_name))

    try:
        variable_correlation_heatmap(df, name)
    except:
        plt.show()
        print("\nNot available.\n")

    return sub_section


def _hist(series, section_number, sub_section, display_name):
    sub_section = util.header(section_number, sub_section, "{} Histogram Graph".format(display_name))
    try:
        dskc_graphs.histogram(series,
                              title="{} histogram".format(display_name),
                              value_on_top=True,
                              percentage_on_top=True)
    except:
        plt.show()
        print("\nNot available.\n")

    return sub_section


def _hist_no_outliers(series, section_number, sub_section, display_name):
    sub_section = util.header(section_number, sub_section, "{} Histogram graph (without outliers)".format(display_name))
    try:
        dskc_graphs.histogram(series,
                              title="{} histogram (without outliers)".format(display_name),
                              no_outliers=True,
                              value_on_top=True,
                              percentage_on_top=True)
    except:
        plt.show()
        print("\nNot available.\n")

    return sub_section


def _dns_plot(df, name, section_number, sub_section, display_name):
    sub_section = util.header(section_number, sub_section, "{} Density Plot ".format(display_name))

    try:
        dskc_graphs.density_plot(df, name)
    except:
        plt.show()
        print("\nNot available.\n")

    return sub_section


def _dns_plot_no_outliers(df, name, section_number, sub_section, display_name):
    sub_section = util.header(section_number, sub_section, "{} Density plot (without outliers)".format(display_name))

    try:
        dskc_graphs.density_plot(df, name, no_outliers=True)
    except:
        plt.show()
        print("\nNot available.\n")

    return sub_section


def _dns_plot_target(df, name, target, section_number, sub_section, display_name):
    sub_section = util.header(section_number, sub_section, "{} Density Plot with Target".format(display_name))

    try:
        dskc_graphs.density_plot(df, name,
                                 target=target)
    except:
        plt.show()
        print("\nNot available.\n")

    return sub_section


def _dns_plot_target_no_outliers(df, name, target, section_number, sub_section, display_name):
    sub_section = util.header(section_number, sub_section,
                              "{} Density plot with target (without outliers)".format(display_name))
    try:
        dskc_graphs.density_plot(df, name,
                                 target=target,
                                 no_outliers=True)
    except:
        plt.show()
        print("\nNot available.\n")

    return sub_section


def _box_plot(df, name, target, category, section_number, sub_section, display_name):
    display_target = get_display_text(target)
    display_category = get_display_text(category)

    sub_section = util.header(section_number, sub_section,
                              "{} Box Plot With {} by {}".format(display_name, display_target, display_category))

    try:
        dskc_graphs.box_plot(df, category, target, name, flip=True, grouped=True, agg_func="mean")
    except:
        plt.show()
        print("\nNot available.\n")

    return sub_section


def number_col(df, name, target, section_number=1, categories=[]):
    '''

    :param df: pandas dataframe
    :param name: name of the column
    :param target: target column variable
    :return:
    '''
    # set names
    display_name = get_display_text(name)
    sub_section = 1

    # set series
    series = df[name]

    # correlation
    sub_section = _correlation(df, name, section_number, sub_section, display_name)

    # histogram
    sub_section = _hist(series, section_number, sub_section, display_name)

    # density plot
    if target:
        sub_section = _dns_plot_target(df, name, target, section_number, sub_section, display_name)
    else:
        sub_section = _dns_plot(df, name, section_number, sub_section, display_name)

    # histogram no outliers
    sub_section = _hist_no_outliers(series, section_number, sub_section, display_name)

    # desnity plot no ouliers
    if target:
        _dns_plot_target_no_outliers(df, name, target, section_number, sub_section, display_name)
    else:
        _dns_plot_no_outliers(df, name, section_number, sub_section, display_name)

    # box plots
    if not target:
        return

    for category in categories:
        if category == target:
            continue

        sub_section = _box_plot(df, name, target, category, section_number, sub_section, display_name)
