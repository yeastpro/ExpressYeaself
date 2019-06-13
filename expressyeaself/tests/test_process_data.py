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
    processed = test.process_raw_data(trial_path, scaffold_type=scaff,
                                      report_times=False, report_loss=False)
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
                                      homogeneous=True, report_times=False,
                                      report_loss=False)
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
    processed = test.process_raw_data(trial_path, scaffold_type=scaff,
                                      pad_front=True, extra_padding=3,
                                      report_times=False, report_loss=False)
    with open(processed, 'r') as g:
        assert utilities.get_seq_count(processed) - 2 == len(oligos)
        g.readline()
        g.readline()  # skip first 2 info lines
        for oligo in oligos[:3]:
            seq, el = utilities.separate_seq_and_el_data(g.readline())
            exp_seq = ('P' * 5) + scaff_pre + oligo + scaff_post
            assert seq == exp_seq
    os.remove(processed)
    # Test case 4: if no processing was performed
    trial_path = 'trial_file.txt'
    oligos = ['A' * 80, 'T' * 80, 'G' * 80, 'C' * 80]
    with open(trial_path, 'w') as f:
        for oligo in oligos:
            f.write(flank_A + oligo + flank_B + '\t123.4\n')
    processed = test.process_raw_data(trial_path, scaffold_type=scaff,
                                      deflank=False,
                                      insert_into_scaffold=False,
                                      report_times=True, report_loss=True)
    with open(trial_path, 'r') as f:
        with open(processed, 'r') as g:
            g.readline()
            g.readline()  # skip first 2 info lines
            assert f.read() == g.read()
    os.remove(trial_path)
    idx = processed.find('20') + 21
    os.remove(processed[:idx] + 'process_report.txt')
    os.remove(processed)
    # Test case 4: pulling out top and bottom percentiles, and sample data
    trial_path = 'trial_file.txt'
    scaff = 'pTpA'
    with open(trial_path, 'w') as f:
        f.write('ATGC\t5.0\n')
        f.write('ATGC\t6.0\n')
        f.write('ATGC\t7.0\n')
        f.write('ATGC\t8.0\n')
    size = 1
    processed = test.process_raw_data(trial_path, scaff, deflank=False,
                                      insert_into_scaffold=False,
                                      report_times=False, report_loss=False,
                                      percentile=0.25,
                                      create_sample_of_size=size)
    assert utilities.get_seq_count(processed) - 2 == 2
    index = processed.rfind('/') + 1
    insert = str(size) + '_from_'
    sample = processed[:index] + insert + processed[index:]
    assert utilities.get_seq_count(sample) - 2 == size
    os.remove(trial_path)
    os.remove(processed)
    os.remove(sample)

    return
