from dskc._util.string import get_display_text
from dskc.visualization import graphs as dskc_graphs
from . import util


def _bars(series, section_number, sub_section, display_name):
    sub_section = util.header(section_number, sub_section, "{}  Bars Graph".format(display_name))

    dskc_graphs.bars(series,
                     title="{} Bars Graph".format(display_name),
                     xlabel=display_name)

    return sub_section


def _bars_proportion(df, name, target, target_true, section_number, sub_section, display_name, display_target):
    sub_section = util.header(section_number, sub_section, "{} Mean Target Sucess  Bars Graph".format(display_name))

    dskc_graphs.bars_target_proportion(df, name, target, target_true=target_true,
                                       title="{} by Mean Success of {}".format(display_name, display_target),
                                       xlabel=display_name)
    return sub_section


def boolean_col(df, name, target, target_true=False, section_number=1):
    # get names
    display_name = get_display_text(name)
    sub_section = 1

    # set series
    series = df[name]

    # bars
    sub_section = _bars(series, section_number, sub_section, display_name)

    # bars proportion
    if target:
        display_target = get_display_text(target)
        _bars_proportion(df, name, target, target_true, section_number, sub_section, display_name,
                                       display_target)
