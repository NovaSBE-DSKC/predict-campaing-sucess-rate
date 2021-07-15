
def _df_to_list(df):
    columns = df.columns
    c_idx = {}
    for i, col in enumerate(columns):
        c_idx[col] = i

    data = df.to_numpy().tolist()

    return data, c_idx, columns

