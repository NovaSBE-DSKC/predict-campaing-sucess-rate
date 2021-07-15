from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import pandas as pd

from dskc.clean import get_text
from dskc.io import get_root_path
from dskc.visualization.graphs.types.bars import bars_util


def _get_stopwords():
    with open(get_root_path() + "/dskc/visualization/graphs/types/word_cloud/stopwords.txt", encoding="utf-8") as f:
        stopwords = []
        for word in f.readlines():
            stopwords.append(word.strip())

        # adding to the file his words doesnt solve the problem, IDK
        stopwords.extend(["a", "é"])

        return stopwords


def text_proportion_success(words_series, text_series, target_series,
                            target_true=1,
                            title="",
                            xlabel="Word",
                            ylabel="Mean Success"):
    data = words_series.value_counts()[:15]

    xlabels = data.index
    ylabels = [[0, 0] for x in xlabels]

    # calc proportion value
    for i, text in enumerate(text_series):
        for j, x in enumerate(xlabels):
            if re.search(str(x), str(text), re.IGNORECASE):
                if target_series.loc[i] == target_true:
                    ylabels[j][0] += 1
                ylabels[j][1] += 1

    myLabels = []
    for x in ylabels:
        if x[1] > 0:
            myLabels.append(x[0] / x[1])
        else:
            myLabels.append(0)

    series = pd.Series(myLabels, index=xlabels)

    bars_util.bars(series,
                   title=title,
                   xlabel=xlabel,
                   ylabel=ylabel,
                   hline=0.5)


def word_cloud(series, stop_words=[]):
    text = get_text(series, stop_words=stop_words)

    wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)

    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def text_by_category(df, textvar, categoryvar):  # todo delete
    text = get_text(df[textvar])
    words = text.split(" ")
    text_series = pd.Series(words)
    auxDF = pd.DataFrame({'word': [], 'category': []})

    for cnt_df in range(len(df[textvar])):

        for cnt_wrds in range(len(text_series)):
            # print(df[textvar][cnt_df])
            # print(text_series[cnt_wrds])
            # print(type(df[textvar][cnt_df]))
            # print(df[textvar][cnt_df].lower())
            # print(text_series[cnt_wrds])
            try:
                if df[textvar][cnt_df].lower() in text_series[cnt_wrds]:
                    print("Im in!")
                    auxDF.word[cnt_wrds] = text_series[cnt_wrds]
                    print(auxDF.word[cnt_wrds])
                    auxDF.category[cnt_wrds] = df.categoryvar[cnt_df]
            except:
                print("Something not good")
                print(df[textvar][cnt_df])
                print(cnt_df)
                print(len(df[textvar]))

    return auxDF
