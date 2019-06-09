"""
This script contains functions to generate unique promoter sequences
by joining random oligonucleotide and scaffold sequences together.
For example: ATGCATGC inserted into AAAANNNNNNNNTTTT would give
AAAAATGCATGCTTTT.
"""
import expressyeaself.organize_data as organize
from expressyeaself.utilities import get_time_stamp as get_time_stamp
from expressyeaself.utilities import smart_open as smart_open
import os
# import pandas as pd
# import xlrd


def remove_flanks_from_seq(oligo_seq, scaffold_type='pTpA'):
    """
    Removes the flanking sequences from the oligonucleotide sequences
    and returns the variable region.
    The input sequences measured in the pTpA scaffold will be of
    the form:
        TGCATTTTTTTCACATC-(variable region)-GTTACGGCTGTT
    Whereas the input sequences measured in the Abf1TATA scaffold
    will be of the form:
        TCACGCAGTATAGTTC-(variable region)-GGTTTATTGTTTATAAAAA

    Args:
    -----
        oligo_seq (str) -- the input oligonucleotide sequence in
        the form as specified above.

        scaffold_type (str) -- the scaffold type (pTpA or Abf1TATA)
        that the input sequences had their expression levels
        measured in. Default: 'pTpA'.

    Returns:
    -----
        oligo_seq (str) -- the variable region of the input
        oligonucleotide resulting from removing the constant flanking
        sequences.
    """
    # Assertions
    assert isinstance(oligo_seq, str), 'Input sequence must be a string'
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
    input sequence doesn't start with appropriate flank seq" % (scaffold_type)
    assert oligo_seq.endswith(flank_B), "Scaffold type specified as %s but \
    input sequence doesn't end with appropriate flank seq" % (scaffold_type)
    oligo_seq = oligo_seq.replace(flank_A, '')
    oligo_seq = oligo_seq.replace(flank_B, '')

    return oligo_seq


def remove_flanks_from_all_seqs(input_seqs, scaffold_type='pTpA'):
    """
    Removes all of the flanking sequences from an input file of
    sequences and their expression levels (tab separated).
    Example input file:
    GSE104878_20160609_average_promoter_ELs_per_seq_pTpA_ALL.shuffled.txt.gz
    from https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE104878

    Args:
    -----
        input_seqs (str) -- the absolute pathname of the file
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
    assert isinstance(input_seqs, str), 'Input file pathname must be \
    passed as a string.'
    assert os.path.exists(input_seqs), 'Input file does not exist.'
    assert isinstance(scaffold_type, str), 'Scaffold type must be passed \
    as a string.'
    assert scaffold_type == 'pTpA' or scaffold_type == 'Abf1TATA', 'Input \
    scaffold type must be either pTpA or Abf1TATA.'
    # Check that all of the flank sequences are the same in all
    # sequences in the input file.
    incorrect = organize.check_oligonucleotide_flanks(input_seqs,
                                                      scaffold_type)
    assert len(incorrect) == 0, 'Not all sequences in input file have same \
    flanking sequences.'
    # Functionality
    # Defining the pathname for the output file.
    time_stamp = get_time_stamp()  # Get unique time stamp for file naming
    relative_path = ('example/' + scaffold_type + '_data/' + time_stamp +
                     '_' + scaffold_type + '_seqs_flanks_removed.txt')
    absolute_path = os.path.join(os.getcwd(), relative_path)
    # Opening the input and output files.
    infile = smart_open(input_seqs, 'r')
    outfile = smart_open(absolute_path, 'w')
    # Remove flanks and write data to output file.
    for line in infile:
        line = organize.check_valid_line(line)
        if line == 'skip_line':
            continue
        seq, exp_level = organize.separate_seq_and_el_data(line)
        deflanked_seq = remove_flanks_from_seq(seq, scaffold_type)
        outfile.write(deflanked_seq + '\t' + str(exp_level) + '\n')
    # Close the input and output files.
    infile.close()
    outfile.close()

    return absolute_path


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
    assert isinstance(seq, str), 'TypeError: Input oligonucleotide sequence \
    must be a string.'
    assert isinstance(scaffold, str), 'TypeError: Input scaffold sequence \
    must be a string.'
    # Functionality
    var_start = scaffold.find('N')  # find index where variable region starts
    var_end = scaffold.rfind('N')  # reverse find where variable region ends
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
    assert isinstance(scaffold_type, str), 'Scaffold type must be passed as \
    a string.'
    assert scaffold_type == 'pTpA' or scaffold_type == 'Abf1TATA', 'Scaffold \
    type must either be passed as "pTpA" or "Abf1TATA".'
    # Functionality
    time_stamp = get_time_stamp()  # get time stamp for unique file naming
    relative_path = ('example/' + scaffold_type + '_data/' + time_stamp +
                     '_' + scaffold_type + '_seqs_inserted_into_scaffold.txt')
    absolute_path = os.path.join(os.getcwd(), relative_path)
    # Open input and output files
    infile = smart_open(input_seqs, 'r')
    outfile = smart_open(absolute_path, 'w')
    # Retrieve the scaffold sequence
    scaff_directory = 'example/' + scaffold_type + '_data/'
    scaff_rel_path = scaff_directory + scaffold_type + '_scaffold.txt'
    scaff_abs_path = os.path.join(os.getcwd(), scaff_rel_path)
    scaff_file = smart_open(scaff_abs_path, 'r')
    scaffold = scaff_file.readline().replace('\n', '')
    # Insert sequences into scaffold and write data to output file
    for line in infile:
        line = organize.check_valid_line(line)
        if line == 'skip_line':
            continue
        seq, exp_level = organize.separate_seq_and_el_data(line)
        complete_seq = insert_seq_into_scaffold(seq, scaffold)
        outfile.write(complete_seq + '\t' + str(exp_level) + '\n')
    # Close the input, output, and scaffold files.
    infile.close()
    outfile.close()
    scaff_file.close()

    return absolute_path


def pad_sequences(input_seqs, pad_front=False, extra_padding=0):
    """
    Pads sequences in an input file to the length of the longest
    sequence in the file, plus any extra padding if specified.
    Pads the sequences at either the front or the back, with 'N'
    characters.

    Args:
    -----
         input_seqs (str) -- the absolute path of the input file
        containing the sequences to be padded and their associated
        expression levels, tab separated.

        pad_front (bool) -- If True, will add padding to the front
        of the sequences. If False (default) pads sequences at the
        end (i.e. the RHS of the sequences).

        extra_padding (int) -- The number of extra null bases to
        add onto the front/back of the sequence

    Returns:
    -----
        absolute_path (str) -- the absolute path of the output file
        containing all of the padded sequences and their associated
        expression levels, tab separated.
    """
    # Assertions
    assert isinstance(input_seqs, str), 'Pathname of input file must be \
    passed as a string.'
    assert os.path.exists(input_seqs), 'File does not exist.'
    assert isinstance(pad_front, bool), 'The pad_front variable must be \
    passed as a bool.'
    assert isinstance(extra_padding, int), 'The amount of extra padding must \
    be passed as an integer.'
    assert extra_padding >= 0, 'The amount of extra padding must be passed as \
    a non-negative integer.'
    # Functionality
    # Define and open the output file
    absolute_path = input_seqs.replace('.txt', '_padded.txt')
    outfile = smart_open(absolute_path, 'w')
    # Retrieve input sequences, pad them, and write them to output file
    max_length, _, _ = organize.get_max_min_mode_length_of_seqs(input_seqs)
    pad_length = max_length + extra_padding
    with smart_open(input_seqs) as f:
        for line in f:
            line = organize.check_valid_line(line)
            if line == 'skip_line':
                continue
            seq, exp_level = organize.separate_seq_and_el_data(line)
            difference = pad_length - len(seq)
            if difference == 0:
                padded_seq = seq
            elif difference > 0:
                padding_seq = 'P' * difference
                if pad_front:
                    padded_seq = padding_seq + seq
                else:  # pad the end of the sequence
                    padded_seq = seq + padding_seq
            else:
                raise Exception('Sequence length longer than padding length.')
            outfile.write(padded_seq + '\t' + str(exp_level) + '\n')
    # Close the output file
    outfile.close()

    return absolute_path


# def extract_scaffold_seqs(infile, outfile):
#     """
#     A function that generates a plain text file containing scaffold
#     IDs and sequences (tab separated) as extracted from the original
#     Excel file that contains them.
#
#     Args:
#     -----
#          infile (str)  -- the absolute path for the input Excel file
#         containing the scaffold data.
#
#         outfile (str) -- the absolute path for the output file
#         containing scaffold IDs and sequences.
#
#     Returns:
#     -----
#         None
#     """
#     # Assertions
#     assert isinstance(infile, str), 'Pathname for input file must be a \
#     string.'
#     assert isinstance(outfile, str), 'Pathname for output file must be a \
#     string.'
#     assert infile != outfile, 'Output file must have a different pathname\
#     as the Input file; otherwise Input data will be overwritten!'
#     # Functionality
#     scaff_df = pd.read_csv(infile)
#     scaff_out = smart_open(outfile, 'w+')
#     scaff_out.close()
#
#     return
