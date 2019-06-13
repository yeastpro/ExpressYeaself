"""
This script contains the functions to encode promoter nucleotide
sequences by different methods, depending on the requirement of the
neural network that will receive the encoded sequence.
"""
import expressyeaself.organize_data as organize
from expressyeaself.utilities import check_valid_line as check_valid_line
from expressyeaself.utilities import (separate_seq_and_el_data as
                                      separate_seq_and_el_data)
from expressyeaself.utilities import smart_open as smart_open
import numpy as np

BASES = ['A', 'T', 'G', 'C']
MAPPING = {'A': [1, 0, 0, 0, 0],
           'T': [0, 1, 0, 0, 0],
           'G': [0, 0, 1, 0, 0],
           'C': [0, 0, 0, 1, 0],
           'N': [0, 0, 0, 0, 1],
           'P': [0, 0, 0, 0, 0]}
METHODS = ['One-Hot']
MODELS = ['1DCNN', '1DLOCCON', 'LSTM']


def encode_sequences_with_method(input_seqs, method='One-Hot',
                                 scale_els=True, model_type='1DCNN',
                                 binarized_els=False):
    """
    A wrapper function that encodes all of the sequences in an
    input file according to the specified method, and returns
    them in a numpy array, as well as returning the associated
    expression levels in a separate numpy array.

    Args:
    -----
        input_seqs (str) -- absolute path of the file containing
        all of the input sequences to be encoded, tab-separated
        withtheir associated expression levels. The first line of
        the file must be the number of sequences in the file, of
        the format: "number_of_seqs_in_file\t<###>" where <###> is
        the number of sequences in the file. The second line in the
        file must be the length to which all sequences are padded,
        of the format: "length_of_each_sequence\t<###>" where <###>
        is the length of every sequence in the file. Assumes
        homogeneity and/or padding of sequences.

        method (str) -- the method by which the sequence should be
        encoded. Must choose from: 'One-Hot'. Default: 'One-Hot'

        scale_els (bool) -- if True (default), scales all of the
        expression levels in the output list exp_levels to between
        -1 and 1, corresponding to the min and max values
        respectively.

        model_type (str) -- the type of model being used. Controls
        the shape of the returned list that contains the encoded
        sequences. Must be one of: '1DCNN' (for 1D-convolutional
        net), '1DLOCCON' (for 1D-locally connected net), or 'LSTM'
        (for Long-Short-Term-Memory net).

    Returns:
    -----
        encoded_seqs (numpy.ndarray) -- a list of all the sequences
        in the input file, encoded with the specified method. Each
        element (i.e. each encoded sequence) is of type list. Shape
        of this array depends on 'model_type'. For example, for an
        input file containing 10000 sequences, each of length 257,
        where the length of each base vector is 5 (corresponding to
        bases A,T,G,C,N), the output shapes of encoded_seqs for each
        model is as follows:
        '1DCONV'   ===> (10000, 257, 5)
        '1DLOCCON' ===> (10000, 257, 5)
        'LSTM'     ===> (10000, 1, 1285) where 1285=257*5

        exp_levels (numpy.ndarray) -- a list of all the expression
        levels associated with the sequences. Each element (i.e.
        each EL) is of type float. Values scaled to between -1 and
        1 if argument 'scale_els=True'.

        abs_max_el (float) -- the maximum expression level value in the
        input file. Returned only if 'scale_els=True'.

    """
    # Assertions
    assert isinstance(input_seqs, str), 'TypeError: Input file path must be \
    passed as a string.'
    assert isinstance(method, str), 'TypeError: Specified method must be a \
    a string.'
    assert method in METHODS, 'Must specify one the method of encoding the \
    sequence. Choose one of: %s' % (METHODS)
    assert isinstance(scale_els, bool), 'scale_els argument must be passed\
    as a bool.'
    assert isinstance(model_type, str), 'model_type argument must be passed\
    as a string.'
    assert model_type in MODELS, 'Must specify model_type as one of the\
    following: %s' % (MODELS)
    # Functionality
    # Open input file
    infile = smart_open(input_seqs, 'r')
    # Initialize output lists, preallocating dimensions for speed.
    num_seqs, len_seq = organize.get_num_and_len_of_seqs_from_file(input_seqs)
    encoded_seqs = np.zeros((int(num_seqs), int(len_seq), 5)).astype(int)
    exp_levels = np.zeros(int(num_seqs))
    # Encode sequences
    line_number = -3
    for line in infile:
        line_number += 1
        if line_number < 0:
            continue  # skip first 2 lines of the file
        line = check_valid_line(line)
        if line == 'skip_line':
            continue  # skip line if not a valid line
        seq, exp_level = separate_seq_and_el_data(line)
        # Encode with One-Hot method
        if method == 'One-Hot':
            try:
                encoded_seq = one_hot_encode_sequence(seq)
            except Exception:
                raise AssertionError('Error on line %s' % (line_number))
        # Encode with another method, i.e. embedding
        else:
            # Another encoding method will go here
            # encoded_seq = another_encoding_method(seq)
            pass
        # Assign encoded sequences and expression levels to output arrays
        encoded_seqs[line_number] = encoded_seq
        exp_levels[line_number] = exp_level
    # Close the input file
    infile.close()
    # Reshape array if needed as input to LSTM model
    if model_type == 'LSTM':
        encoded_seqs = encoded_seqs.reshape(num_seqs, -1)
        encoded_seqs = encoded_seqs.reshape(num_seqs, 1, (len_seq * 5))
    # Scale expression level values to between -1 and 1
    if scale_els:
        abs_max_el = abs(max(exp_levels, key=abs))  # the absolute max value
        # numpy allows easy division of all elements at once
        exp_levels = exp_levels / abs_max_el
    else:  # If no scaling required
        abs_max_el = None
    # If expression levels are binarized, convert them from float ---> int
    if binarized_els:
        exp_levels = exp_levels.astype(int)

    return encoded_seqs, exp_levels, abs_max_el


def one_hot_encode_sequence(promoter_seq):
    """
    Encodes a string nucleotide sequence using the 'One-Hot'
    encoding method into a 2D array.

    Args:
    -----
        promoter_seq (str) -- the promoter sequence to be encoded.

    Returns:
    -----
        one_hot_seq (str) -- the One-Hot encoded nucleotide sequence
        as a 2D array.
    """
    # Assertions
    assert isinstance(promoter_seq, str), 'TypeError: Input nucleotide \
    sequence must be a string.'
    invalid_indices = []
    index = -1  # Iterator for character index in promoter_seq string
    for nuc in promoter_seq:
        index += 1
        nuc = nuc.upper()
        if nuc not in MAPPING.keys():
            invalid_indices.append(index)  # Appends list of incorrect indices
    if len(invalid_indices) != 0:
        raise Exception('Input nucleotide sequence contains a non ATGC or \
        "N" or "P" at string indices %s' % (invalid_indices))
    # Functionality
    one_hot_seq = []
    for nuc in promoter_seq:
        nuc = nuc.upper()
        one_hot_seq.append(MAPPING[nuc])

    return one_hot_seq


# def resize_array(input_array, resize_to=None, edit_front=False):
#     """
#     Takes an M x N 2D array (where M is the length to edit) and
#     resizes it to the specified resize_to length, adding (if too
#     short) null vectors ([0,0,0,0,...] of length N) or removing
#     base vectors (if too long) from either the front or end of
#     the sequence so that the output encoded array is of dimensions
#     (resize_to) x N.
#
#     Args:
#     -----
#         input_array (list) -- the one-hot encoded binary 2D array
#         to resize.
#
#         resize_to (int) -- the length to resize the array to.
#         Default: None (returns the input array with no resizing).
#
#         edit_front (bool) -- whether to add/remove binary base
#         vectors from the front or back of the array. Default:
#         False (so removes them from the back).
#
#     Returns:
#     -----
#         input_array (list) -- the resized array of dimensions
#         (resize_to)x4.
#     """
#     # Assertions
#     assert isinstance(input_array, list), 'Input array must be a list.'
#     assert isinstance(resize_to, (int, type(None))), 'Length to resize the \
#     array to must be an integer or None.'
#     assert isinstance(edit_front, bool), 'TypeError: edit_front must be\
#     a bool.'
#     previous_len = len(input_array[0])
#     for i in range(1, len(input_array)):  # check vectors in array same
#       length
#         current_len = len(input_array[i])
#         assert current_len == previous_len, 'Not all vectors in input\
#                                              array are of the same length.'
#         previous_len = current_len
#     # Functionality
#     len_diff = len(input_array) - resize_to
#     if len_diff == 0:  # doesn't need resizing
#         return input_array
#     elif len_diff > 0:  # Sequence needs trimming
#         if edit_front:
#             return input_array[-resize_to:]
#         else:
#             return input_array[:resize_to]
#     elif len_diff < 0:  # Sequence needs filling
#         # Ensuring null vector to be added matches dimensions of input array
#         null_vect = [0] * len(input_array[0])
#         if edit_front:
#             for i in range(0, len_diff):
#                 input_array.insert(0, null_vect)
#             return input_array
#         else:
#             for i in range(0, len_diff):
#                 input_array.append(null_vect)
#             return input_array
#
#     return
