"""
A script containing unit test functions for the functions in the
build_promoter.py script.
"""

def test_extract_scaffold_seqs():
	"""
	Tests the function that extracts the scaffold IDs and sequences
	from a input Excel file containing this data.
	"""
	infile = '../../example/scaffolds.xlsx'
	outfile = '../../example/extracted_scaffolds.txt'

	try:
		extract_scaffold_seqs(infile, outfile)
	except Exception as e:
		assert isinstance(e, TypeError)

	out = codecs.open(outfile, 'r', encoding='utf-8', errors='ignore')
	for line in out: # checking each line in output file 

	return
