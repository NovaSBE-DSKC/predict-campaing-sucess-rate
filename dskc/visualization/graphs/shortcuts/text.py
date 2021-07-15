from dskc.clean import get_text_from
from dskc.visualization import graphs
from dskc.visualization.graphs.types.word_cloud.word_cloud import word_cloud, text_proportion_success
from dskc._util.string import get_display_text
import pandas as pd
from . import util
from matplotlib import pyplot as plt


def _wordcloud(series, section_number, sub_section, display_name, stop_words):
    sub_section = util.header(section_number, sub_section, "{} Word Cloud".format(display_name))

    word_cloud(series, stop_words=stop_words)
    return sub_section


def _top_words(words_series, top_words, section_number, sub_section, display_name):
    sub_section = util.header(section_number, sub_section, "{} Top {} Words".format(display_name, top_words))

    graphs.bars(words_series,
                title="Top {} words".format(top_words),
                xlabel="Word",
                percentage_on_top=True,
                max_values=top_words)

    return sub_section


def _text_proportion_succcess(series, words_series, target_series, target_true, top_words, section_number, sub_section,
                              display_name):
    sub_section = util.header(section_number, sub_section,
                              "{} Mean Success of Top {} Words".format(display_name, top_words))

    text_proportion_success(words_series, series, target_series,
                            target_true=target_true)
    return sub_section


def text_col(df, name, target=None, target_true=False, section_number=1, top_words=15, stop_words=[]):
    # get names
    display_name = get_display_text(name)
    sub_section = 1

    # set series
    series = df[name]

    # wordcloud
    sub_section = _wordcloud(series, section_number, sub_section, display_name, stop_words)

    # bars graph
    text = get_text_from(series, stop_words=stop_words)

    # set word series
    words = text.split(" ")
    words_series = pd.Series(words)

    # top n words
    sub_section = _top_words(words_series, top_words, section_number, sub_section, display_name)

    # text proportion graphs
    if not target is None:
        try:
            _text_proportion_succcess(series,
                                      words_series,
                                      df[target],
                                      target_true,
                                      top_words,
                                      section_number,
                                      sub_section,
                                      display_name)
        except:
            plt.show()
            print("\nNot available.\n")
