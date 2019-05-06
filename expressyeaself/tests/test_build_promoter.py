"""
A script containing unit tests for the functions in the
build_promoter.py script.
"""
import codecs

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
	count = 0 # keep track of line number in file
	for line in out:
		count += 1
		# Put tab separated ID and seq in a list
		scaff_data = line.rstrip().split("\t")
		for element in scaff_data:
			assert isinstance(element, str), 'Either the ID or sequence on\
				line %s is not a string.'

	return

def test_insert_seq_into_scaffold():
	"""
	Tests the function that inserts an 80 bp oligonucleotide sequence into
	a scaffold sequence to generate a complete promoter sequence.
	"""
	scaff = 'CCTCGACNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN\
				NNNNNNNNNNNNNNNNNNNNNNNNNNNNCCTATG'
	oligo = 'TGCATTTTTTTCACATCTATTGGCTACTAATCAAAGGGACTCGGTGGATTTAATTCTGT\
				TGATTCCGAAGCCTCTTATGTGCTCAAGTTTGGGTAGAGGTTACGGCTGTT'
	try:
		complete = insert_seq_into_scaffold(scaff, oligo)
	except Excpetion as e:
		assert isinstance(e, TypeError)
	assert isinstance(complete, str), 'TypeError: Function not outputting a\
	string.'
	assert len(complete) == len(scaff), ''

	return
