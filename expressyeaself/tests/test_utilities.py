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
    filename = './trial_file.txt'
    file = test.smart_open(filename, 'w')
    file.close()
    assert os.path.exists(filename), 'File does not exist.'
    with test.smart_open(filename, 'w') as f:
        text = 'This is a test'
        f.write(text)
    with test.smart_open(filename, 'r') as f:
        assert f.readline() == text
    os.remove(filename)

    return


def test_get_time_stamp():
    """
    Tests the function that produces a unique time stamp.
    """
    # Test for uniqueness
    test_stamp_1 = test.get_time_stamp()
    test_stamp_2 = test.get_time_stamp()
    assert test_stamp_1 != test_stamp_2
    # Test for format
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

    return
