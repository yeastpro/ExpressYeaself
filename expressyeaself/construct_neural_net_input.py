"""
This script contains a wrapper function to convert raw data into
encoded sequences in the correct format for passing into a
neural network architecture.
"""

import expressyeaself.build_promoter as build
import expressyeaself.encode_sequences as encode
import expressyeaself.organize_data as organize
import os
import time as t
from expressyeaself.utilities import get_time_stamp as get_time_stamp
from expressyeaself.utilities import get_line_count as get_line_count
from expressyeaself.utilities import smart_open as smart_open

def process_raw_data(input_seqs, scaffold_type=None, homogeneous=False,
                        deflank=True, insert_into_scaffold=True,
                        pad_sequences=True, extra_padding=0, pad_front=False,
                        report_loss=True, report_times=True,
                        remove_files=False):
    """
    Takes raw data as retrieved from Carl de Boer's publication
    at https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE104878,
    and processes the sequences, writing them to an output file along
    with their expression levels (tab separated).

    Args:
    -----
        input_seqs (str) -- the absolute pathname of the file that
        contains all of the input sequences and their expression
        levels (tab separated).

        scaffold_type (str) -- the scaffold type (pTpA or Abf1TATA)
        that the input sequences had their expression levels
        measured in.

        homogeneous (bool) -- if True, only sequences of modal
        length will be processed. If False, all sequences will be
        processed regardless of length. Default: False.

        deflank (bool) -- if True, removes the constant flanking
        regions of the input sequences. Default: True.

        insert_into_scaffold (bool) -- if True inserts the input
        sequences into the appropriate scaffold. If False, the
        sequences are encoded as they are. Default: True.

        pad_sequences (bool) -- if True pads all of the encoded
        sequences so that they are the same length (i.e. pads them
        with 'P' characters until they are all the length of the
        longest sequence in the input file). Default: True.

        extra_padding (int) -- the number of 'P' characters greater
        than the maximum sequence length to pad each sequence to.
        Default: 0.

        pad_front (bool) -- whether to pad out the front (left hand
        side) or end (right hand side) of the sequences. If True,
        pads the front. Default: False (will pad the end).

        report_loss (bool) -- if True, reports the number of lines of
        data lost at each step in the process. Default: False.

        report_times (bool) -- if True, reports the time each step in
        the cleaning process takes. Default: False.

        remove_files (bool) -- if True, will remove the intermediate
        files created in the process of processing raw data. Default:
        False (i.e. intermediary files will be kept).

    Returns:
    -----
        processed_data (str) -- the absolute path for the file containing
        processed sequences along with their expression levels.
    """
    # Assertions
    assert isinstance(input_seqs, str), 'Input file path name must be \
    passed as a string.'
    assert os.path.exists(input_seqs), 'Input file does not exist.'
    assert isinstance(scaffold_type, str), 'Scaffold type must \
    be passed as a string if specified.'
    assert scaffold_type == 'pTpA' or scaffold_type == 'Abf1TATA', 'Scaffold \
    type must be specified as either "pTpA" or "Abf1TATA".'
    assert isinstance(homogeneous, bool), 'The homogeneous argument must be \
    passed as a bool.'
    assert isinstance(deflank, bool), 'The deflank argument must be passed \
    as a bool.'
    assert isinstance(insert_into_scaffold, bool), 'The insert_into_scaffold \
    argument must be passed as a bool.'
    assert isinstance(pad_sequences, bool), 'The pad_front argument must be \
    passed as a bool.'
    assert isinstance(extra_padding, int), 'The number of extra vectors to pad \
    each sequence by should be passed as an integer.'
    assert extra_padding >= 0, 'extra_padding must be passed as a non-negative \
    integer.'
    assert isinstance(pad_front, bool), 'The pad_front argument must be passed \
    as a bool.'
    assert isinstance(report_loss, bool), 'The report_loss argument must be \
    passed as a bool.'
    assert isinstance(report_times, bool), 'The report_times argument must be \
    passed as a bool.'
    assert isinstance(remove_files, bool), 'The remove_files argument must be \
    passed as a bool.'
    # Functionality
    raw_data = input_seqs
    # Define final output file path
    time_stamp = get_time_stamp()
    relative_path = 'example/processed_data/' + time_stamp
    processed_data = os.path.join(os.getcwd(), relative_path)
    # Create log file to write reports to
    if report_loss or report_times:
        report = smart_open(processed_data + '_process_report.txt', 'w')
    # Initialize custom operations if specified (i.e loss + timing reports etc.)
    if report_loss:
        loss_report = {}
        loss_report['Raw Data'] = get_line_count(input_seqs)
    if report_times:
        t_init = t.time()
        t0 = t_init
    if remove_files:
        created_files = [] # keep track of the intermediate files created.
    # Create new file of only homogeneous (same length) seqs
    if homogeneous:
        print('Pulling homogeneous sequences from input file...')
        pad_sequences = False # if all seqs same length they don't need padding
        input_seqs = organize.pull_homogeneous_seqs(input_seqs,
                                    scaffold_type=scaffold_type)
        processed_data += '_homogeneous'
        if report_loss:
            loss_report['Homogeneous Seqs'] = get_line_count(input_seqs)
        if report_times:
            t1 = t.time()
            text = '\tFile created in %s s' %(t1 - t0)
            print(text)
            report.write('Homogeneous sequences pulled...\n' + text + '\n')
            t0 = t1
        if remove_files:
            created_files.append(input_seqs)
    # Remove all of the flanking regions from the input sequences
    if deflank:
        print('Removing flank regions from sequences...')
        input_seqs = build.remove_flanks_from_all_seqs(input_seqs,
                                    scaffold_type=scaffold_type)
        processed_data += '_deflanked'
        if report_loss:
            loss_report['Deflanked Seqs'] = get_line_count(input_seqs)
        if report_times:
            t1 = t.time()
            text = '\tFile created in %s s' %(t1 - t0)
            print(text)
            report.write('Sequences deflanked...\n' + text + '\n')
            t0 = t1
        if remove_files:
            created_files.append(input_seqs)
    processed_data += '_sequences'
    # Insert sequences into appropriate scaffold
    if insert_into_scaffold:
        print('Inserting sequences into %s scaffold...' %(scaffold_type))
        input_seqs = build.insert_all_seq_into_one_scaffold(input_seqs,
                                    scaffold_type=scaffold_type)
        processed_data += '_inserted_into_%s_scaffold' %(scaffold_type)
        if report_loss:
            loss_report['Scaffold-Inserted Seqs'] = get_line_count(input_seqs)
        if report_times:
            t1 = t.time()
            text = '\tFile created in %s s' %(t1 - t0)
            print(text)
            report.write('Seqs inserted into '+scaffold_type+' scaffold...\n')
            report.write(text + '\n')
            t0 = t1
        if remove_files:
            created_files.append(input_seqs)
    # Pad sequences
    if pad_sequences or extra_padding > 0:
        print('Padding sequences...')
        input_seqs = build.pad_sequences(input_seqs, pad_front=pad_front,
                                        extra_padding=extra_padding)
        processed_data += '_padded'
        if extra_padding != 0:
            processed_data += '_%s_extra' %(extra_padding)
        if report_loss:
            loss_report['Padded Seqs'] = get_line_count(input_seqs)
        if report_times:
            t1 = t.time()
            text = '\tFile created in %s s' %(t1 - t0)
            print(text)
            report.write('Padded sequences...\n')
            report.write(text + '\n')
            t0 = t1
        if remove_files:
            created_files.append(input_seqs)
    # Rename the final output file to reflect how data has been cleaned.
    processed_data += '_with_exp_levels.txt'
    # Report end of process and print final output file locations.
    if input_seqs != raw_data: # i.e. if the data has been processed in some way
        os.rename(input_seqs, processed_data)
        # Report end of process and print absolute path of processed data.
        text = ('Raw data successfully processed...\nLocation: %s\n'
            %(processed_data))
        print(text)
        report.write(text)
    else: # If no processing was performed.
        text ='No processing performed; change processing specifications.'
        print(text)
        report.write(text + '\n')
        text = 'Raw data remains unchanged.'
        print(text)
        report.write(text + '\n')
        text = 'Location : %s' %(raw_data)
        print(text)
        report.write(text + '\n')
    # Report loss
    if report_loss:
        report.write('\nLine counts at each step of the process:\n')
        for category in loss_report.keys():
            curr_count = loss_report[category]
            if category == 'Raw Data':
                report.write('\t%s : %s\n' %(category, curr_count))
                prev_count = curr_count
            else:
                report.write('\t%s : %s (%s lines lost since last step)\n'
                    %(category,curr_count, (prev_count - curr_count)))
                prev_count = curr_count
    # Remove intermediate files
    if remove_files:
        print('\nRemoving unnecessary intermediate files...')
        organize.remove_files(created_files)
        print('Files successfully removed.')
    print('Process complete.')
    # Report total time taken
    if report_times:
        t_final = t.time()
        text = '\nTotal processing time : %s s' %(t_final - t_init)
        print(text)
        report.write(text)
    report.close()

    return processed_data

# # Encoded and pad sequences
# print('Encoding sequences using the %s method...' %(encoding_method))
# input_seqs = encode.encode_sequences_with_method(input_seqs,
#                         method=encoding_method, pad_sequences=pad_sequences,
#                         extra_padding=extra_padding, pad_front=pad_front)
# encoded_data += '_' + encoding_method
# # Rename the final output file to reflect how data has been cleaned.
# encoded_data = input_seqs.replace('.txt', encoded_data + '.txt')
# os.rename(input_seqs, encoded_data)
# if report_loss:
#     loss_report['Encoded Seqs'] = get_line_count(input_seqs)
# if report_times:
#     t1 = t.time()
#     print('\tFile created in %s s' %(t1 - t0))
