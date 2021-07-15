from IPython.display import display, Markdown

from tabulate import tabulate
import pandas as pd


def markdown_h1(text):
    text = "# " + text
    display(Markdown(text))


def markdown_h2(text):
    text = "## " + text
    display(Markdown(text))


def markdown_h3(text):
    text = "### " + text
    display(Markdown(text))


def markdown(text):
    display(Markdown(text))


def markdown_table(table, format="github"):
    if type(table) == pd.DataFrame:
        table = tabulate(table, headers='keys')
    else:
        table = tabulate(table[1:], headers=table[0], tablefmt=format)

    display(Markdown(table))
