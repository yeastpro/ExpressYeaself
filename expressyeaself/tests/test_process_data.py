"""
A script containing unit tests for the functions in the
encode_sequences.py script.
"""
import expressyeaself.tests.context as context
import os

test = context.process_data
utilities = context.utilities


def test_process_raw_data():
    """
    Tests the wrapper function that processes raw data given in the
    way specified by the function's input arguments.
    """
    # Test case 1: normal input, inhomogeneous sequences.
    trial_path = 'trial_file.txt'
    scaff = 'pTpA'
    flank_A = 'TGCATTTTTTTCACATC'
    flank_B = 'GGTTACGGCTGTT'
    scaff_pre = 'GCTAGCAGGAATGATGCAAAAGGTTCCCGATTCGAACTGCATTTTTTTCACATC'
    scaff_post = ('GGTTACGGCTGTTTCTTAATTAAAAAAAGATAGAAAACATTAGGAGTGTAACACAAG'
                  'ACTTTCGGATCCTGAGCAGGCAAGATAAACGA')
    oligos = ['AAAA', 'TTTTT', 'GGGGGG', 'CCCCCCC']
    with open(trial_path, 'w') as f:
        for oligo in oligos:
            f.write(flank_A + oligo + flank_B + '\t123.4\n')
    processed = test.process_raw_data(trial_path, scaffold_type=scaff)
    with open(processed) as g:
        assert utilities.get_seq_count(processed) - 2 == len(oligos)
        g.readline()
        g.readline()  # skip first 2 info lines
        for i in range(0, len(oligos)):
            seq, el = utilities.separate_seq_and_el_data(g.readline())
            exp_seq = scaff_pre + oligos[i] + scaff_post + ('P' * (3 - i))
            assert seq == exp_seq
    os.remove(trial_path)
    os.remove(processed)
    # Test case 2: pulling homogeneous sequences
    trial_path = 'trial_file.txt'
    scaff = 'pTpA'
    flank_A = 'TGCATTTTTTTCACATC'
    flank_B = 'GGTTACGGCTGTT'
    scaff_pre = 'GCTAGCAGGAATGATGCAAAAGGTTCCCGATTCGAACTGCATTTTTTTCACATC'
    scaff_post = ('GGTTACGGCTGTTTCTTAATTAAAAAAAGATAGAAAACATTAGGAGTGTAACACAAG'
                  'ACTTTCGGATCCTGAGCAGGCAAGATAAACGA')
    oligos = ['A' * 80, 'T' * 80, 'G' * 80, 'C' * 82]
    with open(trial_path, 'w') as f:
        for oligo in oligos:
            f.write(flank_A + oligo + flank_B + '\t123.4\n')
    processed = test.process_raw_data(trial_path, scaffold_type=scaff,
                                      homogeneous=True)
    with open(processed, 'r') as g:
        assert utilities.get_seq_count(processed) - 2 == len(oligos) - 1
        g.readline()
        g.readline()  # skip first 2 info lines
        for oligo in oligos[:3]:
            seq, el = utilities.separate_seq_and_el_data(g.readline())
            exp_seq = scaff_pre + oligo + scaff_post
            assert seq == exp_seq
    os.remove(processed)
    # Test case 3: extra padding at front
    trial_path = 'trial_file.txt'
    processed = test.process_raw_data(trial_path, scaffold_type=scaff,
                                      pad_front=True, extra_padding=3)
    with open(processed, 'r') as g:
        assert utilities.get_seq_count(processed) - 2 == len(oligos)
        g.readline()
        g.readline()  # skip first 2 info lines
        for oligo in oligos[:3]:
            seq, el = utilities.separate_seq_and_el_data(g.readline())
            exp_seq = ('P' * 5) + scaff_pre + oligo + scaff_post
            assert seq == exp_seq
    # Test case 4: if no processing was performed
    trial_path = 'trial_file.txt'
    oligos = ['A' * 80, 'T' * 80, 'G' * 80, 'C' * 80]
    with open(trial_path, 'w') as f:
        for oligo in oligos:
            f.write(flank_A + oligo + flank_B + '\t123.4\n')
    processed = test.process_raw_data(trial_path, scaffold_type=scaff,
                                      deflank=False,
                                      insert_into_scaffold=False)
    with open(trial_path, 'r') as f:
        with open(processed, 'r') as g:
            g.readline()
            g.readline()
            assert f.read() == g.read()

    return
