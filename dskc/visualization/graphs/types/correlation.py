import seaborn as sns
from matplotlib import pyplot as plt


def variable_correlation_heatmap(df, dependent_variable):
    '''
    Takes df, a dependant variable as str
    Returns a heatmap of all independent variables' correlations with dependent variable
    '''
    plt.figure(figsize=(8, 10))
    sns.heatmap(df.corr()[[dependent_variable]].sort_values(by=dependent_variable),
                annot=True,
                cmap='coolwarm',
                vmin=-1,
                vmax=1)
    plt.show()
