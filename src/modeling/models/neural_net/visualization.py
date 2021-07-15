import matplotlib.pyplot as plt

from dskc.visualization import terminal
from dskc import dskc_terminal


def accuracy__graph(history):
    plt.plot(history['accuracy'])
    plt.plot(history['val_accuracy'])

    plt.title('Model accuracy')

    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')

    plt.legend(['Train', 'Test'], loc='upper left')

    plt.show()


def model_loss_graph(history):
    plt.plot(history['loss'])
    plt.plot(history['val_loss'])

    plt.title('Model loss')

    plt.ylabel('Loss')
    plt.xlabel('Epoch')

    plt.legend(['Train', 'Test'], loc='upper left')

    plt.show()


def _plots(historys, train="accuracy", test="val_accuracy", label="Accuracy"):
    # define columns and rows
    columns = min(4, len(historys))
    rows = len(historys) / columns

    if rows > int(rows):
        rows = int(rows) + 1
    else:
        rows = int(rows)

    # define subplots
    fig, axs = plt.subplots(rows, columns, figsize=(15, 15))

    # for each history
    for i, (neurons, history) in enumerate(historys):

        if rows == 1:
            ax = axs[i % columns]
        else:
            ax = axs[i // (columns), i % columns]

        # plot
        ax.plot(history[train])
        ax.plot(history[test])

        # set legends
        title = "Architecture: {}".format(neurons)
        ax.set_title(title)

        ax.set_ylabel(label)
        ax.set_xlabel('Epoch')

        ax.legend(['Train', 'Test'], loc='upper left')

    for i in range(len(historys), rows * columns):
        axs[i // (columns), i % columns].axis('off')

    # show
    plt.tight_layout()
    plt.show()


def accuracy_graphs(historys):
    terminal.markdown_h2("Accuracy")
    print()
    _plots(historys, train="accuracy", test="val_accuracy", label="Accuracy")
    print("\n")


def loss_graphs(historys):
    terminal.markdown_h2("Loss")
    print()
    _plots(historys, train="loss", test="val_loss", label="Loss")
    print("\n")


def metrics_table(historys):
    terminal.markdown_h2("Metrics Table")
    print()
    header = ["Neurons",
              "Accuracy",
              "Max Accuracy",
              "Epoch Max Acc.",
              "Loss",
              "Min Loss",
              "Epoch Min Loss"]

    table = [header]

    # metrics table
    for neurons, history in historys:
        # accuracy
        accuracy = history['val_accuracy'][-1]
        max_accuracy = max(history['val_accuracy'])
        idx_max_accuracy = history['val_accuracy'].index(max_accuracy) + 1

        # loss
        loss = history['val_loss'][-1]
        min_loss = min(history['val_loss'])
        idx_min_loss = history['val_loss'].index(min_loss) + 1

        row = [neurons,
               round(accuracy, 3),
               round(max_accuracy, 3),
               round(idx_max_accuracy),
               round(loss, 3),
               round(min_loss, 3),
               round(idx_min_loss, 3),
               ]

        table.append(row)

    dskc_terminal.table(table)
