"""
A script containing unit tests for the functions in the
encode_sequences.py script.
"""
import expressyeaself.tests.context as context
import numpy as np
import os

test = context.encode_sequences
organize = context.organize_data


def test_encode_sequences_with_method():
    """
    Tests the wrapper function that encodes all promoter sequences
    in an input file by a specified method.
    """
    # Test case 1: homogeneous sequences, no extra padding
    trial_path = 'trial_file.txt'
    oligos = ['AAAA', 'TTTT', 'GGGG', 'CCCC']
    with open(trial_path, 'w') as f:
        el = - 0.67
        num = 5.5
        for oligo in oligos:
            el += num
            f.write(oligo + '\t' + str(el) + '\n')
    organize.write_num_and_len_of_seqs_to_file(trial_path)
    seqs, els, abs_max = test.encode_sequences_with_method(trial_path)
    assert isinstance(seqs, np.ndarray)
    assert isinstance(els, np.ndarray)
    assert isinstance(abs_max, float)
    assert len(seqs) == len(oligos)
    assert max(els) <= 1
    assert min(els) >= -1
    assert abs_max == - 0.67 + (4 * 5.5)
    os.remove(trial_path)

    return


def test_one_hot_encode_sequence():
    """
    Tests the function that encodes the string representation of a
    nucleotide sequence using the 'One-Hot' encoding method.
    """
    # Test case 1 : valid input
    seq = 'AAA'
    one_hot_seq = test.one_hot_encode_sequence(seq)
    print(one_hot_seq)
    assert np.allclose(one_hot_seq, np.array([[1, 0, 0, 0, 0],
                                              [1, 0, 0, 0, 0],
                                              [1, 0, 0, 0, 0]]))
    # Test case 2: valid characters but lower case
    seq = 'acgnt'
    out_seq = test.one_hot_encode_sequence(seq)
    assert np.allclose(out_seq, np.array([[1, 0, 0, 0, 0],
                                          [0, 0, 0, 1, 0],
                                          [0, 0, 1, 0, 0],
                                          [0, 0, 0, 0, 1],
                                          [0, 1, 0, 0, 0]]))
    # Test case 2: invalid input
    seq = 'XYZXYZXYZ'
    try:
        one_hot_seq = test.one_hot_encode_sequence(seq)
    except Exception:
        pass

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
