"""
This script contains functions to organize and split up data based
on several experimental parameters.
"""
import os
import matplotlib as plt
import pandas as pd
from utilities import smart_open as smart_open
import xlrd

def split_scaffolds_by_type(infile):
	"""
	Splits the scaffold data contained within an Excel file
	found at https://www.biorxiv.org/highwire/filestream/85247/
	field_highwire_adjunct_files/1/224907-2.xlsxin by scaffold
	type, creating different output files for each type that
	contain all the scaffold IDs and sequences (tab separated).
	Output files are created in the ExpressYeaself/example
	directory.

	Args:
	-----
		scaff_infile (str) -- the absolute path for the input file
		containing all the scaffold data.

	Returns:
	-----
		None
	"""
	# Assertions
	assert isinstance(infile, str), 'TypeError: input file pathname \
	must be a string.'
	assert os.path.exists(infile), 'Input file does not exist.'
	# Functionality
	scaff_df = pd.read_excel(infile, index_col = 'Scaffold ID')
	types = scaff_df['Scaffold type'].unique()
	for type in types:
		# Create a new output file for each unique type of scaffold
		relative_path = '../example/' + type + '_scaffolds.txt'
		absolute_path = os.path.join(os.getcwd(), relative_path)
		outfile = smart_open(absolute_path, 'wt')
		# Reduce scaffold data to only data of the current type
		type_df = scaff_df[scaff_df['Scaffold type'] == type]
		for index, row in type_df.iterrows():
			outfile.write(index + '\t' + row['Sequence'] + '\r\n')
		outfile.close()

	return

def check_oligonucleotide_flanks(seq_infile, scaffold_type):
	"""
	Checks that all the oligonucleotide sequences in an input file
	consist of the same sequences that flank the variable 80-mer
	sequence. i.e. all sequences in the input file should be of the
	form:
	TGCATTTTTTTCACATC-(variable 80-mer seq)-GTTACGGCTGTT
	Whereas the input sequences measured in the Abf1TATA scaffold
	will be of the form:
	TCACGCAGTATAGTTC-(variable 80-mer sequence)-GGTTTATTGTTTATAAAAA
	These flanking sequences are for in-lab sequencing purposes only,
	so can be discarded when the 80-mer variable sequences are
	inserted into the a scaffold sequence.

	Args:
	-----
		seq_infile (str) -- the absolute path of the input file
		containing all of the oligonucleotide sequences to be
		checked, and their expression level values (tab separated).

		scaffold_type (str) -- the scaffold type (pTpA or Abf1TATA)
		in which the expression levels for the sequences in the
		input file were measured.

	Returns:
	-----
		incorrect_lines (list) -- returns a list of line numbers for
		for sequences that contain incorrect flank sequences.
	"""
	# Assertions
	assert isinstance(seq_infile, str), 'Absolute pathname must be passed \
	as a string.'
	assert isinstance(scaffold_type, str), 'Scaffold type must be passed as a \
	string.'
	assert scaffold_type == 'pTpA' or scaffold_type == 'Abf1TATA', 'Scaffold \
	type must be specified as either pTpA or Abf1TATA.'
	# Functionality
	if scaffold_type == 'pTpA':
		flank_A = 'TGCATTTTTTTCACATC'
		flank_B = 'GGTTACGGCTGTT'
	elif scaffold_type == 'Abf1TATA':
		flank_A = 'TCACGCAGTATAGTTC'
		flank_B = 'GGTTTATTGTTTATAAAAA'
	infile = smart_open(seq_infile, 'rt')
	line_number = 0
	incorrect_lines = []
	for line in infile:
		line_number += 1
		seq, exp_level = separate_seq_and_el_data(line)
		if seq.startswith(flank_A) and seq.endswith(flank_B):
			pass
		else:
			incorrect_lines.append(line_number)

	return incorrect_lines

def create_proxy_one_hot_data(data_size=100, scaffold_type='pTpA'):
	"""
	Creates a small data set (of size data_size) of one-hot-encoded
	sequences, where each sequence is of the number of vectors in
	length specified by the scaffold type.
	For pTpA, the length of each sequence is 223 = 54 + 80 + 89,
	where 80 bp is the variable seq and the 54 and 89 bp either side
	is the pTpA scaffold
	For Abf1TATA, the length of each sequence is 245 = 60 + 80 + 105.

	Args:
	-----
		data_size (int) -- the number of data points in the
		sample data set.

		scaffold_type (str) -- the scaffold type (either pTpA or
		Abf1TATA) to mimic the data on.

	Returns:
	-----
		sample_data (list) -- the sample one-hot encoded data.
	"""
	return

def pull_homogeneous_seqs(input_seqs, scaffold_type=None):
	"""
	Pulls all sequences of the modal length (i.e. 110 bp for pTpA-type
	sequences and 115 bp for Abf1TATA-type) from an input file and
	writes them into an output file.

	Args:
	-----
		input_seqs (str) -- the absolute pathname of the input file
		containing all of the raw oligonucleotide sequences and
		their expression levels, tab separated.

		scaffold_type (str) -- the scaffold type (pTpA or Abf1TATA
		for which the modal length is known to be 110 and 115
		respectively) in which the expression levels for the
		sequences in the input file were measured. If None, the
		modal length is calculated manually. Default: None.

	Returns:
	-----
		absolute_path (str) -- the absolute pathname of the output
		file containing the sequences of modal length.
	"""
	# Assertions
	assert isinstance(input_seqs, str), 'Input file pathname must be a string.'
	assert os.path.isfile(input_seqs), 'Input file does not exist!'
	assert isinstance(scaffold_type, str), 'Scaffold type must be passed as a \
	string.'
	assert scaffold_type == 'pTpA' or scaffold_type == 'Abf1TATA', 'Scaffold \
	type must be specified as either pTpA or Abf1TATA, or else unspecified \
	(takes value of None).'
	# Functionality
	# Defining the path name of the output file.
	relative_path = '../example/'
	time_stamp = get_time_stamp()
	if scaffold_type is None:
		relative_path += ('other_scaffolds/' + time_stamp +
			'_homogeneous_seqs.txt')
	else:
		relative_path += (scaffold_type + '_data/' + time_stamp + '_' +
			scaffold_type + '_homogeneous_seqs.txt')
	absolute_path = os.path.join(os.getcwd(), relative_path)
	# Open the input and output files.
	input_seqs = smart_open(input_seqs, 'rt')
	output_seqs = smart_open(absolute_path, 'wt')
	# Retrieve modal length for sequences in input file.
	if scaffold_type == 'pTpA':
		modal_length = 110
	elif scaffold_type == 'Abf1TATA':
		modal_length == 115
	else:
		_, _, modal_length = get_max_min_mode_length_of_seqs(input_seqs)
	# Find seqs in input file w/ modal length and write them to output file
	for line in input_seqs:
		if line is None or line == "" or line[0]=="#":
			continue
		seq, exp_level = separate_seq_and_el_data(line)
		if len(seq) == modal_length:
			output_seqs.write(line + '\r\n')
		else:
			continue
	# Close the input and output files.
	input_seqs.close()
	output_seqs.close()

	return absolute_path

def separate_seq_and_el_data(line):
	"""
	Takes a string containing a nucleotide sequence and its expression
	level (el) - tab separated - and returns the sequence as a string
	and the expression level as a float.

	Args:
	-----
		line (str) -- the input line containing the sequence and
		expression level (tab separated) to be separated.

	Returns:
	-----
		seq (str) -- the nucleotide sequence.

		exp_level (float) -- the expression level of the sequence.
	"""
	# Assertions
	assert isinstance(line, str), 'Input line must be passed as a string.'
	assert line.count('\t') == 1, 'Input line must contain only 2 types of \
	data, separated by 1 tab.'
	# Functionality
	data = line.rstrip().split('\t')
	seq = data[0]
	try:
		exp_level = float(data[1])
	except ValueError:
		raise ValueError('Second data element must be a the string \
		representation of an integer or float')

	return seq, exp_level

def get_max_min_mode_length_of_seqs(input_seqs):
	"""
	Returns the maximum, minimum, and modal length of the sequences
	in a file containing input sequences.

	Args:
	-----
		input_seqs (str) -- the absolute path of the file containing
		the input sequences and their expression levels, tab separated.

	Returns:
	-----
		max_length (int) -- the length of the longest sequence in the
		input file.
	"""
	seq_lengths = []
	for line in input_seqs:
		seq, exp_level = separate_seq_and_el_data(line)
		seq_lengths.append(len(seq))
	max_length = max(seq_lengths)
	min_length = min(seq_lengths)
	modal_length = max(set(seq_lengths), key=seq_lengths.count)

	return max_length, min_length, modal_length
