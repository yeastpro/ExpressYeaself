"""
A script containing unit tests for the functions in the
encode_sequences.py script.
"""
def test_encode_sequence_with_method():
	"""
	Tests the wrapper function that encodes a promoter sequence by a
	specified method.
	"""
	trial_promoter = 'TCGTACGTACGTCGATGCTG'
	method = 'One-Hot'
	try:
		encoded_seq = encode_sequence_with_method(trial_promoter, method)
	except Exception as e:
		assert is instance(e, TypeError)
	# assert isinstance(encoded_seq, TYPE)

	return

def test_one_hot_encode_sequence():
	"""
	Tests the function that encodes the string representation of a
	nucleotide sequence using the 'One-Hot' encoding method.
	"""
	seq = 'AAA'
	try:
		one_hot_seq = one_hot_encode_sequence(seq)
	except Exception as e:
		assert isinstance(e, TypeError)
	assert one_hot_seq == [[1,0,0,0],[1,0,0,0],[1,0,0,0]]

	return

def test_resize_array():
	"""
	Tests the function that resizes a 2D array to a specified
	desired length by adding or removing vectors from the front
	or end of the array.
	"""
	trial_seq = [1,2,3,4,5,6]
	max_len = 6
	edit_front = True
	try:
		out_1 = resize_array(trial_seq, max_len, edit_front)
	except Exception as e:
		assert isinstance(e, TypeError)
	assert isinstance(out_1, list), 'Function should be outputting a list'
	assert out_1 == trial_seq, 'Max length same as length of input list \
	so function should return list unchanged'
	max_len = 5
	try:
		out_2 = resize_array(trial_seq, max_len, edit_front)
	except Exception as e:
		assert isinstance(e, TypeError)
	assert len(out_2) == max_len
	assert out_2 == [2,3,4,5,6]
	max_len = 7
	try:
		out_3 = resize_array(trial_seq, max_len, edit_front)
	except Exception as e:
		assert isinstance(e, TypeError)
	assert len(out_3) == max_len
	assert out_3 = [0,1,2,3,4,5,6]
	trial_seq_2 = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
	max_len_2 = 3
	edit_front_2 = False
	try:
		out_4 = resize_array(trial_seq_2, max_len_2, edit_front_2)
	except Exception as e:
		assert isinstance(e, TypeError)
	assert out_4 = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1],[0,0,0,0]]

	return
