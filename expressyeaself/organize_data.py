"""
This script contains functions to organize and split up data based
on several experimental parameters.
"""
import os
import matplotlib as plt
import pandas as pd
import xlrd

def split_scaffolds_by_type(infile):
	"""
	Splits the scaffold data found in an excel file up by scaffold
	type, and outputs the scaffold ID and sequence (tab separated) of
	each type to different output files.

	Args:
	-----
		scaff_infile (str) -- the absolute path for the input file
								containing all the scaffold data.
	Returns:
	-----
	"""
	# Assertions
	assert isinstance(infile, str), 'TypeError: input file pathname \
	must be a string.'
	## Check if infile exists

	# Functionality
	scaff_df = pd.read_excel(infile, index_col = 'Scaffold ID')
	types = scaff_df['Scaffold type'].unique()
	for type in types:
		# Create a new output file for each unique type of scaffold
		relative_path = '../example/' + type + '_scaffolds.txt'
		absolute_path = os.path.join(os.getcwd(), relative_path)
		outfile = open(absolute_path, 'w+')
		# Reduce scaffold data to only data of the current type
		type_df = scaff_df[scaff_df['Scaffold type'] == type]
		for index, row in type_df.iterrows():
			outfile.write(index + '\t' + row['Sequence'] + '\r\n')
		outfile.close()

	return

def check_oligonucleotide_flanks(seq_infile):
	"""
	Checks that all the oligonucleotide sequences in an input file
	consist of the same sequences that flank the variable 80-mer
	sequence. i.e. all sequences in the input file should be of the
	form:
		TGCATTTTTTTCACATC-(variable 80-mer seq)-GTTACGGCTGTT
	These flanking sequences are for in-lab sequencing purposes only,
	so can be discarded when the 80-mer variable sequences are
	inserted into the a scaffold sequence.

	Args:
	-----
		seq_infile (str) -- the absolute path of the input file
							containing all of the oligonucleotide
							sequences to be checked, and their
							expression level values (tab separated).
	Returns:
	-----
		result (bool) -- if True, all oligonucleotides contain the
							the appropriate flanks.
	"""
	flank_A = 'TGCATTTTTTTCACATC'
	flank_B = 'GTTACGGCTGTT'
	infile = open(seq_infile, 'r')
	for line in infile:
		data = line.rstrip().split("\t")
		seq = data[0]
		if seq.startswith(flank_A) and seq.endswith(flank_B):
			pass
		else:
			return False
			
	return True
