"""
This script contains utility functions that are useful in areas
of the project.
"""
import datetime as dt
import gzip
import os


def smart_open(filename, mode='r'):
    """
    A function to open a file. If the file is compressed
    (with a '.gz' extension) it is decompressed before being
    opened. Otherwise, the function is opened normally.

    Args:
    -----
        filename (str) -- the absolute pathname of the file
        to be opened.

        mode (str) -- the way in which the file should be
        opened by the gzip.open command. Options: 'r', 'rb',
        'a', 'ab', 'w', 'wb', 'x' or 'xb' for binary files,
        and 'rt', 'at', 'wt', or 'xt' for text files.
        Default: 'r'.

    Returns:
    -----
        opened_file (file type) -- the opened file.

    ** Adapted from Carl de Boer's function in https://github.com/
    Carldeboer/CisRegModels/blob/master/CisRegModels/MYUTILS.py **
    """
    # Assertions
    assert isinstance(filename, str), 'Input file pathname must be a string.'
    assert isinstance(mode, str), 'Opening mode must be passed as a string.'
    if mode.startswith('r'):
        assert os.path.exists(filename), 'Input file does not exist.'
    # Functionality
    if len(filename) > 3 and filename.endswith('.gz'):
        file = gzip.open(filename, mode)
    else:
        file = open(filename, mode)

    return file


def get_time_stamp():
    """
    Creates a unique time stamp number containing no other character
    than digits 0~9.
    For instance:
    '2019-05-17 17:04:19.923192' ---> '20190517170419923192'

    Args:
    -----
        None

    Returns:
    -----
        time_stamp (str) -- a unique numerical string of the
        current time.
    """
    time_stamp = str(dt.datetime.now())
    time_stamp = time_stamp.replace(' ', '').replace('-', '')
    time_stamp = time_stamp.replace('.', '').replace(':', '')

    return time_stamp


def get_seq_count(infile):
    """
    Counts and returns the number of sequences in a file.

    Args:
    -----
        infile (str) -- the absolute path for the input file.

    Returns:
    -----
        line_count (int) -- the number of sequences in the input file.
    """
    # Assertions
    assert os.path.exists(infile), 'Input file does not exist.'
    assert isinstance(infile, str), 'Path name for input file must be passed \
    as a string.'
    # Functionality
    count = 0
    with smart_open(infile, 'r') as file:
        for line in file:
            line = check_valid_line(line)
            if line == 'skip_line':
                continue
            else:
                count += 1

    return count


def separate_seq_and_el_data(line):
    """
    Takes a string containing a nucleotide sequence and its expression
    level (el) - tab separated - and returns the sequence as a string
    and the expression level as a float.

    Args:
    -----
        line (str) -- the input line containing the sequence and
        expression level (tab separated) to be separated.

    Returns:
    -----
        seq (str) -- the nucleotide sequence.

        exp_level (float) -- the expression level of the sequence.
    """
    # Assertions
    assert isinstance(line, str), 'Input line must be passed as a string.'
    # Functionality
    data = line.rstrip().split('\t')
    seq = data[0]
    try:
        exp_level = float(data[1])
    except IndexError:
        raise IndexError('Input line must have the sequence and expression\
                         level tab separated.')

    return seq, exp_level


def check_valid_line(line):
    """
    Takes an line from an input file containing sequence and
    expression level data and returns instructions on what to
    do based on its classification. For example, if the line is
    a comment or is empty, the function will return 'skip_line'.
    If the line is encoded into bytes, it will return the
    decoded line. Not satisfying these conditionals will mean the
    line is valid, and so will be returned as it was inputted.

    Args:
    -----
        line (str or bytes) -- a line from an input file to be
        checked for validity

    Returns:
    -----
        line (str) - if the input line was valid, the decoded line
        is returned. Otherwise, the string 'skip_line' will be
        returned.
    """
    if isinstance(line, bytes):  # decodes line if encoded
        line = line.decode()
    if line is None or line == "" or line[0] == "#":
        return 'skip_line'
    try:
        seq, exp_level = separate_seq_and_el_data(line)
    except IndexError:
        line = 'skip_line'

    return line
