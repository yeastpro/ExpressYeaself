"""
This script contains the functions to encode promoter nucleotide
sequences by different methods, depending on the requirement of the
neural network that will receive the encoded sequence.
Methods by which sequences can be encoded: One-Hot.
"""
import numpy as np
import organize_data as organize
import os
from utilities import smart_open as smart_open
from utilities import get_time_stamp as get_time_stamp

BASES = ['A','T','G','C']
METHODS = ['One-Hot']

def encode_sequences_with_method(input_seqs, method='One-Hot',
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
	assert isinstance(input_seqs, str), 'TypeError: Input file path must be \
	passed as a string.'
	assert isinstance(method, str), 'TypeError: Specified method must be a \
	a string.'
	assert method in METHODS, 'Must specify one the method of encoding the \
	sequence. Choose one of: %s' %(METHODS)
	# Functionality
	# Define absolute path of output file
	time_stamp = get_time_stamp() # get time stamp for unique file naming
	relative_path = ('../example/encoded_data/' + time_stamp +
		'_encoded_sequences')
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
		pass
	relative_path += '.txt'
	absolute_path = os.path.join(os.getcwd(), relative_path)
	# Open input and output files
	infile = smart_open(input_seqs, 'r')
	# outfile = smart_open(absolute_path, 'w')
	# Encode and pad each sequence and write it to file with expression level
	max_length, _, _ = organize.get_max_min_mode_length_of_seqs(input_seqs)
	line_number = 1
	out_dict = {}
	for line in infile:
		line_number += 1
		line = organize.check_valid_line(line)
		if line == 'skip_line':
			continue
		seq, exp_level = organize.separate_seq_and_el_data(line)
		# Encode
		if method == 'One-Hot':
			try:
				encoded_seq = one_hot_encode_sequence(seq)
			except Exception:
				print('Error on line %s' %(line_number))
				raise AssertionError
		else:
			# Another encoding method will go here
			# encoded_seq = another_encoding_method(seq)
			pass
		# Pad
		if pad_sequences:
			resize_len = max_length + extra_padding
		else:
			resize_len = len(encoded_seq) + extra_padding
		if len(encoded_seq) == resize_len: # Doesn't need resizing
			pass
		else:
			encoded_seq = resize_array(encoded_seq, resize_to=resize_len,
										edit_front=pad_front)
		# Write sequence and EL to file.
		# outfile.write(str(encoded_seq) + '\t' + str(exp_level) + '\n')
		out_dict[line_number] = (encoded_seq, exp_level)
	# Close the input and output files
	infile.close()
	# outfile.close()

	# return absolute_path
	return out_dict

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
	mapping =  {'A' : [1,0,0,0,0],
			  	'T' : [0,1,0,0,0],
				'G' : [0,0,1,0,0],
				'C' : [0,0,0,1,0],
				'N' : [0,0,0,0,1],
				'P' : [0,0,0,0,0]}
	invalid_indices = []
	index = -1 # Iterator for character index in promoter_seq string
	for nuc in promoter_seq:
		index += 1
		nuc = nuc.upper()
		if nuc not in mapping.keys():
			invalid_indices.append(index) # Appends list of incorrect indices
	if len(invalid_indices) is not 0:
		raise Exception('Input nucleotide sequence contains a non ATGC or \
		"N" or "P" at string indices %s' %(invalid_indices))
	# Functionality
	one_hot_seq = []
	for nuc in promoter_seq:
		# index = -1 # Iterator for index in BASES list
		# nuc_vector = []
		# if nuc == 'N':
		# 	nuc_vector = [0,0,0,0] # add a null vector
		# else:
		# 	for base in BASES:
		# 		index += 1
		# 		if nuc == base:
		# 			nuc_vector.append(1)
		# 		else:
		# 			nuc_vector.append(0)
		# one_hot_seq.append(nuc_vector)
		nuc = nuc.upper()
		one_hot_seq.append(mapping(nuc))

	return one_hot_seq

def resize_array(input_array, resize_to=None, edit_front=False):
	"""
	Takes an M x N 2D array (where M is the length to edit) and
	resizes it to the specified resize_to length, adding (if too
	short) null vectors ([0,0,0,0,...] of length N) or removing
	base vectors (if too long) from either the front or end of
	the sequence so that the output encoded array is of dimensions
	(resize_to) x N.

	Args:
	-----
		input_array (list) -- the one-hot encoded binary 2D array
		to resize.

		resize_to (int) -- the length to resize the array to.
		Default: None (returns the input array with no resizing).

		edit_front (bool) -- whether to add/remove binary base
		vectors from the front or back of the array. Default:
		False (so removes them from the back).

	Returns:
	-----
		input_array (list) -- the resized array of dimensions
		(resize_to)x4.
	"""
	# Assertions
	assert isinstance(input_array, list), 'Input array must be a list.'
	assert isinstance(resize_to, (int, type(None))), 'Length to resize the \
	array to must be an integer or None.'
	assert isinstance(edit_front, bool), 'TypeError: edit_front must be a bool.'
	previous_len = len(input_array[0])
	for i in range(1, len(input_array)): # check vectors in array same length
		current_len = len(input_array[i])
		assert current_len == previous_len, 'Not all vectors in input array \
		are of the same length.'
		previous_len = current_len
	# Functionality
	len_diff = len(input_array) - resize_to
	if len_diff == 0: # doesn't need resizing
		return input_array
	elif len_diff > 0: # Sequence needs trimming
		if edit_front:
			return input_array[-resize_to:]
		else:
			return input_array[:resize_to]
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
