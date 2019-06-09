"""
This script contains functions to organize and split up data based
on several experimental parameters.
"""
from expressyeaself.utilities import check_valid_line as check_valid_line
from expressyeaself.utilities import get_seq_count as get_seq_count
from expressyeaself.utilities import get_time_stamp as get_time_stamp
from expressyeaself.utilities import smart_open as smart_open
import os


def separate_seq_and_el_data(line):
    """
    Takes a string containing a nucleotide sequence and its expression
    level (el) - tab separated - and returns the sequence as a string
    and the expression level as a float.

    Args:
    -----
        line (str) -- the input line containing the sequence and
        expression level (tab separated) to be separated.

    Returns:
    -----
        seq (str) -- the nucleotide sequence.

        exp_level (float) -- the expression level of the sequence.
    """
    # Assertions
    assert isinstance(line, str), 'Input line must be passed as a string.'
    # Functionality
    data = line.rstrip().split('\t')
    seq = data[0]
    exp_level = float(data[1])

    return seq, exp_level


def get_max_min_mode_length_of_seqs(input_seqs):
    """
    Returns the maximum, minimum, and modal length of the sequences
    in a file containing input sequences.

    Args:
    -----
        input_seqs (str) -- the absolute path of the file
        containing the input sequences and their expression levels,
        tab separated.

    Returns:
    -----
        max_length (int) -- the length of the longest sequence in
        the input file.

        min_length (int) -- the length of the shortest sequence in
        the input file.

        modal_length (int) -- the most common sequence length of
        the sequences in the input file.
    """
    # Assertions
    assert isinstance(input_seqs, str), 'Path name for input file must be \
    passed as a string.'
    assert os.path.exists(input_seqs), 'Input file does not exist.'
    # Functionality
    infile = smart_open(input_seqs, 'r')
    seq_lengths = []
    for line in infile:
        line = check_valid_line(line)
        if line == 'skip_line':
            continue
        seq, exp_level = separate_seq_and_el_data(line)
        seq_lengths.append(len(seq))
    max_length = max(seq_lengths)
    min_length = min(seq_lengths)
    modal_length = max(set(seq_lengths), key=seq_lengths.count)
    # Close the input file.
    infile.close()

    return max_length, min_length, modal_length


def pull_homogeneous_seqs(input_seqs, scaffold_type=None):
    """
    Pulls all sequences of the modal length (i.e. 110 bp for pTpA-type
    sequences and 115 bp for Abf1TATA-type) from an input file and
    writes them into an output file.

    Args:
    -----
        input_seqs (str) -- the absolute pathname of the input file
        containing all of the raw oligonucleotide sequences and
        their expression levels, tab separated.

        scaffold_type (str) -- the scaffold type (pTpA or Abf1TATA
        for which the modal length is known to be 110 and 115
        respectively) in which the expression levels for the
        sequences in the input file were measured. If None, the
        modal length is calculated manually. Default: None.

    Returns:
    -----
        absolute_path (str) -- the absolute pathname of the output
        file containing the sequences of modal length.
    """
    # Assertions
    assert isinstance(input_seqs, str), 'Input file pathname must be a string.'
    assert os.path.isfile(input_seqs), 'Input file does not exist!'
    assert isinstance(scaffold_type, str), 'Scaffold type must be passed as a \
    string.'
    assert scaffold_type == 'pTpA' or scaffold_type == 'Abf1TATA', 'Scaffold \
    type must be specified as either pTpA or Abf1TATA, or else unspecified \
    (takes value of None).'
    # Functionality
    # Defining the path name of the output file.
    relative_path = 'example/'
    time_stamp = get_time_stamp()
    if scaffold_type is None:
        relative_path += ('other_scaffolds/' + time_stamp +
                          '_homogeneous_seqs.txt')
    else:
        relative_path += (scaffold_type + '_data/' + time_stamp + '_' +
                          scaffold_type + '_homogeneous_seqs.txt')
        absolute_path = os.path.join(os.getcwd(), relative_path)
    # Open the input and output files.
    infile = smart_open(input_seqs, 'r')
    output_seqs = smart_open(absolute_path, 'w')
    # Retrieve modal length for sequences in input file.
    if scaffold_type == 'pTpA':
        modal_length = 110
    elif scaffold_type == 'Abf1TATA':
        modal_length = 115
    else:
        _, _, modal_length = get_max_min_mode_length_of_seqs(input_seqs)
    # Find seqs in input file w/ modal length and write them to output file
    # count = 0 ###################
    for line in infile:
        # count += 1 #####################
        line = check_valid_line(line)
        if line == 'skip_line':
            continue
        seq, exp_level = separate_seq_and_el_data(line)
        if len(seq) == modal_length:
            output_seqs.write(seq + '\t' + str(exp_level) + '\n')
        else:
            continue
    # Close the input and output files.
    infile.close()
    output_seqs.close()

    return absolute_path


def check_oligonucleotide_flanks(seq_infile, scaffold_type):
    """
    Checks that all the oligonucleotide sequences in an input file
    consist of the same sequences that flank the variable 80-mer
    sequence. i.e. all sequences in the input file should be of the
    form:
    TGCATTTTTTTCACATC-(variable region)-GTTACGGCTGTT
    Whereas the input sequences measured in the Abf1TATA scaffold
    will be of the form:
    TCACGCAGTATAGTTC-(variable region)-GGTTTATTGTTTATAAAAA
    These flanking sequences are for in-lab sequencing purposes only,
    so can be discarded when the 80-mer variable sequences are
    inserted into the a scaffold sequence.

    Args:
    -----
        seq_infile (str) -- the absolute path of the input file
        containing all of the oligonucleotide sequences to be
        checked, and their expression level values (tab separated).

        scaffold_type (str) -- the scaffold type (pTpA or Abf1TATA)
        in which the expression levels for the sequences in the
        input file were measured.

    Returns:
    -----
        incorrect_lines (list) -- returns a list of line numbers for
        for sequences that contain incorrect flank sequences.
    """
    # Assertions
    assert isinstance(seq_infile, str), 'Absolute pathname must be passed \
    as a string.'
    assert isinstance(scaffold_type, str), 'Scaffold type must be passed as a \
    string.'
    assert scaffold_type == 'pTpA' or scaffold_type == 'Abf1TATA', 'Scaffold \
    type must be specified as either pTpA or Abf1TATA.'
    # Functionality
    if scaffold_type == 'pTpA':
        flank_A = 'TGCATTTTTTTCACATC'
        flank_B = 'GGTTACGGCTGTT'
    elif scaffold_type == 'Abf1TATA':
        flank_A = 'TCACGCAGTATAGTTC'
        flank_B = 'GGTTTATTGTTTATAAAAA'
    infile = smart_open(seq_infile, 'r')
    line_number = 0
    incorrect_lines = []
    for line in infile:
        line_number += 1
        line = check_valid_line(line)
        if line == 'skip_line':
            continue
        seq, exp_level = separate_seq_and_el_data(line)
        if seq.startswith(flank_A) and seq.endswith(flank_B):
            pass
        else:
            incorrect_lines.append(line_number)

    return incorrect_lines


def remove_file_list(files):
    """
    Takes a list of path names for files and deletes each of the
    files from the local system.

    Args:
    -----
        files (list) -- the absolute paths, as strings, of the
        files to be deleted.

    Returns:
    -----
        None
    """
    # Assertions
    for file in files:
        assert isinstance(file, str), 'File path names must be passed as \
        strings.'
    # Functionality
    for file in files:
        if os.path.exists(file):
            os.remove(file)
        else:
            pass

    return


def write_num_and_len_of_seqs_to_file(input_seqs):
    """
    Prepends the number of sequences and the length of the
    sequences in an input file to the first 2 lines of the
    file. Assumes sequences have been processed so that all
    sequences have been padded to the same length. The first
    2 lines of the input file will be in the following format
    after writing the info to the file:
    "
    number_of_seqs_in_file\t<###>
    length_of_each_sequence\t<$$$>
    "
    where '<###>' is the number of sequences in the file, and
    '<$$$>'is the length to which every sequence in the file is
    padded.

    Args:
    -----
        input_seqs (str) -- the absolute path of the processed
        input sequences to extract information from.

    Returns:
    -----
        None
    """
    # Assertions
    assert isinstance(input_seqs, str), 'Absolute pathname must be passed\
    as a string.'
    assert os.path.exists(input_seqs), 'Input file does not exist.'
    # Functionality
    num_seqs = get_seq_count(input_seqs)
    with smart_open(input_seqs, 'r') as f:
        line = f.readline()
        try:
            line = check_valid_line(line)
        except line == 'skip_line':
            raise AssertionError('First line is not valid.')
        seq, _ = separate_seq_and_el_data(line)
        len_seqs = len(seq)  # assumes all sequences padded to same length
    with smart_open(input_seqs, "r+") as f:
        contents = f.read()
    with smart_open(input_seqs, "w+") as f:
        line_to_append = 'number_of_seqs_in_file\t' + str(num_seqs) + '\n'
        line_to_append += 'length_of_each_sequence\t' + str(len_seqs) + '\n'
        if input_seqs.endswith('.gz'):
            line_to_append = line_to_append.encode()
        f.write(line_to_append + contents)

    return


def get_num_and_len_of_seqs_from_file(input_seqs):
    """
    Returns the number of sequences and length of sequences in an
    input file. Assumes sequences have been processed so that all
    sequences have been padded to the same length, and that the
    file containing the process sequences have the first 2 lines in
    the following format:
    "
    number_of_seqs_in_file\t<###>
    length_of_each_sequence\t<$$$>
    "
    where '<###>' is the number of sequences in the file, and
    '<$$$>'is the length to which every sequence in the file is
    padded.

    Args:
    -----
        input_seqs (str) -- the absolute path of the processed
        input sequences to extract information from.

    Returns:
    -----
        num_seqs (int) -- the number of sequences in input_seqs.

        len_seqs (int) -- the length of the all the padded
        sequences in the input file.
    """
    # Assertions
    assert isinstance(input_seqs, str), 'Absolute pathname must be passed\
    as a string.'
    assert os.path.exists(input_seqs), 'Input file does not exist.'
    # Functionality
    with smart_open(input_seqs, 'r') as f:
        # Parse first line of file containing info about num of seqs in file
        first_line = check_valid_line(f.readline())
        assert first_line != 'skip_line', 'Invalid first line of file. Must\
        be of the form: "number_of_seqs_in_file\t<###>" where <###> is the\
        number of sequences in the file.'
        token, num_seqs = separate_seq_and_el_data(first_line)
        try:
            num_seqs = int(num_seqs)
        except ValueError:
            raise AssertionError('Number of sequences on first line must be\
            an integer.')
        assert token == 'number_of_seqs_in_file', 'First line of the input\
        file must be of the form: "number_of_seqs_in_file\t<###>" where\
        <###> is the number of sequences in the file.'

        # Parse 2nd line of file containing info about length of seqs in file
        second_line = check_valid_line(f.readline())
        assert second_line != 'skip_line', 'Invalid second line of file.\
        Must be of the form: "length_of_each_sequence\t<###>" where <###> is\
        the length of every sequence in the file.'
        token, len_seqs = separate_seq_and_el_data(second_line)
        try:
            len_seqs = int(len_seqs)
        except ValueError:
            raise AssertionError('Sequence length on second line must be an\
            integer.')
        assert token == 'length_of_each_sequence', 'Second line of the input\
        file must be of the form: "length_of_each_sequence\t<###>" where\
        <###> is the length of every sequence in the file. Assumes\
        homogeneity and/or padding of sequences.'

    return num_seqs, len_seqs


def create_sample_data(input_seqs, sample_size):
    """
    Takes a sample of size 'sample_size' from an input file
    containing sequences and their associated expression levels,
    and writes them to a separate file. The format of the first
    2 lines of the resulting output file will be of the format:
    "
    number_of_seqs_in_file\t<###>
    length_of_each_sequence\t<$$$>
    "
    where '<###>' is the number of sequences in the file, and
    '<$$$>'is the length to which every sequence in the file is
    padded.

    Args:
    -----
        input_seqs (str) -- the absolute path of the input file
        containing sequence adn expression level data to sample.

        sample_size (int) -- the number of samples to take from
        the input file.

    Returns:
    -----
        sample_data (str) -- the absolute path of the output file
        containing the sample of sequence and expression level
        data.
    """
    # Assertions
    assert isinstance(input_seqs, str), 'Input sequences file path must be\
    passed as a string.'
    assert os.path.exists(input_seqs), 'Input file does not exist.'
    assert isinstance(sample_size, int), 'Number of sequences to sample must\
    be passed as an integer.'
    # Functionality
    index = input_seqs.rfind('/') + 1
    insert = str(sample_size) + '_from_'
    output_seqs = input_seqs[:index] + insert + input_seqs[index:]
    with smart_open(input_seqs, 'r') as inf:
        with smart_open(output_seqs, 'w') as outf:
            count = -1
            while count < sample_size + 1:
                count += 1
                line = inf.readline()
                if count < 2:  # skip the first 2 lines
                    continue
                outf.write(line)
    write_num_and_len_of_seqs_to_file(output_seqs)

    return output_seqs


# def split_scaffolds_by_type(infile):
#     """
#     Splits the scaffold data contained within an Excel file
#     found at https://www.biorxiv.org/highwire/filestream/85247/
#     field_highwire_adjunct_files/1/224907-2.xlsxin by scaffold
#     type, creating different output files for each type that
#     contain all the scaffold IDs and sequences (tab separated).
#     Output files are created in the ExpressYeaself/example
#     directory.
#
#     Args:
#     -----
#         scaff_infile (str) -- the absolute path for the input file
#         containing all the scaffold data.
#
#     Returns:
#     -----
#         None
#     """
#     # Assertions
#     assert isinstance(infile, str), 'TypeError: input file pathname must be \
#     a string.'
#     assert os.path.exists(infile), 'Input file does not exist.'
#     # Functionality
#     scaff_df = pd.read_excel(infile, index_col = 'Scaffold ID')
#     types = scaff_df['Scaffold type'].unique()
#     for type in types:
#         # Create a new output file for each unique type of scaffold
#         relative_path = 'example/' + type + '_scaffolds.txt'
#         absolute_path = os.path.join(os.getcwd(), relative_path)
#         outfile = smart_open(absolute_path, 'w')
#         # Reduce scaffold data to only data of the current type
#         type_df = scaff_df[scaff_df['Scaffold type'] == type]
#         for index, row in type_df.iterrows():
#             outfile.write(index + '\t' + row['Sequence'] + '\n')
#         outfile.close()
#
#     return
