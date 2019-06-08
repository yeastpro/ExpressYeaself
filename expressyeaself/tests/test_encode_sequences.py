"""
A script containing unit tests for the functions in the
encode_sequences.py script.
"""
import expressyeaself.tests.context as context

test = context.encode_sequences

def test_encode_sequences_with_method():
    """
    Tests the wrapper function that encodes all promoter sequences
    in an input file by a specified method.
    """
    # test_file =

    return

def test_one_hot_encode_sequence():
    """
    Tests the function that encodes the string representation of a
    nucleotide sequence using the 'One-Hot' encoding method.
    """
    seq = 'AAA'
    one_hot_seq = test.one_hot_encode_sequence(seq)
    assert one_hot_seq == [[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0]]

    return

# def test_resize_array():
#     """
#     Tests the function that resizes a 2D array to a specified
#     desired length by adding or removing vectors from the front
#     or end of the array.
#     """
#     trial_seq = [[1],[2],[3],[4],[5],[6]]
#     # Test 1
#     out_1 = test.resize_array(trial_seq, resize_to=6, edit_front=True)
#     assert isinstance(out_1, list), 'Function should be outputting a list'
#     assert out_1 == trial_seq, 'Max length same as length of input list \
#     so function should return list unchanged'
#     # Test 2
#     out_2 = test.resize_array(trial_seq, resize_to=5, edit_front=True)
#     assert len(out_2) == 5
#     assert out_2 == [[2],[3],[4],[5],[6]]
#     # Test 3
#     out_3 = test.resize_array(trial_seq, resize_to=7, edit_front=True)
#     assert len(out_3) == 7
#     assert out_3 == [[0],[1],[2],[3],[4],[5],[6]]
#     # Test 4
#     trial_seq = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
#     out_4 = test.resize_array(trial_seq_2, resize_to=5, edit_front=False)
#     assert out_4 == [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1],[0,0,0,0]]
#     # Test 5
#     trial_seq = [[1,0,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1]]
#     out_5
#
#     return
