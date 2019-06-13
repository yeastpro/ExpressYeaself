"""
A script containing unit tests for the functions in the
build_promoter.py script.
"""
import expressyeaself.tests.context as context
import os

test = context.build_promoter
organize = context.organize_data
utilities = context.utilities


def test_remove_flanks_from_seq():
    """
    Tests the function that removes the constant flanking sequences
    from all sequences in an input file.
    """
    # Test case 1: invalid flanks
    flank_A = 'NNNN'
    flank_B = 'NNN'
    trial_seq = flank_A + 'ATGC' + flank_B
    scaff = 'pTpA'
    try:
        test.remove_flanks_from_seq(trial_seq, scaff)
    except AssertionError:
        pass
    # Test case 2: valid seq with valid flanks
    flank_A = 'TCACGCAGTATAGTTC'
    flank_B = 'GGTTTATTGTTTATAAAAA'
    trial_seq = flank_A + 'ATGC' + flank_B
    scaff = 'Abf1TATA'
    out_seq = test.remove_flanks_from_seq(trial_seq, scaff)
    assert out_seq == 'ATGC'
    # Test case 3: empty sequence, with valid flanks
    trial_seq = flank_A + flank_B
    assert test.remove_flanks_from_seq(trial_seq, scaff) == ''

    return


def test_remove_flanks_from_all_seqs():
    """
    Tests the function that removes the flanking regions from the
    oligonucleotide sequence in either the Abf1TATA or pTpA libraries.
    """
    # Test case 1: valid files
    for scaff in ('pTpA', 'Abf1TATA'):
        if scaff == 'pTpA':
            flank_A = 'TGCATTTTTTTCACATC'
            flank_B = 'GGTTACGGCTGTT'
        elif scaff == 'Abf1TATA':
            flank_A = 'TCACGCAGTATAGTTC'
            flank_B = 'GGTTTATTGTTTATAAAAA'
        trial_path = 'trial_file.txt'
        with open(trial_path, 'w+') as f:
            f.write(flank_A + 'AAAA' + flank_B + '\t3.9\n')
            f.write(flank_A + 'TTTT' + flank_B + '\t45\n')
        out_path = test.remove_flanks_from_all_seqs(trial_path, scaff)
        with open(out_path, 'r') as f:
            for i in range(0, 2):
                line = f.readline()
                seq, el = utilities.separate_seq_and_el_data(line)
                if i == 0:
                    assert seq == 'AAAA'
                elif i == 1:
                    assert seq == 'TTTT'
        os.remove(trial_path)
        os.remove(out_path)
    # Test case 2: invalid flank sequences
    scaff = 'Abf1TATA'
    flank_A = 'NNNN'
    flank_B = 'NNNNNNN'
    trial_path = 'trial_file.txt'
    with open(trial_path, 'w+') as f:
        f.write(flank_A + 'AAAA' + flank_B + '\t3.9\n')
        f.write(flank_A + 'TTTT' + flank_B + '\t45\n')
    try:
        out_path = test.remove_flanks_from_all_seqs(trial_path, scaff)
    except AssertionError:
        pass
    # Test case 3: valid flank sequences, but invalid line format
    scaff = 'pTpA'
    flank_A = 'TGCATTTTTTTCACATC'
    flank_B = 'GGTTACGGCTGTT'
    trial_path = 'trial_file.txt'
    with open(trial_path, 'w+') as f:
        f.write(flank_A + 'AAAA' + flank_B + '\t3.9\n')
        f.write(flank_A + 'TTTT' + flank_B + '\t45\n')
        f.write(flank_A + 'GGGG' + flank_B + '\n')
    out_path = test.remove_flanks_from_all_seqs(trial_path, scaff)
    assert utilities.get_seq_count(trial_path) == 2
    with open(out_path, 'r') as f:
        assert f.readline() == 'AAAA\t3.9\n'
        assert f.readline() == 'TTTT\t45.0\n'
    os.remove(trial_path)
    os.remove(out_path)

    return


def test_insert_seq_into_scaffold():
    """
    Tests the function that inserts an 80 bp oligonucleotide sequence into
    a scaffold sequence to generate a complete promoter sequence.
    """
    # Test case 1: empty scaffold
    scaff = 'NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN'
    oligo = ('TGCATTTTTTTCACATCTATTGGCTACTAATCAAAGGGACTCGGTGGATTTAATTCTGT\
                TGATTCCGAAGCCTCTTATGTGCTCAAGTTTGGGTAGAGGTTACGGCTGTT')
    complete = test.insert_seq_into_scaffold(oligo, scaff)
    assert isinstance(complete, str)
    assert len(complete) == len(oligo)
    # Test case 2: empty sequence
    scaff = 'AAAANNNNTTTT'
    oligo = ''
    complete = test.insert_seq_into_scaffold(oligo, scaff)
    assert complete == 'AAAATTTT'

    return


def test_insert_all_seq_into_one_scaffold():
    """
    Tests the function that inserts mutliple olignonucleotide
    sequences from an input file into a single scaffold sequence
    and generates an output file containing all of the new unique
    promoter sequences.
    """
    # Test case 1: valid input
    scaff = 'pTpA'
    trial_path = 'trial_file.txt'
    scaff_pre = 'GCTAGCAGGAATGATGCAAAAGGTTCCCGATTCGAACTGCATTTTTTTCACATC'
    scaff_post = ('GGTTACGGCTGTTTCTTAATTAAAAAAAGATAGAAAACATTAGGAGTGTAACACAAG'
                  'ACTTTCGGATCCTGAGCAGGCAAGATAAACGA')
    with open(trial_path, 'w') as f:
        f.write('GGGG\t1.0\n')
        f.write('CCCC\t2.0\n')
        f.write('AAAA\t3.0\n')
    out_path = test.insert_all_seq_into_one_scaffold(trial_path, scaff)
    with open(out_path, 'r') as f:
        oligos = ['GGGG', 'CCCC', 'AAAA']
        for oligo in oligos:
            line = f.readline()
            seq, _ = utilities.separate_seq_and_el_data(line)
            assert seq == scaff_pre + oligo + scaff_post
    os.remove(trial_path)
    os.remove(out_path)
    # Test case 2: input file has invalid line
    with open(trial_path, 'w') as f:
        f.write('GGGG\t1.0\n')
        f.write('CCCC\t2.0\n')
        f.write('AAAA\n')  # invalid line
    out_path = test.insert_all_seq_into_one_scaffold(trial_path, scaff)
    with open(out_path, 'r') as f:
        assert utilities.get_seq_count(out_path) == 2
        oligos = ['GGGG', 'CCCC']
        for oligo in oligos:
            line = f.readline()
            seq, _ = utilities.separate_seq_and_el_data(line)
            assert seq == scaff_pre + oligo + scaff_post
    os.remove(trial_path)
    os.remove(out_path)

    return


def test_pad_sequences():
    """
    Tests the function that pads the sequences in an input file to
    the length of the longest sequence (plus some extra padding if
    specified).
    """
    # Test case 1; homogeneous sequences, no extra padding
    trial_path = 'trial_file.txt'
    oligos = ['AAAA', 'TTTT', 'GGGG', 'CCCC']
    with open(trial_path, 'w') as f:
        for oligo in oligos:
            f.write(oligo + '\t6.7\n')
    out_path = test.pad_sequences(trial_path)
    with open(trial_path, 'r') as f:
        with open(out_path, 'r') as g:
            assert f.read() == g.read()  # contents shouldn't change
    os.remove(out_path)
    # Test case 2: homogeneous seqs with extra padding, padding at back
    extra = 2
    out_path = test.pad_sequences(trial_path, extra_padding=extra)
    with open(out_path, 'r') as f:
        for oligo in oligos:
            line = f.readline()
            seq, _ = utilities.separate_seq_and_el_data(line)
            assert seq == oligo + ('P' * extra)
    os.remove(out_path)
    # Test case 3: inhomogeneous sequences, with one invalid line
    with open(trial_path, 'w') as f:
        for i in range(0, len(oligos)):
            f.write(oligo * (i + 1) + '\t8.5\n')
        f.write('This is an invalid line.')
    #   a) pad the back
    out_path = test.pad_sequences(trial_path)
    max_l, min_l, mode = organize.get_max_min_mode_length_of_seqs(out_path)
    assert max_l == min_l
    #   b) pad the front
    out_path = test.pad_sequences(trial_path, pad_front=True)
    max_l, min_l, mode = organize.get_max_min_mode_length_of_seqs(out_path)
    assert max_l == min_l
    os.remove(trial_path)
    os.remove(out_path)

    return


# def test_extract_scaffold_seqs():
#     """
#     Tests the function that extracts the scaffold IDs and sequences
#     from a input Excel file containing this data.
#     """
#     infile = '../../example/scaffolds.xlsx'
#     outfile = '../../example/extracted_scaffolds.txt'
#     try:
#         test.extract_scaffold_seqs(infile, outfile)
#     except Exception as e:
#         assert isinstance(e, TypeError)
#
#     out = codecs.open(outfile, 'r', encoding='utf-8', errors='ignore')
#     count = 0 # keep track of line number in file
#     for line in out:
#         count += 1
#         # Put tab separated ID and seq in a list
#         scaff_data = line.rstrip().split("\t")
#         for element in scaff_data:
#             assert isinstance(element, str), 'Either the ID or sequence on \
#             line %s is not a string.'
#
#     return
