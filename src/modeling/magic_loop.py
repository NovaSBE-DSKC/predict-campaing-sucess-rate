'''
Magic loop for comparing fitness among different models
'''

from dskc import dskc_terminal
from src.modeling.models import *

def _display_reports(reports):
    table = []

    # build each report
    for i, report in enumerate(reports):
        table.append(report.table_row())

    # sort by mse
    table.sort(key=lambda x: x[-3])

    # add ranking
    for i, row in enumerate(table):
        row.insert(0, i + 1)

    # add header
    header = ["Ranking"]
    header.extend(reports[0].table_header())

    table.insert(0, header)

    print("\n")
    dskc_terminal.markdown_table(table)


def summary():
    algorithms = [
        dtree,
        nnet,
        log_regression,
        lin_regression,
        xgboost,
        bayesian_ridge,
        random_forest_regressor
    ]

    reports = []

    # test each algorithm
    for algo in algorithms:
        print(algo.__name__, end="... ")

        try:
            model = algo.load_model()
            report = algo.test(model)
        except:
            print("error")
            continue

        reports.append(report)
        print("done")

    _display_reports(reports)


def train(exclude=[]):
    algorithms = [
        dtree,
        nnet,
        log_regression,
        lin_regression,
        xgboost,
        bayesian_ridge,
        random_forest_regressor
    ]


    # test each algorithm
    for algo in algorithms:
        algo_name = algo.__name__
        if algo_name in exclude:
            continue

        print(algo_name + "... ")
        algo.train()
        print("done\n")
