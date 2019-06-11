# import expressyeaself.construct_neural_net_input as construct
# import expressyeaself.encode_sequences as encode
import ast
import numpy as np
import pandas as pd
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
# from keras.layers import Embedding
# from keras.utils import to_categorical
# from keras.datasets import mnist
# from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt


def load_raw_data(data):
    raw_data = pd.read_csv(data, names=['raw_sequence', 'output'], sep='\t')

    return raw_data


def load_raw_sequence_data(raw_matrix):
    """
    """
    sequence_matrix = []
    for sequence in raw_matrix['raw_sequence']:
        one_hot_array_sequence = np.array(ast.literal_eval(sequence))
        sequence_matrix.append(one_hot_array_sequence)
    sequence_matrix = np.array(sequence_matrix)

    return sequence_matrix


def read_length(matrix):
    """
    """
    data_length = matrix.shape[0]
    sequence_length = matrix.shape[1]

    return data_length, sequence_length


def matrix_reshape_to_array(matrix, data_amount, sequence_length):
    sequence_array = matrix.reshape(data_amount, sequence_length, 5)

    return sequence_array


def input_sequence_to_embedding(sequence_matrix, sequence_length):
    sequence_matrix_for_enbedding = []
    for matrix in sequence_matrix:
        matrix = matrix.reshape(1, sequence_length, 5)
        sequence_matrix_for_enbedding.append(matrix)
    sequence_matrix_for_enbedding = np.array(sequence_matrix_for_enbedding)

    return sequence_matrix_for_enbedding


def split_data(input_data, output_data):
    training_sequence = input_data[:int(input_data.shape[0] * 0.8)]
    training_output = output_data[:int(output_data.shape[0] * 0.8)]
    testing_sequence = input_data[int(input_data.shape[0] * 0.8):]
    testing_output = output_data[int(output_data.shape[0] * 0.8):]

    return (training_sequence, training_output, testing_sequence,
            testing_output)


# def load_output(raw_matrix, data_length):
#     output_matrix=np.array(raw_matrix['output']).reshape(data_length, 1, 1)
#     return output_matrix


def scale_output(raw_data, data_length):
    output_data = []
    max_value = raw_data['output'].max()
    for output in raw_data['output']:
        output = output/max_value
        output_data.append(output)
    output_data = np.array(output_data).reshape(data_length, 1, 1)

    return output_data


def input_of_one_hot_sequence(raw_matrix, data_amount, sequence_length):

    sequence_matrix = raw_matrix.reshape(data_amount, -1)
    one_hot_sequence_matrix = sequence_matrix.reshape(data_amount, 1,
                                                      sequence_length * 5)

    return one_hot_sequence_matrix


def lstm_model_on_one_hot_sequence(sequence_length, training_sequence,
                                   training_output, testing_sequence,
                                   testing_output,
                                   self_loss='mean_squared_error',
                                   learning_rate=0.01, epochs_value=20,
                                   batch_size_value=50):
    model = Sequential()
    # model.add(Embedding(5, 1, input_length=1285))
    model.add(Dense(1024, kernel_initializer='uniform',
                    input_shape=(1, 5 * sequence_length,)))
    model.add(Activation('softmax'))
    model.add(Dense(512, kernel_initializer='uniform',
                    input_shape=(1, 1024, )))
    model.add(Activation('softmax'))
    model.add(Dense(256, kernel_initializer='uniform',
                    input_shape=(1, 512, )))
    model.add(Activation('softmax'))
    model.add(Dense(128, kernel_initializer='uniform',
                    input_shape=(1, 256, )))
    model.add(Activation('softmax'))
    model.add(Dense(64, kernel_initializer='uniform',
                    input_shape=(1, 128, )))
    model.add(Activation('softmax'))
    model.add(Dense(32, kernel_initializer='uniform',
                    input_shape=(1, 64, )))
    model.add(Activation('softmax'))
    model.add(Dense(16, kernel_initializer='uniform',
                    input_shape=(1, 32, )))
    model.add(Activation('softmax'))
    model.add(Dense(8, kernel_initializer='uniform',
                    input_shape=(1, 16, )))
    model.add(Activation('softmax'))

    model.add(LSTM(units=1, return_sequences=True))
    sgd = optimizers.SGD(lr=learning_rate, decay=1e-6, momentum=0.9,
                         nesterov=True)
    model.compile(loss=self_loss, optimizer=sgd, metrics=['mae', 'acc'])

    model.fit(training_sequence, training_output, epochs=epochs_value,
              batch_size=batch_size_value, verbose=1)
    score = model.evaluate(testing_sequence, testing_output)
    predicted_output_raw = model.predict(testing_sequence)
    predicted_output = predicted_output_raw.reshape(len(predicted_output_raw),
                                                    1)

    return score, predicted_output


# def LSTM_model_training(LSTM_model, training_sequence, training_output,
#                         epochs_value=20, batch_size_value=50):
#     return LSTM_model.fit(training_sequence, training_output,
#                           epochs=epochs_value,
#                           batch_size=batch_size_value, verbose=1)


# def model_report(LSTM_model, testing_sequence, testing_output,
#                  batch_size_value=50):
# #     LSTM_model.summary()
#     score = model.evaluate(testing_sequence, testing_output)
#     return score


# def predict_data(LSTM_model, testing_sequence):
#     predicted_output_raw=LSTM_model.predict(testing_sequence)
#     predicted_output=predicted_output_raw.reshape(len(predicted_output_raw),
#                                                   1)
#     return predicted_output


def caparison_figure(predict_data, testing_output):
    testing_output_array = testing_output.reshape(len(testing_output), 1)
    index = np.arange(1, len(testing_output) + 1, 1)
    fig = plt.figure(figsize=(9, 6))
    plt.scatter(index, testing_output_array, label='real output')
    plt.scatter(index, predict_data, label='predict output')
    plt.legend()

    return fig


def lstm_training(data_path):
    raw_data = load_raw_data(data_path)
    sequence_list = load_raw_sequence_data(raw_data)
    data_number, bp_number=read_length(sequence_list)
    reshaped_sequence_matrix = input_of_one_hot_sequence(sequence_list,
                                                         data_number,
                                                         bp_number)
    output=scale_output(raw_data, data_number)
    train_x, train_y, test_x, text_y = split_data(reshaped_sequence_matrix,
                                                  output)
    score, predict_data = lstm_model_on_one_hot_sequence(bp_number,
                                                         training_sequence,
                                                         training_output,
                                                         testing_sequence,
                                                         testing_output,
                                                         self_loss='mean_'
                                                         'squared_error',
                                                         learning_rate=0.01,
                                                         epochs_value=2,
                                                         batch_size_value=50)
#     LSTM_model_training(LSTM_model, train_x, train_y, epochs_value=2,
                        # batch_size_value=50)
#     socre=model_report(LSTM_model, testing_sequence, testing_output,
                       # batch_size_value=50)
#     predicted_output=predict_data(LSTM_model, test_x)
    cp_figure=caparison_figure(predict_data, testing_output)

    return score, cp_figure
