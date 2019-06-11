"""
This script contains the unit tests for the functions found in
the utilities.py script.
"""
import expressyeaself.tests.context as context
import os

test = context.utilities


def test_smart_open():
    """
    Tests the function that decompresses (if compressed) and opens
    a file.
    """
    # Test case 1: creating file
    filename = './trial_file.txt'
    with test.smart_open(filename, 'w'):
        assert os.path.exists(filename), 'File does not exist.'
    with test.smart_open(filename, 'w') as f:
        text = 'This is a test'
        f.write(text)
    with test.smart_open(filename, 'r') as f:
        assert f.readline() == text
    # Test case 2: creating and writing to compressed file
    filename = './trial_file.txt.gz'
    with test.smart_open(filename, 'w') as f:
        text = 'This is a test'
        f.write(text.encode())
    with test.smart_open(filename, 'r') as f:
        line = f.readline()
        assert line == text.encode()

    return


def test_get_time_stamp():
    """
    Tests the function that produces a unique time stamp.
    """
    # Test case 1: uniqueness
    test_stamp_1 = test.get_time_stamp()
    test_stamp_2 = test.get_time_stamp()
    assert test_stamp_1 != test_stamp_2
    # Test case 2: format
    forbidden_chars = ['.', '-', ' ', ':']
    idx = test_stamp_1.find('.')
    for char in forbidden_chars:
        idx = test_stamp_1.find(char)
        if idx != -1:
            raise AssertionError('Function not removing non-digit characters\
                                 correctly.')

    return


def test_get_seq_count():
    """
    Tests the function that returns the line count of an input
    file.
    """
    # Test case 1: known line count
    filename = 'trial_file.txt'
    line_count = 10
    with test.smart_open(filename, 'w') as f:
        for i in range(0, line_count):
            f.write('ATGC\t%s\n' % (str(i)))
    seq_count = test.get_seq_count(filename)
    assert isinstance(seq_count, int)
    assert seq_count == line_count
    # Test case 2: file with invalid line
    with test.smart_open(filename, 'a') as f:
        f.write('This line is invalid')
    seq_count = test.get_seq_count(filename)
    assert seq_count == line_count
    # Test case 3: non-existent file
    try:
        test.get_seq_count('made_up_file.txt')
    except AssertionError:
        pass

    return


def test_separate_seq_and_e_data():
    """
    Test the function that takes a line of an input file and
    sepaarates and returns the nucleotide sequence as a string
    and its associated expression level as a float.
    """
    # Test case 1: known line
    trial_line = 'ATCGCTAGCT\t5'
    seq, el = test.separate_seq_and_el_data(trial_line)
    assert isinstance(seq, str)
    assert isinstance(el, float)
    assert seq == 'ATCGCTAGCT'
    assert el == 5.0
    # Test case 2: non-string input
    trial_input = True
    try:
        test.separate_seq_and_el_data(trial_input)
    except AssertionError:
        pass
    # Test case 3: invalid line
    trial_line = 'ATGC 6'
    try:
        test.separate_seq_and_el_data(trial_line)
    except IndexError:
        pass

    return


def test_check_valid_line():
    """
    Tests the function that checks the validity of a line from an
    input file, containing a nucleotide sequence tab separated from
    its associated expression level.
    """
    # Test case 1: comment line
    trial_line = '#This is a comment'
    assert test.check_valid_line(trial_line) == 'skip_line'
    # Test case 2: invalid line
    trial_line = 'Invalid line'
    assert test.check_valid_line(trial_line) == 'skip_line'
    # Test case 3: valid line
    trial_line = 'ATGC\t5'
    assert test.check_valid_line(trial_line) == trial_line
    # Test case 4: valid encoded line
    trial_line = 'ATGC\t5'
    assert test.check_valid_line(trial_line.encode()) == trial_line

    return
