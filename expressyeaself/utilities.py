"""
This script contains utility functions that are useful in areas
of the project.
"""
import datetime as dt
import gzip
import os
import subprocess

def smart_open(filename, mode='r'):
	"""
	A function to open a file. If the file is compressed
	(with a '.gz' extension) it is decompressed before being
	opened. Otherwise, the function is opened normally.

	Args:
	-----
		filename (str) -- the absolute pathname of the file
		to be opened.

		mode (str) -- the way in which the file should be
		opened by the gzip.open command. Options: 'r', 'rb',
		'a', 'ab', 'w', 'wb', 'x' or 'xb' for binary files,
		and 'rt', 'at', 'wt', or 'xt' for text files.
		Default: 'rt'.

	Returns:
	-----
		opened_file (file type) -- the opened file.

	** Adapted from Carl de Boer's function in https://github.com/Carldeboer/CisRegModels/blob/master/CisRegModels/MYUTILS.py **
	"""
	# Assertions
	assert isinstance(filename, str), 'Input file pathname must be a string.'
	assert isinstance(mode, str), 'Opening mode must be passed as a string.'
	if mode.startswith('r'):
		assert os.path.exists(filename), 'Input file does not exist.'
	# Functionality
	if len(filename) > 3 and filename.endswith('.gz'):
		file = gzip.open(filename, mode)
	else:
		file = open(filename,mode);

	return file

def get_time_stamp():
	"""
	Creates a unique time stamp number containing no other character
	than digits 0~9.
	For instance:
		'2019-05-17 17:04:19.923192' ---> '20190517170419923192'
	Args:
	-----
		-
	Returns:
	-----
		time_stamp (str) -- a unique numerical string of the
		current time.
	"""
	time_stamp = str(dt.datetime.now())
	time_stamp = time_stamp.replace(' ', '').replace('-', '')
	time_stamp = time_stamp.replace('.', '').replace(':', '')

	return time_stamp

def get_line_count(infile):
	"""
	Counts and returns the number of lines in a file.

	Args:
	-----
		infile (str) -- the absolute path for the input file.

	Returns:
	-----
		line_count (int) -- the number of lines in the input file.
	"""
	# Assertions
	assert os.path.exists(infile), 'Input file does not exist.'
	assert isinstance(infile, str), 'Path name for input file must be passed \
	as a string.'
	# Functionality
	file = smart_open(infile, 'r')
	count = 0
	for line in file:
		count += 1
	file.close()

	return count
