"""
This script contains a wrapper function that processes raw data.
"""
import expressyeaself.build_promoter as build
import expressyeaself.organize_data as organize
from expressyeaself.utilities import get_seq_count as get_seq_count
from expressyeaself.utilities import get_time_stamp as get_time_stamp
from expressyeaself.utilities import smart_open as smart_open
import os
import time as t


def process_raw_data(input_seqs, scaffold_type=None, percentile=None,
                     binarize_els=True, homogeneous=False, deflank=True,
                     insert_into_scaffold=True, extra_padding=0,
                     pad_front=False, report_loss=True, report_times=True,
                     remove_files=True, create_sample_of_size=None):
    """
    A wrapper function that:
    Takes raw data as retrieved from Carl de Boer's publication
    at https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE104878,
    and processes the sequences according to the custom arguments,
    pads them to same length, and writes them to an output file
    along with their expression levels (tab separated). The end of
    the file contains comments specifying the number of sequences
    in the file and the lengths of the padded sequences.

    Args:
    -----
        input_seqs (str) -- the absolute pathname of the file that
        contains all of the input sequences and their expression
        levels (tab separated).

        scaffold_type (str) -- the scaffold type (pTpA or Abf1TATA)
        that the input sequences had their expression levels
        measured in.

        percentile (float) -- the proportion of the raw input data
        to extract from the sequences with the highest and lowest
        expression levels. i.e if 'percentile=0.1' then the top
        10 % of sequences with highest expression levels, and the
        bottom 10 % of sequences with lowest expression levels will
        be extracted from the raw input data. The resulting data
        file will contain ~ 20 % of the data as the raw input data.

        binarize_els (bool) -- if (and only if) a 'percentile'
        value is passed, this argument determines whether the
        expression level values (Els) will be binarized or not. If
        True (defualt), sequences with ELs in the top percentile
        will have their ELs binarized to 1, and sequences with ELs
        in the bottom percentile will have their ELs binarized
        to 0.

        homogeneous (bool) -- if True, only sequences of modal
        length will be processed. If False, all sequences will be
        processed regardless of length. Default: False.

        deflank (bool) -- if True, removes the constant flanking
        regions of the input sequences. Default: True.

        insert_into_scaffold (bool) -- if True inserts the input
        sequences into the appropriate scaffold. If False, the
        sequences are encoded as they are. Default: True.

        extra_padding (int) -- the number of 'P' characters greater
        than the maximum sequence length to pad each sequence to.
        Default: 0.

        pad_front (bool) -- whether to pad out the front (left hand
        side) or end (right hand side) of the sequences. If True,
        pads the front. Default: False (will pad the end).

        report_loss (bool) -- if True, reports the number of lines
        of data lost at each step in the process. Default: False.

        report_times (bool) -- if True, reports the time each step
        in the cleaning process takes. Default: False.

        remove_files (bool) -- if True, will remove intermediate
        files created in the process of processing raw data.
        Default: False (i.e. intermediary files will be kept).

        create_sample_of_size (int) -- if a number is passed, a
        sample of this size will be taken by pseudo-random from
        the file containing processed data, and written to a
        separate file.

    Returns:
    -----
        processed_data (str) -- the absolute path for the file
        containing processed sequences along with their expression
        levels.
    """
    # Assertions
    assert isinstance(input_seqs, str), ('Input file path name must be '
                                         'passed as a string.')
    assert os.path.exists(input_seqs), 'Input file does not exist.'
    assert isinstance(scaffold_type, str), ('Scaffold type must be passed as '
                                            'a string if specified.')
    assert scaffold_type == 'pTpA' or scaffold_type == 'Abf1TATA', 'Scaffold \
    type must be specified as either "pTpA" or "Abf1TATA".'
    assert isinstance(percentile, (float, type(None))), ('The "percentile" '
                                                         'argument must be '
                                                         'passed as a float.')
    if percentile is not None:
        assert percentile < 0.5, '"percentile" must be less that 0.5'
    assert isinstance(homogeneous, bool), ('The homogeneous argument must be '
                                           'passed as a bool.')
    assert isinstance(deflank, bool), ('The deflank argument must be passed '
                                       'as a bool.')
    assert isinstance(insert_into_scaffold, bool), ('insert_into_scaffold '
                                                    'argument must be passed '
                                                    'as a bool.')
    assert isinstance(extra_padding, int), ('The number of extra vectors to '
                                            'pad each sequence by should be '
                                            'passed as an integer.')
    assert extra_padding >= 0, ('extra_padding must be passed as a non-'
                                'negative integer.')
    assert isinstance(pad_front, bool), ('The pad_front argument must be '
                                         'passed as a bool.')
    assert isinstance(report_loss, bool), ('The report_loss argument must be '
                                           'passed as a bool.')
    assert isinstance(report_times, bool), ('The report_times argument must '
                                            'be passed as a bool.')
    assert isinstance(remove_files, bool), ('The remove_files argument must '
                                            'be passed as a bool.')
    if create_sample_of_size is not None:
        assert isinstance(create_sample_of_size, int), ('Sample size must be '
                                                        'passed as an int')
    # Functionality
    print('Starting processing of raw data...')
    raw_data = input_seqs
    # Define final output file path
    time_stamp = get_time_stamp()
    relative_path = 'example/processed_data/' + time_stamp
    processed_data = os.path.join(os.getcwd(), relative_path)
    # Create log file to write reports to
    if report_loss or report_times:
        report = smart_open(processed_data + '_process_report' + '.txt', 'w')
    # Initialize custom operations if specified (i.e loss + timing reports)
    if report_loss:
        loss_report = {}
        loss_report['Raw Data'] = get_seq_count(input_seqs)
    if report_times:
        t_init = t.time()
        t0 = t_init
    if remove_files:
        created_files = []  # keep track of the intermediate files created.
    # Pull out the top and bottom percentiles of data
    if percentile is not None:
        print('Pulling out the top and bottom percentiles...')
        df = organize.sort_by_exp_level(input_seqs)
        df = organize.discard_mid_data(df, percentile=percentile)
        processed_data += '_percentiles'
        if binarize_els:
            print('Binarizing expression levels...')
            df = organize.binarize_data(df)
            processed_data += '_els_binarized'
        input_seqs = organize.write_df_to_file(df)
        if report_loss:
            loss_report['Percentile Seqs'] = get_seq_count(input_seqs)
        if report_times:
            t1 = t.time()
            text = '\tFile created in %s s' % (t1 - t0)
            print(text)
            report.write('Top & bottom percentiles pulled...\n' + text + '\n')
            t0 = t1
        if remove_files:
            created_files.append(input_seqs)
    # Create new file of only homogeneous (same length) seqs
    if homogeneous:
        print('Pulling homogeneous sequences from input file...')
        input_seqs = organize.pull_homogeneous_seqs(input_seqs, scaffold_type)
        processed_data += '_homogeneous'
        if report_loss:
            loss_report['Homogeneous Seqs'] = get_seq_count(input_seqs)
        if report_times:
            t1 = t.time()
            text = '\tFile created in %s s' % (t1 - t0)
            print(text)
            report.write('Homogeneous sequences pulled...\n' + text + '\n')
            t0 = t1
        if remove_files:
            created_files.append(input_seqs)
    # Remove all of the flanking regions from the input sequences
    if deflank:
        print('Removing flank regions from sequences...')
        input_seqs = build.remove_flanks_from_all_seqs(input_seqs,
                                                       scaffold_type)
        processed_data += '_deflanked'
        if report_loss:
            loss_report['Deflanked Seqs'] = get_seq_count(input_seqs)
        if report_times:
            t1 = t.time()
            text = '\tFile created in %s s' % (t1 - t0)
            print(text)
            report.write('Sequences deflanked...\n' + text + '\n')
            t0 = t1
        if remove_files:
            created_files.append(input_seqs)
    processed_data += '_sequences'
    # Insert sequences into appropriate scaffold
    if insert_into_scaffold:
        print('Inserting sequences into %s scaffold...' % (scaffold_type))
        input_seqs = build.insert_all_seq_into_one_scaffold(input_seqs,
                                                            scaffold_type)
        processed_data += '_inserted_into_%s_scaffold' % (scaffold_type)
        if report_loss:
            loss_report['Scaffold-Inserted Seqs'] = get_seq_count(input_seqs)
        if report_times:
            t1 = t.time()
            text = '\tFile created in %s s' % (t1 - t0)
            print(text)
            report.write('Seqs inserted into ' + scaffold_type +
                         'scaffold...\n')
            report.write(text + '\n')
            t0 = t1
        if remove_files:
            created_files.append(input_seqs)
    # Pad sequences
    if homogeneous and extra_padding == 0:
        pass
    else:
        print('Padding sequences...')
        input_seqs = build.pad_sequences(input_seqs, pad_front=pad_front,
                                     extra_padding=extra_padding)
    if not homogeneous:  # then they will have been padded
        processed_data += '_padded_at'
        if pad_front:
            processed_data += '_front'
        else:
            processed_data += '_back'
    if extra_padding != 0:
        processed_data += '_%s_extra' % (extra_padding)
    if report_loss:
        loss_report['Padded Seqs'] = get_seq_count(input_seqs)
    if report_times:
        t1 = t.time()
        text = '\tFile created in %s s' % (t1 - t0)
        print(text)
        report.write('Padded sequences...\n')
        report.write(text + '\n')
        t0 = t1
    # Remove intermediate files created in the process
    if remove_files:
        created_files.append(input_seqs)
    # Rename the final output file to reflect how data has been cleaned.
    processed_data += '_with_exp_levels.txt'
    # Report end of process and print final output file locations.
    if input_seqs != raw_data:  # i.e. if data has been processed in some way
        os.rename(input_seqs, processed_data)
        # Report end of process and print absolute path of processed data.
        text = ('\nRaw data successfully processed.\nLocation: %s\n'
                % (processed_data))
        print(text)
        if report_loss or report_times:
            report.write(text)
    else:  # If no processing was performed.
        text = '\nNo processing performed.\n'
        text += 'Change processing specifications and try again.'
        print(text)
        report.write(text + '\n')
        text = 'Raw data remains unchanged.'
        print(text)
        report.write(text + '\n')
        text = 'Location : %s' % (raw_data)
        print(text)
        if report_loss or report_times:
            report.write(text + '\n')
    # Write the number of seqs and length of seqs to the start of file
    organize.write_num_and_len_of_seqs_to_file(processed_data)
    # Report loss
    if report_loss:
        report.write('\nLine counts at each step of the process:\n')
        for category in loss_report.keys():
            curr_count = loss_report[category]
            if category == 'Raw Data':
                report.write('\t%s : %s\n' % (category, curr_count))
                prev_count = curr_count
            else:
                report.write('\t%s : %s (%s lines lost since last step)\n'
                             % (category, curr_count, (prev_count -
                                curr_count)))
                prev_count = curr_count
    # Remove intermediate files
    if remove_files:
        print('\nRemoving intermediate files...')
        organize.remove_file_list(created_files)
        print('Files successfully removed.')
    print('Process complete.')
    # Report total time taken
    if report_times:
        t_final = t.time()
        text = '\nTotal processing time : %s s' % (t_final - t_init)
        print(text)
        report.write(text)
        print('Please find the process report in the same directory as the'
              ' output file for reports of data losses and timings.')
    if report_times or report_loss:
        report.close()
    # Create sample data
    if create_sample_of_size is not None:
        size = create_sample_of_size
        print('\n\nCreating sample of size %s ...' % str(size))
        sample_seqs = organize.create_sample_data(processed_data, size)
        print('\nSample data successfully created.')
        print('\nLocation: %s \n' % (sample_seqs))

    return processed_data
