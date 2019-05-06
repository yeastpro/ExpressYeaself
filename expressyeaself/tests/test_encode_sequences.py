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


	return
