'''
Write files
'''
import json

from dskc.io.settings import ANSWERS_DIRECTORY


def save_answers(id, answers):
  filename="{}{}.json".format(ANSWERS_DIRECTORY,id)
  with open(filename, 'w') as file:
    json.dump(answers, file)
