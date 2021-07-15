
def get_x_y(df,target):
    '''

    :param df:
    :param idx_divider:
    :return:
    '''
    y = df[target]
    x = df.drop([target], axis=1)

    return x, y


