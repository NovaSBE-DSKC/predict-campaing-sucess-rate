import pandas as pd

from dskc.visualization import graphs
from dskc.visualization import terminal


def get_features_importance(model
                            , feature_names
                            , top=10):
    # graph
    terminal.markdown_h2("Top {} Feature Importances".format(top))
    print()

    feature_importances = model.feature_importances_
    df_feature_importances = pd.DataFrame({"importance": feature_importances}, index=feature_names) \
        .sort_values('importance', ascending=False)

    top_df = df_feature_importances.head(top)
    graphs.bars(top_df["importance"],
                percentage_on_top=False,
                title='Feature Importances',
                ylabel="Importance",
                xlabel="Feature",
                data_processed=True)

    # break line
    print("\n")

    # table
    terminal.markdown_h2("Feature Importances")
    print()

    table = [["Feature", "Importance"]]
    content = []
    for i, x in enumerate(feature_importances):
        content.append([feature_names[i], round(x, 3)])

    content.sort(key=lambda x: x[1], reverse=True)

    table += content

    terminal.markdown_table(table)

    # return df_feature_importances
