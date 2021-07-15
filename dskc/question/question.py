from dskc.io import write, read
from dskc.visualization.terminal import terminal


def _list_options(options):
  print("\n")
  for i, option in enumerate(options):
    print("{} - {}".format(i + 1, option))
  print("\n")


def _get_option_index(label, index, max):
  print("{} / {}".format(index + 1, max))
  print(label)

  while True:
    value = input(">> ")

    try:
      value = int(value) - 1
    except:
      print("Opção incorrecta")
      continue

    if value >= 0 and value < max:
      return value


def question_boolean(questionary_id, title, list, force_questionary=False):
  # load from file if saved
  if not force_questionary:
    exists, data = read.read_answers(questionary_id)
    if exists:
      return data

  terminal.question(title)
  values = {}
  options = ["True", "False"]

  for i, label in enumerate(list):
    _list_options(options)
    index = _get_option_index(label, i, len(list))
    values[label] = index == 0

  # save in files
  write.save_answers(questionary_id, values)

  return values


def match_answers_with_list(answers, my_list):
  values = []
  for i, value in enumerate(my_list):
    if value in answers:
      my_list[i] = answers[value]
    else:
      values.append(value)

  return values


def match_boolean_answers_with_list(answers, my_list, true_value=None, false_value=None, change_on_true=True,
                                    change_on_false=True):
  for i, value in enumerate(my_list):
    if value in answers:
      correct = answers[value]
      if correct:
        if change_on_true:
          my_list[i] = true_value
      else:
        if change_on_false:
          my_list[i] = false_value
