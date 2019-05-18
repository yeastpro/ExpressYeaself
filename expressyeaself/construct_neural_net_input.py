"""
This script contains a wrapper function to convert raw data into
encoded sequences in the correct format for passing into a
neural network architecture.
"""

import build_promoter as build
import encode_sequences as encode
from encode_sequences import BASES as BASES
from encode_sequences import METHODS as METHODS
import organize_data as organize
import os
from utilities import smart_open as smart_open
from utilities import get_time_stamp as get_time_stamp

def convert_raw_to_encoded(input_seqs, scaffold_type='pTpA', homogeneous=True,
							deflank=True, insert_into_scaffold=True,
							encoding_method='One-Hot', pad_sequences=True,
							extra_padding=0, pad_front=False):
	"""
	Takes raw data as retrieved from Carl de Boer's publication
	at https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE104878,
	and processes and encodes the sequences, writing them to an output
	file along with their expression levels (tab separated).

	Args:
	-----
		input_seqs (str) -- the absolute pathname of the file that
		contains all of the input sequences and their expression
		levels (tab separated).

		scaffold_type (str) -- the scaffold type (pTpA or Abf1TATA)
		that the input sequences had their expression levels
		measured in.

		homogeneous (bool) -- if True, only sequences of modal
		length will be used in the data set. If False, all sequences
		will be encoded regardless of length.

		deflank (bool) -- if True, removes the constant flanking
		regions of the input sequences.

		insert_into_scaffold (bool) -- if True inserts the input
		sequences into the appropriate scaffold. If False, the
		sequences are encoded as they are.

		encoding_method (str) -- the method by which the sequences
		should be encoded.

		pad_sequences (bool) -- if True pads all of the encoded
		sequences so that they are the same length.

		extra_padding (int) -- the number of vectors greater than the
		maximum sequence length to pad each encoded sequence to.
		Default: 0.

		pad_front (bool) -- whether to pad out the front (left hand side)
		or end (right hand side) of the encoded sequences. If True, pads
		the front. Default: False (will pad the end).

	Returns:
	-----
		encoded_data (str) -- the absolute path for the file containing
		encoded sequences along with their expression levels.
	"""
	# Assertions
	assert isinstance(input_seqs, str), 'Input file path name must be \
	passed as a string.'
	assert isinstance(scaffold_type, str), 'Scaffold type must \
	be passed as a string if specified.'
	assert scaffold_type == 'pTpA' or scaffold_type == 'Abf1TATA', 'Scaffold \
	type must be specified as either "pTpA" or "Abf1TATA".'
	assert isinstance(homogeneous, bool), 'The homogeneous argument must be \
	passed as a bool.'
	assert isinstance(deflank, bool), 'The deflank argument must be passed \
	as a bool.'
	assert isinstance(insert_into_scaffold, bool), 'The insert_into_scaffold \
	argument must be passed as a bool.'
	assert isinstance(encoding_method, str), 'The encoding method should be \
	passed as a string.'
	assert encoding method in METHODS, 'Not a valid method of encoding, must \
	be of the following : %s' %(METHODS)
	assert isinstance(pad_sequences, bool), 'The pad_front argument must be \
	passed as a bool.'
	assert isinstance(extra_padding, int), 'The number of extra vectors to pad \
	each sequence by should be passed as an integer.'
	assert extra_padding >= 0, 'extra_padding must be passed as a non-negative \
	integer.'
	assert isinstance(pad_front, bool), 'The pad_front argument must be passed \
	as a bool.'
	# Functionality
	encoded_data = get_time_stamp() + scaffold_type + 'encoded_sequences'
	# Create new file of only homogeneous (same length) seqs
	if homogeneous:
		pad_sequences = False # if all seqs same length they don't need padding
		input_seqs = organize.pull_homogeneous_seqs(input_seqs,
									scaffold_type=scaffold_type)
		encoded_data += '_homogeneous'

	# Remove all of the flanking regions from the input sequences
	if deflank:
		input_seqs = build.remove_flanks_from_all_seqs(input_seqs,
									scaffold_type=scaffold_type)
		encoded_data += '_deflanked'
	# Insert sequences into appropriate scaffold
	if insert_into_scaffold:
		input_seqs = build.insert_all_seq_into_one_scaffold(input_seqs,
									scaffold_type=scaffold_type)
		encoded_data += '_inserted_into_scaffold'
	# Encode sequences by the method specified by encoding_method

	encoded_data += encoding_method
	# Encoded and pad sequences
	
	if pad_sequences:
		if homogeneous: # Don't need to pad to maximum length as all same length
			continue
		else: # need to pad all sequences to the maximum length
			if pad_front:
				# pad front of sequence
				encoded_data += '_front_padded'
			else:
				# pad end
				encoded_data += '_end_padded'
		if extra_padding != 0:
			# add extra vectors
			if pad_front:
				# add extras to front
			else:
				# add extras to end
			encoded_data += '_extra_%s' %(extra_padding)
		else:
			continue
	else:
		encoded_data += '_unpadded'
		continue

	encoded_data += '.txt'

	return encoded_data
