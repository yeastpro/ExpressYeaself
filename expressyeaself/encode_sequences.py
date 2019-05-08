"""
This script contains the functions to encode promoter nucleotide
sequences by different methods, depending on the requirement of the
neural network that will receive the encoded sequence.
Methods by which sequences can be encoded: One-Hot.
"""

BASES = ['A','T','G','C']
METHODS = ['One-Hot']

def encode_sequence_with_method(promoter_seq, method):
	"""
	A wrapper function that takes a promoter sequence and encodes it
	according to the method specified as an argument.

	Args:
	-----
		promoter_seq (str) -- the promoter sequence to be encoded.
		method (str)       -- the method by which the sequence should be
								encoded. Must choose from: 'One-Hot'.
	Returns:
	-----
		encoded_seq (TYPE) -- the nucleotide sequence encoded by the
								specified method.
	"""
	# Assertions
	assert isinstance(promoter_seq, str), 'TypeError: Input nucleotide \
	sequence must be a string.'
	assert isinstance(method, str), 'TypeError: Specified method must be a \
	a string.'
	assert method in METHODS, 'Must specify one the method of encoding the \
	sequence. Choose one of: %s' %(METHODS)
	non_ATGC_indices = []
	index = -1 # Iterator for character index in promoter_seq string
	for i in check:
	    index += 1
	    if i not in BASES:
	        non_ATGC_indices.append(index) # Appends list of incorrect indices
	if len(non_ATGC_indices) is not 0:
	    raise Exception('Input nucleotide sequence contains a non ATGC base at \
		string indices %s' %(non_ATGC_indices))

	# Functionality
	if method == 'One-Hot':
		encoded_seq = one_hot_encode_sequence(promoter_seq)


	return encoded_seq

def one_hot_encode_sequence(promoter_seq):
	"""
	Encodes a string nucleotide sequence using the 'One-Hot' encoding
	method, typically for use in a 1D convolutional neural network.

	Args:
	-----
		promoter_seq (str) -- the promoter sequence to be encoded.

	Returns:
	-----
		one_hot_seq (str) -- the One-Hot encoded nucleotide sequence.
	"""
	# Assertions
	assert isinstance(promoter_seq, str), 'TypeError: Input nucleotide \
	sequence must be a string.'
	non_ATGC_indices = []
	index = -1 # Iterator for character index in promoter_seq string
	for i in check:
	    index += 1
	    if i not in BASES:
	        non_ATGC_indices.append(index) # Appends list of incorrect indices
	if len(non_ATGC_indices) is not 0:
	    raise Exception('Input nucleotide sequence contains a non ATGC base at \
		string indices %s' %(non_ATGC_indices))

	# Functionality

	return one_hot_seq
