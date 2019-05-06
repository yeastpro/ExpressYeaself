"""
This script contains functions to generate unique promoter sequences
by joining random oligonucleotide and scaffold sequences together.
For example: ATGCATGC inserted into AAAANNNNNNNNTTTT would give
AAAAATGCATGCTTTT.

"""
import pandas as pd
import xlrd

def extract_scaffold_seqs(infile, outfile):
	"""
	A function that generates a plain text file containing scaffold
	IDs and sequences (tab separated) as extracted from the original
	Excel file that contains them.

	Args:
	-----
	 	infile (str)  -- the pathname for the input Excel file containing the
						 the scaffold data.
		outfile (str) -- the pathname for the output file containing the
						 scaffold IDs and sequences.
	Returns:
	-----
	"""
	# Assertions
	assert isinstance([infile, outfile], str), 'Pathnames for input and output\
	files must be strings'
	assert infile != outfile, 'Output file must have a different pathname as\
	the Input file; otherwise Input data will be overwritten!'
	assert outfile

	# Functionality
	scaff_df = pd.read_csv(infile)
	scaff_out = open(outfile, 'w+')

	return

def insert_seq_into_scaffold(scaff_seq, oligo_seq):
	"""
	Inserts an oligonucleotide sequence into a scaffold sequence
	(ie....ATGCNNNN...ATCG...) in place of its variable region (NNN...)
	of the same length.

	Args:
	-----
		scaff_seq (str) -- the scaffold sequence containing a variable region
							of repeating 'N' characters.
		oligo_seq (str) -- the oligonucleotide sequence to be
							inserted into the scaffold sequence in place
							of the variable region. Must be the same length as
							the variable region in the scaffold.
	Returns:
	-----
		complete_seq (str) -- the complete nucleotide sequence, where the
								variable region of the scaffold has been
								replaced with the input oligonucleotide.
	"""
	# Assertions
	assert isinstance(scaff_seq, str), 'TypeError: Input scaffold sequence\
	must be	a string.'
	assert isinstance(oligo_seq, str), 'TypeError: Input oligonucleotide\
	sequence must be a string.'
	var_start = scaff_seq.find('N') # find index where variable region starts
	var_end = scaff_seq.rfind('N')  # rverse find where variable region ends
	variable_seq = scaff_seq[var_start:var_end+1]
	assert len(oligo_seq) == len(variable_seq), 'Oligonucleotide sequence to be\
	inserted into the scaffold must be equal to length of variable region.'

	# Functionality
	complete_seq = scaff_seq[:var_start] + oligo_seq + scaff_seq[var_end:]

	return complete_seq
