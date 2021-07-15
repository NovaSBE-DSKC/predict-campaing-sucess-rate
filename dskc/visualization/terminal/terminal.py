from tabulate import tabulate
import pandas as pd

from dskc.io import get_root_path

MAX_LEN_ROW = 150


def section():
    '''
    prints "==============="
    :return:
    '''
    print("=" * MAX_LEN_ROW)


def sub_section():
    '''
     prints "--------------"
     :return:
     '''
    print("-" * MAX_LEN_ROW)


def highlight(text):
    section()
    print(text)
    section()
    print()


def text_section(text):
    section()
    print(text)
    section()
    print()


def space(n=5):
    print("\n" * (n - 1))


def table(table, format="github"):
    print(tabulate(table[1:], headers=table[0], tablefmt=format))


def dataframe_table_transpose(df):
    df = df.transpose()

    pd.set_option('display.width', 500)
    df = df.iloc[:].apply(pd.to_numeric, errors='coerce')

    print(tabulate(df, headers='keys'))


def exploration_banner():
    with open("{}/dskc/visualization/terminal/banner.txt".format(get_root_path())) as f:
        print(f.read())


def number_with_commas(number):
    print("{:,}".format(number))


def end_banner():
    with open("{}/dskc/visualization/terminal/banner_end.txt".format(get_root_path())) as f:
        print(f.read())


def question(title):
    print(title)
    sub_section()
