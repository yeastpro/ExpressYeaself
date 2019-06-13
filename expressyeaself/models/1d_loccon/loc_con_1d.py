"""
This file consists of all the functions utilized to run the
LocallyConnected1D neural net.
"""
# import pandas as pd
# import numpy as np
# from sklearn import linear_model, datasets
from sklearn.model_selection import train_test_split
# import keras as k
# import ast
from keras.models import Sequential
from keras.layers import (Dense, Dropout, Flatten,  # InputLayer
                          LocallyConnected1D)  # BatchNormalization
import matplotlib.pyplot as plt
import context
# %matplotlib inline

encode = context.encode_sequences


def encode_data(datapath):
    """
    This function reads in a file and outputs a file with each of the
    sequences encoded.
    Input: file path
    Output: file consisting of encoded sequences
    (encoded by scripted from encode_sequences file)
    """
    seqs, exp_levels, max_el = encode.encode_sequences_with_method(datapath)

    return seqs, exp_levels, max_el


def data_shape(sequences):
    """
    This function reads in the np.array sequence matrix and outputs its
    dimensions.
    Input: np.array of sequences
    Output: tuple consisting of the dimensions of the input matrix
    """
    shape = sequences.shape

    return shape


def plot_results(fit):
    """
    This function takes the results from the model fit and evaluations
    and returns a visualization for the test-train accuracies and model
    losses.
    Input: model.fit() object results, specifically accuracies and
    losses of the train and test data
    Output: matplotlib graphical visualizations of each
    """
    # Create plot with subplots
    fig, ax = plt.subplots(1, 2, figsize=(12, 10))

    # Plot the accuracy plot
    ax1 = plt.subplot(221, xlabel='Epoch', ylabel='Accuracy',
                      title='Model Accuracy Plot')
    ax1.plot(fit['acc'], color='goldenrod', lw=2, alpha=0.5)
    ax1.plot(fit['val_acc'], color='rebeccapurple', lw=2, alpha=0.5)

    # Plot the loss plot
    ax2 = plt.subplot(222, xlabel='Epoch', ylabel='Loss',
                      title='Model Loss Plot')
    ax2.plot(fit['loss'], color='goldenrod', lw=2, alpha=0.5)
    ax2.plot(fit['val_loss'], color='rebeccapurple', lw=2, alpha=0.5)

    # create a list to store the axes
    axes_list = [ax1, ax2]
    # edit common components using a for loop
    for ax in axes_list:
        ax.title.set_fontsize(20)
        ax.xaxis.label.set_fontsize(14)
        ax.yaxis.label.set_fontsize(14)
        ax.legend(['Train', 'Test'], loc='upper left')

    return ax1, ax2


def tt_split(sequences, expression_levels):
    """
    This function reads in the np.array sequence matrix and
    expressions levels and performs a test-train split on the data.
    Input: np.arrays of sequences and expression levels
    Output: train_x, test_x, train_y, test_y
    """
    train_x, test_x, train_y, test_y = train_test_split(sequences,
                                                        expression_levels,
                                                        test_size=0.25)

    return train_x, test_x, train_y, test_y


def loc_con_1d_model(filters, kernel_size, strides, drop_rate, dense_units1,
                     dense_units_final, optimizer, loss):
    """
    This function reads in various parameters to compiles a
    LocallyConnected1D model, consisting of various layers
    including Dropout, Flatten and Dense. The function returns
    the model summary.
    Input: Various parameters including filter size, kernel size,
    number of strides, x and y dimensional input values, dropout
    rate (for Dropout Layers), dense units (for Dense Layers) and
    the optimizer and loss methods for the model.compile function.
    Output: model summary (based on model.summary() object)
    """
    # make a global variable
    global model

    # import shape for inputs
    shape = data_shape(sequences)  # noqa: F821
    input_x = shape[1]
    input_y = shape[2]

    # initialize model
    model = Sequential()
    model.add(LocallyConnected1D(filters, kernel_size, strides=strides,
                                 input_shape=(input_x, input_y),
                                 activation='relu'))

    # additional layers
#     model.add(Dense(50))
#     model.add(Dropout(drop_rate))
#     model.add(LocallyConnected1D(50, 15, activation='relu'))
#     model.add(Dense(10))
#     model.add(Dropout(drop_rate))
#     model.add(Dense(10))
#     model.add(Dropout(drop_rate))
    model.add(Dense(dense_units1))
    model.add(Dropout(drop_rate))

    # final flatten and dense layers
    model.add(Flatten())
    model.add(Dense(dense_units_final))

    # compile model
    model.compile(optimizer=optimizer, loss=loss, metrics=['mae', 'acc'])

    # return model summary
    return (model, model.summary())


def model_eval(sequences, expression_levels, epochs, batch_size):
    """
    This function fits the LocallyConnected1D model, generated in
    the loc_con_1d_model() function, using the given train and test
    data sets. The model evaluates accuracy and loss scores and
    outputs these values as well as a graphical visualization by
    calling the plot_results() function and passing through these
    values.
    Input: sequences and expression_level array, number of epochs
    to run the model for, and batch size (number of samples to
    train)
    Output: accuracy and loss values, accuracy and loss plots
    """
    # initialize training and testing values
    train_x, test_x, train_y, test_y = tt_split(sequences, expression_levels)

    # fit model
    fit = model.fit(train_x, train_y, epochs=epochs, batch_size=batch_size,
                    validation_data=(test_x, test_y))

    # evaluate model (run tests)
    scores = model.evaluate(test_x, test_y)

    # plot results
    plt = plot_results(fit.history)  # noqa F841

    # return model accuracy
    return ("Values: " + str(model.metrics_names[0]) + ': ' + str(scores[0])
            + ' ' + str(model.metrics_names[2]) + ': ' + str(scores[2] * 100)
            + '%')
