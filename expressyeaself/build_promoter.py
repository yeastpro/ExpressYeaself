"""
This script contains functions to generate unique promoter sequences
by joining random oligonucleotide and scaffold sequences together.
For example: ATGCATGC inserted into AAAANNNNNNNNTTTT would give
AAAAATGCATGCTTTT.

"""
import organize_data as organize
import pandas as pd
from utilities import smart_open as smart_open
from utilities import get_time_stamp as get_time_stamp
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
		None
	"""
	# Assertions
	assert isinstance(infile, str), 'Pathname for input file must be a \
	string.'
	assert isinstance(outfile, str), 'Pathname for output file must be a \
	string.'
	assert infile != outfile, 'Output file must have a different pathname as \
	the Input file; otherwise Input data will be overwritten!'
	# Functionality
	scaff_df = pd.read_csv(infile)
	scaff_out = smart_open(outfile, 'w+')
	scaff_out.close()

	return

def insert_seq_into_scaffold(seq, scaffold):
	"""
	Inserts an oligonucleotide sequence into a scaffold sequence
	(i.e. ATGC...NNNN...ATCG) in place of its variable region
	(NNN...). The input  sequence and variable region of the
	scaffold must be the same length.

	Args:
	-----
		seq (str) -- the oligonucleotide sequence to be
		inserted into the scaffold sequence in place of the
		variable region. Must be the same length as the variable
		region in the scaffold.

		scaffold (str) -- the scaffold sequence containing a
		variable region of repeating 'N' characters.

	Returns:
	-----
		complete_seq (str) -- the complete nucleotide sequence,
		where the variable region of the scaffold has been
		replaced with the input oligonucleotide.
	"""
	# Assertions
	assert isinstance(seq, str), 'TypeError: Input oligonucleotide \
	sequence must be a string.'
	assert isinstance(scaffold, str), 'TypeError: Input scaffold sequence \
	must be	a string.'
	var_start = scaffold.find('N') # find index where variable region starts
	var_end = scaffold.rfind('N')  # reverse find where variable region ends
	variable_seq = scaffold[var_start : var_end + 1]
	assert len(seq) == len(variable_seq), 'Oligonucleotide sequence to \
	be inserted into the scaffold must be equal to length of variable region.'
	# Functionality
	complete_seq = scaffold[:var_start] + seq + scaffold[var_end+1:]

	return complete_seq

def insert_all_seq_into_one_scaffold(input_seqs, scaffold_type='pTpA'):
	"""
	Takes an input file containing N sequences and inserts them into
	a single scaffold sequence, outputting the N unique promoter
	sequences to an output file along with their expression levels
	(tab separated).

	Args:
	-----
		input_seqs (str) -- the absolute path for the input file
		containing all the oligonucleotide sequences to be inserted
		into the single scaffold sequence. All sequences must be of
		the same length as the scaffold variable region.

		scaffold_type (str) -- the scaffold type (pTpA or Abf1TATA)
		that the input sequences had their expression levels
		measured in. Default: 'pTpA'.

	Returns:
	-----
		absolute_path (str) -- the absolute path for the output file
		containing all of the complete promoter sequences (where each
		input sequence has been inserted into the scaffold sequence).
	"""
	# Assertions
	assert isinstance(input_seqs, str), 'TypeError: pathname for input file \
	must be a string.'
	assert isinstance(scaffold, str), 'TypeError: scaffold sequence must be \
	passed as a string.'
	assert isinstance(scaffold_type, str), 'Scaffold type must be passed as \
	a string.'
	assert scaffold_type == 'pTpA' or scaffold_type == 'Abf1TATA', 'Scaffold \
	type must either be passed as "pTpA" or "Abf1TATA".'
	# Functionality
	time_stamp = get_time_stamp() # get time stamp for unique file naming
	relative_path = ('../example/' + scaffold_type + '_data/' + time_stamp +
		'_' + scaffold_type + '_seqs_inserted_into_scaffold.txt')
	absolute_path = os.path.join(os.getcwd(), relative_path)
	# Open input and output files
	input_seqs = smart_open(input_seqs, 'rt')
	outfile = smart_open(absolute_path, 'wt')
	# Retrieve the scaffold sequence
	scaff_directory = '../example/' + scaffold_type + '_data/'
	scaff_rel_path = scaffold_directory + scaffold_type + '_scaffold.txt'
	scaff_abs_path = os.path.join(os.getcwd(), scaff_rel_path)
	scaff_file = smart_open(scaffold_path, 'rt')
	scaffold = scaffold_file.readline().replace('\n', '')
	# Insert sequences into scaffold and write data to output file
	for line in input_seqs:
		seq, exp_level = organize.separate_seq_and_el_data(line)
		complete_seq = insert_seq_into_scaffold(seq, scaffold)
		outfile.write(complete_seq + '\t' + str(exp_level) + '\r\n')
	# Close the input, output, and scaffold files.
	infile.close()
	outfile.close()
	scaff_file.close()

	return absolute_path

def remove_flanks_from_seq(oligo_seq, scaffold_type='pTpA'):
	"""
	Removes the flanking sequences from the oligonucleotide sequences
	and returns the variable 80-mer sequence.
	The input sequences measured in the pTpA scaffold will be of
	the form:
		TGCATTTTTTTCACATC-(variable 80-mer seq)-GTTACGGCTGTT
	Whereas the input sequences measured in the Abf1TATA scaffold
	will be of the form:
		TCACGCAGTATAGTTC-(variable 80-mer sequence)-GGTTTATTGTTTATAAAAA
	where the constant flank regions exist purely for in-lab sequencing
	purposes and aren't needed for insertion into a scaffold sequence.

	Args:
	-----
		oligo_seq (str) -- the input oligonucleotide sequence in
		the form as specified above.

		scaffold_type (str) -- the scaffold type (pTpA or Abf1TATA)
		that the input sequences had their expression levels
		measured in. Default: 'pTpA'.

	Returns:
	-----
		oligo_seq (str) -- the variable 80-mer sequence of the input
		oligonucleotide resulting from removing the constant flanking
		sequences.
	"""
	# Assertions
	assert isinstance(oligo_seq, str), 'Input sequence must be a string'
	assert len(oligo_seq) == 110, 'Input sequence must be of length 110'
	assert isinstance(scaffold_type, str), 'Scaffold type must be passed \
	as a string.'
	assert scaffold_type == 'pTpA' or scaffold_type == 'Abf1TATA', 'Input \
	scaffold type must be either pTpA or Abf1TATA'
	# Functionality
	if scaffold_type == 'pTpA':
		flank_A = 'TGCATTTTTTTCACATC'
		flank_B = 'GGTTACGGCTGTT'
	elif scaffold_type == 'Abf1TATA':
		flank_A = 'TCACGCAGTATAGTTC'
		flank_B = 'GGTTTATTGTTTATAAAAA'

	assert oligo_seq.startswith(flank_A), "Scaffold type specified as %s but \
	input sequence doesn't start with appropriate flank seq" %(scaffold_type)
	assert oligo_seq.endswith(flank_B), "Scaffold type specified as %s but \
	input sequence doesn't end with appropriate flank seq" %(scaffold_type)

	oligo_seq = oligo_seq.replace(flank_A, '')
	oligo_seq = oligo_seq.replace(flank_B, '')

	return oligo_seq

def remove_flanks_from_all_seqs(input_sequences, scaffold_type='pTpA'):
	"""
	Removes all of the flanking sequences from an input file of
	sequences and their expression levels (tab separated).
	Example input file:
	GSE104878_20160609_average_promoter_ELs_per_seq_pTpA_ALL.shuffled.txt.gz
	from https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE104878

	Args:
	-----
		input_sequences (str) -- the absolute pathname of the file
		containing all of the input sequences and their expression
		levels (tab separated).

		scaffold_type (str) -- the scaffold type (pTpA or Abf1TATA)
		that the input sequences had their expression levels
		measured in.

	Returns:
	-----
		out_abs_path (str) -- the absolute path for the output file
		containing all of the sequences with their flanks removed,
		along with their expression levels (tab separated).
	"""
	# Assertions
	assert isinstance(input_sequences, str), 'Input file pathname must be \
	passed as a string.'
	assert os.path.exists(input_sequences), 'Input file does not exist.'
	assert isinstance(scaffold_type, str), 'Scaffold type must be passed \
	as a string.'
	assert scaffold_type == 'pTpA' or scaffold_type == 'Abf1TATA', 'Input \
	scaffold type must be either pTpA or Abf1TATA.'
	assert isinstance(outfile, str), 'Output file pathname must be \
	passed as a string.'
	# Check that all of the flank sequences are the same in all
	# sequences in the input file.
	incorrect = organize.check_oligonucleotide_flanks(infile,scaffold_type)
	assert len(incorrect) == 0, 'Not all sequences in input file have same \
	flanking sequences.'
	# Functionality
	# Defining the pathname for the output file.
	time_stamp = get_time_stamp() # Get unique time stamp for file naming
	relative_path = ('../example/' + scaffold_type + '_data/' + time_stamp +
		'_' + scaffold_type + '_seqs_flanks_removed.txt')
	absolute_path = os.path.join(os.getcwd(), relative_path)
	# Opening the input and output files.
	infile = smart_open(input_sequences, 'rt')
	outfile = smart_open(absolute_path, 'wt')
	# Remove flanks and write data to output file.
	for line in input_sequences:
		seq, exp_level = organize.separate_seq_and_el_data(line)
		deflanked_seq = remove_flanks_from_seq(seq,scaffold_type=scaffold_type)
		outfile.write(deflanked_seq + '\t' + exp_level + '\r\n')
	infile.close()
	outfile.close()

	return absolute_path
