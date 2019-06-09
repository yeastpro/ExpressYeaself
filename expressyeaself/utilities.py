"""
This script contains utility functions that are useful in areas
of the project.
"""
import datetime as dt
import gzip
# import expressyeaself.organize_data as organize
import os
import expressyeaself.context as context

organize = context.organize_data


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
            line = organize.check_valid_line(line)
            if line == 'skip_line':
                continue
            else:
                count += 1

    return count
