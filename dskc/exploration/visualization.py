from dskc.visualization.graphs import matshow
from dskc.visualization import terminal
from dskc.visualization import graphs
from dskc.exploration import pearson_correlation


def show_exploration(df, data_head, columns, n_samples, corr_pearson, hists):
    terminal.exploration_banner()

    # columns list
    columns_list = list(df.columns.values)

    # ndata head
    terminal.text_section("First 5 rows ")
    print("(transpose view)\n")
    data_head = data_head.astype(str)
    for c in columns_list:
        data_head[c] = data_head[c].str[:20]

    #transpose
    terminal.dataframe_table_transpose(data_head)
    terminal.space()

    # n samples
    terminal.text_section("Samples")
    terminal.number_with_commas(n_samples)
    terminal.space()

    # columns
    terminal.text_section("Columns")
    print("{} columns\n".format(len(columns_list)))
    terminal.markdown_table(columns)
    terminal.space()

    # correlation pearson
    title = "Pearson's Correlation"
    terminal.text_section(title)

    print("\n(graph)")
    #matshow(corr_pearson)

    no_correlated = pearson_correlation.no_correlation_lables(corr_pearson)

    print("\nColumns with values no higher than 0.05: ")

    # print each label
    for label in no_correlated:
        print("- {}".format(label))

    if not no_correlated:
        print("(0 columns)")

    terminal.space()

    # variables exploration
    if hists:
        terminal.text_section("Variable Histogram")

    # for each selected coloumn
    for label in hists:

        # get data type
        dtype = str(df[label].dtype)

        # continue if not number
        if not (dtype.find("int") >= 0 or dtype.find("float") >= 0):
            continue

        # histogram
        graphs.histogram(df[label].to_numpy(), label)

        # print that was plotted
        print("({|} histogram)".format(label))

    terminal.space()
