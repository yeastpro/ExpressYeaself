"""
This script contains the functions to encode promoter nucleotide
sequences by different methods, depending on the requirement of the
neural network that will receive the encoded sequence.
"""
import numpy as np
import expressyeaself.organize_data as organize
import os
from expressyeaself.utilities import smart_open as smart_open
from expressyeaself.utilities import get_time_stamp as get_time_stamp

BASES = ['A','T','G','C']
MAPPING =  {'A' : [1,0,0,0,0],
            'T' : [0,1,0,0,0],
            'G' : [0,0,1,0,0],
            'C' : [0,0,0,1,0],
            'N' : [0,0,0,0,1],
            'P' : [0,0,0,0,0]}
METHODS = ['One-Hot']

def encode_sequences_with_method(input_seqs, method='One-Hot',
                                scale_els=True):
    """
    A wrapper function that encodes all of the sequences in an
    input file according to the specified method, and returns
    them in a list, as well as returning the associated expression
    levels in a separate list.

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

    Returns:
    -----
        encoded_seqs (numpy.ndarray) -- a list of all the sequences
        in the input file, encoded with the specified method. Each
        element (i.e. each encoded sequence) is of type list.

        exp_levels (numpy.ndarray) -- a list of all the expression
        levels associated with the sequences. Each element (i.e.
        each EL) is of type float. Values scaled to between -1 and
        1 if argument 'scale_els=True'.

        min (float) -- the minimum expression level value in the
        input file.

        max (float) -- the maximum expression level value in the
        input file.
    """
    # Assertions
    assert isinstance(input_seqs, str), 'TypeError: Input file path must be \
    passed as a string.'
    assert isinstance(method, str), 'TypeError: Specified method must be a \
    a string.'
    assert method in METHODS, 'Must specify one the method of encoding the \
    sequence. Choose one of: %s' %(METHODS)
    with smart_open(input_seqs, 'r') as f:
        token, num_seqs = organize.separate_seq_and_el_data(f.readline())
        assert token == 'number_of_seqs_in_file', 'First line of the input\
        file must be of the form: "number_of_seqs_in_file\t<###>" where\
        <###> is the number of sequences in the file.'
        token, len_seqs = organize.separate_seq_and_el_data(f.readline())
        assert token == 'length_of_each_sequence', 'Second line of the input\
        file must be of the form: "length_of_each_sequence\t<###>" where\
        <###> is the length of every sequence in the file. Assumes\
        homogeneity and/or padding of sequences.'
    # Functionality
    # Open input
    infile = smart_open(input_seqs, 'r')
    # Initialize output lists, preallocating dimensions for speed.
    encoded_seqs = np.zeros((int(num_seqs),int(len_seqs),5))
    exp_levels = np.zeros(int(num_seqs))
    # Encode and pad each sequence and write it to file with expression level
    max_length, _, _ = organize.get_max_min_mode_length_of_seqs(input_seqs)
    line_number = -3
    for line in infile:
        line_number += 1
        if line_number == -2 or line_number == -1:
            continue # skip the 1st line (just the num of seqs in file)
        line = organize.check_valid_line(line)
        if line == 'skip_line':
            continue
        seq, exp_level = organize.separate_seq_and_el_data(line)
        # Encode
        if method == 'One-Hot':
            try:
                encoded_seq = one_hot_encode_sequence(seq)
            except Exception:
                raise AssertionError('Error on line %s' %(line_number))
        else:
            # Another encoding method will go here
            # encoded_seq = another_encoding_method(seq)
            pass
        # Reassign elements in ouput arrays
        encoded_seqs[line_number] = encoded_seq
        exp_levels[line_number] = exp_level
    # Close the input file
    infile.close()
    # Scale expression level values to between -1 and 1
    if scale_els:
        


    return encoded_seqs, exp_levels

def one_hot_encode_sequence(promoter_seq):
    """
    Encodes a string nucleotide sequence using the 'One-Hot' encoding
    method into a 2D array.

    Args:
    -----
        promoter_seq (str)    -- the promoter sequence to be encoded.

    Returns:
    -----
        one_hot_seq (str) -- the One-Hot encoded nucleotide sequence
        as a 2D array.
    """
    # Assertions
    assert isinstance(promoter_seq, str), 'TypeError: Input nucleotide \
    sequence must be a string.'
    invalid_indices = []
    index = -1 # Iterator for character index in promoter_seq string
    for nuc in promoter_seq:
        index += 1
        nuc = nuc.upper()
        if nuc not in MAPPING.keys():
            invalid_indices.append(index) # Appends list of incorrect indices
    if len(invalid_indices) is not 0:
        raise Exception('Input nucleotide sequence contains a non ATGC or \
        "N" or "P" at string indices %s' %(invalid_indices))
    # Functionality
    one_hot_seq = []
    for nuc in promoter_seq:
        nuc = nuc.upper()
        one_hot_seq.append(MAPPING[nuc])

    return one_hot_seq

def resize_array(input_array, resize_to=None, edit_front=False):
    """
    Takes an M x N 2D array (where M is the length to edit) and
    resizes it to the specified resize_to length, adding (if too
    short) null vectors ([0,0,0,0,...] of length N) or removing
    base vectors (if too long) from either the front or end of
    the sequence so that the output encoded array is of dimensions
    (resize_to) x N.

    Args:
    -----
        input_array (list) -- the one-hot encoded binary 2D array
        to resize.

        resize_to (int) -- the length to resize the array to.
        Default: None (returns the input array with no resizing).

        edit_front (bool) -- whether to add/remove binary base
        vectors from the front or back of the array. Default:
        False (so removes them from the back).

    Returns:
    -----
        input_array (list) -- the resized array of dimensions
        (resize_to)x4.
    """
    # Assertions
    assert isinstance(input_array, list), 'Input array must be a list.'
    assert isinstance(resize_to, (int, type(None))), 'Length to resize the \
    array to must be an integer or None.'
    assert isinstance(edit_front, bool), 'TypeError: edit_front must be a bool.'
    previous_len = len(input_array[0])
    for i in range(1, len(input_array)): # check vectors in array same length
        current_len = len(input_array[i])
        assert current_len == previous_len, 'Not all vectors in input array \
        are of the same length.'
        previous_len = current_len
    # Functionality
    len_diff = len(input_array) - resize_to
    if len_diff == 0: # doesn't need resizing
        return input_array
    elif len_diff > 0: # Sequence needs trimming
        if edit_front:
            return input_array[-resize_to:]
        else:
            return input_array[:resize_to]
    elif len_diff < 0: # Sequence needs filling
        # Ensuring null vector to be added matches dimensions of input array
        null_vect = [0] * len(input_array[0])
        if edit_front:
            for i in range(0, len_diff):
                input_array.insert(0, null_vect)
            return input_array
        else:
            for i in range(0, len_diff):
                input_array.append(null_vect)
            return input_array

    return
