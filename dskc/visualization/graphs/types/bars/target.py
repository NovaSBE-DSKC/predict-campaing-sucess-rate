import pandas as pd
from dskc.visualization.graphs.types.bars import bars_util


def bars_target_proportion(df,
                           column,
                           target,
                           target_true=1,
                           sort_labels=False,
                           horizontal=False,
                           max_values=None,
                           bins=False,
                           percentage_on_top=False,
                           value_on_top=True,
                           title="",
                           xlabel="",
                           xticks=False,
                           xticks_rotation_horizontal=False,
                           ylabel="% Mean Success",
                           hline=0.5):
    uniques = df[column].unique()

    labels = []
    proportions = []

    for name in uniques:
        df_name = df[df[column] == name]
        trues = df_name[df_name[target] == target_true][column].count()
        all = df_name.shape[0]

        labels.append(name)
        proportions.append(trues / all * 100)

    series = pd.Series(proportions, index=labels)

    bars_util.bars(series,
                   sort_labels=sort_labels,
                   horizontal=horizontal,
                   max_values=max_values,
                   bins=bins,
                   percentage_on_top=percentage_on_top,
                   value_on_top=value_on_top,
                   title=title,
                   xlabel=xlabel,
                   xticks=xticks,
                   xticks_rotation_horizontal=xticks_rotation_horizontal,
                   ylabel=ylabel,
                   hline=hline)
