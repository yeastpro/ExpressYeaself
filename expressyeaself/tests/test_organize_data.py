"""
This script contains the unit tests for the functions found in
the organize_data.py script.
"""
import expressyeaself.tests.context as context
import os

test = context.organize_data
utilities = context.utilities


def test_get_max_min_mode_length_of_seqs():
    """
    Tests the function that returns the maximum, minimum, and modal
    length of the sequences in an input file.
    """
    # Test case 1: non-string input
    trial_file = True
    try:
        test.get_max_min_mode_length_of_seqs(trial_file)
    except AssertionError:
        pass
    # Test case 2: non-existent file
    trial_file = 'made_up_file.txt'
    try:
        test.get_max_min_mode_length_of_seqs(trial_file)
    except AssertionError:
        pass
    # Test case 3: file with 3 valid lines containing same length sequences,
    #   and 1 invalid line containing sequence of different length
    trial_file = './trial_file.txt'
    with open(trial_file, 'w') as f:
        for i in range(0, 3):
            f.write('ATGC\t10\n')  # valid lines
        f.write('ATGCCC')
    max_len, min_len, mode = test.get_max_min_mode_length_of_seqs(trial_file)
    assert max_len == min_len  # Should ignore invalid line.

    return


def test_pull_homogenous_seqs():
    """
    Tests the function that pulls all sequences of modal length
    from an input file of sequences and returns
    """
    # Test case 1: check output file placed in correct place
    trial_file = 'trial_file.txt'
    homogeneous_line = 'ATGC\t10.0\n'
    with open(trial_file, 'w') as f:
        for i in range(0, 3):
            f.write(homogeneous_line)
        f.write('ATGCCC\t10.0\n')  # inhomogeneous relative to other lines
        f.write('This is an invalid line.')
    #   a) pTpA
    scaff = 'pTpA'
    outfile = test.pull_homogeneous_seqs(trial_file, scaff)
    assert os.path.exists(outfile)
    assert outfile.find('pTpA_data/') != -1
    os.remove(outfile)
    #   b) Abf1TATA
    scaff = 'Abf1TATA'
    outfile = test.pull_homogeneous_seqs(trial_file, scaff)
    assert os.path.exists(outfile)
    assert outfile.find('Abf1TATA_data/') != -1
    os.remove(outfile)
    #   c) Unspecified scaffold
    outfile = test.pull_homogeneous_seqs(trial_file)
    assert os.path.exists(outfile)
    assert outfile.find('other_scaffolds/') != -1
    # Test case 2: check contents of output file
    with open(outfile) as f:
        for line in f:
            assert line == homogeneous_line
    os.remove(outfile)

    return


def test_check_oligonucleotide_flanks():
    """
    Tests the function that checks the flanking sequences of all of
    the sequences in an input file and returns a list of lines with
    incorrect flanks.
    """
    # Test case 1: file with known number of sequences without valid flanks.
    scaffolds = ['pTpA', 'Abf1TATA']
    num_wrong_flanks = 10
    trial_file = './trial_file.txt'
    with open(trial_file, 'w+') as f:
        for i in range(0, num_wrong_flanks):
            f.write('ATGC\t5.0\n')
        f.write('This is an invalid line.')
    for scaff in scaffolds:
        incorrect_lines = test.check_oligonucleotide_flanks(trial_file, scaff)
        assert len(incorrect_lines) == num_wrong_flanks
    # os.remove(trial_file)
    # Test case 2: file with known number of valid flanks
    num_wrong_flanks = 10
    for scaff in scaffolds:
        if scaff == 'pTpA':
            test_seq = 'TGCATTTTTTTCACATCAAAAGGTTACGGCTGTT'
        elif scaff == 'Abf1TATA':
            test_seq = 'TCACGCAGTATAGTTCTTTTGGTTTATTGTTTATAAAAA'
        trial_file = './trial_file.txt'
        with open(trial_file, 'w+') as f:
            for i in range(0, num_wrong_flanks):
                f.write('ATGC\t5.0\n')
                f.write(test_seq + '\t5.0\n')
            f.write('This is an invalid line.')
        incorrect_lines = test.check_oligonucleotide_flanks(trial_file, scaff)
        assert len(incorrect_lines) == num_wrong_flanks
        for i in range(0, num_wrong_flanks):
            assert incorrect_lines[i] == 2 * i + 1  # odd lines are wrong

    return


def test_remove_files():
    """
    Tests the function that takes as input a list containing the
    strings of the absolute paths of one or more files, and removes
    them.
    """
    # Test case 1: file in list doesn't exist
    filenames = ['trial_1.txt', 'trial_2.txt', 'trial_3.txt', 'trial_4.txt']
    for idx in range(0, len(filenames) - 1):  # only create first 3 files.
        open(filenames[idx], 'w+')
        assert os.path.exists(filenames[idx])
    test.remove_file_list(filenames)
    # Test case 2: improper input
    trial_list = ['string1', 'string2', 6.0]
    try:
        test.remove_file_list(trial_list)
    except AssertionError:
        pass

    return


def test_write_num_and_len_of_seqs_from_file():
    """
    Tests the function that writes the number and lengths of the
    sequences in an input file from the first 2 lines of the file
    that contain this information.
    """
    # Test case 1: valid first line of file
    trial_path = 'trial_file.txt'
    num_seqs = 10
    trial_seq = 'ATGC'
    with open(trial_path, 'w') as f:
        for i in range(0, num_seqs):
            f.write(trial_seq + '\t10.8\n')
    test.write_num_and_len_of_seqs_to_file(trial_path)
    num, leng = test.get_num_and_len_of_seqs_from_file(trial_path)
    assert num == num_seqs
    assert len(trial_seq) == leng
    # Test case 2: valid first line of compressed file
    trial_path = 'trial_file.txt'
    num_seqs = 10
    trial_seq = 'ATGC'
    with open(trial_path, 'wb') as f:
        for i in range(0, num_seqs):
            text = trial_seq + '\t10.8\n'
            f.write(text.encode())
    test.write_num_and_len_of_seqs_to_file(trial_path)
    num, leng = test.get_num_and_len_of_seqs_from_file(trial_path)
    assert num == num_seqs
    assert len(trial_seq) == leng
    # Test case 3: invalid first line of file
    trial_path = 'trial_file.txt'
    num_seqs = 10
    trial_seq = 'ATGC'
    with open(trial_path, 'w') as f:
        f.write('This is an invalid line.')
        for i in range(0, num_seqs):
            f.write(trial_seq + '\t10.8\n')
    try:
        test.write_num_and_len_of_seqs_to_file(trial_path)
    except AssertionError:
        pass

    return


def test_get_num_and_len_of_seqs_from_file():
    """
    Tests the function that retrieves the number and lengths of the
    sequences in an input file from the first 2 lines of the file
    that contain this information.
    """
    # Test case 1: correctly formatted input file
    trial_path = 'trial_file.txt'
    trial_num = 12345
    trial_len = 00000
    with open(trial_path, 'w+') as f:
        f.write('number_of_seqs_in_file\t' + str(trial_num) + '\n')
        f.write('length_of_each_sequence\t' + str(trial_len) + '\n')
    num, len = test.get_num_and_len_of_seqs_from_file(trial_path)
    assert num == trial_num
    assert len == trial_len
    # Test case 2: incorrectly formatted input file
    trial_path = 'trial_file.txt'
    trial_num = 'hello'
    trial_len = 'hi'
    with open(trial_path, 'w+') as f:
        f.write('number_of_seqs_in_file\t' + trial_num + '\n')
        f.write('length_of_each_sequence\t' + trial_num + '\n')
    try:
        num, leng = test.get_num_and_len_of_seqs_from_file(trial_path)
    except ValueError:
        pass
    # Test case 3: incorrectly formatted number
    trial_path = 'trial_file2.txt'
    trial_num = 12345.6
    trial_len = 45
    with open(trial_path, 'w+') as f:
        f.write('number_of_seqs_in_file\t' + str(trial_num) + '\n')
        f.write('length_of_each_sequence\t' + str(trial_num) + '\n')
    try:
        num, leng = test.get_num_and_len_of_seqs_from_file(trial_path)
    except ValueError:
        pass

    return

def test_create_sample_data():
    """
    Tests the function that creates a file containing a given
    amount of sample data from an input
    """
    # Test case 1: sample size larger than input data
    trial_path = 'trial_file.txt'
    num_input_seqs = 10
    with open(trial_path, 'w') as f:
        for i in range(0, num_input_seqs):
            f.write('ATGC\t7.7\n')
    try:
        sample = test.create_sample_data(trial_path, num_input_seqs + 1)
    except AssertionError:
        pass
    # Test case 2: checking output
    sample_size = num_input_seqs // 2
    sample = test.create_sample_data(trial_path, sample_size)
    assert os.path.exists(sample)
    assert utilities.get_seq_count(sample) - 2 == sample_size
    os.remove(sample)
    # Test case 3: non-existent input file
    trial_path = 'made_up_file.txt'
    try:
        sample = test.create_sample_data(trial_path, 10)
    except AssertionError:
        pass
    # Test case 3: improper type of input
    trial_path = 'trial_file.txt'
    file = open(trial_path, 'w')
    try:
        sample = test.create_sample_data(trial_path, 10)
    except AssertionError:
        pass
    os.remove(trial_path)

    return


# def test_split_scaffolds_by_type():
#     """
#     Tests the function that splits an input excel file of scaffold
#     data by their type, outputting the different types to different
#     output files.
#     """
#
#     return
