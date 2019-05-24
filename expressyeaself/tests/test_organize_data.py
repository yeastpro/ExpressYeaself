"""
This script contains the unit tests for the functions found in
the organize_data.py script.
"""
import expressyeaself.tests.context as context

test = context.organize_data()

def test_separate_seq_and_e_data():
    """
    Test the function that takes a line of an input file and
    sepaarates and returns the nucleotide sequence as a string
    and its associated expression level as a float.
    """

    return

def test_check_valid_line():
    """
    Tests the function that checks the validity of a line from an
    input file, containing a nucleotide sequence tab separated from
    its associated expression level.
    """

    return

def test_get_max_min_mode_length_of_seqs():
    """
    Tests the function that returns the maximum, minimum, and modal
    length of the sequences in an input file.
    """

    return

def test_pull_homogenous_seqs():
    """
    Tests the function that pulls all sequences of modal length
    from an input file of sequences and returns
    """

    return

def test_check_oligonucleotide_flanks():
    """
    Tests the function that checks the flanking sequences of all of
    the sequences in an input file and returns a list of lines with
    incorrect flanks.
    """

    return

def test_remove_files():
    """
    Tests the function that takes as input a list containing the
    strings of the absolute paths of one or more files, and removes
    them.
    """

    return

def test_split_scaffolds_by_type():
    """
    Tests the function that splits an input excel file of scaffold
    data by their type, outputting the different types to different
    output files.
    """

    return
