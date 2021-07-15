from dskc.clean.util import df_column_map


def get_str_length(df, column):
  values = df_column_map(df, column, lambda x: len(str(x)) if x else 0)
  return values


def clean_word(word, list_bad_letters):
  return "".join(filter(lambda x: x not in list_bad_letters, word))
