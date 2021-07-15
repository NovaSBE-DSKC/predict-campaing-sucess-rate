'''
Read files
'''

import csv
import json

from dskc.io.settings import ANSWERS_DIRECTORY


def read_csv(name="../dataset/raw/data.csv", delimiter=";", encoding="utf-8"):
  rows = []
  with open(name, encoding=encoding) as file:
    csv_file = csv.reader(file, delimiter=delimiter)

    first = True
    for row in csv_file:
      if first:
        header = row
        first = False
        continue

      rows.append(row)

  return header, rows


def read_answers(id):
  filename = "{}{}.json".format(ANSWERS_DIRECTORY, id)

  try:
    with open(filename, 'r') as file:
      return True, json.load(file)
  except:
    return False, None
