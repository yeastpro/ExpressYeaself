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
import time as t
from utilities import get_time_stamp as get_time_stamp
from utilities import get_line_count as get_line_count
from utilities import smart_open as smart_open

def process_raw_data(input_seqs, scaffold_type='pTpA', homogeneous=True,
						deflank=True, insert_into_scaffold=True,
						encoding_method='One-Hot', pad_sequences=True,
						extra_padding=0, pad_front=False,
						report_loss=False, report_times=False,
						remove_files=False):
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
		measured in. Default: 'pTpA'.

		homogeneous (bool) -- if True, only sequences of modal
		length will be used in the data set. If False, all sequences
		will be encoded regardless of length. Default: True.

		deflank (bool) -- if True, removes the constant flanking
		regions of the input sequences. Default: True.

		insert_into_scaffold (bool) -- if True inserts the input
		sequences into the appropriate scaffold. If False, the
		sequences are encoded as they are. Default: True.

		encoding_method (str) -- the method by which the sequences
		should be encoded. Default: 'One-Hot'.

		pad_sequences (bool) -- if True pads all of the encoded
		sequences so that they are the same length. Default: True.

		extra_padding (int) -- the number of vectors greater than the
		maximum sequence length to pad each encoded sequence to.
		Default: 0.

		pad_front (bool) -- whether to pad out the front (left hand side)
		or end (right hand side) of the encoded sequences. If True, pads
		the front. Default: False (will pad the end).

		report_loss (bool) -- if True, reports the number of lines of
		data lost at each step in the process. Default: False.

		report_times (bool) -- if True, reports the time each step in the
		cleaning process takes. Default: False.

		remove_files (bool) -- if True, will remove the intermediate
		files created in the process of converting raw data into encoded
		data. Default: False (i.e. intermediary files will be kept).

	Returns:
	-----
		encoded_data (str) -- the absolute path for the file containing
		encoded sequences along with their expression levels.
	"""
	# Assertions
	assert isinstance(input_seqs, str), 'Input file path name must be \
	passed as a string.'
	assert os.path.exists(input_seqs), 'Input file does not exist.'
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
	assert encoding_method in METHODS, 'Not a valid method of encoding, must \
	be of the following : %s' %(METHODS)
	assert isinstance(pad_sequences, bool), 'The pad_front argument must be \
	passed as a bool.'
	assert isinstance(extra_padding, int), 'The number of extra vectors to pad \
	each sequence by should be passed as an integer.'
	assert extra_padding >= 0, 'extra_padding must be passed as a non-negative \
	integer.'
	assert isinstance(pad_front, bool), 'The pad_front argument must be passed \
	as a bool.'
	assert isinstance(report_loss, bool), 'The report_loss argument must be \
	passed as a bool.'
	assert isinstance(report_times, bool), 'The report_times argument must be \
	passed as a bool.'
	assert isinstance(remove_files, bool), 'The remove_files argument must be \
	passed as a bool.'
	# Functionality
	encoded_data = ''
	if report_loss:
		categories = (['Raw Data', 'Homogeneous Seqs',
					   'Deflanked Seqs', 'Scaffold-Inserted Seqs',
					   'Scaffold-Inserted Seqs'])
		loss_report = {}
		loss_report['Raw Data'] = get_line_count(input_seqs)
	if report_times:
		t_init = t.time()
		t0 = t_init
	if remove_files:
		created_files = [] # to keep track of the intermediate files created.
	# Create new file of only homogeneous (same length) seqs
	if homogeneous:
		print('Pulling homogeneous sequences from input file...')
		pad_sequences = False # if all seqs same length they don't need padding
		input_seqs = organize.pull_homogeneous_seqs(input_seqs,
									scaffold_type=scaffold_type)
		encoded_data += '_homogeneous'
		if report_loss:
			loss_report['Homogeneous Seqs'] = get_line_count(input_seqs)
		if report_times:
			t1 = t.time()
			print('\tFile created in %s s' %(t1 - t0))
			t0 = t1
		if remove_files:
			created_files.append(input_seqs)
	# Remove all of the flanking regions from the input sequences
	if deflank:
		print('Removing flank regions from sequences...')
		input_seqs = build.remove_flanks_from_all_seqs(input_seqs,
									scaffold_type=scaffold_type)
		encoded_data += '_deflanked'
		if report_loss:
			loss_report['Deflanked Seqs'] = get_line_count(input_seqs)
		if report_times:
			t1 = t.time()
			print('\tFile created in %s s' %(t1 - t0))
			t0 = t1
		if remove_files:
			created_files.append(input_seqs)
	# Insert sequences into appropriate scaffold
	if insert_into_scaffold:
		print('Inserting sequences into %s scaffold...' %(scaffold_type))
		input_seqs = build.insert_all_seq_into_one_scaffold(input_seqs,
									scaffold_type=scaffold_type)
		encoded_data += '_inserted_into_scaffold'
		if report_loss:
			loss_report['Scaffold-Inserted Seqs'] = get_line_count(input_seqs)
		if report_times:
			t1 = t.time()
			print('\tFile created in %s s' %(t1 - t0))
			t0 = t1
		if remove_files:
			created_files.append(input_seqs)
	# Pad sequences

	# Encoded and pad sequences
	print('Encoding sequences using the %s method...' %(encoding_method))
	input_seqs = encode.encode_sequences_with_method(input_seqs,
							method=encoding_method, pad_sequences=pad_sequences,
							extra_padding=extra_padding, pad_front=pad_front)
	encoded_data += '_' + encoding_method
	# Rename the final output file to reflect how data has been cleaned.
	encoded_data = input_seqs.replace('.txt', encoded_data + '.txt')
	os.rename(input_seqs, encoded_data)
	if report_loss:
		loss_report['Encoded Seqs'] = get_line_count(input_seqs)
	if report_times:
		t1 = t.time()
		print('\tFile created in %s s' %(t1 - t0))
	# Report loss
	if report_loss:
		print('Line counts at each step of the process:')
		for category in categories:
			curr_count = loss_report[category]
			if category == 'Raw Data':
				print('\t%s : %s' %(category, curr_count))
				prev_count = curr_count
			else:
				print('\t%s : %s , where %s lines have been lost since the \
				last step.' %(category, curr_count, (curr_count - prev_count)))
				prev_count = curr_count
	if report_times:
		t_final = t.time()
		print('Total time : %s' %(t_final - t_init))
	# Remove intermediate files
	if remove_files:
		print('Removing unnecessary intermediate files...')
		organize.remove_files(created_files)
		print('Files successfully removed.')
	# Report end of process and print absolute path of encoded data.
	print('Process complete. Raw data successfully converted into encoded \
	data, which can be found at %s' %(encoded_data))

	return encoded_data
