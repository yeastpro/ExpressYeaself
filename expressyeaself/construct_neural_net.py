"""
This script contains functions to aid building, training, testing
and optimizing a neural network model.
"""
import expressyeaself.encode_sequences as encode
from expressyeaself.utilities import get_time_stamp as get_time_stamp
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import tensorflow  # noqa: F401
from tensorflow.keras.models import load_model

ROOT_DIR = os.getcwd()[:os.getcwd().rfind('Express')] + 'ExpressYeaself/'
MODELS_TO_USE = ['1d_cnn_classifier',
                 '1d_cnn_sequential',
                 '1d_cnn_parallel',
                 '1d_loccon_classifier']


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


def get_saved_model_path(model_to_use):
    """
    Returns the absolute file path of one of ExpressYeaself's
    pre-trained models, based on the choice of model to use.

    Args:
    -----
        model_to_use (str) -- the type of pre-existing model to
        load.

    Returns:
    -----
        saved_model_json (str) -- the absolute file path of the
        saved model json file.

        saved_model_weights (str) -- the absolute file path of
        saved model weights.
    """
    # Assertions
    assert isinstance(model_to_use, str)
    assert model_to_use in MODELS_TO_USE
    # Functionality
    saved_model = ROOT_DIR + 'expressyeaself/models/'
    if model_to_use.startswith('1d_cnn'):
        saved_model += '1d_cnn/'
        saved_model += 'saved_models/' + model_to_use + '_onehot.hdf5'
    elif model_to_use.startswith('1d_loccon'):
        saved_model += '1d_loccon/'
        saved_model += 'saved_models/' + model_to_use + '_onehot.hdf5'
    elif model_to_use.startswith('lstm'):
        saved_model += 'lstm/'
        saved_model += 'saved_models/' + model_to_use + '_onehot.hdf5'

    return saved_model


def load_saved_model(saved_model):
    """
    Loads a pre-trained model and returns the model object.

    Args:
    ----
        saved_model (str) -- the absolute path of the saved model

    Returns:
    -----
        loaded_model (tensorflow.keras.
        engine.training.Model) -- the loaded model.
    """
    # Assertions
    assert isinstance(saved_model, str)
    assert os.path.exists(saved_model)
    # Functionality
    # with open(saved_model, 'rb', encoding='utf-8') as f:
    loaded_model = load_model(saved_model)

    return loaded_model


def get_prediction(loaded_model, sequence):
    """
    Predicts the expression level of a given input sequence
    via a pre-loaded model.

    Args:
    -----
        loaded_model (tensorflow.python.keras.
        engine.training.Model) -- the loaded model.

        sequence (str) -- the input nucleotide sequence to
        have its expression level predicted. Assumes correct
        length for loaded model.
    """
    # Assertions
    assert isinstance(sequence, str), 'Input seq must be a string.'
    # Functionality
    # Encode the sequence via One-Hot encoding
    encoded_seq = encode.one_hot_encode_sequence(sequence)
    prediction = loaded_model.predict(np.array([encoded_seq]))[0][0]

    return prediction


def get_predictions_for_input_file(input_seqs, model_to_use, sort_df=True,
                                   write_to_file=False):
    """
    Takes an input file of sequences and returns a DataFrame of
    the sequences and their predicted expression levels, based
    on the specified model (sorted in descending order of
    prediction expression level if specified 'sorted=True').

    Args:
    -----
        input_seqs (str) -- the absolute path of the input file
        containing sequences to get predictions for. Must be one
        sequence per line and sequences must be of the same length
        as the sequences the model was trained on.

        model_to_use (str) -- the type of pre-existing model to
        load.

        sort_df (bool) -- whether or not to sort the resulting
        data frame in descending order based on expression level.

        write_to_file (bool) -- whether or not to write the results
        of the prediction to an output file.

    Returns:
    -----
        results_df (pandas.DataFrame) -- the resulting data frame
        containing input sequences and predicted expression levels.
    """
    # Assertions
    assert isinstance(input_seqs, str)
    assert os.path.exists(input_seqs), 'Input file doesn not exist.'
    assert isinstance(model_to_use, str)
    assert model_to_use in MODELS_TO_USE
    assert isinstance(sort_df, bool)
    # Functionality
    results_df = pd.read_csv(input_seqs, names=['seq', 'el_prediction'])
    # Define and load model
    saved_model = get_saved_model_path(model_to_use)
    loaded_model = load_saved_model(saved_model)
    # Encode sequences, get predictions, insert values into data frame.
    for i in range(0, len(results_df)):
        seq = results_df['seq'][i]
        pred = get_prediction(loaded_model, seq)
        results_df['el_prediction'][i] = pred
    if sort_df:
        results_df = results_df.sort_values('el_prediction', ascending=False)
        results_df = results_df.reset_index()
    if write_to_file:
        out_path = ROOT_DIR + 'expressyeaself/models/prediction_results/'
        stamp = get_time_stamp()
        filename = stamp + '_' + model_to_use + '_prediction_results.txt'
        abs_path = out_path + filename
        if sort_df:
            columns = ['index', 'seq', 'el_prediction']
        else:
            columns = ['seq', 'el_prediction']
        results_df.to_csv(abs_path, header=None, index=None,
                          sep='\t', mode='w+', columns=columns)
        print('Results can be found at: ' + abs_path)

    return results_df
