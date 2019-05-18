"""
This script contains the functions to encode promoter nucleotide
sequences by different methods, depending on the requirement of the
neural network that will receive the encoded sequence.
Methods by which sequences can be encoded: One-Hot.
"""
import numpy as np
import organize_data as organize
from utilities import get_time_stamp as get_time_stamp

BASES = ['A','T','G','C']
METHODS = ['One-Hot']

def encode_sequence_with_method(input_seqs, method='One-Hot',
								pad_sequences=True, extra_padding=0,
								pad_front=False):
	"""
	A wrapper function that encodes all of the sequences in an
	input file according to the specified method, pads them to
	the maximum sequence length (if specified), and writes the
	them to an output file along with their expression levels
	(tab separated).

	Args:
	-----
		input_seqs (str) -- the absolute path of the file containing
		all of the input sequences to be encoded.

		method (str) -- the method by which the sequence should be
		encoded. Must choose from: 'One-Hot'. Default: 'One-Hot'

		pad_sequences (bool) -- If True will pad the sequences with
		null vectors to be the length of the longest sequence in the
		input file. If False will not change their length.
		Default: True.

		extra_padding (int) -- the number of vectors greater than the
		maximum sequence length to pad each encoded sequence to.
		Default: 0.

		pad_front (bool) -- whether to pad the front or end of the
		encoded sequences, if pad_sequences is specified to be True.
		Default: False (will therefore pad the ends).

	Returns:
	-----
		absolute_path (list) -- the absolute path of the file containing
		all of the encoded sequences and their expression levels, tab
		separated.
	"""
	# Assertions
	assert isinstance(input_seq, str), 'TypeError: Input file path must be \
	passed as a string.'
	assert isinstance(method, str), 'TypeError: Specified method must be a \
	a string.'
	assert method in METHODS, 'Must specify one the method of encoding the \
	sequence. Choose one of: %s' %(METHODS)
	# Functionality
	# Define absolute path of output file
	time_stamp = get_time_stamp() # get time stamp for unique file naming
	relative_path = '../example/encoded_data/' + time_stamp
	if pad_sequences:
		if pad_front:
			relative_path += '_front_padded'
		else:
			relative_path += '_end_padded'
	else:
		relative_path += '_unpadded'
 	if extra_padding != 0:
		relative_path += '_extra_%s' %(extra_padding)
	else:
		continue
	relative_path += '_encoded_sequences.txt'
	absolute_path = os.path.join(os.getcwd(), relative_path)
	# Open input and output files
	input_seqs = smart_open(input_seqs, 'rt')
	outfile = smart_open(absolute_path, 'wt')
	# Encode and pad each sequence and write it to file with expression level
	max_length, _, _ = organize.get_max_min_mode_length_of_seqs(input_seqs)
	for line in input_seqs:
		seq, exp_level = organize.separate_seq_and_el_data(line)
		if method = 'One-Hot':
			encoded_seq = one_hot_encode_sequence(seq)
			if pad_sequences:
				encoded_seq = resize_array(encoded_seq,
									max_length=(max_length + extra_padding),
									edit_front=pad_front)
		outfile.write(encoded_seq + '\t' + exp_level + '\r\n')
	# Close the input and output files
	input_seqs.close()
	outfile.close()

	return absolute_path

def one_hot_encode_sequence(promoter_seq):
	"""
	Encodes a string nucleotide sequence using the 'One-Hot' encoding
	method into a 2D array.

	Args:
	-----
		promoter_seq (str)	-- the promoter sequence to be encoded.

	Returns:
	-----
		one_hot_seq (str) -- the One-Hot encoded nucleotide sequence
		as a 2D array.
	"""
	# Assertions
	assert isinstance(promoter_seq, str), 'TypeError: Input nucleotide \
	sequence must be a string.'
	non_ATGC_indices = []
	index = -1 # Iterator for character index in promoter_seq string
	for nuc in promoter_seq:
	    index += 1
	    if nuc not in BASES:
	        non_ATGC_indices.append(index) # Appends list of incorrect indices
	if len(non_ATGC_indices) is not 0:
	    raise Exception('Input nucleotide sequence contains a non ATGC base at \
		string indices %s' %(non_ATGC_indices))
	# Functionality
	one_hot_seq = []
	for nuc in promoter_seq:
		index = -1 # Iterator for index in BASES list
		nuc_vector = []
		for base in BASES:
			index += 1
			if nuc == base:
				nuc_vector.append(1)
			else:
				nuc_vector.append(0)
		one_hot_seq.append(nuc_vector)

	return one_hot_seq

def resize_array(input_array, max_length=223, edit_front=False):
	"""
	Takes an M x N 2D array (where M is the length to resize) and
	resizes it to the specified maximum length, adding (if too short)
	null vectors ([0,0,0,0,...] of length N) or removing
	base vectors (if too long) from either the front or end of the
	sequence so that the output encoded array is of dimensions
	(max_length) x N.

	Args:
	-----
		input_array (list) -- the one-hot encoded binary 2D array
		to resize.

		max_length (int) -- the length to resize the array to.

		edit_front (bool) -- whether to add/remove binary base
		vectors from the front or back of the array. Default: False.

	Returns:
	-----
		input_array (list) -- the resized array of dimensions
		(max_length)x4.
	"""
	# Assertions
	assert isinstance(input_array, list), 'Input array must be a list.'
	assert isinstance(max_length, int), 'Max length must be an integer.'
	assert isinstance(edit_front, bool), 'TypeError: edit_front must be a bool.'
	previous_len = len(input_array[0])
	for i in range(1, len(input_array)): # check vectors in array same length
	    current_len = len(input_array[i])
	    assert current_len == previous_len, 'Not all vectors in input array \
		are of the same length.'
	    previous_len = current_len
	# Functionality
	len_diff = len(input_array) - max_length
	if len_diff == 0: # doesn't need resizing
		return input_array
	elif len_diff > 0: # Sequence needs trimming
		if edit_front:
			return input_array[-max_length:]
		else:
			return input_array[:max_length]
	elif len_diff < 0: # Sequence needs filling
		# Ensuring null vector to be added matches dimensions of input array
		null_vect = [0] * len(input_array[0])
		if edit_front:
			for i in range(0, len_diff):
				input_array.insert(0, null_vect)
			return input_array
		else:
			for i in range(0, len_diff):
				input_array.append(null_vect)
			return input_array

	return
