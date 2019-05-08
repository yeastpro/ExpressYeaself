"""
This script contains functions to organize and split up data based
on several experimental parameters.
"""
import os
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
