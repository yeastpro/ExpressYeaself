"""
This script contains functions to organize and split up data based
on several experimental parameters.
"""
# import expressyeaself.utilities. as utilities  # noqa: F401
from expressyeaself.utilities import check_valid_line as check_valid_line
from expressyeaself.utilities import get_seq_count as get_seq_count
from expressyeaself.utilities import get_time_stamp as get_time_stamp
from expressyeaself.utilities import (separate_seq_and_el_data as
                                      separate_seq_and_el_data)
from expressyeaself.utilities import smart_open as smart_open
import numpy as np
import os
import pandas as pd
import random


def sort_by_exp_level(input_seqs):
    """
    Given an input file of sequences tab separated with their
    associated expression levels, sorts the lines of the file
    by expression level, with the highest levels at the top of
    the file.

    Args:
    -----
        input_seqs (str) -- the absolute path of the input file
        containing sequences to be sorted by expression level.

    Returns:
    -----
        sorted_df (pandas.DataFrame) -- a data frame where rows
        are sorted in descending order based on expression level.
    """
    # Assertions
    assert isinstance(input_seqs, str), 'Path name for input file must be \
    passed as a string.'
    assert os.path.exists(input_seqs), 'Input file does not exist.'
    # Functionality
    with smart_open(input_seqs, 'r') as f:
        line = check_valid_line(f.readline())
        seq1, _ = separate_seq_and_el_data(line)
        line = check_valid_line(f.readline())
        seq2, _ = separate_seq_and_el_data(line)
        exp_seq1 = 'number_of_seqs_in_file'
        exp_seq2 = 'length_of_each_sequence'
        if seq1 == exp_seq1 and seq2 == exp_seq2:
            skip = 2
        else:
            skip = 0
    # Import data into a pandas data frame
    df = pd.read_csv(input_seqs, sep='\t', names=['seq', 'el'], skiprows=skip)
    # Sort it based on expression level
    sorted_df = df.sort_values('el', ascending=False)
    sorted_df = sorted_df.reset_index()
    sorted_df = sorted_df.drop(columns='index')

    return sorted_df


def discard_mid_data(sorted_df, percentile=0.25):
    """
    Takes a pandas data frame of sequences and their associated
    expression levels, sorted in descending order by these values,
    and returns a data frame containing only the top and bottom
    'percentile' fractions of the data with regard to expression
    level. For example, if 'percentile=0.25', the middle 50 % of the
    data will be discarded, and the resulting data frame will only
    contain rows of the highest 25 % and lowest 25 % of exp levels.

    Args:
    -----
        sorted_df (pandas.DataFrame) -- the input data frame with
        sequence data in a column labelled 'seq' and the associated
        expression level data in a column labelled 'el'. Rows are
        sorted in descending order based on expression level.

        percentile (float) -- the fraction of data with the highest
        and lowest expression levels to be kept.

    Returns:
    -----
        df_mid_discarded (pandas.DataFrame) -- the resulting data
        frame after discarding the middle (1 - 2 * percentile)
        rows. This data frame has length:
        (2 * percentile * len(sorted_df))
    """
    # Assertions
    assert isinstance(sorted_df, pd.DataFrame), ('Input data frame must be of'
                                                 ' type pandas.DataFrame')
    assert isinstance(percentile, float), ('The "percentile" variable must be'
                                           ' passed as a float.')
    assert percentile < 0.5, ('"percentile" must be less than 0.5')
    # Functionality
    df_len = len(sorted_df)
    divisor = int(1 / percentile)
    high_index = df_len // divisor
    low_index = df_len * (divisor - 1) // divisor
    df_high = sorted_df.iloc[:high_index]
    df_low = sorted_df.iloc[low_index:]
    difference = len(df_high) - len(df_low)
    # Ensuring data slices are the same size
    if difference != 0:
        if difference > 0:
            high_index -= difference
        if difference < 0:
            low_index += difference
    df_high = sorted_df.iloc[:high_index]
    df_low = sorted_df.iloc[low_index:]
    df_mid_discarded = pd.concat([df_high, df_low])

    return df_mid_discarded


def binarize_data(input_df):
    """
    Takes a data frame of sequence and expression level data, where
    rows have been sorted in descending order based on expression
    level, and the middle portion has been discarded (so that only
    the top and bottom percentiles remain), and binarizes the
    expression levels. Binarization will see those sequences in the
    top percentile to have an expression level of 1 (expresses) and
    sequences in the bottom percentile having an expression level
    of 0 (does not express). Assumes columns are labelled 'seq' and
    'el' respectively.

    Args:
    -----
        input_df (pandas.DataFrame) -- the input data frame, where
        rows have been sorted based on expression levels, and the
        middle portion of the data has been discarded so that only
        the top and bottom pecentiles remain.

    Returns:
    -----
        input_df (pandas.DataFrame) -- data frame modified so
        that expression levels have been binarized into 1 or 0.
    """
    # Assertions
    assert isinstance(input_df, pd.DataFrame), ('Input data frame must be of'
                                                'type pandas.DataFrame')
    # Functionality
    # Define an array of binary values
    does_express = np.ones(len(input_df) // 2).astype(int)
    does_not_express = np.zeros(len(input_df) // 2).astype(int)
    assert len(does_express) == len(does_not_express)
    binary_values = np.concatenate((does_express, does_not_express), axis=0)
    input_df = input_df.drop(columns='el')
    input_df['el'] = binary_values

    return input_df


def write_df_to_file(input_df):
    """
    Writes the content of an input pandas data frame containing
    sequence data (in a column called 'seq') and expression level
    data (in a column called 'el') to an output file of specified
    path.

    Args:
    -----
        input_df (pandas.DataFrame) -- the input data frame whose
        contents will be written to file.

    Returns:
    -----
        absolute_path (str) -- the absolute path of the the output
        file where the contents of the data frame are written.
    """
    # Assertions
    assert isinstance(input_df, pd.DataFrame), ('Input data frame must be of'
                                                 ' type pandas.DataFrame')
    # Functionality
    # Defining the path name of the output file.
    relative_path = 'example/'
    time_stamp = get_time_stamp()
    relative_path += 'processed_data/' + time_stamp + '_df_to_file.txt'
    absolute_path = os.path.join(os.getcwd(), relative_path)
    # Writing to file
    input_df.to_csv(absolute_path, header=None, index=None,
                    sep='\t', mode='w', columns=['seq', 'el'])

    return absolute_path


def get_max_min_mode_length_of_seqs(input_seqs):
    """
    Returns the maximum, minimum, and modal length of the sequences
    in a file containing input sequences.

    Args:
    -----
        input_seqs (str) -- the absolute path of the file
        containing the input sequences and their expression levels,
        tab separated.

    Returns:
    -----
        max_length (int) -- the length of the longest sequence in
        the input file.

        min_length (int) -- the length of the shortest sequence in
        the input file.

        modal_length (int) -- the most common sequence length of
        the sequences in the input file.
    """
    # Assertions
    assert isinstance(input_seqs, str), 'Path name for input file must be \
    passed as a string.'
    assert os.path.exists(input_seqs), 'Input file does not exist.'
    # Functionality
    infile = smart_open(input_seqs, 'r')
    seq_lengths = []
    for line in infile:
        line = check_valid_line(line)
        if line == 'skip_line':
            continue
        seq, exp_level = separate_seq_and_el_data(line)
        seq_lengths.append(len(seq))
    max_length = max(seq_lengths)
    min_length = min(seq_lengths)
    modal_length = max(set(seq_lengths), key=seq_lengths.count)
    # Close the input file.
    infile.close()

    return max_length, min_length, modal_length


def pull_homogeneous_seqs(input_seqs, scaffold_type=None):
    """
    Pulls all sequences of the modal length (i.e. 110 bp for pTpA-type
    sequences and 115 bp for Abf1TATA-type) from an input file and
    writes them into an output file.

    Args:
    -----
        input_seqs (str) -- the absolute pathname of the input file
        containing all of the raw oligonucleotide sequences and
        their expression levels, tab separated.

        scaffold_type (str) -- the scaffold type (pTpA or Abf1TATA
        for which the modal length is known to be 110 and 115
        respectively) in which the expression levels for the
        sequences in the input file were measured. If None, the
        modal length is calculated manually. Default: None.

    Returns:
    -----
        absolute_path (str) -- the absolute pathname of the output
        file containing the sequences of modal length.
    """
    # Assertions
    assert isinstance(input_seqs, str), ('Input file pathname must be a'
                                         'string.')
    assert os.path.isfile(input_seqs), 'Input file does not exist!'
    assert isinstance(scaffold_type, (str, type(None))), 'Scaffold type must\
    be passed as a string.'
    if isinstance(scaffold_type, str):
        assert scaffold_type == 'pTpA' or scaffold_type == 'Abf1TATA', 'Scaff\
        type must be specified as either pTpA or Abf1TATA, or else\
        unspecified (in which case it takes value of None).'
    # Functionality
    # Defining the path name of the output file.
    relative_path = 'example/'
    time_stamp = get_time_stamp()
    if scaffold_type is None:
        relative_path += ('other_scaffolds/' + time_stamp +
                          '_homogeneous_seqs.txt')
    else:
        relative_path += (scaffold_type + '_data/' + time_stamp + '_' +
                          scaffold_type + '_homogeneous_seqs.txt')
    absolute_path = os.path.join(os.getcwd(), relative_path)
    # Open the input and output files.
    infile = smart_open(input_seqs, 'r')
    output_seqs = smart_open(absolute_path, 'w')
    # Retrieve modal length for sequences in input file.
    if scaffold_type == 'pTpA':
        modal_length = 110
    elif scaffold_type == 'Abf1TATA':
        modal_length = 115
    else:
        _, _, modal_length = get_max_min_mode_length_of_seqs(input_seqs)
    # Find seqs in input file w/ modal length and write them to output file
    for line in infile:
        line = check_valid_line(line)
        if line == 'skip_line':
            continue
        seq, exp_level = separate_seq_and_el_data(line)
        if len(seq) == modal_length:
            output_seqs.write(seq + '\t' + str(exp_level) + '\n')
        else:
            continue
    # Close the input and output files.
    infile.close()
    output_seqs.close()

    return absolute_path


def check_oligonucleotide_flanks(seq_infile, scaffold_type):
    """
    Checks that all the oligonucleotide sequences in an input file
    consist of the same sequences that flank the variable 80-mer
    sequence. i.e. all sequences in the input file should be of the
    form:
    TGCATTTTTTTCACATC-(variable region)-GTTACGGCTGTT
    Whereas the input sequences measured in the Abf1TATA scaffold
    will be of the form:
    TCACGCAGTATAGTTC-(variable region)-GGTTTATTGTTTATAAAAA
    These flanking sequences are for in-lab sequencing purposes only,
    so can be discarded when the 80-mer variable sequences are
    inserted into the a scaffold sequence.

    Args:
    -----
        seq_infile (str) -- the absolute path of the input file
        containing all of the oligonucleotide sequences to be
        checked, and their expression level values (tab separated).

        scaffold_type (str) -- the scaffold type (pTpA or Abf1TATA)
        in which the expression levels for the sequences in the
        input file were measured.

    Returns:
    -----
        incorrect_lines (list) -- returns a list of line numbers for
        for sequences that contain incorrect flank sequences.
    """
    # Assertions
    assert isinstance(seq_infile, str), 'Absolute pathname must be passed \
    as a string.'
    assert isinstance(scaffold_type, str), 'Scaffold type must be passed as a\
    string.'
    assert scaffold_type == 'pTpA' or scaffold_type == 'Abf1TATA', 'Scaffold \
    type must be specified as either pTpA or Abf1TATA.'
    # Functionality
    if scaffold_type == 'pTpA':
        flank_A = 'TGCATTTTTTTCACATC'
        flank_B = 'GGTTACGGCTGTT'
    elif scaffold_type == 'Abf1TATA':
        flank_A = 'TCACGCAGTATAGTTC'
        flank_B = 'GGTTTATTGTTTATAAAAA'
    infile = smart_open(seq_infile, 'r')
    line_number = 0
    incorrect_lines = []
    for line in infile:
        line_number += 1
        line = check_valid_line(line)
        if line == 'skip_line':
            continue
        seq, exp_level = separate_seq_and_el_data(line)
        if seq.startswith(flank_A) and seq.endswith(flank_B):
            pass
        else:
            incorrect_lines.append(line_number)

    return incorrect_lines


def remove_file_list(files):
    """
    Takes a list of path names for files and deletes each of the
    files from the local system.

    Args:
    -----
        files (list) -- the absolute paths, as strings, of the
        files to be deleted.

    Returns:
    -----
        None
    """
    # Assertions
    for file in files:
        assert isinstance(file, str), 'File path names must be passed as \
        strings.'
    # Functionality
    for file in files:
        if os.path.exists(file):
            os.remove(file)
        else:
            pass

    return


def write_num_and_len_of_seqs_to_file(input_seqs):
    """
    Prepends the number of sequences and the length of the
    sequences in an input file to the first 2 lines of the
    file. Assumes sequences have been processed so that all
    sequences have been padded to the same length. The first
    2 lines of the input file will be in the following format
    after writing the info to the file:
    "
    number_of_seqs_in_file\t<###>\n
    length_of_each_sequence\t<$$$>\n
    "
    where '<###>' is the number of sequences in the file, and
    '<$$$>'is the length to which every sequence in the file is
    padded.

    Args:
    -----
        input_seqs (str) -- the absolute path of the processed
        input sequences to extract information from.

    Returns:
    -----
        None
    """
    # Assertions
    assert isinstance(input_seqs, str), 'Absolute pathname must be passed\
    as a string.'
    assert os.path.exists(input_seqs), 'Input file does not exist.'
    # Functionality
    num_seqs = get_seq_count(input_seqs)
    with smart_open(input_seqs, 'r') as f:
        line = check_valid_line(f.readline())
        if line == 'skip_line':
            raise AssertionError('First line is not valid.')
        seq, _ = separate_seq_and_el_data(line)
        len_seqs = len(seq)  # assumes all sequences padded to same length
    with smart_open(input_seqs, 'r+') as f:
        contents = f.read()
    with smart_open(input_seqs, 'w+') as f:
        line_to_append = 'number_of_seqs_in_file\t' + str(num_seqs) + '\n'
        line_to_append += 'length_of_each_sequence\t' + str(len_seqs) + '\n'
        if input_seqs.endswith('.gz'):
            line_to_append = line_to_append.encode()
        f.write(line_to_append + contents)

    return


def get_num_and_len_of_seqs_from_file(input_seqs):
    """
    Returns the number of sequences and length of sequences in an
    input file. Assumes sequences have been processed so that all
    sequences have been padded to the same length, and that the
    file containing the process sequences have the first 2 lines in
    the following format:
    "
    number_of_seqs_in_file\t<###>
    length_of_each_sequence\t<$$$>
    "
    where '<###>' is the number of sequences in the file, and
    '<$$$>'is the length to which every sequence in the file is
    padded.

    Args:
    -----
        input_seqs (str) -- the absolute path of the processed
        input sequences to extract information from.

    Returns:
    -----
        num_seqs (int) -- the number of sequences in input_seqs.

        len_seqs (int) -- the length of the all the padded
        sequences in the input file.
    """
    # Assertions
    assert isinstance(input_seqs, str), 'Absolute pathname must be passed\
    as a string.'
    assert os.path.exists(input_seqs), 'Input file does not exist.'
    # Functionality
    with smart_open(input_seqs, 'r') as f:
        # Parse first line of file containing info about num of seqs in file
        first_line = check_valid_line(f.readline())
        assert first_line != 'skip_line', 'Invalid first line of file. Must\
        be of the form: "number_of_seqs_in_file\t<###>" where <###> is the\
        number of sequences in the file.'
        token, num_seqs = separate_seq_and_el_data(first_line)
        if num_seqs % 1 != 0:
            raise ValueError('Number of sequences on first line must be\
            an integer.')
        assert token == 'number_of_seqs_in_file', 'First line of the input\
        file must be of the form: "number_of_seqs_in_file\t<###>" where\
        <###> is the number of sequences in the file.'

        # Parse 2nd line of file containing info about length of seqs in file
        second_line = check_valid_line(f.readline())
        assert second_line != 'skip_line', 'Invalid second line of file.\
        Must be of the form: "length_of_each_sequence\t<###>" where <###> is\
        the length of every sequence in the file.'
        token, len_seqs = separate_seq_and_el_data(second_line)
        if len_seqs % 1 != 0:
            raise ValueError('Sequence length on second line must be an\
            integer.')
        assert token == 'length_of_each_sequence', 'Second line of the input\
        file must be of the form: "length_of_each_sequence\t<###>" where\
        <###> is the length of every sequence in the file. Assumes\
        homogeneity and/or padding of sequences.'

    return num_seqs, len_seqs


def create_sample_data(input_seqs, sample_size):
    """
    Takes a sample of size 'sample_size' from an input file
    containing sequences and their associated expression levels,
    and writes them to a separate file. The format of the first
    2 lines of the resulting output file will be of the format:
    "
    number_of_seqs_in_file\t<###>
    length_of_each_sequence\t<$$$>
    "
    where '<###>' is the number of sequences in the file, and
    '<$$$>'is the length to which every sequence in the file is
    padded.

    Args:
    -----
        input_seqs (str) -- the absolute path of the input file
        containing sequence and expression level data to sample.

        sample_size (int) -- the number of samples to take from
        the input file.

    Returns:
    -----
        sample_data (str) -- the absolute path of the output file
        containing the sample of sequence and expression level
        data.
    """
    # Assertions
    assert isinstance(input_seqs, str), 'Input sequences file path must be\
    passed as a string.'
    assert os.path.exists(input_seqs), 'Input file does not exist.'
    assert isinstance(sample_size, int), 'Number of sequences to sample must\
    be passed as an integer.'
    assert sample_size < get_seq_count(input_seqs), 'Sample size must be\
    smaller than the number of sequences in the input file.'
    # Functionality
    # Define output file path
    index = input_seqs.rfind('/') + 1
    insert = str(sample_size) + '_from_'
    sample_seqs = input_seqs[:index] + insert + input_seqs[index:]
    # Pull sequences to create sample data
    with smart_open(input_seqs, 'r') as inf:
        inf.readline()
        inf.readline()  # skip the first 2 info lines
        all_lines = inf.readlines()
        for i in range(50):
            lines = random.sample(all_lines, sample_size)
    with smart_open(sample_seqs, 'w') as g:
        for line in lines:
            g.write(line)
    # Write number and length of sequence info to top of resulting file
    write_num_and_len_of_seqs_to_file(sample_seqs)

    return sample_seqs


# def split_scaffolds_by_type(infile):
#     """
#     Splits the scaffold data contained within an Excel file
#     found at https://www.biorxiv.org/highwire/filestream/85247/
#     field_highwire_adjunct_files/1/224907-2.xlsxin by scaffold
#     type, creating different output files for each type that
#     contain all the scaffold IDs and sequences (tab separated).
#     Output files are created in the ExpressYeaself/example
#     directory.
#
#     Args:
#     -----
#         scaff_infile (str) -- the absolute path for the input file
#         containing all the scaffold data.
#
#     Returns:
#     -----
#         None
#     """
#     # Assertions
#     assert isinstance(infile, str), 'TypeError: input file pathname must be \
#     a string.'
#     assert os.path.exists(infile), 'Input file does not exist.'
#     # Functionality
#     scaff_df = pd.read_excel(infile, index_col = 'Scaffold ID')
#     types = scaff_df['Scaffold type'].unique()
#     for type in types:
#         # Create a new output file for each unique type of scaffold
#         relative_path = 'example/' + type + '_scaffolds.txt'
#         absolute_path = os.path.join(os.getcwd(), relative_path)
#         outfile = smart_open(absolute_path, 'w')
#         # Reduce scaffold data to only data of the current type
#         type_df = scaff_df[scaff_df['Scaffold type'] == type]
#         for index, row in type_df.iterrows():
#             outfile.write(index + '\t' + row['Sequence'] + '\n')
#         outfile.close()
#
#     return
