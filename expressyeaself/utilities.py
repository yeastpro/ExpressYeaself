"""
This script contains utility functions that are useful in areas
of the project.
"""
import datetime as dt
import gzip

def smart_open(filename, mode='rt'):
	"""
	A function to open a file. If the file is compressed
	(with a '.gz' extension) it is decompressed before being
	opened. Otherwise, the function is opened normally.

	Args:
	-----
		filename (str) -- the absolute pathname of the input
		file to be opened.

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
	assert os.path.exists(filename), 'Input file does not exist.'
	# Functionality
	if len(filename) > 3 and filename[-3:].lower() == '.gz':
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
