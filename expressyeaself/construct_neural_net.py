"""
This script contains functions to aid building, training, testing
and optimizing a neural network model.
"""
import matplotlib.pyplot as plt


def plot_results(hist):
    """
    Plots the model's accuracy and loss as functions of the
    epoch.

    Args:
    -----
        hist (dict) --

    Returns:
    -----
        plt () --
    """
    # Summarize history for accuracy
    plt.subplot(1, 2, 1)
    plt.plot(hist['acc'])
    plt.plot(hist['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')

    # Summarize history for loss
    plt.subplot(1, 2, 2)
    plt.plot(hist['loss'])
    plt.plot(hist['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.tight_layout()

    return plt
