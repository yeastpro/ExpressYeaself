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
	 	infile (str)  -- the absolute path for the input Excel file
							containing the scaffold data.
		outfile (str) -- the absolute path for the output file
							containing scaffold IDs and sequences.
	Returns:
	-----
	"""
	# Assertions
	assert isinstance([infile, outfile], str), 'Pathnames for input and output \
	files must be strings'
	assert infile != outfile, 'Output file must have a different pathname as \
	the Input file; otherwise Input data will be overwritten!'
	# assert outfile

	# Functionality
	scaff_df = pd.read_csv(infile)
	scaff_out = open(outfile, 'w+')

	return

def insert_seq_into_scaffold(scaff_seq, oligo_seq):
	"""
	Inserts an oligonucleotide sequence into a scaffold sequence
	(ie....ATGCNNNN...ATCG...) in place of its variable region
	(NNN...) of the same length.

	Args:
	-----
		scaff_seq (str) -- the scaffold sequence containing a variable
							region of repeating 'N' characters.
		oligo_seq (str) -- the oligonucleotide sequence to be
							inserted into the scaffold sequence in place
							of the variable region. Must be the same length
							as the variable region in the scaffold.
	Returns:
	-----
		complete_seq (str) -- the complete nucleotide sequence, where the
								variable region of the scaffold has been
								replaced with the input oligonucleotide.
	"""
	# Assertions
	assert isinstance(scaff_seq, str), 'TypeError: Input scaffold sequence \
	must be	a string.'
	assert isinstance(oligo_seq, str), 'TypeError: Input oligonucleotide \
	sequence must be a string.'
	var_start = scaff_seq.find('N') # find index where variable region starts
	var_end = scaff_seq.rfind('N')  # rverse find where variable region ends
	variable_seq = scaff_seq[var_start:var_end+1]
	assert len(oligo_seq) == len(variable_seq), 'Oligonucleotide sequence to be\
	 inserted into the scaffold must be equal to length of variable region.'

	# Functionality
	complete_seq = scaff_seq[:var_start] + oligo_seq + scaff_seq[var_end+1:]

	return complete_seq

def insert_all_seq_into_one_scaffold(scaff_seq, oligo_infile):
	"""
	Takes an input file containing N sequences and inserts them into
	a single scaffold sequence, outputting the N unique promoter
	sequences to an output file along with their expression levels
	(tab separated).

	Args:
	-----
		scaff_seq (str)    -- the scaffold sequence containing a variable
								region of repeating 'N' characters that
								will be replaced by the oligonucleotide
								sequence.
		oligo_infile (str) -- the absolute path for the input file
								containing all the oligonucleotide
								sequences to be inserted into the single
								scaffold sequence. All sequences must be
								of the same length as the scaffold variable
								region.

	"""
	# Assertions
	assert isinstance(scaff_seq, str), 'TypeError: scaffold sequence must be \
	passed as a string.'
	assert isinstance(oligo_infile, str), 'TypeError: pathname for input file \
	must be a string.'

	# Functionality
	infile = open(oligo_infile, 'r')


	return

def remove_flanks_from_oligo(oligo_seq):
	"""
	Removes the flanking sequences from the oligonucleotide sequences
	and returns the variable 80-mer sequence.
	The input sequence will be of the form:
		TGCATTTTTTTCACATC-(variable 80-mer seq)-GTTACGGCTGTT
	where the constant flank regions exist purely for in-lab sequencing
	purposes and aren't needed for insertion into a scaffold sequence.

	Args:
	-----
		oligo_seq (str) -- the input oligonucleotide sequence in the
							form as specified above.
	Returns:
	-----
		80mer_seq (str) -- the variable 80-mer sequence of the input
							oligonucleotide resulting from removing
							the constant flanking sequences.
	"""
	assert isinstance(oligo_seq, str), 'Input sequence must be a string'
	assert len(oligo_seq) == 110, 'Input sequence must be of length 110'
	assert oligo_seq.startswith()
