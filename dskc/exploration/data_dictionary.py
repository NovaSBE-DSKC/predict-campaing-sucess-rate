from dskc.exploration.exploration import summary


def _save(matrix, filename):
  DELIMITER = ";"
  text = ""

  # matrix to text
  for row in matrix:
    for elem in row:
      text += str(elem) + DELIMITER
    text += "\n"

  # write file
  with open(filename, 'w',encoding="UTF-8") as out:
    out.write(text)


def data_dictionary(df, filename="Data Dictionary.csv", name="", description=""):
  '''
  :param filename: data dictionary filename
  :param df: dataframe
  :return: saves a file with  a basic exploration of the dataframe
  '''

  dictionary = []

  # header dictionary
  n_samples = df.shape[0]
  header = ['Dataset', "Samples", "Description"]
  header_data = [name, n_samples, description]

  dictionary.append(header)
  dictionary.append(header_data)

  # space
  dictionary.append([])

  # content
  columns = summary(df)

  for row in columns:
    dictionary.append(row)

  # save
  _save(dictionary, filename)
