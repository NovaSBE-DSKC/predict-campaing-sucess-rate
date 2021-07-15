'''
Pre-processing algorithms
'''
from dskc.question import question
from dskc import dskc_clean


def get_countries(df, column):
  data = df[column]
  values = []

  for value in data:
    temp = value.split(", ")

    portugal = "Portugal"

    if len(temp) > 1:
      local = temp[-1].strip().lstrip().capitalize()
      local = dskc_clean.clean_word(local, ".()")
    else:
      local = portugal

    values.append(local)

  # question Portugal
  answers = question.question_boolean("country", "É Portugal", set(values))
  question.match_boolean_answers_with_list(answers, values, true_value=portugal, change_on_false=False)

  # question usa
  to_question = filter(lambda x: x != "Portugal", values)
  answers = question.question_boolean("countryUSA", "É USA", set(to_question))
  question.match_boolean_answers_with_list(answers, values, true_value="USA", change_on_false=False)

  # question sao tome
  discard = ["Portugal", "USA"]
  to_question = filter(lambda x: x not in discard, values)
  answers = question.question_boolean("countrySAOTOME", "É SAO TOME", set(to_question))
  question.match_boolean_answers_with_list(answers, values, true_value="S. Tomé e Príncipe", change_on_false=False)

  return values


def get_percentage_raised(df):
  target = df['TARGET']
  raised = df['RAISED']

  values = []
  for i, target_value in enumerate(target):
    values.append(raised[i] / target_value)
  return values


def get_raised_and_percentage_self_funded(df, pledges_df):
  raised_values = []
  percentage_self_funded_values = []

  for index, row in df.iterrows():
    # amount
    amount = pledges_df[(pledges_df["PID"] == row["PID"]) & (pledges_df["UID"] == row["UID"])]["AMOUNT"].sum()
    raised_values.append(amount)

    # percentage self funded
    percentage = amount / row["TARGET"]
    percentage_self_funded_values.append(percentage)

  return raised_values, percentage_self_funded_values

