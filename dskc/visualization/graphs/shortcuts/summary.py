from IPython.core.display import display

from dskc.exploration import exploration
from dskc.visualization.graphs.shortcuts.time import date_col
from dskc.visualization.graphs.shortcuts import data_types
from dskc.visualization.graphs.shortcuts.boolean import boolean_col
from dskc.visualization.graphs.shortcuts.category import categories_col
from dskc.visualization.graphs.shortcuts.number import number_col
from dskc.visualization.graphs.shortcuts.text import text_col
from dskc.visualization import terminal


def _get_types(df):
    '''
    Returns a list of tuples with each column name and his datatype, the datatype are:
    CATEGORICAL, NUMBER, TEXT, DATE and BOOLEAN

    :param df: pandas dataframe
    :return: list of tuples (column name, data type)
    '''
    summary = exploration.summary(df)

    types = []

    for row in summary.iterrows():
        row = row[1]

        name = row[0]
        type = row[1]
        distinct = row[2]

        # boolean
        if distinct == 2:
            types.append((name, data_types.BOOLEAN))

        # string
        elif type.find("object") >= 0:
            # text
            if distinct > 400:
                types.append((name, data_types.TEXT))
            # categories
            else:
                types.append((name, data_types.CATEGORICAL))

        # date
        elif type.find("date") >= 0 or name.split("_")[-1] in ["YEAR", "MONTH", "DAY", "WEEKDAY"]:
            types.append((name, data_types.DATE))

        # number
        elif type.find("int") >= 0 or type.find("float") >= 0:
            types.append((name, data_types.NUMBER))

    return types


def _list(title, types, datatype):
    '''

    :param title: string
    :param types: list of tuples
    :param datatype: datatype necessary to print
    :return:
    '''
    print(title)
    for column, dtype in list(filter(lambda x: x[1] == datatype, types)):
        print("- " + column)
    print()


def _print_types(types):
    '''
    prints all data types
    :param types: list of tuples
    :return:
    '''
    _list("Categories:", types, data_types.CATEGORICAL)
    _list("Numbers:", types, data_types.NUMBER)
    _list("Dates:", types, data_types.DATE)
    _list("Booleans:", types, data_types.BOOLEAN)
    _list("Text:", types, data_types.TEXT)


def _describe_object(df, name):
    series = df[name]
    describe = series.describe()
    headers = ["Type", "Missing", "Count", "Unique", "Top", "Top Freq."]

    values = list(describe.to_numpy())

    missing = 1 - values[0] / len(df)
    missing = "{:.1%}".format(missing)
    values.insert(0, missing)
    values.insert(0, series.dtype)

    table = [headers, values]

    return table


def _describe_number(df, name):
    series = df[name]
    describe = series.describe()
    headers = ["Type", "Missing", "Count", "Mean", "STD", "Min.", "25%", "50%", "75%", "Max."]

    values = list(describe.to_numpy())

    missing = 1 - values[0] / len(df)
    missing = "{:%}".format(missing)
    values.insert(0, missing)
    values.insert(0, series.dtype)

    table = [headers, values]

    return table


def _describe_datetime(df, name):
    series = df[name]
    describe = series.describe()
    headers = ["Type", "Missing", "Count", "Unique", "Top", "Top Freq.", "First", "Last"]

    values = list(describe.to_numpy())

    missing = 1 - values[0] / len(df)
    missing = "{:%}".format(missing)
    values.insert(0, missing)
    values.insert(0, series.dtype)

    table = [headers, values]

    return table


def describe(df, name):
    dtype = df[name].dtype

    if dtype == "object":
        table = _describe_object(df, name)

    elif str(dtype).find("datetime") > -1:
        table = _describe_datetime(df, name)

    else:
        table = _describe_number(df, name)

    print()
    terminal.markdown_h3("Values")
    table1 = [table[0][:3], table[1][:3]]
    terminal.markdown_table(table1)

    print("\n")
    terminal.markdown_h3("Basic Stats")
    table2 = [table[0][3:], table[1][3:]]
    terminal.markdown_table(table2)


def _item_graphs(df, data_type, name, target, target_true, section_number, categories):
    '''

    :param item:
    :return:
    '''

    print()
    terminal.markdown_h1("{}. {}".format(section_number,name))

    # describe
    describe(df, name)

    # categories
    if data_type == data_types.CATEGORICAL:
        categories_col(df, name, target, target_true=target_true, section_number=section_number)

    # numbers
    if data_type == data_types.NUMBER:
        number_col(df, name, target, section_number=section_number, categories=categories)

    # dates
    if data_type == data_types.DATE:
        date_col(df, name, target, target_true=target_true, section_number=section_number)

    # booleans
    if data_type == data_types.BOOLEAN:
        boolean_col(df, name, target, target_true=target_true, section_number=section_number)

    # text
    if data_type == data_types.TEXT:
        text_col(df, name, target, target_true=target_true, section_number=section_number)


def all_graphs(df, target=None, target_true=False, gui=False):
    '''
    The magic visualization function

    :param df: pandas dataframe
    :param target: target column
    :param target_true: 1 by default, set the value that identifies the target as true
    :return:
    '''

    types = _get_types(df)
    types_dict = {}
    for i, x in enumerate(types):
        types_dict["{}. {}".format(i, x[0])] = x[1]

    categories = []
    for x in types:
        if x[1] in [data_types.CATEGORICAL, data_types.BOOLEAN]:
            categories.append(x[0])

    if gui:
        import ipywidgets as widgets
        from IPython.display import clear_output

        menu = widgets.Dropdown(
            options=types_dict.keys(),
            description='Column:')

        def on_change(change):
            if change['type'] == 'change' and change['name'] == 'value':
                section_name = change['new']

                # get data type
                data_type = types_dict[section_name]

                # get column name
                section_name = section_name.split(". ")
                section_number = section_name[0]
                column_name = section_name[1]

                # clear and display dropdown
                clear_output()
                display(menu)

                # display graphs
                _item_graphs(df, data_type, column_name, target, target_true, section_number, categories)

        menu.observe(on_change)
        display(menu)

        return

    _print_types(types)

    for i, (name, data_type) in enumerate(types):
        # print markdown
        section_number = i + 1
        var_name = name.replace("_", " ").lower().capitalize()
        markdown_h1("{}. {}".format(section_number, var_name))

        _item_graphs(df, types_dict, name, target, target_true, section_number, categories)
