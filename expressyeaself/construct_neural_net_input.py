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

def get_input(input_sequences, scaffold_type=None, homogeneous=True,
				encoding_method='One-Hot'):
	"""
	Converts raw data as retrieved from Carl de Boer's publication
	at https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE104878
	into encoded sequences and expression levels in the correct format
	for input into a neural network.

	Args:
	-----
		input_file (str) -- the absolute pathname of the file that
		contains all of the input sequences and their expression
		levels (tab separated).

		scaffold_type (str) -- the scaffold type (pTpA or Abf1TATA)
		that the input sequences had their expression levels
		measured in.

		homogeneous (bool) -- if True, only sequences of modal
		length will be used in the data set. If False, all sequences
		will be encoded regardless of length.

		encoding_method (str) -- the method by which the sequences
		should be encoded.

	Returns:
	-----
		encoded_data (TYPE) -- the encoded data, ready for input
		into a neural network architecture.
	"""
	# Assertions
	assert isinstance(input_sequences, str), 'Input file path name must be \
	passed as a string.'
	assert isinstance(scaffold_type, (str, type(None)), 'Scaffold type must \
	be passed as a string if specified.'
	if scaffold_type is not None:
		assert scaffold_type == 'pTpA' or scaffold_type == 'Abf1TATA', 'If \
		specified, the scaffold type must be either pTpA or Abf1TATA'
	assert isinstance(homogeneous, bool), 'The homogeneous argument must be \
	passed as a bool.'
	assert isinstance(encoding_method, str), 'The encoding method should be \
	passed as a string.'
	assert encoding method in METHODS, 'Not a valid method of encoding, must \
	be of the following : %s' %(METHODS)
	# Functionality
	infile = input_sequences
	# Create new file of only homogeneous (same length) sequences if specified
	if homogeneous:
		relative_path = '../example/' + scaffold_type + '_data/' + \
		scaffold_type + '_homogeneous_seqs.txt'
		infile = os.path.join(os.getcwd(), relative_path)
		organize.pull_homogeneous_sequences(input_sequences, outfile=infile,
											scaffold_type=scaffold_type)
	# Remove all of the flanking sequences from the input sequences
	if scaffold_type != None:
		build.remove_flanks_from_all_seqs(infile,
										scaffold_type=scaffold_type, outfile)
	



	return encoded_data
