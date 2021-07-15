from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt


def table(table_data):
    fig = plt.figure(dpi=200)
    ax = fig.add_subplot(1, 1, 1)

    table = ax.table(cellText=table_data, loc='center')
    table.set_fontsize(100)
    table.scale(1, 2)
    ax.axis('off')

    for (row, col), cell in table.get_celld().items():
        if (row == 0) or (col == -1):
            cell.set_text_props(fontproperties=FontProperties(weight='bold'))

    plt.show()
