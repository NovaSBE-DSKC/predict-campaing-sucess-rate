from dskc.visualization.graphs import bars, bars_target_proportion
from dskc._util.string import get_display_text
from dskc.visualization.terminal.jupyter import markdown_h2
from dskc._util.dates import get_weekdays
from . import util


def time_graphs(df, column, ylabel="", year=True, month=True, day=True, weekday=True):
    '''
    Display graphs by year, month, day and weekday

    :param df: pandas dataframe
    :param column: column name
    :param ylabel:
    :param year:
    :param month:
    :param day:
    :param weekday:
    :return:
    '''
    ylabel = ylabel.capitalize()

    if year:
        series = df[column + "_YEAR"]
        title = "over the Years"
        if ylabel:
            title = ylabel + " " + title

        title = title.capitalize()

        bars(series,
             sort_labels=True,
             title=title,
             xlabel="Year",
             ylabel=ylabel)

    if month:
        series = df[column + "_MONTH"]
        title = "over the Months"
        if ylabel:
            title = ylabel + " " + title

        title = title.capitalize()

        bars(series,
             sort_labels=True,
             title=title,
             xlabel="Month",
             ylabel=ylabel)

    if day:
        title = "over the Days"
        if ylabel:
            title = ylabel + " " + title

        title = title.capitalize()
        bars(df[column + "_DAY"],
             title=title,
             sort_labels=True,
             xlabel="Day",
             ylabel=ylabel)

    if weekday:
        series = df[column + "_WEEKDAY"]
        title = "over the Weeks"
        if ylabel:
            title = ylabel + " " + title

        title = title.capitalize()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        bars(series,
             sort_labels=True,
             title=title,
             xlabel="Day of the Week",
             xticks=days,
             ylabel=ylabel)


def _bars(series, xticks, section_number, sub_section, display_name):
    sub_section = util.header(section_number, sub_section, "{} Bars Graph".format(display_name))

    bars(series,
         sort_labels=True,
         xticks=xticks)

    return sub_section


def _bars_proportion(df, name, xticks, target, target_true, section_number, sub_section, display_name):
    sub_section = util.header(section_number, sub_section, "{} Mean Success  Bars Graph".format(display_name))

    bars_target_proportion(df, name, target,
                           sort_labels=True,
                           target_true=target_true,
                           xticks=xticks)
    return sub_section


def date_col(df, name, target, target_true=False, section_number=1):
    # set names
    display_name = get_display_text(name)
    sub_section = 1

    # set series
    series = df[name]

    # graphs
    if str(series.dtype).find("date") >= 0:
        return
        markdown_h2("Line graph")
        # todo line

    if name.lower().endswith("_weekday"):
        xticks = get_weekdays()
    else:
        xticks = False

    # bars
    sub_section = _bars(series, xticks, section_number, sub_section, display_name)

    # bars proportion
    if target:
        _bars_proportion(df, name, xticks, target, target_true, section_number, sub_section, display_name)
