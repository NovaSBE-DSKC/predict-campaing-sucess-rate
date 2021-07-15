import os


def get_root_path():
  '''

  :return: root path of the project
  '''

  path = os.getcwd()
  MAX_ITERATIONS = 10

  i = 0
  while True:
    # check inside folders
    for x in os.walk(path):
      if x[0].endswith("dskc"):
        return path

    # go to father directory
    path = os.path.normpath(path + os.sep + os.pardir)

    #check if passed max iteration
    i += 1
    if i > MAX_ITERATIONS:
      return
