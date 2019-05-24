"""
This script contains the unit tests for the functions found in
the utilities.py script.
"""
import expressyeaself.tests.context as context
import os

test = context.utilities()

def test_smart_open():
    """
    Tests the function that decompresses (if compressed) and opens
    a file.
    """
    file = test.smart_open('./trial_file.txt', 'w')
    assert os.path.exists(file), 'File does not exist.'
    os.remove(file)

    return

def test_get_time_stamp():
    """
    Tests the function that produces a unique time stamp.
    """

    return

def test_get_line_count():
    """
    Tests the function that returns the line count of an input
    file.
    """

    return
