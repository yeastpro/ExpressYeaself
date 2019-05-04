"""
This script contains functions to generate unique promoter sequences
by joining random oligonucleotide and scaffold sequences together.
For example: ATGCATGC inserted into AAAANNNNNNNNTTTT would give
AAAAATGCATGCTTTT
"""
import pandas as pd

def extract_scaffold_seqs(infile, outfile):
	"""
	A function that generates a plain text file containing scaffold
	IDs and sequences (tab separated) as extracted from the original
	Excel file that contains them.

	Args:
	-----
	 	infile (str)  -- the pathname for the input file containing the
						 the scaffold data.
		outfile (str) -- the pathname for the output file containing the
						 scaffold IDs and sequences.
	Returns:
	-----
	"""
	# Assertions
	assert isinstance([infile, outfile], str), 'Pathnames for input and \
		output files must be strings'
	assert infile != outfile, 'Output file must have a different path-\
		name as the Input file; otherwise Input data will be overwritten!'
	# Functionality

	return
