import math
import re
import pandas as pd

from dskc._util.pandas import df_to_list_w_column_idx
from dskc.clean import insert_next_to
from dskc.io import get_root_path


def _get_stopwords():
    with open(get_root_path() + "/dskc/visualization/graphs/types/word_cloud/stopwords.txt", encoding="utf-8") as f:
        stopwords = []
        for word in f.readlines():
            stopwords.append(word.strip())

        # adding to the file his words doesnt solve the problem, IDK
        stopwords.extend(["a", "é"])

        return stopwords


def get_text_from(series, stop_words=[]):
    stop_words.extend(_get_stopwords())
    new_list = []

    # for each row
    for text in series:
        words = []

        if not text or (type(text) == float and math.isnan(text)):
            continue

        # filter line
        text = re.sub('[!?-]', ' ', str(text))
        text = text.replace("'", "")
        text = text.replace(":", "")
        text = text.split()

        # for each word
        for word in text:
            word = str(word).lower()

            # add if not in stopwords
            if len(word) <= 1:
                continue
            if not word in stop_words:
                words.append(word)

        new_list.append(words)

    return new_list


def _get_lexicon():
    path = get_root_path() + "/dskc/clean/lexicons/en_pt_lex.csv"  # todo json
    lexicon = pd.read_csv(path)
    return lexicon


def sentiment_calculator(word_list, lexicon):
    num_pos_words = 0
    num_neg_words = 0

    for word in word_list:
        if word not in lexicon:
            continue

        sentiment = lexicon[word]
        if sentiment == "positive":
            num_pos_words += 1
        elif sentiment == "negative":
            num_neg_words += 1

    sentiment_sum = num_pos_words - num_neg_words

    return sentiment_sum


def get_sentiment(series):
    lexicon, c_idx, columns = df_to_list_w_column_idx(_get_lexicon())  # refactor to be json

    lexicon_dict = {}
    for row in lexicon:
        lexicon_dict[row[c_idx["word"]]] = row[c_idx["sentiment"]]

    words_list = get_text_from(series)
    results = [sentiment_calculator(x, lexicon_dict) for x in words_list]

    return pd.Series(results)


def set_sentiment(df, column, sufix="_sentiment"):
    results = get_sentiment(df[column])
    insert_next_to(df, column + sufix, column, results)





def get_text(series, stop_words=[]):
    stop_words.extend(_get_stopwords())
    words = []

    # for each text variable
    for text in series:

        if not text or (type(text) == float and math.isnan(text)):
            continue

        # filter line
        text = re.sub('[!?]', ' ', str(text))
        text = re.split('; |, |\n| ', str(text))

        # for each word
        for word in text:
            word = str(word).lower()

            # add if not in stopwords
            if len(word) <= 1:
                continue
            if not word in stop_words:
                words.append(word)

    return " ".join(words)

def most_freq_words(series, stop_words=[]):
    # transform the series into a single string
    text = get_text(series, stop_words=stop_words)

    # break the string into list of words
    str_list = text.split()

    # gives set of unique words
    unique_words = set(str_list)
    word = []
    frequency = []
    for words in unique_words:
        word.append(words)
        frequency.append(str_list.count(words))

    return pd.DataFrame({'Word': word,
                         'Frequency': frequency}).sort_values(by='Frequency',
                                                              ascending=False).reset_index(drop=True)


def categories_from_word_series(df, series, categories=10, stop_words=[], prefix="CAT_"):
    # Selecting the top categories
    categories = most_freq_words(df[series], stop_words=stop_words).iloc[0:categories]

    # assigning "new?series?name" to the new pd column not working
    df[prefix + str(series).upper()] = 'outros'

    for cat in categories['Word']:
        df.loc[(df[series].str.contains(cat, na=False, case=False)) & (
                df[prefix + str(series).upper()] == 'outros'), prefix + str(series).upper()] = cat

    return df

